from operator import attrgetter

from kumir_compose.preprocessor.lexer import Lexer
from tests.utils import read_fix_file


def test_basic_kumir_syntax(snapshot):
    """Test that Kumir syntax is parsed."""
    lexer = Lexer("", read_fix_file("all_possible_lexemes.kum"))
    tokens = lexer.scan()
    str_repr = "\n".join(map(str, tokens))
    assert str_repr == snapshot


def test_original_file_restorable():
    """Test that we can recreate original file from tokens."""
    orig_source = read_fix_file("all_possible_lexemes.kum")
    lexer = Lexer("", orig_source)
    tokens = lexer.scan()
    restored_source = "".join(map(attrgetter("lexeme"), tokens))
    orig_source = orig_source.replace("\r", "")
    assert restored_source == orig_source
