#!/bin/bash
# Script to force connection to a hidden network.
# The NetworkManager can't handle hidden ESSIDs.
# Keep on trying forever, which is usefull when the router
# restarts at night.
#
# 2008: jpa: orig

key=f107262016b7803eb0d69409ae
essid=Crystal2464
# Keep the connection working overnight.
while true; do
  su - -c "service NetworkManager stop"
  su - -c "service avahi-daemon stop"
  # su - -c "service network stop"
  su - -c "pkill dhclient"
  su - -c "iwconfig eth0 essid $essid mode managed ap any enc restricted $key"
  su - -c "dhclient -1 eth0"
  while true; do
    ping -c 1 -w 1 192.168.1.1 >/dev/null || break
    sleep $(( 30 * 60 ))
  done
  sleep $(( 5 * 60 ))
done
