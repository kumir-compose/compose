import logging
import re
import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from kumir_compose.kspi.integrations.http import attach_http_funcs
from kumir_compose.kspi.integrations.psql import attach_psql_funcs
from kumir_compose.kspi.integrations.stdio import attach_stdio_funcs
from kumir_compose.kspi.kspi import KumirInterface
from kumir_compose.kspi.messages import Message, base_dump
from kumir_compose.utils.kcollections_adapter import assemble_dict, serialize
from kumir_compose.web.interfaces import BaseRequestHandler, HandlerFactory


@dataclass
class KSPIBasedHandlerFactory(HandlerFactory):
    base_dir: str
    path_config: dict[str, str]
    vm_path: str

    def create(self):
        return KSPIBasedHandler(
            base_dir=self.base_dir,
            path_config=self.path_config,
            vm_path=self.vm_path,
            plugins=[
                attach_psql_funcs,
                attach_http_funcs,
                attach_stdio_funcs
            ]
        )


@dataclass
class KSPIBasedHandler(BaseRequestHandler):
    base_dir: str
    path_config: dict[str, str]
    vm_path: str
    plugins: list[Callable[[KumirInterface], None]]

    answer: tuple[int, dict[str, str], str] = (200, {}, "OK")
    kspi: KumirInterface = KumirInterface()

    def find_exec_for_path(self, method: str, path: str) -> str | None:
        path = f"{method.upper()} {path}"
        exec_path = next((
            exec_path for path_regex, exec_path in self.path_config.items()
            if re.fullmatch(path_regex, path)
        ), None)
        if not exec_path:
            logging.warning("Route not found for path %s", path)
            exec_path = self.path_config.get("_")
        if not exec_path:
            return None
        exec_path = f"{exec_path}.kod"
        if not Path(self.base_dir, exec_path).exists():
            logging.error("Exec not found for path %s", path)
            return None
        return exec_path

    def handle_answer(self, _, ans: tuple[int, dict[str, str], str]) -> None:
        self.answer = ans
        self.kspi.request_stop()

    def handle_request(
            self,
            method: str,
            path: str,
            query: str,
            headers: dict[str, str],
            body: str
    ) -> tuple[int, dict[str, str], str]:
        self.kspi = KumirInterface()
        executable = self.find_exec_for_path(method, path)
        if not executable:
            return 404, {}, "Not found"
        for plugin in self.plugins:
            plugin(self.kspi)
        self.kspi.add_listener("web_ans", _ans_parser, self.handle_answer)
        proc = subprocess.Popen(
            [self.vm_path, str(Path(self.base_dir, executable).absolute())],
            stdout=subprocess.PIPE,
            stderr=sys.stderr,
            stdin=subprocess.PIPE,
            text=True,
            encoding="UTF-8-sig",
            errors="ignore"
        )
        self.kspi.connect(proc.stdout, proc.stdin)
        self.kspi.send(
            IncomingHTTPRequest(
                method=method,
                query=query,
                path=path,
                body=body,
                headers=headers
            ),
            incoming_http_dumper
        )
        self.kspi.listen_forever()
        proc.wait()
        return self.answer


def _ans_parser(_, request: str) -> tuple[int, dict[str, str], str]:
    status, body = request.split("\n", maxsplit=1)
    headers, body = body.split("---\n", maxsplit=1)
    headers = [
        h.split(":", maxsplit=1)
        for h in headers.split("\n")
        if ":" in h
    ]
    headers = {h[0]: h[1] for h in headers}
    return int(status), headers, body


@dataclass(kw_only=True)
class IncomingHTTPRequest(Message):
    type: str = "req"
    method: str
    path: str
    query: str
    headers: dict[str, str]
    body: str


def incoming_http_dumper(message: IncomingHTTPRequest) -> str:
    enc_headers = assemble_dict({
        k: serialize(v) for k, v in message.headers.items()
    })
    enc_body = serialize(message.body)
    return base_dump(
        "req",
        f"{message.method}\n"
        f"{message.path}\n"
        f"{message.query}\n"
        f"{enc_headers}\n"
        f"{enc_body}\n"
    )
