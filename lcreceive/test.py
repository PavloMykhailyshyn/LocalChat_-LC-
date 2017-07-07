import socket
import fcntl
import struct
import sys
from string import maketrans

class Get_broadcast():

    broadcast_ip = ''

    def __dec_to_bin(self, ip):
        octets = map(int, ip.split('/')[0].split('.')) # '1.2.3.4'=>[1, 2, 3, 4]
        binary = '{0:08b}{1:08b}{2:08b}{3:08b}'.format(*octets)
        range = int(ip.split('/')[1]) if '/' in ip else None
        return binary[:range] if range else binary    

    def get_net_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80)) # hardcode just to know an ip address
        ip_addr = s.getsockname()[0]
        s.close()
        return ip_addr
       
    def get_broadcast_ip(self):
        mask = get_net_mask()
        ip = self.get_net_ip()
        broadcast_dec_list = []    
        ip_addr = self.__dec_to_bin(ip)
        net_mask = self.__dec_to_bin(mask)
        net_mask = net_mask.translate(maketrans('10','01'))
        bit_broadcast = (bitstr(ip_addr) | bitstr(net_mask))
        list_broadcast = list(map(''.join, zip(*[iter(bit_broadcast)]*8)))# dividing 
        for octet in list_broadcast:
            broadcast_dec_list.append(int(octet,2))
        for dec in broadcast_dec_list:
            self.broadcast_ip = self.broadcast_ip + str(dec) + '.'
        return self.broadcast_ip[:-1]


def get_net_mask(ifname = 'enp3s0'):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x891b, struct.pack('256s',ifname))[20:24])

class bitstr(str):
        def __or__(self, other):
            return bin(int(self, 2) | int(other, 2))[2:]



a = Get_broadcast()
print(a.get_broadcast_ip())
