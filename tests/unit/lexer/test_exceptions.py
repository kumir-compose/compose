import pytest

from kumir_compose.preprocessor.exceptions import (
    UnexpectedCharacterException,
    UnknownDirectiveException,
)
from kumir_compose.preprocessor.lexer import Lexer


@pytest.mark.parametrize(
    ("src", "expected_exception"),
    [
        (
            "|| unknown directive",
            UnknownDirectiveException
        ),
        (
            "|| задать,",
            UnexpectedCharacterException
        ),
        (
            "^",
            UnexpectedCharacterException
        ),
        (
            '"abcabc',
            UnexpectedCharacterException
        )
    ]
)
def test_invalid_code(src, expected_exception):
    """Test that invalid code raises exceptions."""
    lexer = Lexer("", src)
    with pytest.raises(expected_exception):
        lexer.scan()


def test_exception_formatting():
    """Test that exceptions are formatted correctly."""
    exception = UnexpectedCharacterException(
        got="1",
        expected="2",
        filename="file.name",
        source="...\n...\nprint 1\n...",
        line=3,
        char=6
    )
    expected = (
        "Unexpected character '1', expected '2'\n"
        "At file file.name, line 3, char 6:\n"
        "3 |  print 1\n"
        "           ^"
    )
    assert str(exception) == expected
