#!/bin/bash

ssh pi@rasp00.lab.es.aau.dk "killall -q correlation"
ssh pi@rasp05.lab.es.aau.dk "sudo ./kill_tcpdump.sh"
ssh pi@rasp01.lab.es.aau.dk "killall -q correlation"
ssh pi@rasp02.lab.es.aau.dk "killall -q correlation"
ssh pi@rasp03.lab.es.aau.dk "killall -q correlation"
ssh pi@rasp04.lab.es.aau.dk "killall -q correlation"
ssh pi@rasp06.lab.es.aau.dk "killall -q correlation"
