''' This module works with all needed network data. Get broadcast address of current subnet '''

import socket
import fcntl
import struct
import sys
import os
from string import maketrans

TEST_IP = '8.8.8.8'
TEST_PORT = 80
PATH_TO_IFACE_CARDS = '/sys/class/net/'
BITS = 8
BITS_IN_IP = 32
WHITE_SPACE = ' '
SLASH = '/'

class Get_broadcast:

    __IFACE_CARD = ''  # it will contain the name of current network interface card
    broadcast_ip = ''

    def __bitwise_or(self, first, second):
        ''' Function will make a bitwise or with bin numbers which contains in strings which given as an argument  '''
        return bin(int(first, 2) | int(second, 2))[2:]

    def __get_iface_card(self):
        ''' Function will get an interface card '''
        all_ifaces = os.listdir(PATH_TO_IFACE_CARDS)
        for iface in all_ifaces:
            if iface == 'enp3s0' or iface == 'eth0':
                self.__IFACE_CARD = iface

    def __get_net_mask(self, ifname):
        ''' Function will return a mask of current network in this format: 'X.X.X.X' '''       
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x891b, struct.pack('256s',ifname))[20:24])

    def __dec_to_bin(self, ip):
        ''' Function transform the string of numbers which is given as an argument to binary, and return it '''
        octets = map(int, ip.split(SLASH)[0].split('.')) # '1.2.3.4'=>[1, 2, 3, 4]
        binary = '{0:08b}{1:08b}{2:08b}{3:08b}'.format(*octets)
        range = int(ip.split(SLASH)[1]) if SLASH in ip else None
        return binary[:range] if range else binary    

    def get_net_ip(self):
        ''' Function return ip address of a current machine '''
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((TEST_IP, TEST_PORT)) # hardcode just to know an ip address
        ip_addr = s.getsockname()[0]
        s.close()
        return ip_addr
       
    def get_broadcast_ip(self):
        ''' Function return a broadcast ip '''
        self.__get_iface_card()
        dec_mask = self.__get_net_mask(self.__IFACE_CARD)
        dec_ip = self.get_net_ip()
        broadcast_dec_list = []    
        bin_ip_addr = self.__dec_to_bin(dec_ip)
        bin_net_mask = self.__dec_to_bin(dec_mask)
        bin_net_mask = bin_net_mask.translate(maketrans('10','01'))
        while len(bin_net_mask) != BITS_IN_IP:
            bin_net_mask = '0' + bin_net_mask
        bit_broadcast = self.__bitwise_or(bin_ip_addr, bin_net_mask)
        list_broadcast = list(map(''.join, zip(*[iter(bit_broadcast)]*BITS)))  # dividing the list into 4 equal parts
        for octet in list_broadcast:
            broadcast_dec_list.append(int(octet,2))  # convert it into dec
        for dec in broadcast_dec_list:
            self.broadcast_ip = self.broadcast_ip + str(dec) + '.'
        return self.broadcast_ip[:-1]

