from abc import abstractmethod
from typing import Protocol


class HandlerFactory(Protocol):
    @abstractmethod
    def create(self):
        ...


class BaseRequestHandler(Protocol):
    @abstractmethod
    def handle_request(
            self,
            method: str,
            path: str,
            query: str,
            headers: dict[str, str],
            body: str
    ):
        """Handle request"""
