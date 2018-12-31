#!/usr/bin/env python

import binascii

ciphertext = binascii.unhexlify('a891997b60d8c6dd7ef4334f20f77f4a8c5cffb7443e3498efd93d761cb2d288cf3f97234355d0b8caaacfa54f0ba69de174080b7acb07338398a3a4d8a7a2a3ec7fd935bbfceb392b7141efd247163398264abf8b5315d3f2b934c22788a5b5056c47dba25b5dad4f95bf847320a84e0053feffb4709486f04fbd24c35fcf2b78960f91c262edc12e4480c55cd45582f30f331c91a905')
provided = 'Thank You Mario, But Our Princess is in Another Castle. Encrypt this: f42df92b389fffca59598465c7a51d36082ecfea567a900e5eac9e5e9fb1'
encrypt_this = binascii.unhexlify('f42df92b389fffca59598465c7a51d36082ecfea567a900e5eac9e5e9fb1')

keystream = [(ord(a) - ord(b)) % 256 for a, b in zip(ciphertext, provided)]
plaintext = ''.join([chr((ord(a) + b) % 256) for a, b in zip(encrypt_this, keystream)])
print plaintext
