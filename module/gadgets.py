import socket
import struct
import IPy
import re

def isIP(str):
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(str):
        return True
    else:
        return False

def string_to_file_name(str):
    for _ in [":","?",",","╲","/","*","'",'"',"<",">","|"]:
        tmp=str.replace(_,"_")
        str=tmp
    return tmp

def ipcidr_to_netmask(ip,net_bits):
    network=ip
    host_bits = 32 - int(net_bits)
    netmask = socket.inet_ntoa(struct.pack('!I', (1 << 32) - (1 << host_bits)))
    network=str(IPy.IP(network).make_net(netmask))
    return network, netmask,ip


def netmask_to_cidr(netmask):
    '''
    :param netmask: netmask ip addr (eg: 255.255.255.0)
    :return: equivalent cidr number to given netmask ip (eg: 24)
    '''
    return sum([bin(int(x)).count('1') for x in netmask.split('.')])

def cidr_to_netmask(cidr):
  cidr = int(cidr)
  mask = (0xffffffff >> (32 - cidr)) << (32 - cidr)
  return (str( (0xff000000 & mask) >> 24)   + '.' +
          str( (0x00ff0000 & mask) >> 16)   + '.' +
          str( (0x0000ff00 & mask) >> 8)    + '.' +
          str( (0x000000ff & mask)))

# print(ipcidr_to_netmask("192.168.23.10","24"))
# print(cidr_to_netmask("192.178.0.234/24"))
# print(netmask_to_cidr("255.255.255.0"))
# print(cidr_to_netmask(24))
# print(cidr_to_netmask1("192.168.1.1/24"))