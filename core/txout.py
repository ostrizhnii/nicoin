from crypto.helpers.numendian import little_endian_to_int, int_to_little_endian
from script.script import Script


class TxOut:
    def __init__(self, amount, pubkey_script):
        self.amount = amount
        self.pubkey_script = pubkey_script

    def __repr__(self):
        return '{}:{}'.format(self.amount, self.pubkey_script)

    @classmethod
    def parse(cls, stream):
        amount = little_endian_to_int(stream.read(8))
        pubkey_script = Script.parse(stream)
        return cls(amount, pubkey_script)

    def serialize(self):
        result = int_to_little_endian(self.amount, 8)
        result += self.pubkey_script.serialize()
        return result
