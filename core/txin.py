from core.txfetcher import TxFetcher
from crypto.helpers.numendian import little_endian_to_int, int_to_little_endian
from script.script import Script


class TxIn:
    def __init__(self, prev_tx, prev_index, sig_script=None, sequence=0xffffffff):
        self.prev_tx = prev_tx
        self.prev_index = prev_index
        self.sig_script = Script() if sig_script is None else sig_script
        self.sequence = sequence

    def __repr__(self):
        return '{}:{}'.format(self.prev_tx.hex(), self.prev_index)

    @classmethod
    def parse(cls, stream):
        prev_tx = stream.read(32)[::-1]
        prev_index = little_endian_to_int(stream.read(4))
        sig_script = Script.parse(stream)
        sequence = little_endian_to_int(stream.read(4))
        return cls(prev_tx, prev_index, sig_script, sequence)

    def serialize(self):
        result = self.prev_tx[::-1]
        result += int_to_little_endian(self.prev_index, 4)
        result += self.sig_script.serizlize()
        result += int_to_little_endian(self.sequence, 4)
        return result

    def fetch_tx(self, testnet=False):
        return TxFetcher.fetch(self.prev_tx.hex(), testnet)

    def value(self, testnet=False):
        tx = self.fetch_tx(testnet)
        return tx.tx_outs[self.prev_index].amount

    def pubkey_script(self, testnet=False):
        tx = self.fetch_tx(testnet)
        return tx.tx_outs[self.prev_index].pubkey_script

