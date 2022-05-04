import pickle
import numpy as np
import matplotlib.pyplot as plt

with open("data/rps-size-10-servers-3", "rb") as t:
    x1 = pickle.load(t)
with open("data/success-size-10-servers-3", "rb") as s:
    y1 = pickle.load(s)
with open("data/delay-size-10-servers-3", "rb") as d:
    z1 = pickle.load(d)
with open("data/rps-size-10-servers-3-fault-kill-follower", "rb") as t:
    x2 = pickle.load(t)
with open("data/success-size-10-servers-3-fault-kill-follower", "rb") as s:
    y2 = pickle.load(s)
with open("data/delay-size-10-servers-3-fault-kill-follower", "rb") as d:
    z2 = pickle.load(d)
with open("data/rps-size-10-servers-3-fault-cpulimit-follower", "rb") as t:
    x3 = pickle.load(t)
with open("data/success-size-10-servers-3-fault-cpulimit-follower", "rb") as s:
    y3 = pickle.load(s)
with open("data/delay-size-10-servers-3-fault-cpulimit-follower", "rb") as d:
    z3 = pickle.load(d)
with open("data/rps-size-10-servers-3-fault-memlimit-follower-limit-1000kb", "rb") as t:
    x4 = pickle.load(t)
with open("data/success-size-10-servers-3-fault-memlimit-follower-limit-1000kb", "rb") as s:
    y4 = pickle.load(s)
with open("data/delay-size-10-servers-3-fault-memlimit-follower-limit-1000kb", "rb") as d:
    z4 = pickle.load(d)

throughput1 = []
latency1 = z1
for num1, num2 in zip(x1, y1):
    throughput1.append(num1 * num2)
throughput2 = []
latency2 = z2
for num1, num2 in zip(x2, y2):
    throughput2.append(num1 * num2)
throughput3 = []
latency3 = z3
for num1, num2 in zip(x3, y3):
    throughput3.append(num1 * num2)
throughput4 = []
latency4 = z4
for num1, num2 in zip(x4, y4):
    throughput4.append(num1 * num2)

x = ['Baseline \nPerformance', 'Node \nCrash', 'CPU \nContention', 'Memory \nContention']
throughput = [max(throughput1), max(throughput2), max(throughput3), max(throughput4)]

x_pos = [i for i, _ in enumerate(x)]
color = ["#32a897", "#a84032", "#3285a8", "#9a32a8"]
hatch = ["-", "*", "o", "+"]

for i in range(len(x)):
    plt.bar(x[i], throughput[i], color = color[i], hatch = hatch[i])
    plt.xlabel("Type of fault")
    plt.ylabel("Throughput (QPS)")
    plt.title("Failure injection in follower")

# plt.grid()
plt.xticks(x_pos, x)
plt.tight_layout()
plt.savefig("plots/overall-follower.svg")

plt.clf()

latency_values = [latency1, latency2, latency3[:27], latency4[:7]]

for i in range(len(x)):
    count, bins_count = np.histogram(latency_values[i], bins = 100)
    pdf = count / sum(count)
    cdf = np.cumsum(pdf)
    plt.plot(bins_count[1:], cdf, label = x[i])

plt.grid()
plt.legend()
plt.tight_layout()
plt.savefig("plots/overall-latency-follower.svg")

plt.clf()

throughput_values = [throughput1, throughput2, throughput3[:27], throughput4[:7]]

# multiple line plots
for i in range(len(x)):
    plt.plot(throughput_values[i], latency_values[i], marker = 'o', markerfacecolor = color[i], markeredgecolor = color[i], markersize = 8, color = '#000000', linewidth = 2, linestyle = "-", label = x[i])
    # plt.axvline(x = max(throughput_values[i]), color = 'r', linestyle = '--')
plt.legend(loc = 'best', fontsize = 10)

# plt.ylim(bottom = 0, top = 5000)
# plt.xlim(left = 0, right = 60)
plt.tick_params(axis='both', which='major', labelsize=14)
plt.tick_params(axis='both', which='minor', labelsize=14)

# ax = plt.gca()
# ax.axes.yaxis.set_visible(False)

plt.xlabel("Throughput (QPS serviced)", fontsize = 14)
plt.ylabel("Average request latency (ms)", fontsize = 14)

plt.grid()
plt.tight_layout()

# show graph
plt.savefig("plots/overall-throughput-latency-follower.svg")
