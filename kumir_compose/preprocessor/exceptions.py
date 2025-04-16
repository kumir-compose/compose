from kumir_compose.preprocessor.tokens import DIRECTIVES, Token, TokenType


class PositionedException(Exception):
    """Base class for lexer exceptions."""

    def __init__(
            self,
            message: str,
            filename: str,
            source: str,
            line: int,
            char: int
    ) -> None:
        """Create exception."""
        self.message = message
        self.filename = filename
        self.src = source
        self.line = line
        self.char = char

    @property
    def formatted_message(self) -> str:
        """Create beautiful representation of exception."""
        line_str = self.src.splitlines()[self.line - 1]
        line_str_prefix = f"{self.line} |  "
        pointer_margin = " " * (len(line_str_prefix) + self.char)
        return (
            f"{self.message}\n"
            f"At file {self.filename}, line {self.line}, char {self.char}:\n"
            f"{line_str_prefix}{line_str}\n"
            f"{pointer_margin}^"
        )

    def __str__(self):
        """Convert to string repr."""
        return self.formatted_message


class UnexpectedCharacterException(PositionedException):
    """Raised when encountered unexpected character."""

    def __init__(
            self,
            got: str,
            expected: str,
            filename: str,
            source: str,
            line: int,
            char: int
    ) -> None:
        """Create exception and message."""
        got = f"'{got}'" if got else "END OF FILE"
        super().__init__(
            f"Unexpected character {got}, expected '{expected}'",
            filename,
            source,
            line,
            char,
        )


class UnknownDirectiveException(PositionedException):
    """Raised when encountered unexpected directive."""

    def __init__(
            self,
            got: str,
            filename: str,
            source: str,
            line: int,
            char: int
    ) -> None:
        """Create exception and message."""
        super().__init__(
            (
                f"Unexpected character '{got}', "
                f"expected one of {DIRECTIVES.keys()}"
            ),
            filename,
            source,
            line,
            char,
        )


class ParserException(PositionedException):
    """Base class for parser exceptinons."""

    def __init__(
            self,
            message: str,
            filename: str,
            source: str,
            token: Token
    ) -> None:
        """Create exception and transfer location info from token."""
        super().__init__(message, filename, source, token.line, token.char)
        self.token = token


class UnexpectedTokenException(ParserException):
    """Raised when an unexpected token is encountered."""

    default_message = "Expected {expected}, but got {got}"

    def __init__(
            self,
            got: Token | None,
            expected: TokenType | str,
            *,
            filename: str,
            source: str,
            token: Token,
            message: str | None
    ) -> None:
        super().__init__(
            (message or self.default_message).format(
                expected=(
                    expected if isinstance(expected, str)
                    else expected.name
                ),
                got="none" if got is None else got.lexeme
            ),
            filename,
            source,
            token
        )


class IncludeFileNotFoundException(ParserException):
    """Raised when tried to include file that does not exist."""

    default_message = "Tried to include {incl_file}, but it does not exist"

    def __init__(
            self,
            incl_file: str,
            *,
            filename: str,
            source: str,
            token: Token,
            message: str | None = None
    ) -> None:
        super().__init__(
            (message or self.default_message).format(
                incl_file=incl_file
            ),
            filename,
            source,
            token
        )
