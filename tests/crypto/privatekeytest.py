from unittest import TestCase

from crypto.privatekey import PrivateKey


class PrivateKeyTest(TestCase):
    def test_wif(self):
        private_key = PrivateKey(5003)
        expected_wif = 'cMahea7zqjxrtgAbB7LSGbcQUr1uX1ojuat9jZodMN8rFTv2sfUK'
        self.assertEqual(expected_wif, private_key.wif(True, True))
        private_key = PrivateKey(2021 ** 5)
        expected_wif = '91avARGdfge8E4tZfYLoxeJ5sGBdNJQH4kvjpWAxgzczjbCwxic'
        self.assertEqual(expected_wif, private_key.wif(False, True))
        private_key = PrivateKey(0x54321deadbeef)
        expected_wif = 'KwDiBf89QgGbjEhKnhXJuH7LrciVrZi3qYjgiuQJv1h8Ytr2S53a'
        self.assertEqual(expected_wif, private_key.wif(True, False))
