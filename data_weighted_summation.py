from numpy import *


# 参数为所有级别的所有统计数据的合集c_alllevel，需要获取数据的隐私级别level
def data_weighted_summation(c_alllevel, level_d,epsilon,h,n):
    w = get_w(level_d,epsilon,h,n)
    rs = [0] * h
    for i in range(level_d):
        for j in range(len(c_alllevel[i])):
            rs[j] += w[i] * c_alllevel[i][j]

    return rs

# 得到w参数
# 输入参数为，当前隐私级别level_d，隐私预算epsilon，定义域范围h，各隐私级别人数n
def get_w(level_d, epsilon, h, n):
    w = [0] * level_d
    tempall = 0

    for eachlevel in range(1, level_d + 1):
        p = exp(epsilon * eachlevel) / (exp(epsilon * eachlevel) + h - 1)
        q = (1 - p) / (h - 1)
        eachn = n[eachlevel - 1]
        w[eachlevel - 1] = (eachn * (p - q) * (p - q)) / (p * (1 - p) + (h - 1) * q * (1 - q))
        tempall += w[eachlevel - 1]


    for i in range(len(w)):
        w[i] /= tempall

    return w

