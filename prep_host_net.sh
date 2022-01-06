#!/bin/bash

ip link add name br0 type bridge
ip link set dev br0 up
ip tuntap add mode tap tap0
ip link set tap0 up
ip link set tap0 master br0

ip addr add 10.0.0.1/24 brd + dev br0
ip addr add 10.0.1.1/24 brd + dev br0
ip addr add 192.168.0.1/24 brd + dev br0

ip route add 10.0.0.0/24 via 10.0.0.1 dev br0
ip route add 10.0.1.0/24 via 10.0.1.1 dev br0
ip route add 192.168.0.0/24 via 192.168.0.1 dev br0