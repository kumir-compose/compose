def char_range(*chars: str) -> str:
    """Get range of chars."""
    res_str = ""
    for crange in chars:
        if len(crange) == 1:
            res_str += crange
        elif len(crange) == 2:
            res_str += _char_range(crange[0], crange[1])
        else:  # pragma: no cover
            raise ValueError(crange)
    return res_str


def _char_range(from_c: str, to_c: str) -> str:
    return "".join(
        map(chr, range(ord(from_c), ord(to_c) + 1))
    )
