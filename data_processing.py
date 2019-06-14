# 读取数据文件，返回list形式的数据,返回定义域
def data_read():
    with open('kosarak.dat', 'r') as f:

        userdata = []
        for line in f.readlines():
            # 移除头尾换行符
            line = line.strip()
            # 将一行中的数字划分开
            linelist = line.split(' ')
            # 检查是否有非数字元素
            for i in linelist:
                if not i.isnumeric():
                    print(line)
            for i in range(len(linelist)):
                linelist[i] = int(linelist[i])
            userdata.append(linelist)

        min = 10000
        max = 0
        s = set()
        num = 0
        for i in userdata:
            for j in i:
                num += 1
                if j > max:
                    max = j
                if j < min:
                    min = j
                s.add(j)
        print('数据中最小值为%d' % min)
        print('数据中最大值为%d' % max)
        print('数据种类共有%d个' % s.__len__())
        print('共有数据%d个' % num)
        print('共有用户%d个'%userdata.__len__())
    # 将list形式的数据返回，userdata中每个元素都是个list，包含一行的数字
    # return userdata, s
    return userdata, list(s)
