#!/usr/bin/env python

'''
Santa has caught up with the information age and does not trust
clear-text commands anymore.  
He has decided that all communications
have to be encrypted to prevent an unfriendly take-over of his team.
Santa chooses a simple, secure, and toolless encryption scheme.
However, his team's memory capacity is limited and so he can only use
their names (Dasher, Dancer, Prancer, Vixen, Comet, Cupid, Donder and
Blitzen) as keys.
Where is the team headed to?
'''

keys = [ 'Dasher', 'Dancer', 'Prancer', 'Vixen', 'Comet', 'Cupid', 'Donder', 'Blitzen' ]
ciphertext = 'STTYN YATLOEP DNEA ONBL TGNTO MHEHH EISTIARIB FHSRA LD IIONA NL HERUV LN17-PTAA-RTON-RDOE-MCTN-AHCO'

from pycipher import ColTrans
import itertools

def attempt(k, ct, chain=''):
    result = ColTrans(k).decipher(ct)
    if 'SANTA' in result or 'HV17' in result:
        print '{}: {}'.format(chain, result)
    return result

for combos in itertools.permutations(keys,2):
    result = ciphertext
    current = ''
    for key in combos:
        current += ' ' + key
        result = attempt(key, result, current)
