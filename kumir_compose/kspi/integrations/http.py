from dataclasses import dataclass

import requests

from kumir_compose.kspi.kspi import KumirInterface
from kumir_compose.kspi.messages import Message, base_dump


@dataclass(kw_only=True)
class RequestMessage(Message):
    method: str
    url: str
    headers: dict[str, str]
    body: str
    type: str = "http_req"


@dataclass(kw_only=True)
class ResponseMessage(Message):
    status: int
    headers: dict[str, str]
    body: str
    type: str = "http_resp"


def http_request_parser(_, request: str) -> RequestMessage:
    request = request.replace("\r\n", "\n").replace("\r", "\n")
    request_head, body = request.split("\n", maxsplit=1)
    method, url = request_head.split(maxsplit=1)
    headers, body = body.split("---\n", maxsplit=1)
    headers = [
        h.split(":", maxsplit=1)
        for h in headers.split("\n")
        if ":" in h
    ]
    headers = {h[0]: h[1] for h in headers}
    return RequestMessage(
        method=method, url=url, headers=headers, body=body
    )


def http_response_dumper(message: ResponseMessage) -> str:
    return base_dump(
        ResponseMessage.type,
        (
            "{status}\n"
            "{headers}\n"
            "---\n"
            "{body}"
        ).format(
            status=message.status,
            headers="\n".join(f"{k}: {v}" for k, v in message.headers.items()),
            body=message.body
        )
    )


def handle_http_request(
        kspi: KumirInterface,
        message: RequestMessage
) -> None:
    response = requests.request(
        method=message.method,
        url=message.url,
        headers=message.headers,
        data=message.body
    )
    kspi.send(ResponseMessage(
        status=response.status_code,
        headers=dict(response.headers),
        body=response.text
    ), http_response_dumper)


def attach_http_funcs(kspi: KumirInterface) -> None:
    kspi.add_listener(
        RequestMessage.type,
        http_request_parser,
        handle_http_request
    )
