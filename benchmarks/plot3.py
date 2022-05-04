import pickle
import numpy as np
import matplotlib.pyplot as plt

with open("data/rps-size-10-servers-3", "rb") as t:
    x1 = pickle.load(t)
with open("data/success-size-10-servers-3", "rb") as s:
    y1 = pickle.load(s)
with open("data/delay-size-10-servers-3", "rb") as d:
    z1 = pickle.load(d)
with open("data/rps-size-10-servers-3-fault-memlimit-follower-limit-1000kb", "rb") as t:
    x2 = pickle.load(t)
with open("data/success-size-10-servers-3-fault-memlimit-follower-limit-1000kb", "rb") as s:
    y2 = pickle.load(s)
with open("data/delay-size-10-servers-3-fault-memlimit-follower-limit-1000kb", "rb") as d:
    z2 = pickle.load(d)
with open("data/rps-size-10-servers-3-fault-memlimit-follower-limit-5000kb", "rb") as t:
    x3 = pickle.load(t)
with open("data/success-size-10-servers-3-fault-memlimit-follower-limit-5000kb", "rb") as s:
    y3 = pickle.load(s)
with open("data/delay-size-10-servers-3-fault-memlimit-follower-limit-5000kb", "rb") as d:
    z3 = pickle.load(d)
with open("data/rps-size-10-servers-3-fault-memlimit-follower-limit-10000kb", "rb") as t:
    x4 = pickle.load(t)
with open("data/success-size-10-servers-3-fault-memlimit-follower-limit-10000kb", "rb") as s:
    y4 = pickle.load(s)
with open("data/delay-size-10-servers-3-fault-memlimit-follower-limit-10000kb", "rb") as d:
    z4 = pickle.load(d)
with open("data/rps-size-10-servers-3-fault-memlimit-follower-limit-15000kb", "rb") as t:
    x5 = pickle.load(t)
with open("data/success-size-10-servers-3-fault-memlimit-follower-limit-15000kb", "rb") as s:
    y5 = pickle.load(s)
with open("data/delay-size-10-servers-3-fault-memlimit-follower-limit-15000kb", "rb") as d:
    z5 = pickle.load(d)

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
throughput5 = []
latency5 = z5
for num1, num2 in zip(x5, y5):
    throughput5.append(num1 * num2)

x = ['Baseline \nPerformance', 'Memory limit \nat 1mb', 'Memory limit \nat 5mb', 'Memory limit \nat 10mb', 'Memory limit \nat 15mb']
throughput = [max(throughput1), max(throughput2), max(throughput3), max(throughput4), max(throughput5)]

x_pos = [i for i, _ in enumerate(x)]
color = ["#32a897", "#a84032", "#3285a8", "#9a32a8", "#eba834"]
hatch = ["-", "*", "o", "+", "/"]

for i in range(len(x)):
    plt.bar(x[i], throughput[i], color = color[i], hatch = hatch[i])
    plt.xlabel("Memory limit")
    plt.ylabel("Throughput (QPS)")
    plt.title("Memory contention in follower")

# plt.grid()
plt.xticks(x_pos, x)
plt.tight_layout()
plt.savefig("plots/overall-throughput-different-levels-memory-follower.svg")

plt.clf()

latency_values = [latency1, latency2[:7], latency3, latency4, latency5]

for i in range(len(x)):
    count, bins_count = np.histogram(latency_values[i], bins = 100)
    pdf = count / sum(count)
    cdf = np.cumsum(pdf)
    plt.plot(bins_count[1:], cdf, label = x[i])

plt.grid()
plt.legend()
plt.tight_layout()
plt.savefig("plots/overall-latency-different-levels-memory-follower.svg")

plt.clf()

throughput_values = [throughput1, throughput2[:7], throughput3, throughput4, throughput5]

# multiple line plots
for i in range(len(x)):
    plt.plot(throughput_values[i], latency_values[i], marker = 'o', markerfacecolor = color[i], markeredgecolor = color[i], markersize = 8, color = '#000000', linewidth = 2, linestyle = "-", label = x[i], alpha = 1)
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
plt.savefig("plots/overall-throughput-latency-different-levels-memory-follower.svg")
