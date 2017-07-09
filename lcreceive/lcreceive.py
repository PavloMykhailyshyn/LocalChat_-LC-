#!/usr/bin/python

import threading
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
import scapy.all as scapy
import argparse
from network import *

# Default values for packets
DEFAULT_TTL = 20
DEFAULT_TIMEOUT = 2


# Separators
SEPARATOR_IN_PACKET = '#'
SEPARATOR_LIST_MESSAGES = '-'*20

# Labels for send and receive packets
GET_MESSAGES_LABEL = 'getmessages'
MESSAGES_LABEL = 'messages'+ SEPARATOR_IN_PACKET


CODING = 'utf-8'

def generate_package_get(ip, name):
    return scapy.IP(dst=ip, ttl=DEFAULT_TTL) / scapy.ICMP() / (GET_MESSAGES_LABEL + SEPARATOR_IN_PACKET + name)

def send_request(ip, name):
    scapy.send(generate_package_get(ip, name), verbose=False)

def get_messages():

    catched_packets = scapy.sniff(filter='icmp', timeout=DEFAULT_TIMEOUT)
    for pckt in catched_packets:
        try:
            packet_load = pckt.getlayer(scapy.Raw).load
            raw_str = str(packet_load.decode(CODING))
            if raw_str.find(MESSAGES_LABEL) == 0:
                show_messages(raw_str[len(MESSAGES_LABEL):].split(SEPARATOR_IN_PACKET))
                return

        except UnicodeDecodeError:
            pass
        except AttributeError:
            pass
	
    print("Don't found messages for this receiver")

def show_messages(msgs):
    for msg in set(msgs):
        print(SEPARATOR_LIST_MESSAGES)
        print(msg)
        print(SEPARATOR_LIST_MESSAGES)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "receive messages from user whose name is given as an argument")
    parser.add_argument('-r', '--receive', type=str, help="argument to receive")
    args = parser.parse_args()
    name = args.receive

    if (' ' in name):
        print("Name of receiver contain whitespaces, please type your request in this way:\n")
        print("lcreceive -r name_of_receiver")
    elif name:
        my_net = Get_broadcast()
        my_broadcast = my_net.get_broadcast_ip()

        send_request(my_broadcast, name)

        thread = threading.Thread(target=get_messages)
        thread.start()
        thread.join()

