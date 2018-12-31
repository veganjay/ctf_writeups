#!/usr/bin/env python

import cryptomath

# coding: utf-8
ct = int('1398ED7F59A62962D5A47DD0D32B71156DD6AF6B46BEA949976331B8E1', 16)

p = 73197682537506302133452713613304371
q = 79797652691134123797009598697137499
n = p * q 

assert(n ==  0x0D8A7A45D9BE42BB3F03F710CF105628E8080F6105224612481908DC721)

phi = (p - 1) * (q - 1)

e = 65537
d = cryptomath.findModInverse(e, phi)

pt = (pow(ct, d, n))

pt_hex = '%x' % pt

print pt_hex.decode('hex')

