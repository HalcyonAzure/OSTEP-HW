import os
import re
import matplotlib.pyplot as plt
import numpy as np


# 执行彩票概率检查，返回概率结果
def countLottery(length, seed):
    r = os.popen(
        "./lottery.py -l " + length + ":100," + length + ":100 -c" + " -s " + seed)
    text = r.read()
    r.close()
    lottery_time = re.findall(r"^--> .* (\d*)", text, re.M)
    return int(lottery_time[0])/int(lottery_time[1])


def average(length):
    sum = 0
    # 调整重复
    time = 20
    for i in range(1, time):
        sum += countLottery(length, str(i))
    return sum / (time - 1)


length = []
chance = []

# 设定工作长度和间隔
length_start = 1
length_end = 100
step = 5
for i in np.arange(length_start, length_end, step):
    length.append(i)
    chance.append(average(str(int(i))))

plt.ylabel("Fairness")
plt.xlabel("Job Length")

plt.plot(length, chance, 'b-')

plt.savefig("./lottery.png")
