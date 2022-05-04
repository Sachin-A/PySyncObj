import sys
import subprocess

rps_start = int(sys.argv[1])
rps_stop = int(sys.argv[2])
rps_step = int(sys.argv[3])
size = sys.argv[4]
selfAddr = sys.argv[5]
restAddr = sys.argv[6:]

for i in range(rps_start, rps_stop, rps_step):
    print(i)
    cmd = ["taskset -c 3 python2 /home/sachina3/Projects/PySyncObj/benchmarks/simple_client.py"] + [str(i)] + [size] + [selfAddr] + restAddr
    cmd = " ".join(cmd)
    theproc = subprocess.run(cmd, shell = True)
