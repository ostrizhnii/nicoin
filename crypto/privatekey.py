import hashlib
import hmac

from crypto.helpers.encode_base58 import encode_base58_checksum
from crypto.helpers.numendian import big_endian_to_int, int_to_bit_endian
from crypto.s256point import G, N
from crypto.signature import Signature


class PrivateKey:
    def __init__(self, secret):
        self.secret = secret
        self.public = secret * G

    def __repr__(self):
        return '{:x}'.format(self.secret).zfill(64)

    def sign(self, z):
        k = self.deterministic_k(z)
        k_inv = pow(k, N - 2, N)
        r = (k * G).x.num
        s = (z + self.secret * r) * k_inv % N
        if s > N / 2:
            s = N - s
        return Signature(r, s)

    def deterministic_k(self, z):
        k = b'\x00' * 32
        v = b'\x01' * 32
        if z > N:
            z -= N
        z_bytes = int_to_bit_endian(z)
        secret_bytes = int_to_bit_endian(self.secret)
        sha256 = hashlib.sha256
        k = hmac.new(k, v + b'\x00' + secret_bytes + z_bytes, sha256).digest()
        v = hmac.new(k, v, sha256).digest()
        k = hmac.new(k, v + b'\x01' + secret_bytes + z_bytes, sha256).digest()
        v = hmac.new(k, v, sha256).digest()
        while True:
            v = hmac.new(k, v, sha256).digest()
            candidate = big_endian_to_int(v)
            if 1 < candidate < N:
                return candidate
            k = hmac.new(k, v + b'\x00', sha256).digest()
            v = hmac.new(k, v, sha256).digest()

    def wif(self, compressed=True, testnet=False):
        secret_bytes = int_to_bit_endian(self.secret)
        prefix = b'\xef' if testnet else b'\x80'
        suffix = b'\x01' if compressed else b''
        return encode_base58_checksum(prefix + secret_bytes + suffix)
