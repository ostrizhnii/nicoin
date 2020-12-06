from crypto.fieldelement import FieldElement
from crypto.secp256k1 import *


class S256FieldElement(FieldElement):
    def __init__(self, num, prime=None):
        super().__init__(num, P)

    def __repr__(self):
        return '{:x}'.format(self.num).zfill(64)
