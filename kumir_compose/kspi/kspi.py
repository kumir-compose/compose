import logging
from collections.abc import Callable, Generator
from io import StringIO
from logging import Logger
from typing import Any, IO

from kumir_compose.kspi.messages import (
    BadRequestMessage,
    InternalErrorMessage, Message,
    builtin_error_dumper,
)

type MessageParser[_Message_T: Message] = Callable[[str, str], _Message_T]
type MessageDumper[_Message_T: Message] = Callable[[_Message_T], str]
type MessageHandler[_Message_T: Message] = Callable[
    [KumirInterface, _Message_T], None
]
type Ticker = Callable[[], None]
type Stream = IO[str]


class ParseError(ValueError):
    """MessageParser error."""


class KumirInterface:
    def __init__(self, logger: Logger | None = None) -> None:
        self._incoming_listeners: dict[
            str, tuple[MessageParser[Any], MessageHandler[Any]]
        ] = {}
        self._outgoing: Stream = StringIO()
        self._incoming: Stream = StringIO()
        self.log = logger or logging.getLogger("kspi")
        self._ticking: list[Ticker] = []
        self._should_stop = False

    def connect(self, incoming: Stream, outgoing: Stream) -> None:
        self._outgoing = outgoing
        self._incoming = incoming

    def add_listener[_Message_T](
            self,
            message_type: str,
            parser: MessageParser[_Message_T],
            handler: MessageHandler[_Message_T]
    ) -> None:
        self._incoming_listeners[message_type] = (parser, handler)

    def remove_listener(self, message_type: str) -> None:
        self._incoming_listeners.pop(message_type)

    def add_ticker(self, ticker: Ticker) -> None:
        self._ticking.append(ticker)

    def request_stop(self) -> None:
        self._should_stop = True

    def send[_Message_T: Message](
            self, message: _Message_T, dumper: MessageDumper[_Message_T]
    ) -> None:
        self.send_raw(dumper(message))

    def send_str(self, message_t: str, message: str) -> None:
        self._outgoing.write(f"{message_t};{len(message)};{message}")
        self._outgoing.flush()

    def send_raw(self, message: str) -> None:
        self._outgoing.write(message)
        self._outgoing.flush()

    def received(self, message_t: str, message_contents: str) -> None:
        self.log.debug("Received %s type", message_t)
        if message_t not in self._incoming_listeners:
            self.log.warning(
                "%s type hasn't got any listeners attached", message_t
            )
            return
        parser, handler = self._incoming_listeners[message_t]
        try:
            message = parser(message_t, message_contents)
        except ParseError as exc:
            self.log.exception("Parse error")
            self.send(BadRequestMessage(), builtin_error_dumper)
            return
        except Exception as exc:
            self.log.exception("Unhandled exception when parsing message")
            self.send(InternalErrorMessage(), builtin_error_dumper)
            return
        try:
            handler(self, message)
        except Exception as exc:
            self.log.exception("Unhandled exception when handling message")
            self.send(InternalErrorMessage(), builtin_error_dumper)

    def listen_loop(self) -> Generator[None]:
        yield
        while not self._should_stop:
            message_t = ""
            while (c := self._incoming.read(1)) != ";":
                message_t += c
                yield
            content_length_str = ""
            while (c := self._incoming.read(1)) != ";":
                content_length_str += c
                yield
            message_contents = ""
            for _ in range(int(content_length_str)):
                message_contents += self._incoming.read(1)
                yield
            self._incoming.read(1)  # consume trailing LF
            self.received(message_t, message_contents)
            yield

    def listen_forever(self) -> None:
        loop = self.listen_loop()
        while not self._should_stop:
            for ticker in self._ticking:
                ticker()
            try:
                next(loop)
            except StopIteration:
                return
