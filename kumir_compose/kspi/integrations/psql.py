from dataclasses import dataclass
from typing import Any, Final

import psycopg2

from kumir_compose.kspi.kspi import KumirInterface
from kumir_compose.kspi.messages import Message, base_dump


_C_US: Final = chr(0x1f)
_C_RS: Final = chr(0x1e)


@dataclass(kw_only=True)
class RequestMessage(Message):
    connection_str: str
    query: str
    type: str = "psql_req"


@dataclass(kw_only=True)
class ResponseMessage(Message):
    rows: list[list[Any]] | None
    type: str = "psql_resp"


def psql_request_parser(_, request: str) -> RequestMessage:
    request = request.replace("\r\n", "\n").replace("\r", "\n")
    connect, query = request.split("\n", maxsplit=1)
    return RequestMessage(
        connection_str=connect, query=query
    )


def psql_response_dumper(message: ResponseMessage) -> str:
    if message.rows is None:
        return base_dump(ResponseMessage.type, "")
    return base_dump(
        ResponseMessage.type,
        "O" + _C_RS.join(_C_US.join(map(str, row)) for row in message.rows)
    )


def handle_psql_request(
        kspi: KumirInterface,
        message: RequestMessage
) -> None:
    try:
        conn = psycopg2.connect(message.connection_str)
        cur = conn.cursor()
        cur.execute(message.query)
        conn.commit()
        contents = None
        if cur.pgresult_ptr is not None:
            contents = cur.fetchall()
        kspi.send(ResponseMessage(rows=contents), psql_response_dumper)
    except Exception as exc:
        kspi.send_raw(base_dump(ResponseMessage.type, "E"))


def attach_psql_funcs(kspi: KumirInterface) -> None:
    kspi.add_listener(
        RequestMessage.type,
        psql_request_parser,
        handle_psql_request
    )
