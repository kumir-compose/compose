def serialize(data: str) -> str:
    return "".join(
        hex(ord(c))[2:].zfill(4) for c in data
    )


def assemble_list(items: list[str]) -> str:
    list_str = f"{chr(28)}L{len(items)}"
    for item in items:
        list_str += chr(29) + item
    return list_str


def assemble_dict(items: dict[str, str]) -> str:
    d_keys = f"{chr(28)}L{len(items)}"
    d_items = f"{chr(28)}L{len(items)}"
    for k, v in items.items():
        d_keys += chr(29) + k
        d_items += chr(29) + v
    return chr(30) + d_keys + chr(30) + d_items
