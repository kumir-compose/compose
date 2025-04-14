import logging
from dataclasses import dataclass

from kumir_compose.kspi.kspi import KumirInterface
from kumir_compose.kspi.messages import Message


@dataclass(kw_only=True)
class LogMessage(Message):
    level: str
    text: str
    type: str = "log"


def log_request_parser(_, request: str) -> LogMessage:
    level, text = request.split(";", maxsplit=1)
    return LogMessage(text=text, level=level)


def handle_log_request(
        kspi: KumirInterface,
        message: LogMessage
) -> None:
    levels = {
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR
    }
    kspi.log.log(levels.get(message.level, logging.INFO), message.text)


def attach_stdio_funcs(kspi: KumirInterface) -> None:
    kspi.add_listener(
        LogMessage.type,
        log_request_parser,
        handle_log_request
    )
