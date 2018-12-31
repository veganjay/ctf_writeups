#!/usr/bin/env python3

from spritz import Spritz
import binascii

# provided = 'Thank You Mario, But Our Princess is in Another Castle. Encrypt this: f42df92b389fffca59598465c7a51d36082ecfea567a900e5eac9e5e9fb1'
key = bytearray(b'shuffle*whip$crush%squeeze\x00')

spritz = Spritz()
output = spritz.encrypt(key, bytearray.fromhex('f42df92b389fffca59598465c7a51d36082ecfea567a900e5eac9e5e9fb1'))
print(output.decode('utf-8'))
