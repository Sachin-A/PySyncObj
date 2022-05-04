import matplotlib.pyplot as plt
import numpy as np
import pickle

with open("data/rps-size-10-servers-3-fault-memlimit-leader-limit-1000kb", "rb") as t:
    x1 = pickle.load(t)
with open("data/success-size-10-servers-3-fault-memlimit-leader-limit-1000kb", "rb") as s:
    y1 = pickle.load(s)
with open("data/delay-size-10-servers-3-fault-memlimit-leader-limit-1000kb", "rb") as d:
    z1 = pickle.load(d)

# with open("data/rps50", "rb") as t:
#     x2 = pickle.load(t)
# with open("data/success50", "rb") as s:
#     y2 = pickle.load(s)
# with open("data/delay50", "rb") as d:
#     z2 = pickle.load(d)

# with open("data/rps100", "rb") as t:
#     x3 = pickle.load(t)
# with open("data/success100", "rb") as s:
#     y3 = pickle.load(s)
# with open("data/delay100", "rb") as d:
#     z3 = pickle.load(d)

throughput1 = []
latency1 = z1
for num1, num2 in zip(x1, y1):
    throughput1.append(num1 * num2)

# throughput2 = []
# latency2 = z2
# for num1, num2 in zip(x2, y2):
#     throughput2.append(num1 * num2)

# throughput3 = []
# latency3 = z3
# for num1, num2 in zip(x3, y3):
#     throughput3.append(num1 * num2)

# multiple line plots
plt.plot(throughput1, latency1, marker = 'o', markerfacecolor = '#4287f5', markeredgecolor = '#061c40', markersize = 8, color = '#000000', linewidth = 2, linestyle = "-", label = "Workload on PySyncObj/RAFT")
# plt.plot(throughput2[:20], latency2[:20], marker = '*', markerfacecolor = '#a83242', markeredgecolor = '#570f18', markersize = 8, color = '#000000', linewidth = 2, linestyle = "-", label = "Workload Run 2")# plt.plot(throughput3[:20], latency3[:20], marker = 'X', markerfacecolor = '#791dab', markeredgecolor = '#3d0a59', markersize = 8, color = '#000000', linewidth = 2, linestyle = "-", label = "Workload Run 3")
plt.axvline(x = max(throughput1), color = 'r', linestyle = '--')
plt.legend(loc = 'best', fontsize = 14)

# plt.ylim(bottom = 0, top = 300)
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
plt.savefig("plots/baseline-fault-memlimit-leader-limit-1000kb.svg")

plt.clf()

# multiple line plots
plt.plot(x1, [(1 - j) * 100 for j in y1], marker = 'o', markerfacecolor = '#4287f5', markeredgecolor = '#061c40', markersize = 8, color = '#000000', linewidth = 2, linestyle = "-", label = "Workload on PySyncObj/RAFT")
# plt.plot(x2[:20], [(1 - j) * 100 for j in y2[:20]], marker = '*', markerfacecolor = '#a83242', markeredgecolor = '#570f18', markersize = 8, color = '#000000', linewidth = 2, linestyle = "-", label = "Workload Run 2")
# plt.plot(x3[:20], [(1 - j) * 100 for j in y3[:20]], marker = 'X', markerfacecolor = '#791dab', markeredgecolor = '#3d0a59', markersize = 8, color = '#000000', linewidth = 2, linestyle = "-", label = "Workload Run 3")
plt.legend(loc = 'best', fontsize = 14)

# plt.ylim(bottom = 0, top = 300)
# plt.xlim(left = 0, right = 60)
plt.tick_params(axis='both', which='major', labelsize=14)
plt.tick_params(axis='both', which='minor', labelsize=14)

# ax = plt.gca()
# ax.axes.yaxis.set_visible(False)

plt.xlabel("QPS issued", fontsize = 14)
plt.ylabel("QPS error %", fontsize = 14)

plt.grid()
plt.tight_layout()

# show graph
plt.savefig("plots/baseline2-fault-memlimit-leader-limit-1000kb.svg")


