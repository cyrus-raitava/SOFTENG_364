# -*- coding: utf-8 -*-
import os
import sys
import socket
import struct
import time

import collections
from checksum import internet_checksum

assert 3 <= sys.version_info[0], 'Requires Python 3'

# For readability in time conversions
MILLISEC_PER_SEC = 1000.0

# Selects the right-most 16 bits
RIGHT_HEXTET = 0xffff

# Size in bits of buffer in which socket data is received
BUFFER_SIZE = 2 << 5

# A port number is required for socket.socket, even though port
# numbers are unused by ICMP. We use a legal (i.e. strictly positive)
# port number, just to be safe.
ICMP_PORT_PLACEHOLDER = 1
ICMP_HEADER_LENGTH = 28
ICMP_STRUCT_FIELDS = "BBHHH"  # for use with struct.pack/unpack


# Exception class to represent Checksum Errors
class ChecksumError(Exception):
    pass


# Note that TimeoutError already exists in the Standard Library
# class TimeoutError(PingError):
#    pass

# See IETF RFC 792: https://tools.ietf.org/html/rfc792
# NB: The order of the fields *is* significant
ICMPMessage = collections.namedtuple(
    'ICMPMessage',
    ['type', 'code', 'checksum', 'identifier', 'sequence_number'])
# For ICMP type field:
# See https://en.wikipedia.org/wiki/Internet_Control_Message_Protocol
#     http://www.iana.org/assignments/icmp-parameters/icmp-parameters.xhtml
ICMPTypeCode = collections.namedtuple('ICMPTypeCode', ['type', 'code'])
ECHO_REQUEST = ICMPTypeCode(8, 0)
ECHO_REPLY = ICMPTypeCode(0, 0)


def this_instant():
    return time.perf_counter()


def ping(client_socket, dest_host, client_id, seq_no=0):
    """
   Sends echo request, receives response, and returns RTT.
    """

    def icmp_header(host_checksum):
        message = ICMPMessage(
                    type=ECHO_REQUEST.type,
                    code=ECHO_REQUEST.code,
                    checksum=socket.htons(host_checksum),
                    identifier=client_id,
                    sequence_number=seq_no)
        return struct.pack(ICMP_STRUCT_FIELDS, *message)

    #  Create payload for ICMP packet, being the time of its creation
    icmp_payload = struct.pack('d', this_instant())  # double-precision float
    #  Structure packet with checksum value initialised as zero
    icmp_packet_without_checksum = icmp_header(0) + icmp_payload
    #  Calculate checksum value to be used
    checksum = internet_checksum(icmp_packet_without_checksum)
    #  Create final packet to send, with checksum in header, and payload
    icmp_packet = icmp_header(checksum) + icmp_payload

    #  Create variable of the IPv4 destination address, for future use
    dest_host = socket.gethostbyname(dest_host)

    #  Send previously created ICMP packet, to dest host, via client socket
    client_socket.sendto(icmp_packet, (dest_host, ICMP_PORT_PLACEHOLDER))

    #  Blocking code, that waits for reply from the receiver of ICMP packet
    datagram, address = client_socket.recvfrom(BUFFER_SIZE)

    #  Store this_instant() at which datagram was received
    time_recv = this_instant()

    #  Strip IP header off of received datagram (to isolate ICMP packet)
    icmp_packet = datagram[20:]

    #  Use checksum to validate contents of ICMP packet
    checksum = internet_checksum(icmp_packet)
    if (checksum != 0):
        raise ChecksumError

    #  Extract header information of response ICMP packet
    icmp_header_response = ICMPMessage(
        *struct.unpack(ICMP_STRUCT_FIELDS, icmp_packet[:8]))

    #  Extract body of response of ICMP response packet
    icmp_message_response = icmp_packet[8:]

    #  Unpack binary data to recover what time the packet was sent at
    time_sent = struct.unpack('d', icmp_message_response)[0]

    #  Calculate round-trip time by finding the diff between time sent/received
    RTT = (time_recv - time_sent)*MILLISEC_PER_SEC

    #  Return both the RTT, and the header of the response
    return (RTT, icmp_header_response)


def verbose_ping(host, timeout=2.0, count=4, log=print):
    """
    Send ping and print session details to command prompt.
    """
    try:
        host_ip = socket.gethostbyname(host)
    except OSError as error:
        log(error)
        log('Could not find host {}.'.format(host))
        log('Please check name and try again.')
        return

    # Log the host being contacted, and number of bytes being sent
    log("Contacting {} with {} bytes of data ".format(host, 36))

    # Create set to hold round trip times of all packets sent
    round_trip_times = []

    for seq_no in range(count):
        try:
            #
            with socket.socket(
                    family=socket.AF_INET,
                    type=socket.SOCK_RAW,  # <=="raw socket"
                    proto=socket.getprotobyname('icmp')) as client_socket:

                # Set time-out duration (in seconds) on socket
                client_socket.settimeout(timeout/MILLISEC_PER_SEC)

                client_id = os.getpid() & RIGHT_HEXTET

                # Send ping to dest host, via client_socket, with header info
                delay, response = ping(
                                client_socket,
                                host,
                                client_id=client_id,
                                seq_no=seq_no)

            # Print response info from destination host, and delay
            log("Reply from {:s} in {}ms: {}".format(host_ip, delay, response))

            # Add delay value to set of RTTs
            round_trip_times.append(delay)

        # Handle timeout error of socket, and print corresponding error message
        except socket.timeout as ste:
            log("Request timed out after {}ms".format(timeout))

        # Handle Checksum Error, and print message
        except ChecksumError as cse:
            log("Checksum Error: computed checksum error mismatch.")

        except OSError as error:
            log("OS error: {}. Please check name.".format(error.strerror))
            if isinstance(error, PermissionError):
                # Display the likely explanation for
                # TCP Socket Error Code "1 = Operation not permitted":
                log("NB: On some sytems, ICMP messages can"
                    " only be sent from processes running as root.")
            break

    print('closing socket. woop woop')
    client_socket.close()

    # Print ping header
    log("Ping statistics for {}:".format(host_ip))

    # Calculate relevant figures, to be printed
    packets_lost = count - len(round_trip_times)
    packets_recieved = len(round_trip_times)
    percentage_loss = round((packets_lost/count)*100, 2)

    # Format/print all information
    log("\tPackets: Sent = {}, Received = {}, Lost = {} ({}% loss)"
        .format(count, packets_recieved, packets_lost, percentage_loss))

    # Calculate/print RTT statistics
    if (packets_recieved > 0):
        minRTT = round(min(round_trip_times))
        maxRTT = round(max(round_trip_times))
        avgRTT = round(sum(round_trip_times)/len(round_trip_times))
        log("Approximate round trip times in milli-seconds:")
        log("\tMinimum = {}ms, Maximum = {}ms, Average = {}ms"
            .format(minRTT, maxRTT, avgRTT))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Test a host.')
    parser.add_argument('-w', '--timeout',
                        metavar='timeout',
                        type=int,
                        default=1000,
                        help='Timeout to wait for each reply (milliseconds).')
    parser.add_argument('-c', '--count',
                        metavar='num',
                        type=int,
                        default=4,
                        help='Number of echo requests to send')
    parser.add_argument('hosts',
                        metavar='host',
                        type=str,
                        nargs='+',
                        help='URL or IPv4 address of target host(s)')
    args = parser.parse_args()

    for host in args.hosts:
        verbose_ping(host, timeout=args.timeout, count=args.count)
