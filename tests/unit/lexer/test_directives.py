from kumir_compose.preprocessor.lexer import Lexer
from tests.utils import read_fix_file


def test_directives_parsed(snapshot):
    """Test that directives are parsed."""
    lexer = Lexer("", read_fix_file("directives.kum"))
    tokens = lexer.scan()
    str_repr = "\n".join(map(str, tokens))
    assert str_repr == snapshot
