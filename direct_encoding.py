# 这个文件是直接编码的扰动和统计函数


from numpy import *
from collections import Counter


# xu代表用户的真实数据，epsilon代表用户所选的隐私级别,h代表定义域的取值个数
def directencoding_perturbing(xu, epsilon, s):
    # h为定义域中取值的个数
    h = len(s)
    # pu为扰动后的值
    pu = []
    p = exp(epsilon) / (exp(epsilon) + h - 1)
    for x in xu:
        # 以p的概率保持本身
        if random.uniform(0, 1) <= p:
            pu.append(x)
        else:
            # temps = s.copy()
            # temps.remove(x)
            # templ = list(temps)
            # pu.append(templ[random.randint(1, h - 1)])
            tempnum = random.randint(0, h)
            while x == s[tempnum]:
                tempnum = random.randint(0, h)
            pu.append(s[tempnum])
    return pu


# 对扰动后的数据进行频率估计
def directestimation(gu, epsilon, s):
    # h为定义域中取值的个数
    h = len(s)
    # n为用户集合g中的元素个数
    n = len(gu)

    p = exp(epsilon) / (exp(epsilon) + h - 1)
    q = (1 - p) / (h - 1)

    # 对定义域s中每个元素出现的次数进行统计
    # scount = [0] * len(s)
    # for i in gu:
    #     scount[s.index(i)] += 1
    scount = dict(Counter(gu))

    c = []

    for i in s:
        # ni = scount[i]
        ni = scount.get(i,0)
        ci = (ni - n * q) / (n * (p - q))
        c.append(ci)

    return c


# 对真实的数据进行频率估计
def rawestimation(rawdata, s):
    xu = []
    for i in rawdata:
        xu += i

    scount = dict(Counter(xu))

    c = []

    for i in s:
        ni = scount[i]
        ci = ni / len(xu)
        c.append(ci)
    return c
