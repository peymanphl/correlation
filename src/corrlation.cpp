#include "sender.h"
#include "receiver.h"
#include <boost/program_options.hpp>

using namespace std;
namespace po = boost::program_options;

int main(int argc, char *argv[])
{
	int id = 1;
	string type = "source";
	int rate = 5;
	int max_tx = 1000;
	int port = 9991;
	string output = "verbose";
	
	po::options_description desc("Allowed options");
        desc.add_options()
            ("help", "produce help message")
            ("type", po::value<string>(&type), "node type: source, destination, relay")
            ("port", po::value<int>(&port), "protocol port")
            ("rate", po::value<int>(&rate), "sending rate [kilobytes/sec]")
            ("max_tx", po::value<int>(&max_tx), "maximum transmissions")
            ("id", po::value<int>(&id), "node ID")
            ("format", po::value<string>(&output), "output format: verbose, python");
	po::variables_map vm;
        po::store(po::parse_command_line(argc, argv , desc), vm);
        po::notify(vm);
       
	if (type == "source")
	{
		cout << "sender"<<endl;
		auto s = new sender(id, max_tx, rate, port);
		s->send_hello();
	}
       if (type == "destination")
	{
		auto r = new receiver (id, port, output); 
		r->receive_hello();
	}
}
