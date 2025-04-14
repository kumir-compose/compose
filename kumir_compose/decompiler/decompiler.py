from collections.abc import Sequence

from kumir_compose.decompiler.exceptions import DecompilerException
from kumir_compose.decompiler.instructions import INSTRUCTIONS, Instruction


class Decompiler:
    def __init__(self, code: bytes) -> None:
        self._code = code
        self._i = 0
        self._instr = []

    @property
    def _at_end(self):
        return self._i >= len(self._code)

    def _error(self, message: str) -> None:
        raise DecompilerException(self._i, message)

    def _next(self) -> int:
        if self._at_end:
            self._error("Unexpected end")
        self._i += 1
        return self._code[self._i - 1]

    def decompile(self) -> Sequence[Instruction]:
        while not self._at_end:
            self._scan_opcode()
        return self._instr

    def _scan_opcode(self) -> None:
        loc = self._i
        opcode = self._next()
        if opcode not in INSTRUCTIONS:
            self._error(f"Unknown opcode {hex(opcode)}")
        instr_type = INSTRUCTIONS[opcode]
        args = {arg_name: self._next() for arg_name in instr_type.args}
        self._instr.append(Instruction(loc, instr_type, args))


if __name__ == '__main__':
    code = bytes([
        0x00, 0x01, 0x02, 0x0A
    ])
    decompiler = Decompiler(code)
    decompiled = decompiler.decompile()
    print("\n".join(map(str, decompiled)))
