#pragma once

#include "PracticalSocket.h"
#include <map>
#include <cstdint>
#include <string>
#include <vector>
#include <boost/shared_ptr.hpp>

// This class estimates the link quality between two nodes
using namespace std;


class sender 
{

public:
	sender(int identification,
							 int maximum_tx,
							 int tx_rate,
							 int destinationPort);
	~sender();




	UDPSocket tx_sock;
	
	int id;
	int max_tx;
	int rate;
	int destPort;
	
public:

	void send_hello();
	

};
