#include "PracticalSocket.h"
#include "sender.h"
#include <boost/chrono.hpp>
#include <boost/thread.hpp>

using namespace std;

sender::sender(int identification,
							 int maximum_tx,
							 int tx_rate,
							 int destinationPort)
{
	id = identification;
	max_tx = maximum_tx;
	rate = tx_rate;
	destPort = destinationPort;
}


void sender::send_hello()
{
    int x = 0;
    string destAddress = "10.0.0.255";
    string finishAddress = "172.26.13.255";
    int i = 0;
    int finished = 0;
    int interval = 1/(rate);
    boost::chrono::milliseconds dur(interval);
    boost::chrono::seconds last_sleep(5);
 
    while (i < max_tx)
	{

        i++;
        std::vector<uint8_t> payload(0);
	
	if(i == max_tx)
		finished = 1;

        payload.insert(payload.end(), (char *)&finished, ((char *)&finished) + 4);
        payload.insert(payload.end(), (char *)&x, ((char *)&x) + 4);
        payload.insert(payload.end(), (char *)&id, ((char *)&id) + 4);

        x++;
        try
        {
	    if (finished == 0)
           	 sender::tx_sock.sendTo((char *)&payload[0], payload.size(), destAddress , destPort);
	    else 
	    {
           	
		boost::this_thread::sleep_for(last_sleep);
		sender::tx_sock.sendTo((char *)&payload[0], payload.size(), finishAddress , destPort);
	
 	    }
	    boost::this_thread::sleep_for(dur);
        }
        catch (SocketException &e)
        {
            cerr << e.what() << endl;
            exit(0);
        }
    }
}



