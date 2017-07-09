#!/usr/bin/python

import re
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
import scapy.all as scapy
import argparse
import datetime
from network import *

# regular expressions

RECIPIENT_NAME_REGEXP   = "^[a-zA-Z0-9]{0,25}$"
MESSAGE_REGEXP          = "^[\d\w\s]{0,100}$"

# Default values for packets

DEFAULT_TTL     = 20
DEFAULT_TIMEOUT = 2

# Labels for send and receive packets

SEND_MESSAGE_LABEL  = "send"
DELIMITER           = '#'

def send_message(name_receiver, msg):
    my_net = Get_broadcast()
    my_broadcast = my_net.get_broadcast_ip()

    packet = scapy.IP(dst = my_broadcast, ttl = DEFAULT_TTL) / \
             scapy.ICMP() / \
             (SEND_MESSAGE_LABEL + DELIMITER \
              + name_receiver + DELIMITER \
              + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") \
              + DELIMITER + msg)

    scapy.send(packet, verbose=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "To run program correctly please pass recipient name and message")
    parser.add_argument("-r", "--recipient", type = str, help = "recipient name (latin letters and numbers without spaces <max 25 symbols>)", required = True)
    parser.add_argument("-m", "--message", type = str, help = "message (any ASCII characters <max 100 symbols>)", required = True)

    args = parser.parse_args()

    if re.match(RECIPIENT_NAME_REGEXP, str(args.recipient)) and re.match(MESSAGE_REGEXP, str(args.message)):
        recipient = str(args.recipient)
        message = str(args.message)
        send_message(recipient, message)
    else:
        print "Please pass \"-h\" to find more info"
