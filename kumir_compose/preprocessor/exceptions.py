from kumir_compose.preprocessor.tokens import DIRECTIVES


class LexerException(Exception):
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


class UnexpectedCharacterException(LexerException):
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


class UnknownDirectiveException(LexerException):
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
