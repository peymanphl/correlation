#include "receiver.h"
#include "PracticalSocket.h"
#include <stdio.h>
#include <fstream>

using namespace std;

receiver::receiver(int identification, int destinationPort, std::string out)
{
	id = identification;
	destPort = destinationPort;
	rx_sock.setLocalPort(destPort);
	output = out;
}


void receiver::receive_hello()
{
	const int MAXRCVSTRING = 1500;
	short unsigned int sourcePort = 0;
	string sourceAddress;
	char recvString[MAXRCVSTRING + 1]; // Buffer for echo string + \0
  	int doublicate;
	ofstream log;

	log.open("log.txt");

	if (log == NULL)
		perror ("Error opening file");

	
	while (true)
	{
		try
		{
			int bytesRcvd = rx_sock.recvFrom(recvString, MAXRCVSTRING,
											  sourceAddress, sourcePort);
			int id = *(int *)(&recvString[bytesRcvd - 4]);
			int seq = *(int *)(&recvString[bytesRcvd - 8]);
			int finished = *(int *)(&recvString[bytesRcvd - 12]);
			


			if (link_quality_table.find(id) == link_quality_table.end() )
			{
				boost::shared_ptr<LinkQualityEntry> new_entry(new LinkQualityEntry);
				std::cout << "new Entry " <<std::endl;
				new_entry->last = seq;
				new_entry->first = seq;
				new_entry->received = 1;
				new_entry->last_refresh = 0;

				//boost::shared_ptr<LinkQualityEntry> new_entry1(&new_entry);
				link_quality_table[id] = new_entry;

			}
			else
			{
				boost::shared_ptr<LinkQualityEntry> entry = link_quality_table[id];
				if (seq <= entry->last)
				{
					doublicate++;
					continue;
				}


				entry->received++;
				entry->last = seq;
				entry->lost_prob = (entry->last - entry->first - entry->received + 1)/(entry->last - entry->first + 1) ;
				entry->last_refresh = 0;
		       
	

			}
	
			if (output == "verbose")
		         {
				cout << "seq:" << seq << endl;
				cout << "source ID:" << id << endl;
				log  << "seq:" << seq << "\n";
				log  << "source ID:" << id << "\n"; 
			
			 }

			if (finished == 1)
				break;


		}
		catch (SocketException &e)
       		 {
          		  cerr << e.what() << endl;
          		  exit(1);
      		  }

 	}

	print_result();

}

void receiver::print_result()
{
	std::map<uint32_t , boost::shared_ptr<LinkQualityEntry>>::iterator itr = link_quality_table.begin();;
	std::cout << "result:"<< link_quality_table.size() << endl;

	while (itr != link_quality_table.end())
	{
		std::cout << "ID:"<< itr->first<< endl;
		std::cout << "loss:"<< itr->second->lost_prob<< endl;
		std::cout << "last:"<< itr->second->last<< endl;
		std::cout << "first:"<< itr->second->first<< endl;
		std::cout << "received:"<< itr->second->received<< endl;
		itr++;
	}

}
