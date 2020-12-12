from unittest import TestCase

from crypto.helpers.hash256 import hash256
from crypto.helpers.numendian import big_endian_to_int
from crypto.privatekey import PrivateKey
from crypto.s256point import S256Point


class S256PointTest(TestCase):
    def test_sign_and_verify(self):
        message_hash = big_endian_to_int(hash256(b'Programming Bitcoin!'))
        private_key = PrivateKey(12345)
        signature = private_key.sign(message_hash)
        self.assertTrue(private_key.public.verify(message_hash, signature))

    def test_sec_uncompressed(self):
        e = 5000
        expect = '04ffe558e388852f0120e46af2d1b370f85854a8eb0841811ece0e3e03d282d57c315dc72890a4f10a1481c031b03b351b0dc79901ca18a00cf009dbdb157a1d10'
        public_key = PrivateKey(e).public
        self.assertTrue(public_key.sec(False).hex() == expect)
        self.assertTrue(S256Point.parse(bytes.fromhex(expect)) == public_key)
        e = 2018 ** 5
        expect = '04027f3da1918455e03c46f659266a1bb5204e959db7364d2f473bdf8f0a13cc9dff87647fd023c13b4a4994f17691895806e1b40b57f4fd22581a4f46851f3b06'
        public_key = PrivateKey(e).public
        self.assertTrue(public_key.sec(False).hex() == expect)
        self.assertTrue(S256Point.parse(bytes.fromhex(expect)) == public_key)
        e = 0xdeadbeef12345
        expect = '04d90cd625ee87dd38656dd95cf79f65f60f7273b67d3096e68bd81e4f5342691f842efa762fd59961d0e99803c61edba8b3e3f7dc3a341836f97733aebf987121'
        public_key = PrivateKey(e).public
        self.assertTrue(S256Point.parse(bytes.fromhex(expect)) == public_key)
        self.assertTrue(public_key.sec(False).hex() == expect)

    def test_sec_compressed(self):
        e = 5001
        expect = '0357a4f368868a8a6d572991e484e664810ff14c05c0fa023275251151fe0e53d1'
        public_key = PrivateKey(e).public
        self.assertTrue(public_key.sec(True).hex() == expect)
        self.assertTrue(S256Point.parse(bytes.fromhex(expect)) == public_key)
        e = 2019 ** 5
        expect = '02933ec2d2b111b92737ec12f1c5d20f3233a0ad21cd8b36d0bca7a0cfa5cb8701'
        public_key = PrivateKey(e).public
        self.assertTrue(public_key.sec(True).hex() == expect)
        self.assertTrue(S256Point.parse(bytes.fromhex(expect)) == public_key)
        e = 0xdeadbeef54321
        expect = '0296be5b1292f6c856b3c5654e886fc13511462059089cdf9c479623bfcbe77690'
        public_key = PrivateKey(e).public
        self.assertTrue(S256Point.parse(bytes.fromhex(expect)) == public_key)
        self.assertTrue(public_key.sec(True).hex() == expect)

    def test_address(self):
        private_key = PrivateKey(5002)
        expected_address = 'mmTPbXQFxboEtNRkwfh6K51jvdtHLxGeMA'
        self.assertEqual(expected_address, private_key.public.address(False, True))
        private_key = PrivateKey(2020 ** 5)
        expected_address = 'mopVkxp8UhXqRYbCYJsbeE1h1fiF64jcoH'
        self.assertEqual(expected_address, private_key.public.address(True, True))
        private_key = PrivateKey(0x12345deadbeef)
        expected_address = '1F1Pn2y6pDb68E5nYJJeba4TLg2U7B6KF1'
        self.assertEqual(expected_address, private_key.public.address(True, False))

