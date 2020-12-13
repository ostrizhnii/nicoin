from script.opcode.op_checksig import op_checksig
from script.opcode.op_dup import op_dup
from script.opcode.op_hash160 import op_hash160
from script.opcode.op_hash256 import op_hash256

OP_CODE_FUNCTIONS = {
    118: op_dup,
    169: op_hash160,
    170: op_hash256,
    172: op_checksig,
}
