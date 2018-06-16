# -*- coding: utf-8 -*-
from bitarray import bitarray


def xor_at(a, b, offset=0):
    for k, bk in enumerate(b):
        index = offset + k
        a[index] = a[index] ^ bk


def crc(d, g):
    # We'd prefer not to modify the argument in xor_at
    dcopy = d.copy()

    # Generator/data length
    gLength = len(g)
    dLength = len(dcopy)

    # Empty bitarray, of generator length
    gZero = bitarray([0] * gLength)

    # Loop through, and perform necessary edits to data, via xor_at
    for i in range(0, (dLength - gLength + 1)):
        # If leading bit is zero, perform xor_at with zeroes bitarray
        if (dcopy[i] == 0):
            xor_at(dcopy, gZero, i)
        # Else perform xor_at with original generator
        else:
            xor_at(dcopy, g, i)

    # Return the appropriate remainder
    return dcopy[dLength - gLength + 1: dLength]


if __name__ == '__main__':

    print("From Kurose & Ross (7e), page 478:")
    g = bitarray('1001')            # generator
    d = bitarray('101110')          # data (without padding/shifting)
    p = bitarray('000')             # padding
    r = crc(d + p, g)               # error-correction bits
    assert r == bitarray('011')     # known quotient
    assert crc(d + r, g) == p       # perform CRC check

    print("From Wikipedia, [en.wikipedia.org/wiki/Cyclic_redundancy_check]:")
    g = bitarray('1011')            # generator
    d = bitarray('11010011101100')  # data (without padding/shifting)
    p = bitarray('000')             # padding
    r = crc(d + p, g)               # error-correction bits
    assert r == bitarray('100')     # known quotient
    assert crc(d + r, g) == p       # perform CRC check
