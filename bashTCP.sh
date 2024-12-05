#!/bin/bash
print_usage() {
echo "Usage: $0 ip_addr device"
}
if [ $# -ne 2 ]; then
echo "Error: Too few arguments" >&2
print_usage
exit 1
fi
iperf -c $1 -i 1 -t 30 | tee tcp_$2.txt