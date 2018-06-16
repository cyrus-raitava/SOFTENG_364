# -*- coding: utf-8 -*-


def hextet_complement(num):
    '''
    Internet Checksum of a bytes array.
    Further reading:
    1. https://tools.ietf.org/html/rfc1071
    2. http://www.netfor2.com/checksum.html
    '''

    # Create bitmask to help calculate one's complement
    mask = 0xffff

    # Use the invert operator, alongside the bitmask, to calculate result
    return (~num & mask)


def internet_checksum(data, total=0x0):
    '''
    Internet Checksum of a bytes array.
    Further reading:
    1. https://tools.ietf.org/html/rfc1071
    2. http://www.netfor2.com/checksum.html
    '''

    # Create temp array to hold/manipulate data from data input
    temp = []
    # If number of bytes is odd, append extra zero byte
    # For every even-numbered element in the array, shift it to the right
    # by 8 bits, to allow for the final summing
    for x in range(0, len(data)):
        if (x % 2 == 0):
            temp.append(data[x] << 8)
        else:
            temp.append(data[x])

    # Sum all of the elements in the now edited array
    checksum = sum(temp)

    # take only 16 bits out of the 32 bit sum and add up the carries
    while (checksum >> 16) > 0:
        checksum = (checksum & 0xffff) + (checksum >> 16)

    # Return the hextet_complement of the sum of the checksum and total
    return hextet_complement(checksum + total)
