#!/usr/bin/env python

import sys
import threading
import scapy.all as scapy

# Default values for packets
DEFAULT_TTL = 20
DEFAULT_TIMEOUT = 2

def generate_packege_get(ip, name):
    return scapy.IP(dst=ip, ttl=DEFAULT_TTL) / scapy.ICMP() / ('getmessages' + name)

def send_request(ip, name):
    scapy.send(generate_packege_get(ip, name))

def get_messages():

    catched_packtes = scapy.sniff(filter='icmp', timeout=DEFAULT_TIMEOUT)

    for pckt in catched_packtes:
        try:
            packet_load = pckt.getlayer(scapy.Raw).load
            raw_str = str(packet_load.decode('utf-8'))

            if raw_str.find('message:') == 0:

                return raw_str[len('messages:'):].split('#')

        except UnicodeDecodeError:
            pass
        except AttributeError:
            pass

if __name__ == '__main__':
    send_request('172.20.8.137',sys.argv[1])
    lst = get_messages()
    print lst
