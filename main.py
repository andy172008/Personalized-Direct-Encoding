from numpy import *
import time
import copy as cp
from data_processing import *
from direct_encoding import *
from data_weighted_summation import *
from data_redisturbance import *


def main(maxlevel, epsilon, level_d):
    # 统计运行时间
    start1 = time.perf_counter()

    userdata, s = data_read()

    start2 = time.perf_counter()
    # print('数据处理完成，程序耗时：%f' % (start2 - start1))

    # 初始隐私预算为epsilon,之后隐私预算为2倍epsilon，一直到level倍的epsilon为止
    # epsilon
    # level为最大隐私级别，level越小，代表级别越高，隐私保护效果越好，隐私预算越小
    # 隐私级别为1～level，对应的隐私预算为 epsilon * 隐私级别
    # level = 10

    # gu中存放扰动后的数据，其中有level个list，对应每个级别
    gu = []
    for i in range(10):
        gu.append([])

    for x in userdata:
        # 随机选择一个隐私级别
        eachlevel = random.randint(1, maxlevel + 1)
        gu[eachlevel - 1].extend(directencoding_perturbing(x, epsilon * eachlevel, s))
    # print(gu.__len__())
    # print(gu[level_d - 1].__len__())

    # 此处进行再随机化处理,这里一定要用deepcopy
    ru = cp.deepcopy(gu)
    for i in range(level_d + 1, maxlevel + 1):
        ru[level_d - 1].extend(data_redisturbance(level_d * epsilon, ru[i - 1], i * epsilon, s))

    # print(ru[level_d - 1].__len__())
    # print(gu[level_d - 1].__len__())

    num_of_eachlevel = []
    num_of_eachlevel_re = []
    for i in gu:
        num_of_eachlevel.append(len(i))
    for i in ru:
        num_of_eachlevel_re.append(len(i))

    start3 = time.perf_counter()
    # print('编码完成，程序耗时：%f' % (start3 - start2))

    #  对每个级别开始解码
    # 未再扰动的数据
    c_estimated_all = []
    # 再扰动后的数据
    c_estimated_all_re = []
    for i in range(maxlevel):
        c_estimated = directestimation(gu[i], epsilon * (i + 1), s)
        c_estimated_all.append(c_estimated)
        c_estimated = directestimation(ru[i], epsilon * (i + 1), s)
        c_estimated_all_re.append(c_estimated)

    # 当前隐私级别暂定为5
    rs_dws = data_weighted_summation(c_estimated_all, level_d, epsilon, len(s), num_of_eachlevel)
    rs_dws_re = data_weighted_summation(c_estimated_all_re, level_d, epsilon, len(s), num_of_eachlevel_re)

    start4 = time.perf_counter()
    # print('对扰动数据完成频率估计，程序耗时：%f' % (start4 - start3))

    c_raw = rawestimation(userdata, s)

    start5 = time.perf_counter()
    # print('对原始数据完成频率统计，程序耗时：%f' % (start5 - start4))

    # 计算MSE
    dws = 0
    re = 0
    dws_re = 0
    notdws_notre = 0
    for i in range(len(s)):
        # ac += rs[i]
        # notac += c_estimated_all[5][i]
        dws += (c_raw[i] - rs_dws[i]) ** 2
        re += (c_raw[i] - c_estimated_all_re[level_d - 1][i]) ** 2
        dws_re += (c_raw[i] - rs_dws_re[i]) ** 2
        notdws_notre += (c_raw[i] - c_estimated_all[levle_d - 1][i]) ** 2
    print('level_d',level_d)
    print('dws:', dws)
    print('re', re)
    print('dws_re', dws_re)
    print('notdws_notre', notdws_notre)

    # print(c_estimated)
    # print(' @@@@@@@@@@@@@@@@@@@@@@@@@@@')
    # print(c_raw)

    print('程序总耗时：%f' % (time.perf_counter() - start1))


maxlevel = 10
epsilon = 2

# 在多个隐私预算上进行实验
# for epsilon in [0.1,0.5,1.0,1.5,2]:
print('当前epsilon为',epsilon,'**********************')
for levle_d in range(1,maxlevel+1):
    main(maxlevel, epsilon, levle_d)

# main(maxlevel, epsilon, levle_d)
