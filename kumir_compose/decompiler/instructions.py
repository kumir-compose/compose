from types import MappingProxyType
from typing import Final

from attrs import frozen


@frozen
class InstructionType:
    opcode: int
    name: str
    args: tuple[str, ...] = tuple()
    doc: str = ""


_INSTRUCTIONS: Final = (
    InstructionType(
        0x00, "NOP", (),
        "No operation"
    ),
    InstructionType(
        0x0A, "CALL", (),
        "Call compiled function"
    ),
    InstructionType(
        0x0C, "INIT", (),
        "Initialize variable"
    ),
    InstructionType(
        0x0D, "SETARR", (),
        "Set array bounds"
    ),
    InstructionType(
        0x0E, "STORE", (),
        "Store value in variable"
    ),
    InstructionType(
        0x0F, "STOREARR", (),
        "Store value in array"
    ),
    InstructionType(
        0x10, "LOAD", (),
        "Get value from variable"
    ),
    InstructionType(
        0x11, "LOADARR", (),
        "Get value froma array"
    ),
    InstructionType(
        0x12, "SETMON", (),
        "Set variable monitor"
    ),
    InstructionType(
        0x13, "UNSETMON", (),
        "Unset variable monitor"
    ),
    InstructionType(
        0x14, "JUMP", (),
        "Unconditional jump"
    ),
    InstructionType(
        0x15, "JNZ", (),
        "Conditional jump if non-zero value in specified register"
    ),
    InstructionType(
        0x16, "JZ", (),
        "Conditional jump if zero value in specified register"
    ),
    InstructionType(
        0x18, "POP", (),
        "Pop from stack to register"
    ),
    InstructionType(
        0x19, "PUSH", (),
        "Push to stack from register"
    ),
    InstructionType(
        0x1B, "RET", (),
        "Return from function"
    ),
    InstructionType(
        0x1D, "PAUSE", (),
        "Force pause"
    ),
    InstructionType(
        0x1E, "ERRORR", (),
        "Abort evaluation"
    ),
    InstructionType(
        0x1F, "LINE", (),
        "Emit line number"
    ),
    InstructionType(
        0x20, "REF", (),
        "Get reference to variable"
    ),
    InstructionType(
        0x21, "REFARR", (),
        "Get reference to array element"
    ),
    InstructionType(
        0x22, "SHOWREG", (),
        "Show register value at margin"
    ),
    InstructionType(
        0x23, "CLEARMARG", (),
        "Clear margin text from current line to specified"
    ),
    InstructionType(
        0x24, "SETREF", (),
        "Set reference value to variable"
    ),
    InstructionType(
        0x26, "HALT", (),
        "Terminate"
    ),
    InstructionType(
        0x27, "CTL", (),
        "Control VM behaviour"
    ),
    InstructionType(
        0x28, "INRANGE", (),
        "Pops 4 values...a, b, c, x from stack and "
        "returns c >= 0? a < x <= b: a <= x < b"
    ),
    InstructionType(
        0x29, "UPDARR", (),
        "Updates array bounds"
    ),

    InstructionType(
        0x30, "CSTORE", (),
        "Copy value from stack head and push it to cache"
    ),
    InstructionType(
        0x31, "CLOAD", (),
        "Pop value from cache to push it to main stack"
    ),
    InstructionType(
        0x32, "CDROPZ", (),
        "Drop cache value in case of zero value in specified register"
    ),
    InstructionType(
        0x33, "CACHEBEGIN", (),
        "Push begin marker into cache"
    ),
    InstructionType(
        0x34, "CACHEEND", (),
        "Clear cache until marker"
    ),
    InstructionType(
        0xF1, "SUM", (),
        "Arithmetic SUM operator"
    ),
    InstructionType(
        0xF2, "SUB", (),
        "Arithmetic SUB operator"
    ),
    InstructionType(
        0xF3, "MUL", (),
        "Arithmetic MUL operator"
    ),
    InstructionType(
        0xF4, "DIV", (),
        "Arithmetic DIV operator"
    ),
    InstructionType(
        0xF5, "POW", (),
        "Arithmetic POW operator"
    ),
    InstructionType(
        0xF6, "NEG", (),
        "Arithmetic NEG operator"
    ),
    InstructionType(
        0xF7, "AND", (),
        "Arithmetic AND operator"
    ),
    InstructionType(
        0xF8, "OR", (),
        "Arithmetic OR operator"
    ),
    InstructionType(
        0xF9, "EQ", (),
        "Arithmetic EQ operator"
    ),
    InstructionType(
        0xFA, "NEQ", (),
        "Arithmetic NEQ operator"
    ),
    InstructionType(
        0xFB, "LS", (),
        "Arithmetic LS operator"
    ),
    InstructionType(
        0xFC, "GT", (),
        "Arithmetic GT operator"
    ),
    InstructionType(
        0xFD, "LEQ", (),
        "Arithmetic LEQ operator"
    ),
    InstructionType(
        0xFE, "GEQ", (),
        "Arithmetic GEQ operator"
    )
)

INSTRUCTIONS: Final = MappingProxyType(
    {
        instr.opcode: instr for instr in _INSTRUCTIONS
    }
)


@frozen
class Instruction:
    location: int
    type: InstructionType
    args: dict[str, int]

    def __str__(self) -> str:
        arg_str = ", ".join(f"{k}={v}" for k, v in self.args.items())
        return f"{self.location:04} | {self.type.name}({arg_str})"
