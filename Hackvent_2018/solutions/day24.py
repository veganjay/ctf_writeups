#!/usr/bin/env python2

import Rabbit_Cipher
import struct

def solve_bluepill():
    iv = '1071effec36ed401'.decode('hex')
    key = [ 0x87, 0x05, 0x89, 0xcd, 0xa8, 0x75, 0x62, 0xef, 0x38, 0x45, 0xff, 0xd1, 0x41, 0x37, 0x54, 0xd5 ]
    key = ''.join([chr(c) for c in key])

    with open('flag_encrypted.blue', 'rb') as ct:
        blue_bytes = ct.read()
        cipher=Rabbit_Cipher.Rabbit(key, iv)
        data=cipher.crypt(blue_bytes)
    return data

def solve_redpill():
    iv  = '45288109'
    key = iv + iv

    with open('flag_encrypted.red', 'rb') as ct:
        red_bytes = ct.read()
        cipher=Rabbit_Cipher.Rabbit(key, iv)
        data=cipher.crypt(red_bytes)
    return data

if __name__ == "__main__":
    data_redpill = solve_redpill()
    data_bluepill = solve_bluepill()

    with open('red_out.bin', 'wb') as output:
        output.write(data_redpill)

    with open('blue_out.bin', 'wb') as output:
        output.write(data_bluepill)

    # Expected[ 0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a ]
    with open('day24.png', 'wb') as output:
        for blue_byte, red_byte in zip(data_bluepill, data_redpill):
            blue_byte_upper = ord(blue_byte) & 0xf0
            blue_byte_lower = (ord(blue_byte) & 0x0f) << 4
            red_byte_upper = ((ord(red_byte) & 0xf0) >> 4)
            red_byte_lower = (ord(red_byte) & 0x0f)

            combined1 = chr(blue_byte_upper | red_byte_upper)
            combined2 = chr(blue_byte_lower | red_byte_lower)
            output.write(combined1)
            output.write(combined2)
