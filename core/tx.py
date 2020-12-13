from core.txin import TxIn
from core.txout import TxOut
from crypto.helpers.hash256 import hash256
from crypto.helpers.numendian import int_to_little_endian, little_endian_to_int
from crypto.helpers.varint import read_varint, encode_varint


class Tx:
    def __init__(self, version, tx_ins, tx_outs, locktime, testnet=False):
        self.version = version
        self.tx_ins = tx_ins
        self.tx_outs = tx_outs
        self.locktime = locktime
        self.testnet = testnet

    def __repr__(self):
        tx_ins = ''
        for tx_in in self.tx_ins:
            tx_ins += tx_in.__repr__() + '\n'
        tx_outs = ''
        for tx_out in self.tx_outs:
            tx_outs += tx_out.__repr__() + '\n'
        return 'tx: {} \n version: {} \n tx_ins: {} \n tx_outs: {} \n locktime: {}'.format(
            self.id(),
            self.version,
            tx_ins,
            tx_outs,
            self.locktime
        )

    def id(self):
        return self.hash().hex()

    def hash(self):
        return hash256(self.serialize())[::-1]

    @classmethod
    def parse(cls, stream, testnet=False):
        version = little_endian_to_int(stream.read(4))
        tx_ins = cls.__parse_tx_ins(stream)
        tx_outs = cls.__parse_tx_outs(stream)
        locktime = little_endian_to_int(stream.read(4))
        return cls(version, tx_ins, tx_outs, locktime, testnet)

    @staticmethod
    def __parse_tx_ins(stream):
        tx_ins = []
        tx_ins_count = read_varint(stream)
        for _ in range(tx_ins_count):
            tx_ins += TxIn.parse(stream)
        return tx_ins

    @staticmethod
    def __parse_tx_outs(stream):
        tx_outs = []
        tx_outs_count = read_varint(stream)
        for _ in range(tx_outs_count):
            tx_outs += TxOut.parse(stream)
        return tx_outs

    def serialize(self):
        result = int_to_little_endian(self.version, 4)
        result += self.__serialize_tx_ins()
        result += self.__serialize_tx_outs()
        result += int_to_little_endian(self.locktime, 4)

    def __serialize_tx_ins(self):
        result = encode_varint(len(self.tx_ins))
        for tx_in in self.tx_ins:
            result += tx_in.serialize()
        return result

    def __serialize_tx_outs(self):
        result = encode_varint(len(self.tx_outs))
        for tx_out in self.tx_outs:
            result += tx_out.serialize()
        return result

    def fee(self, testnet=False):
        tx_ins_amount = 0
        for tx_in in self.tx_ins:
            tx_ins_amount += tx_in.value(testnet)
        tx_outs_amount = 0
        for tx_out in self.tx_outs:
            tx_outs_amount += tx_out.amount
        return tx_ins_amount - tx_outs_amount
