from collections.abc import Callable, Iterable
from typing import Any
from wsgiref.types import StartResponse

from kumir_compose.web.handler import KSPIBasedHandlerFactory


def create_compose_app(
        routes: dict[str, str], kumir_vm: str
) -> Callable[[dict[str, Any], StartResponse], Iterable[bytes]]:
    class ComposeWSGIApp:
        def __init__(self, environ, start_response) -> None:
            self.env = environ
            self.start_response = start_response
            self.factory = KSPIBasedHandlerFactory(
                "routes", routes, kumir_vm
            )

        def __iter__(self):
            handler = self.factory.create()
            input_object = self.env.get("wsgi.input")
            data = b""
            if input_object:
                data = input_object.read()
            status, headers, resp = handler.handle_request(
                self.env["REQUEST_METHOD"],
                self.env["PATH_INFO"],
                self.env["QUERY_STRING"],
                {
                    k: str(v)
                    for k, v in self.env.items()
                    if k.startswith("HTTP") or k.startswith("X")
                },
                data.decode()
            )
            self.start_response(str(status), headers.items())
            yield resp.encode()
    return ComposeWSGIApp
