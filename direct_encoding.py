# 这个文件是直接编码的扰动和统计函数


from numpy import *
from collections import Counter


# xu代表用户的真实数据，epsilon代表用户所选的隐私级别,s为原始数据定义域,h代表定义域的取值个数
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
            # 等概率投射到其他数值
            tempnum = random.randint(0, h)
            # 如果恰巧又投射到原数据，再次进行等概率投射操作
            while x == s[tempnum]:
                tempnum = random.randint(0, h)
            pu.append(s[tempnum])
    return pu


# 对扰动后的数据进行频率估计
def directestimation(gu, epsilon, s):
    # h为定义域中取值的个数
    h = len(s)
    # n为用户集合gu中的元素个数
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
        # 得到ni，若查不到对应数据，则返回0
        ni = scount.get(i, 0)
        ci = (ni - n * q) / (n * (p - q))
        c.append(ci)

    return c


# 对真实的数据进行频率估计
def rawestimation(rawdata, s):
    # 这里的xu应该是可以删去的，直接使用rawdata就行。但为了保险起见，还是新建一个list用于承放rawdata的数据
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
