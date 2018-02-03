#!/bin/sh

#op="${1:-op}"
#mac="${2:-mac}"
#ip="${3:-ip}"
op="${1}"
mac="${2}"
ip="${3}"
hostname="${4}"

tstamp="`date '+%Y-%m-%d %H:%M:%S'`"

payload="${op} ${ip} ${tstamp} (host=${hostname}): mac=${mac}"

echo $payload >> /home/nbeasley/dhcp.log

echo $payload |  socat - udp-datagram:255.255.255.255:2000,broadcast

