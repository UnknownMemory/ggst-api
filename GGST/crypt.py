"""
original code by Theoretical
https://github.com/Theoretical/ggst-py/blob/main/src/crypto.py
"""
from binascii import hexlify, unhexlify
from base64 import urlsafe_b64encode
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from msgpack import packb, unpackb

# key obtained from hooking strive EVP_EncryptInit_ex_0
# RVA: 0x3036460
# Encoding + Concating RVA: 0xB248D0
# GGST Timestamp: 63906742
key = unhexlify('EEBC1F57487F51921C0465665F8AE6D1658BB26DE6F8A069A3520293A572078F')


def encrypt_request_data(data: list):
    msg = packb(data)
    iv = get_random_bytes(12)
    cipher = AES.new(key, AES.MODE_GCM, iv)
    encrypted = cipher.encrypt(msg)
    tag = cipher.digest()
    encrypted = hexlify(iv + encrypted + tag)
    return urlsafe_b64encode(unhexlify(encrypted))


def decrypt_response_data(data: list):
    decoded = unhexlify(data)
    iv = decoded[:12]
    cipher = AES.new(key, AES.MODE_GCM, iv)
    decrypted = cipher.decrypt(decoded[12:])
    return unpackb(decrypted[:-16])
