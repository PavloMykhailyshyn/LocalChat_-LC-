#ifndef SENDERRAWSOCKET_H
#define SENDERRAWSOCKET_H

#include "common.h"

namespace rawsocket
{
class senderrawsocket
{
    static const std::string ip_;
    static const std::uint32_t port_;

    std::int32_t raw_socket_;

    char datagram_[DATAGRAM_SIZE];
    char source_ip_[SOURCE_IP_SIZE];
    char * data_;
    char * pseudogram_;

    //IP header
    iphdr * iph_;

    //TCP header
    tcphdr * tcph_;
    sockaddr_in sin_;
    pseudo_header psh_;

    void IPheader();
    void IPchecksum();
    void TCPheader();
    void TCPchecksum();

    //Generic checksum calculation function
    unsigned short csum(unsigned short * ptr, std::int32_t nbytes);

public:
    senderrawsocket(std::string, std::string);
    senderrawsocket(const senderrawsocket&)                 = delete;
    senderrawsocket operator = (const senderrawsocket&)     = delete;
    ~senderrawsocket()                                      = default;

    void SendTo();
};
}

#endif // SENDERRAWSOCKET_H
