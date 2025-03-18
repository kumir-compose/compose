import enum
from types import MappingProxyType
from typing import Final

from attrs import frozen

from kumir_compose.preprocessor.char_range import char_range


class TokenType(enum.Enum):
    """Defines a token type."""

    ID = enum.auto()
    PUNCTUATION = enum.auto()
    STRING = enum.auto()
    KEYWORD = enum.auto()
    COMMENT = enum.auto()
    SPACE = enum.auto()
    NEWLINE = enum.auto()
    NUMBER = enum.auto()

    DEFINE = enum.auto()
    IFDEF = enum.auto()
    IFNDEF = enum.auto()
    ENDIF = enum.auto()
    UNDEF = enum.auto()
    INCLUDE = enum.auto()


@frozen
class Token:
    """Represents a token."""

    type: TokenType
    lexeme: str
    value: str
    line: int
    char: int

    def __str__(self):
        """Convert token to string representation with info."""
        return f"{self.type}:{self.lexeme}:{self.line}:{self.char}"


KEYWORDS: Final = frozenset((
    "аргрез", "знач", "цел", "вещ",
    "лог", "сим", "лит", "таб",
    "целтаб", "вещтаб", "логтаб",
    "литтаб", "и", "или", "не", "да",
    "нет", "утв", "выход", "ввод", "вывод",
    "нс", "если", "то", "иначе", "все",
    "выбор", "при", "нц", "кц", "кц_при",
    "раз", "пока", "для", "от", "до", "шаг",
    "алг", "нач", "кон", "исп", "кон_исп",
    "дано", "надо", "арг", "рез",
))

PUNCTUATION_CHARS: Final = frozenset(
    "()[]+-*/,<>:=;"
)

DIRECTIVES: Final = MappingProxyType({
    "включить": TokenType.INCLUDE,
    "еслизад": TokenType.IFDEF,
    "еслинезад": TokenType.IFNDEF,
    "задать": TokenType.DEFINE,
    "конецесли": TokenType.ENDIF,
    "забыть": TokenType.UNDEF,
})
DIRECTIVES_WITH_ARGS: Final = frozenset((
    "включить",
    "еслизад",
    "еслинезад",
    "задать",
    "забыть",
))

VALID_ID_CHARS: Final = frozenset(
    char_range("AZ", "az", "АЯ", "ая", "_", " ", "09")
)
