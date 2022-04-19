import os
import re
import matplotlib.pyplot as plt


def execRelocation(seed, limit, num):
    r = os.popen('python3 relocation.py -s %d -l %d -c' % (seed, limit))
    pass_num = r.read().count("VALID")
    r.close()
    return pass_num / num


if __name__ == '__main__':
    limitTop = 1024
    limit_list = []
    case_list = []
    for i in range(0, limitTop, 50):
        # 从 10 - limitTop开始依次测试对应通过的概率
        sum = 0
        for j in range(0, 20):
            sum += execRelocation(j, i, 10)
        case_list.append(sum / 10)  # 将在 i 对应的概率存入 case_list
        limit_list.append(i)

    plt.xlabel("limit")
    plt.ylabel("pass rate")

    plt.plot(limit_list, case_list)

    plt.savefig("limit.png")
