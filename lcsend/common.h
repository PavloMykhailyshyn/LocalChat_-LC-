#ifndef COMMON_H
#define COMMON_H

#include <unistd.h>
#include <iostream>
#include <regex>
#include <string>
#include <cstring>

#include <arpa/inet.h>
#include <sys/socket.h>     //  For socket
#include <errno.h>          //  For errno - the error number
#include <netinet/tcp.h>    //  Provides declarations for tcp header
#include <netinet/ip.h>     //  Provides declarations for ip header

#define NUMB_OF_MAX_ARGS              5
#define TIME_TO_WAIT                  3
#define NUMB_OF_MIN_ARGS              2
#define HELP_ARG                      1
#define EXIT                          0

#define RECIPIENT                   "-r"
#define MESSAGE                     "-m"
#define HELP                        "-h"


#define INCORRECT()                 std::cerr << "Incorrect input arguments\n\n"; \
                                    std::cout << "Please find more information passing argument ""-h""" << std::endl << std::endl; \
                                    return false;

#define R_iNCORRECT()               std::cerr << "<recipient> - recipient name (latin letters and numbers without spaces)\n\n"; \
                                    std::cout << "Please find more information passing argument ""-h""" << std::endl << std::endl; \
                                    return false;

#define M_iNCORRECT()               std::cerr << "\"message\" - message (any ASCII characters)\n\n"; \
                                    std::cout << "Please find more information passing argument ""-h""" << std::endl << std::endl; \
                                    return false;

#define SOURCE_ADDR                 "127.0.0.1"
#define PORT                        1111
#define DESTINATION_ADDR            "1.2.3.4"
#define SOCK_CREATION_ERR           -1
#define DATAGRAM_SIZE               4096
#define SOURCE_IP_SIZE              32
#define DELIMITER                   '#'
#define PACKET_ID                   54321
#define HEADER_LENGTH               5
#define VERSION                     4
#define TIME_TO_LIVE                255
#define TCP_SOURCE                  1234
#define TCP_HEADER_SIZE             5
#define MAX_WINDOW_SIZE             5840

/*
    96 bit (12 bytes) pseudo header needed for tcp header checksum calculation
*/
struct pseudo_header
{
    std::uint32_t source_address;
    std::uint32_t dest_address;
    std::uint8_t placeholder;
    std::uint8_t protocol;
    std::uint16_t tcp_length;
};

#endif // COMMON_H
