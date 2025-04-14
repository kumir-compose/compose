from dataclasses import dataclass


@dataclass
class Message:
    """ADC for messages."""

    type: str


@dataclass
class BadRequestMessage(Message):
    """Sent when request couldn't be parsed."""

    type: str = "bad_request"


@dataclass
class InternalErrorMessage(Message):
    """Sent when request couldn't be parsed."""

    type: str = "internal_error"


def builtin_error_dumper(message: Message) -> str:
    return f"{message.type};0;"


def base_dump(message_t: str, content: str) -> str:
    return f"{message_t};{len(content.encode())};{content}"
