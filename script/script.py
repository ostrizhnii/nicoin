from logging import getLogger

from crypto.helpers.numendian import little_endian_to_int, int_to_little_endian
from crypto.helpers.varint import read_varint, encode_varint
from script.opfunctions import OP_CODE_FUNCTIONS
from script.opnames import OP_CODE_NAMES

LOGGER = getLogger(__name__)


class Script:
    def __init__(self, cmds=None):
        if cmds is None:
            cmds = []
        self.cmds = cmds

    def __add__(self, other):
        return self.__class__(self.cmds + other.cmds)

    @classmethod
    def parse(cls, stream):
        length = read_varint(stream)
        cmds = []
        count = 0
        while count < length:
            current = stream.read(1)
            count += 1
            current_byte = current[0]
            if 1 <= current_byte <= 75:  # Next n bytes is an element
                n = current_byte
                cmds.append(stream.read(n))
                count += n
            elif current_byte == 76:  # OP_PUSHDATA1
                data_length = little_endian_to_int(stream.read(1))
                cmds.append(stream.read(data_length))
                count += data_length + 1
            elif current_byte == 77:  # OP_PUSHDATA2
                data_length = little_endian_to_int(stream.read(2))
                cmds.append(stream.read(data_length))
                count += data_length + 2
            else:
                op_code = current_byte
                cmds.append(op_code)
        if count != length:
            raise SyntaxError('Script parsing is was failed')
        return cls(cmds)

    def serialize(self):
        result = self.raw_serialize()
        script_length = len(result)
        return encode_varint(script_length) + result

    def raw_serialize(self):
        result = b''
        for cmd in self.cmds:
            if type(cmd) == int:
                result += int_to_little_endian(cmd)
            else:
                length = len(cmd)
                if length <= 75:
                    result += int_to_little_endian(length, 1)
                elif 75 < length < 256:
                    result += int_to_little_endian(length, 2)
                elif 256 <= length <= 520:
                    result += int_to_little_endian(77, 1)
                    result += int_to_little_endian(length, 2)
                else:
                    raise ValueError('cmd {} is too long'.format(cmd))
                result += cmd
        return result

    def evaluate(self, z):
        cmds = self.cmds[:]
        stack = []
        altstack = []
        while len(cmds) > 0:
            cmd = cmds.pop(0)
            if type(cmd) == int:
                operation = OP_CODE_FUNCTIONS[cmd]
                if cmd in (99, 100):
                    if not operation(stack, cmds):
                        LOGGER.info('Bad op: {}'.format(OP_CODE_NAMES[cmd]))
                        return False
                elif cmd in (107, 108):
                    if not operation(stack, altstack):
                        LOGGER.info('Bad op: {}'.format(OP_CODE_NAMES[cmd]))
                        return False
                elif cmd in (172, 173, 174, 175):
                    if not operation(stack, z):
                        LOGGER.info('Bad op: {}'.format(OP_CODE_NAMES[cmd]))
                        return False
                else:
                    if not operation(stack):
                        LOGGER.info('Bad op: {}'.format(OP_CODE_NAMES[cmd]))
                        return False
            else:
                stack.append(cmd)
        if len(stack) == 0:
            return False
        if stack.pop() == b'':
            return False
        return True


