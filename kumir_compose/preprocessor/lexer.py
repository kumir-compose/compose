from collections.abc import Sequence
from pathlib import Path
from typing import cast

from kumir_compose.preprocessor.exceptions import (
    PositionedException,
    UnexpectedCharacterException,
    UnknownDirectiveException,
)
from kumir_compose.preprocessor.tokens import (
    DIRECTIVES,
    KEYWORDS,
    PUNCTUATION_CHARS,
    VALID_ID_CHARS,
    Token,
    TokenType,
)

type char = str


class Lexer:
    """Lexical analyser."""

    def __init__(self, filename: str, code: str) -> None:
        """Init analyser."""
        self._filename = filename
        self._code = code
        self._tokens: list[Token] = []
        self._pos = 0
        self._start = 0
        self._line = 1
        self._char = 0

    @property
    def _at_end(self) -> bool:
        return self._pos >= len(self._code)

    def _consume(self) -> char:
        if self._at_end:
            raise AssertionError(
                "Unexpected end of stream. "
                "Seems like someone forgot to check for EOF."
            )
        self._pos += 1
        self._char += 1
        return self._code[self._pos - 1]

    @property
    def _peek(self) -> char | None:
        return self._code[self._pos] if not self._at_end else None

    def _add_token(
            self,
            tok_type: TokenType,
            value: str | None = None
    ) -> None:
        lexeme = self._code[self._start:self._pos]
        value = value or lexeme
        if tok_type == TokenType.ID:
            self._pos -= _count_trailing_whitespaces(lexeme)
            lexeme = lexeme.strip()
            value = value.strip()
        self._start = self._pos
        self._tokens.append(
            Token(tok_type, lexeme, value, self._line, self._char)
        )

    def _match(self, target: char) -> char | None:
        if self._peek == target:
            return self._consume()
        return None

    @property
    def _previous(self) -> char:
        return self._code[self._pos - 1]

    def _error(self, exc_type: type[PositionedException], *args, **kwargs) -> None:
        kwargs["filename"] = self._filename
        kwargs["source"] = self._code
        kwargs["line"] = self._line
        kwargs["char"] = self._char
        raise exc_type(*args, **kwargs)

    def _require(self, target: char) -> char:
        ch = self._match(target)
        if ch is None:
            self._error(UnexpectedCharacterException, got=ch, expected=target)
        return cast(char, ch)

    def scan(self) -> Sequence[Token]:
        """Analyse and obtain tokens from code."""
        while not self._at_end:
            self._scan_token()
        return self._tokens

    def _scan_token(self):
        ch = self._consume()
        match ch:
            case "\t" | " ":
                self._add_token(TokenType.SPACE)
            case "\n":
                self._add_token(TokenType.NEWLINE)
                self._char = 0
                self._line += 1
            case "'" | '"':
                self._scan_string()
            case "|":
                if self._match("|"):
                    self._scan_directive()
                else:
                    self._scan_comment()
            case _:
                if ch in PUNCTUATION_CHARS:
                    self._add_token(TokenType.PUNCTUATION)
                elif ch.isnumeric() or ch == ".":
                    self._scan_number()
                elif ch in VALID_ID_CHARS:
                    self._scan_identifier()
                else:
                    self._error(
                        UnexpectedCharacterException,
                        got=ch,
                        expected="any valid kumir syntax"
                    )

    def _scan_string(self) -> None:
        quote = self._previous
        while self._peek and self._peek != quote:
            self._consume()
        lexeme = self._code[self._start + 1:self._pos]
        self._require(quote)
        self._add_token(TokenType.STRING, lexeme)

    def _scan_directive(self) -> None:
        while self._peek == " ":
            self._consume()
        directive_name = ""
        while self._peek and self._peek.isalpha():
            directive_name += self._consume()
        if directive_name not in DIRECTIVES:
            self._error(
                UnknownDirectiveException,
                got=directive_name
            )
        directive_type = DIRECTIVES[directive_name]
        self._add_token(directive_type)

    def _scan_comment(self) -> None:
        while self._peek and self._peek not in "\r\n":
            self._consume()
        self._add_token(TokenType.COMMENT)

    def _scan_number(self) -> None:
        while self._peek and self._peek.isnumeric():
            self._consume()
        if self._match("."):
            while self._peek and self._peek.isnumeric():
                self._consume()
        self._add_token(TokenType.NUMBER)

    def _scan_identifier(self) -> None:
        last_space = self._start
        while self._peek and self._peek in VALID_ID_CHARS:
            if self._peek == " ":
                lexeme = self._code[last_space:self._pos]
                if lexeme.strip() in KEYWORDS:
                    if self._code[self._start:last_space].strip():
                        this_pos = self._pos
                        self._pos = last_space
                        self._add_token(TokenType.ID)
                        self._pos = this_pos
                    self._start = last_space
                    while self._code[self._start] == " ":
                        self._tokens.append(
                            Token(
                                TokenType.SPACE,
                                " ",
                                " ",
                                line=self._line,
                                char=self._start
                            )
                        )
                        self._start += 1
                    self._add_token(TokenType.KEYWORD)
                    return
                last_space = self._pos
            self._consume()
        self._add_token(TokenType.ID)


def _count_trailing_whitespaces(text: str) -> int:  # pragma: no cover
    count = len(text)
    for pos in range(len(text)):  # noqa: WPS518
        if text[-(pos + 1)] != " ":
            count = pos
            break
    return count


def scan_file(filename: str, encoding: str | None = None) -> Sequence[Token]:
    """Scan file to tokens."""
    src = Path(filename).read_text(encoding=encoding)
    lexer = Lexer(filename, src)
    return lexer.scan()
