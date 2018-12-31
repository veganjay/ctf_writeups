#!/usr/bin/env python

import zipfile
import shutil

CHARACTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ .1234567890-!@#$%^&**(),.<>;:;"\''

def crack_character(zipfilename):
    zip_file = zipfile.ZipFile(zipfilename)
    for char in CHARACTERS:
        try:
            char = char.strip('\n')
            zip_file.extractall(pwd=char)
            password = 'Password found: %s' % char
            print(password)
            return char
        except Exception as e:
            pass

def main():
    """
    Zipfile password cracker using a brute-force dictionary attack
    """
    zipfilename = 'z-cur.zip'
    shutil.copyfile('z-orig.zip', zipfilename)

    result = ''

    for i in range(1100):
        password = crack_character(zipfilename)
        result += password
        print 'result = {}'.format(result)
        shutil.copyfile('z.zip', zipfilename)

    print(password)

if __name__ == '__main__':
   main()
