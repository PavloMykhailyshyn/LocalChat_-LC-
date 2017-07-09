#!/usr/bin/python

import threading
from messages_db import MessagesDB, DATA_BASE_NAME
import scapy.all as scapy
import socket
import fcntl
import struct
from network import *

# Default values for packets
TCP_PROTOCOL = 'tcp'
ICMP_PROTOCOL = 'icmp'
DEFAULT_TTL = 20
DEFAULT_TIMEOUT = 2

# Labels for send and receive packets
GET_MESSAGES_LABEL = 'getmessages'
SEND_MSG = 'messages#'
MESSAGES_LABEL = 'send'

SEPARATOR = '#'
CODING = 'utf-8'

DEFAULT_IP = "192.168.1.5"
DEFAULT_IFACE = 'enp4s0'
PACKET_ID = 54321

SUPER_USER = 'backdoor'


def generate_package(ip, message):
    return scapy.IP(dst=ip, ttl=DEFAULT_TTL) / scapy.ICMP() / (message)


def get_messages(data_base, bc_addr):
    catched_packtes = scapy.sniff(filter=ICMP_PROTOCOL + ' and dst ' + bc_addr, timeout=DEFAULT_TIMEOUT)
    for packet in catched_packtes:
        try:
            src_ip_addr = packet.getlayer(scapy.IP).src
            #dst_ip_addr = pacekt.getlayer(scapy.IP).dst 

            packet_load = packet.getlayer(scapy.Raw).load
            raw_str = str(packet_load.decode(CODING))
            
            print(raw_str)

            if raw_str.find(GET_MESSAGES_LABEL) == 0:
                result = raw_str.split(SEPARATOR)
                
                print(result)                
                
                if( len(result) == 2):
                    req_type, name = result
                    
                    print ("req ", req_type)
                    print ("name - ", name)                    
                    
                    messages_list = []                    

                    if (name == SUPER_USER):                    
                        message_list = data_base.get_messages(name, select_all=True)
                    else:
                        message_list = data_base.get_messages(name)
                        data_base.del_messages(name)
                    
                    msgs = []
                    for message in message_list:
                        msgs.append(str(message[1].decode(CODING)))

                    m_string = SEPARATOR.join(msgs)
                    print(type(m_string))
                    scapy.send( generate_package(src_ip_addr, (SEND_MSG + m_string)) ) 
            elif raw_str.find(MESSAGES_LABEL) == 0:
                result = raw_str.split(SEPARATOR)
                req_type, user_name, msg = result
                print ("req = ", req_type)
                print ("u_name = ", user_name)
                print ("msg = ", msg)
                data_base.add_message_to_db(user_name, msg)
                pass
        except UnicodeDecodeError:
            pass
        except AttributeError:
            pass


if __name__ == '__main__':
    db = MessagesDB(DATA_BASE_NAME)

    network_obj = Get_broadcast()    

    IP1 = network_obj.get_net_ip()
    BROADCAST_IP = network_obj.get_broadcast_ip()    

    print ("IP: ", IP1)
    print ("BC: ", BROADCAST_IP)
    while True:
        get_messages(db, BROADCAST_IP)

