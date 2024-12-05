import subprocess
import re
import sys
server_ip = '10.0.0.1'

ACCESSED_METHODS = [
    "client"
]

args = sys.argv[1:]

if len(args) < 1:
    print("You must set a method!")
    exit(1)
elif len(args) < 2:
    print("You must set a server ip!")
    exit(1)

def client(server_ip: str):
    try:
        result = subprocess.run(
            ['iperf', '-c', server_ip],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout, result.stderr
    except Exception as e:
        return None, str(e)

def parse_iperf_output(output):
    bitrate = None
    match = re.search(r'(\d+\.\d+)\sGbits/sec', output)
    if match:
        bitrate = float(match.group(1))
    return bitrate

if __name__ == "__main__":
    func = args[0]
    ip = args[1]

    if func not in ACCESSED_METHODS:
        print("This method is not exist or you don't have an access to this method!")
        exit(1)

    result, error = eval(func)(server_ip)
    if error:
        print(f"Connection error: {error}")
    else:
        print("Test result iperf:")
        print(result)

        bitrate = parse_iperf_output(result)
        if bitrate is None:
            print("Not found")
        else:
            print(f"Speed: {bitrate} Gbit/sec")
