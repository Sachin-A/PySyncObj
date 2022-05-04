import re
import os
import sys
import psutil
import signal
import subprocess

cluster = [2001, 2002, 2003, 2004]

port_core_map = {
    '2001': 0,
    '2002': 1,
    '2003': 2,
    '2004': 3
}

port_pid_map = {
    '2001': -1,
    '2002': -1,
    '2003': -1,
    '2004': -1
}

failure_type = str(sys.argv[1])
node_type = str(sys.argv[2])
percentage = int(sys.argv[3])

pid_1 = -1

for proc in psutil.process_iter(attrs=['pid', 'name']):
    if 'simple_bench.py' in str(proc.cmdline()):
        pid_1 = proc.info['pid']

assert pid_1 != -1

for proc in psutil.process_iter(attrs=['pid', 'name']):
    if 'simple_server.py' in str(proc.cmdline()):
        r1 = re.search(r"localhost:\d+", str(proc.cmdline())).group()
        node = str(r1[-4:])
        port_pid_map[node] = proc.info['pid']

print(port_pid_map)

cmd_2 = "syncobj_admin -conn localhost:2004 -status"
process_2 = subprocess.getoutput(cmd_2)
r2 = re.findall(r"leader: localhost:\d+", process_2)
leader_2 = str(r2[0][-4:])
print(leader_2)

should_exit = False

if failure_type == 'kill':
    if node_type == 'leader':
        if leader_2 != '2004':
            p_3 = psutil.Process(port_pid_map[leader_2])
            p_3.terminate()
            print("Leader with pid " + str(port_pid_map[leader_2]) + " running on core " + str(port_core_map[leader_2]) + " killed!")
        else:
            print("Can't kill server listening on port 2004!")
    
    elif node_type == 'follower':
        for i in range(len(cluster)):
            if (cluster[i] != int(leader_2) and cluster[i] != 2004):
                p_3 = psutil.Process(port_pid_map[str(cluster[i])])
                p_3.terminate()
                print("Follower with pid " + str(port_pid_map[str(cluster[i])]) + " running on core " + str(port_core_map[str(cluster[i])]) + " killed!")
                break
    else:
        print("Incorrect node type!")
        pass

elif failure_type == 'cpu_limit':
    if node_type == 'leader':
        if leader_2 != '2004':
            core_4 = port_core_map[leader_2]
        else:
            print("Can't constrain compute on server listening on port 2004!")
            should_exit = True
    elif node_type == 'follower':
        for i in range(len(cluster)):
            if (cluster[i] != int(leader_2) and cluster[i] != 2004):
                core_4 = port_core_map[str(cluster[i])]
                break
    else:
        print("Incorrect node type!")
        should_exit = True
        pass
    
    if (not should_exit):
        cmd_5 = "taskset -c " + str(core_4) + " stress-ng --cpu 0 -l " + str(percentage)
        print(cmd_5)
        process_5 = subprocess.Popen(cmd_5, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = True, start_new_session = True)

        while process_5.returncode == None:
            if not psutil.pid_exists(pid_1):
                os.killpg(os.getpgid(process_5.pid), signal.SIGTERM)
                break
        else:
            process_5.wait()

elif failure_type == 'mem_limit':
    if node_type == 'leader':
        if leader_2 != '2004':
            pid_6 = port_pid_map[leader_2]
        else:
            print("Can't constrain compute on server listening on port 2004!")
            should_exit = True
    elif node_type == 'follower':
        for i in range(len(cluster)):
            if (cluster[i] != int(leader_2) and cluster[i] != 2004):
                pid_6 = port_pid_map[str(cluster[i])]
                break
    else:
        print("Incorrect node type!")
        should_exit = True
        pass

    if (not should_exit):
        os.system("mkdir -p /sys/fs/cgroup/memory/sachina3/raft_cgroup")
        os.system("echo %d > /sys/fs/cgroup/memory/sachina3/raft_cgroup/cgroup.procs" % pid_6)
        # os.system("echo %d >> /sys/fs/cgroup/memory/sachina3/raft_cgroup/cgroup.procs" % psutil.Process(pid_6).ppid())
        # for child in psutil.Process(pid_6).children():
            # print(child.pid)
            # os.system("echo %d >> /sys/fs/cgroup/memory/sachina3/raft_cgroup/cgroup.procs" % child.pid)
        os.system("echo $((%d * 1024)) > /sys/fs/cgroup/memory/sachina3/raft_cgroup/memory.limit_in_bytes" % percentage)
else:
    print("Unrecognized failure type!")
    pass
