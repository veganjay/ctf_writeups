#!/usr/bin/env python2

import Rabbit_Cipher
import struct
import Filetimes

def bluepill_crunch(msg):
    f = []
    for index in range(0, len(msg), 2):
        f.append(((msg[index] & 0xf0)) | ((msg[index+1] >> 4) & 0x0f))
    return f

def attempt(msg, out, key, iv):
    cipher=Rabbit_Cipher.Rabbit(key, iv)
    data=cipher.crypt(Rabbit_Cipher.st(msg))

    match = True
    for x, y in zip(out, data):
        if ord(y) != x:
            match = False

    if match:
        print '[+] Found iv={}'.format(iv.encode('hex'))

    return match

def brute():
    key = [ 0x87, 0x05, 0x89, 0xcd, 0xa8, 0x75, 0x62, 0xef, 0x38, 0x45, 0xff, 0xd1, 0x41, 0x37, 0x54, 0xd5 ]
    key = ''.join([chr(c) for c in key])

    guess = 0x1d49ef8a010f190 - 10000
    msg = [ 0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a ]
    out = [ 0x7e, 0x42, 0xe9, 0x41 ]
    blue = bluepill_crunch(msg)

    for guess in xrange(0x1d49ef8a010f190 - 1000, 0x1d49ef8a010f190 + 1000):
        iv = struct.pack('<Q', guess)
        attempt(blue, out, key, iv)

if __name__ == "__main__":
    brute()
