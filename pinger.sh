#!/bin/bash
if [ $# -ne 1 ];then
    echo "Usage - ./pinger.sh [/24 network address]"
    echo "Example - ./pinger.sh 192.168.1.0"
    echo "Example will perform an ICMP ping sweep of the 192.168.0.0/24 network"
    exit
fi
prefix=$(echo $1|cut -d '.' -f 1-3)
for addr in $(seq 1 254);do
    ping -c 1 $prefix.$addr | grep "bytes from" | cut -d " " -f 4 | cut -d ":" -f 1 &
done