#pragma once

#include "PracticalSocket.h"
#include <map>
#include <cstdint>
#include <string>
#include <vector>
#include <boost/shared_ptr.hpp>

// This class estimates the link quality between two nodes
using namespace std;


class receiver
{

public:
	receiver(int identification, int destinationPorti, std::string output);
	~receiver();


	// for each link the information of the link is stored in the following struct
	struct LinkQualityEntry 
	{
		double last;
		double first;
		double received;
		double lost;
		int last_refresh;	   
		double lost_prob;	   
	};


        UDPSocket rx_sock;
	
	int id;
	int destPort;
	std::string output;
	
public:

	void receive_hello();
	void print_result();
	
	std::map<uint32_t , boost::shared_ptr<LinkQualityEntry>> link_quality_table;

};
