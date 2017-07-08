#include "senderrawsocket.h"


bool CorrectArguments(std::int32_t, char**, std::string&, std::string&);

std::int32_t main(std::int32_t argc, char** argv)
{
    std::string recipient, message;
    if (CorrectArguments(argc, argv, recipient, message))
    {
        rawsocket::senderrawsocket LCsender_local(recipient, message, true);
        rawsocket::senderrawsocket LCsender(recipient, message);
        LCsender_local.SendTo();
        LCsender.SendTo();
    }
    else
    {
        sleep(TIME_TO_WAIT);
        exit(EXIT);
    }
    return 0;
}

bool CorrectArguments(std::int32_t argc, char** argv, std::string& recipient, std::string& message)
{
    if (argc == NUMB_OF_MIN_ARGS)
    {
        if (strcmp(argv[HELP_ARG], HELP) == 0)
        {
            std::cout << "H E L P menu\n\n"
                         "\t -r <recipient> - recipient name (latin letters and numbers without spaces <max 25 symbols>) --> (main argument)\n"
                         "\t -m \"message\" - message (any ASCII characters <max 100 symbols>) --> (main argument)\n"
                         "\t -h - help" <<
            std::endl << std::endl;
            return false;
        }
    }
    if (argc < NUMB_OF_MAX_ARGS)
    {
        std::cerr << "Need more arguments\n\n";
        std::cout << "\t -r <recipient> - recipient name (latin letters and numbers without spaces <max 25 symbols>) --> (main argument)\n"
                     "\t -m \"message\" - message (any ASCII characters <max 100 symbols>) --> (main argument)\n"
                     "\t -h - help" <<
        std::endl << std::endl;
        return false;
    }
    else if (argc > NUMB_OF_MAX_ARGS)
    {
        std::cerr << "Too many arguments\n\n";
        std::cout << "Please find more information passing argument \"-h\"" << std::endl << std::endl;
        return false;
    }
    else if (argc == NUMB_OF_MAX_ARGS)
    {
        for (std::int32_t i(0); i < argc - 2; i += 2)
        {
            if (strcmp(argv[i + 1], RECIPIENT) == 0)
            {
                std::string recipient_name(argv[i + 2]);
                std::regex letters_and_numbers("([a-zA-Z0-9]{0,25})");
                if (!std::regex_match(recipient_name, letters_and_numbers))
                {
                    R_iNCORRECT();
                }
                recipient = recipient_name;
            }
            else if (strcmp(argv[i + 1], MESSAGE) == 0)
            {
                std::string msg(argv[i + 2]);
                std::regex ASCII("([\\d\\w\\s]{0,100})");
                if (!std::regex_match(msg, ASCII))
                {
                    M_iNCORRECT();
                }
                message = msg;
            }
        }
        if (recipient != "" && message != "")
        {
            return true;
        }
        else
        {
            INCORRECT();
        }
    }
    exit(EXIT);
}
