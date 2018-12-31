#!/usr/bin/env python3

import numpy as np
import string
from PIL import Image

flip = 1

matrix = np.array([
    [1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1],
    [1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1],
    [0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1],
    [0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0],
    [1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1],
    [0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
    [1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1],
    [0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0],
    [0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0],
    [1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1],
    [1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0],
    [0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1],
    [1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1],
    [0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1],
    [0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0],
    [1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
    [1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1],
    [1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1],
    [1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1],
    [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1],
    [1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
    ])

def spiral_print(m, n, a):
    '''
    Arguments:
        m (int): ending row index
        n (int): ending column index
        a ([int, int]): two dimensional array
    '''
    i = 0 # iterator
    k = 0 # Starting row index
    l = 0 # Starting column index

    result = ''

    while k < m and l < n:
        # Print the first row from the remaining rows
        i = l
        while i < n:
            result += str(a[k][i])
            i += 1
        k += 1

        # Print the last column from the remaining columns
        i = k
        while i < m:
            result += str(a[i][n - 1])
            i += 1

        n -= 1

        # Print the last row from the remaining rows
        if k < m:
            i = n - 1
            while i >= l: 
                result += str(a[m - 1][i])
                i -= 1
            m -= 1

        # Print the first column for the remaining columns
        if l < n:
            i = m - 1
            while i >= k: 
                result += str(a[i][l])
                i -= 1
            l += 1

    return result

def spiral_reverse(m, n, a):
    '''
    Arguments:
        m (int): ending row index
        n (int): ending column index
        a ([int, int]): two dimensional array
    '''
    i = 0 # iterator
    k = 0 # Starting row index
    l = 0 # Starting column index

    values = []

    while k < m and l < n:
        # Print the first row from the remaining rows
        i = l
        while i < n:
            values.append(a[k][i])
            i += 1
        k += 1

        # Print the last column from the remaining columns
        i = k
        while i < m:
            values.append(a[i][n - 1])
            i += 1

        n -= 1

        # Print the last row from the remaining rows
        if k < m:
            i = n - 1
            while i >= l: 
                values.append(a[m - 1][i])
                i -= 1
            m -= 1

        # Print the first column for the remaining columns
        if l < n:
            i = m - 1
            while i >= k: 
                values.append(a[i][l])
                i -= 1
            l += 1

    # Now copy the elements in reverse
    m = 25
    n = 25

    i = 0 # iterator
    k = 0 # Starting row index
    l = 0 # Starting column index
    result = np.zeros([25,25])

    #values.reverse()

    while k < m and l < n:
        # Print the first row from the remaining rows
        i = l
        while i < n:
            result[k][i] = values.pop()
            i += 1
        k += 1

        # Print the last column from the remaining columns
        i = k
        while i < m:
            result[i][n - 1] = values.pop()
            i += 1

        n -= 1

        # Print the last row from the remaining rows
        if k < m:
            i = n - 1
            while i >= l: 
                result[m - 1][i] = values.pop()
                i -= 1
            m -= 1

        # Print the first column for the remaining columns
        if l < n:
            i = m - 1
            while i >= k: 
                result[i][l] = values.pop()
                i -= 1
            l += 1

    return result

def reverse(s): 
    str = "" 
    for i in s: 
        str = i + str
    return str

def flip_bits(s):
    return s.replace('1', 'Z').replace('0', '1').replace('Z', '0')

def first_row():
    x = ''
    for i in range(1,25):
        #x = x + str(matrix[0][i])
        x = str(matrix[0][i]) + x
    return x

def first_col(a=matrix):
    x = ''
    for i in range(25):
        x = x + str(matrix[i][0])
    return x

def last_row(a=matrix):
    x = ''
    for i in range(1,25):
        #x = x + str(matrix[0][i])
        x = str(matrix[24][i]) + x
    return x

def last_col(a=matrix):
    x = ''
    for i in range(25):
        x = x + str(matrix[i][24])
    return x

def do_print(s):
    print(s)
    for i in range(len(s)):
        print_chars(s, i)
        print_chars(flip_bits(s), i)
        print_chars(reverse(s), i)
        print_chars(reverse(flip_bits(s)), i)

def print_as_matrix(s):
    start = 0
    end = 25

    while end <= len(s):
        print(s[start:end])
        start +=25
        end += 25

def write_image_old(data, name):
    imgdata = []

    for y in range(0, 25): 
        for x in range(0, 25):
            val = data[y][x]
            imgdata.append(1 if val == 0 else 0)
    
    img = Image.new("1", (25, 25))
    img.putdata(imgdata)
    img.save(name)

def write_image(data, name):
    imgdata = []

    for c in data:
        if c == '0':
            imgdata.append(1)
        else:
            imgdata.append(0)

    img = Image.new("1", (25, 25))
    img.putdata(imgdata)
    img.save(name)


def try_flip(m):
    global flip
    m_flip = np.flip(m)
    result_flip = spiral_print(25, 25, m)
    print_as_matrix(result_flip)
    print(' ')
    write_image(result_flip, 'flip{}.png'.format(flip))
    write_image(reverse(result_flip), 'flip{}-rev.png'.format(flip))
    flip += 1

def try_spiral_reverse():
    result = spiral_reverse(25, 25, matrix)
    write_image(result, 'result1.png')

    matrix2 = np.rot90(matrix)
    result2 = spiral_reverse(25, 25, matrix2)
    write_image(result2, 'result2.png')

    matrix3 = np.rot90(matrix2)
    result3 = spiral_reverse(25, 25, matrix3)
    write_image(result3, 'result3.png')

    matrix4 = np.rot90(matrix3)
    result4 = spiral_reverse(25, 25, matrix4)
    write_image(result4, 'result4.png')

if __name__ == '__main__':
    matrix1 = matrix
    matrix2 = np.rot90(matrix1)
    matrix3 = np.rot90(matrix2)
    matrix4 = np.rot90(matrix3)

    matrix5 = np.flip(matrix1,axis=1)
    matrix6 = np.flip(matrix2,axis=1)
    matrix7 = np.flip(matrix3,axis=1)
    matrix8 = np.flip(matrix4,axis=1)

    i = 1
    for m in [matrix1, matrix2, matrix3, matrix4, matrix5, matrix6, matrix7, matrix8]:
        result = spiral_print(25,25,m)
        print_as_matrix(result)
        write_image(result, 'result{}.png'.format(i))
        i = i + 1
        print(' ')
        print_as_matrix(reverse(result))
        write_image(reverse(result), 'result{}.png'.format(i))
        print(' ')
        i = i + 1
