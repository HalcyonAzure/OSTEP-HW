import os
import sys
import re
import matplotlib.pyplot as plt


def execRelocation(page_number, trival):
    r = os.popen(
        './tlb %d %d' % (page_number, trival))
    text = r.read()
    pattern = r"(\d+)"
    tlb = re.findall(pattern, text)
    r.close()
    return tlb


page_number = sys.argv[1]
trival = sys.argv[2]

hit_time_access = []
miss_time_access = []
vpn_n = []

for vpn in range(1, int(page_number), 128):
    print(str(vpn) + "/" + str(page_number))
    tlb = execRelocation(vpn, int(trival))
    hit_time_access.append(int(tlb[0]))
    miss_time_access.append(int(tlb[1]))
    vpn_n.append(vpn)

plt.xlabel("Virtual Page Number")
plt.ylabel("Time Per Access")

plt.scatter(vpn_n, hit_time_access, label="Hit")
plt.scatter(vpn_n, miss_time_access, label="Miss")

plt.savefig("./paging.png")
