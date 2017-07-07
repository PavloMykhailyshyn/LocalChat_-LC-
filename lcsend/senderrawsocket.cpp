#include "senderrawsocket.h"
namespace rawsocket
{

const std::string senderrawsocket::ip_ = SOURCE_ADDR;
const std::uint32_t senderrawsocket::port_ = PORT;

senderrawsocket::senderrawsocket(std::string recipient, std::string message)
{
    std::string recipient_and_message = recipient + DELIMITER + message;

    raw_socket_ = socket (PF_INET, SOCK_RAW, IPPROTO_TCP);

    if(raw_socket_ == SOCK_CREATION_ERR)
    {
        //socket creation failed, may be because of non-root privileges
        perror("Failed to create socket");
        exit(1);
    }

    //zero out the packet buffer
    memset (datagram_, 0, DATAGRAM_SIZE);

    iph_ = (iphdr *) datagram_;

    //TCP header
    tcph_ = (tcphdr *) (datagram_ + sizeof (ip));

    //Data part
    data_ = datagram_ + sizeof(iphdr) + sizeof(tcphdr);
    strcpy(data_, recipient_and_message.c_str());

    //some address resolution
    strcpy(source_ip_, ip_.c_str());
    sin_.sin_family = AF_INET;
    sin_.sin_port = htons(port_);
    sin_.sin_addr.s_addr = inet_addr(DESTINATION_ADDR);

    IPheader();
    IPchecksum();

    TCPheader();
    TCPchecksum();
}

void senderrawsocket::IPheader()
{
    iph_->ihl = HEADER_LENGTH;
    iph_->version = VERSION;
    iph_->tos = 0;
    iph_->tot_len = sizeof(iphdr) + sizeof(tcphdr) + strlen(data_);
    iph_->id = htonl(PACKET_ID);                 //Id of this packet
    iph_->frag_off = 0;
    iph_->ttl = TIME_TO_LIVE;
    iph_->protocol = IPPROTO_TCP;
    iph_->check = 0;                             //Set to 0 before calculating checksum
    iph_->saddr = inet_addr( source_ip_ );       //Spoof the source ip address
    iph_->daddr = sin_.sin_addr.s_addr;
}

void senderrawsocket::IPchecksum()
{
    iph_->check = csum((unsigned short *) datagram_, iph_->tot_len);
}

void senderrawsocket::TCPheader()
{
    tcph_->source = htons(TCP_SOURCE);
    tcph_->dest = htons(port_);
    tcph_->seq = 0;
    tcph_->ack_seq = 0;
    tcph_->doff = TCP_HEADER_SIZE;
    tcph_->fin = 0;
    tcph_->syn = 1;
    tcph_->rst = 0;
    tcph_->psh = 0;
    tcph_->ack = 0;
    tcph_->urg = 0;
    tcph_->window = htons(MAX_WINDOW_SIZE);
    tcph_->check = 0;
    tcph_->urg_ptr = 0;
}

void senderrawsocket::TCPchecksum()
{
    psh_.source_address = inet_addr( source_ip_ );
    psh_.dest_address = sin_.sin_addr.s_addr;
    psh_.placeholder = 0;
    psh_.protocol = IPPROTO_TCP;
    psh_.tcp_length = htons(sizeof(tcphdr) + strlen(data_));

    std::int32_t psize = sizeof(struct pseudo_header) + sizeof(tcphdr) + strlen(data_);
    pseudogram_ = (char*)malloc(psize);

    memcpy(pseudogram_, (char*) &psh_, sizeof(pseudo_header));
    memcpy(pseudogram_ + sizeof(struct pseudo_header), tcph_, sizeof(tcphdr) + strlen(data_));

    tcph_->check = csum( (unsigned short*) pseudogram_, psize);
}

unsigned short senderrawsocket::csum(unsigned short * ptr, std::int32_t nbytes)
{
    register long sum;
    unsigned short oddbyte;
    register short answer;

    sum = 0;
    while(nbytes > 1)
    {
        sum += *ptr++;
        nbytes -= 2;
    }
    if(nbytes == 1)
    {
        oddbyte = 0;
        *((u_char*)&oddbyte) = *(u_char*)ptr;
        sum += oddbyte;
    }

    sum = (sum >> 16) + (sum & 0xffff);
    sum = sum + (sum >> 16);
    answer = (short)~sum;

    return(answer);
}

void senderrawsocket::SendTo()
{
    //IP_HDRINCL to tell the kernel that headers are included in the packet
    int one = 1;
    const int * val = &one;

    if (setsockopt (raw_socket_, IPPROTO_IP, IP_HDRINCL, val, sizeof(one)) < 0)
    {
        perror("Error setting IP_HDRINCL");
        exit(0);
    }

    //Send the packet
    if (sendto (raw_socket_, datagram_, iph_->tot_len ,  0, (sockaddr *) &sin_, sizeof(sin_)) < 0)
    {
        perror("sendto failed");
    }
    //Data send successfully
    else
    {
        std::cout << "Packet Send. Length : " << iph_->tot_len << std::endl;
    }
}

}
