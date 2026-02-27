import os
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

class ChimeraEngineV5:
    def __init__(self, master_key):
        self._MAP = {0: 'A', 1: 'T', 2: 'G', 3: 'C'}
        self._REV_MAP = {v: k for k, v in self._MAP.items()}
        self._MASTER_KEY = master_key

    def _derive_key(self, salt):
        # NIST Standard: PBKDF2 with 100k iterations
        return PBKDF2(self._MASTER_KEY, salt, dkLen=32, count=100000)

    def _bytes_to_dna(self, data):
        dna = ""
        for b in data:
            for j in range(4):
                dna += self._MAP[(b >> (j * 2)) & 0b11]
        return dna

    def _dna_to_bytes(self, dna):
        data = bytearray()
        for i in range(0, len(dna), 4):
            val = 0
            for j in range(4):
                val |= (self._REV_MAP[dna[i + j]] << (j * 2))
            data.append(val)
        return bytes(data)

    def process_encode(self, raw_str):
        salt = os.urandom(16)
        key = self._derive_key(salt)
        cipher = AES.new(key, AES.MODE_GCM)
        ciphertext, auth_tag = cipher.encrypt_and_digest(raw_str.encode('utf-8'))
        # Packet: Nonce(16) + Tag(16) + Ciphertext
        encrypted_blob = cipher.nonce + auth_tag + ciphertext
        return {
            "sequence": self._bytes_to_dna(encrypted_blob),
            "locus": salt.hex()
        }

    def process_decode(self, dna_sequence, salt_hex):
        salt = bytes.fromhex(salt_hex)
        encrypted_blob = self._dna_to_bytes(dna_sequence)
        nonce, auth_tag, ciphertext = encrypted_blob[:16], encrypted_blob[16:32], encrypted_blob[32:]
        
        key = self._derive_key(salt)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        return cipher.decrypt_and_verify(ciphertext, auth_tag).decode('utf-8')