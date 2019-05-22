import random  # 导入random模块，使可调用random静态方法生成随机数
import math  # 有关数学计算的模块


# 初始化生成一个种群，其中population_size为种群中的个体数，chromosome_length为个体染色体大小（即二进制编码长度）
def species_origin(population_size, chromosome_length):
    population = [[]]
    # 二维列表，包含染色体和基因
    for i in range(population_size):  # 生成种群
        temporary = []
        # 染色体暂存器
        for j in range(chromosome_length):  # 染色体长度的遍历
            temporary.append(random.randint(0, 1))
            # 随机产生0，1序列，组成一个染色体
        population.append(temporary)
        # 将染色体添加到种群中
    return population[1:]
    # 将种群返回，种群是个二维数组，个体和染色体两维，去掉第一个空项


# 从二进制到十进制
# 参数为种群,染色体长度
def translation(population, chromosome_length):
    temporary = []
    # 存储十进制数
    for i in range(len(population)):
        # 个体数量大小的循环
        total = 0
        # 每个染色体二进制序列的十进制表示
        for j in range(chromosome_length):
            total += population[i][j] * (math.pow(2, j))
            # 从第一个基因开始，每位对2求幂，再求和
        temporary.append(total)
        # 一个染色体编码完成，由一个二进制数编码为一个十进制数
    return temporary


# 目标函数
def function(population, chromosome_length):
    function1 = []
    # 存储适应值
    temporary = translation(population, chromosome_length)
    # 暂存种群中的所有的染色体(十进制)
    for i in range(len(temporary)):
        x = temporary[i]
        function1.append(2 * math.sin(x) + math.cos(x))
        # 这里将2*sin(x)+cos(x)作为目标函数，也是适应度函数
    return function1  # 返回适应度值


# 取非负适应值
def fitness(function1):
    fitness1 = []
    # 适应度数组
    for i in range(len(function1)):
        # 循环次数为适应度值个数
        if (function1[i] > 0):
            # 如果适应度值大于0
            temporary = function1[i]
            #  则定为原值
        else:
            temporary = 0.0
        # 如果适应度小于0,则定为0
        fitness1.append(temporary)
        # 将适应度添加到列表中
    return fitness1  # 返非负数组


# 计算适应度和
def sum(fitness1):
    total = 0
    # 总和
    for i in range(len(fitness1)):
        total += fitness1[i]  # 累加
    return total  # 返回和


# 此函数作用为为适应度划分区间，第一个值为第一个区间，第二值为原数组中第一个值+第二个值，
# 这个值与第一个值之间的大小即为原数组中第二个值大小，以此类推，
def cumsum(fitness1):
    for i in range(len(fitness1) - 2, -1, -1):
        # 此处为倒计数，从倒数第二个开始
        total = 0
        # 区间段值
        j = 0
        # 计数器
        while (j <= i):
            # 计算区间和
            total += fitness1[j]
            j += 1
        fitness1[i] = total
        # 确定区间
    fitness1[len(fitness1) - 1] = 1  # 将最后一个值赋为1


# 选择
# fitness1为经筛选后的非负适应度值
def selection(population, fitness1):
    new_fitness = []
    # 单个公式暂存器
    total_fitness = sum(fitness1)
    # 将所有的适应度求和
    for i in range(len(fitness1)):
        new_fitness.append(fitness1[i] / total_fitness)
    # 将所有个体的适应度概率化,采用单个值除以总值的方法
    cumsum(new_fitness)
    # 将所有个体的适应度划分成区间，
    ms = []
    # 存活的个体
    pop_len = len(population)
    # 求出种群长度
    for i in range(pop_len):
        ms.append(random.random())
    # 产生种群大小个随机值，为随机浮点数
    ms.sort()
    # 存活的种群排序
    fitin = 0
    newin = 0
    # 作为两个数组的下标
    new_pop = population
    # 创建一个新的个体数组
    # 轮盘赌方式
    while newin < pop_len:
        # 当存活数组小于种群个体数
        if (ms[newin] < new_fitness[fitin]):
            # 此时的随机浮点数值小于此区间值，则代表这个新生成的个体落在此区间
            new_pop[newin] = population[fitin]
            # 个体落入此区间
            newin += 1  # 下一个个体
        else:
            fitin += 1
    # 如果随机数在某个区间便取该区间序号的个体，例如得到的适应度值为[1,2,3,4],则得到的适应度值区间为[0.1,0.3,0.6,1],
    # 若随机数取到了0.2，则取第二个区间的数即2代表的个体入新种群


# 数组相加
def add(a_list, b_list):
    a = len(a_list)  # 获取a数组长度
    new_list = []  # 创建新个体数组
    for i in range(0, a):  # 从0到a的遍历
        new_list.append(a_list[i] + b_list[i])  # b数组+a数组的值放入新矩阵
    return new_list  # 返回新个体数组


# 数组的数乘
def multiply(a, b_list):
    b = len(b_list)  # 获取b数组长度
    new_list = []  # 创建新个体数组
    for i in range(0, b):  # 从0到b的遍历
        new_list.append(a * b_list[i])  # b数组每个数乘以a
    return new_list  # 返回新个体数组


# 生成概率模型，参数为已选择种群,概率分布数组，染色体长度
def probability(population, p, ch_len):
    y = 0.5  # 学习因子 定为0.5
    x = []  # 当前迭代中个体概率分布
    pi = []  # 储存新生成的概率分布
    for i in range(ch_len):  # 染色体长度的遍历
        for j in range(len(population)):  # 种群个体数的遍历
            x[i] = x[i] + population[j] / ch_len
            # 计算最优个体此位置上1生成的概率
    pi.append(add(multiply((1 - y), p), multiply(y, x)))
    # 概率模型函数pi+1=（1-y）pi+y*(1/n)Σxi
    return pi

# 生成新种群，参数为概率分布数组，种群个体数,染色体长度
def build(p,pop_len,ch_len):
    pop=[]  # 新种群
    for i in range(pop_len):  # 按种群个数生成新种群
        for j in range(ch_len):  # 按染色体长度生成新个体
            if(random.random()<p[j]): #产生一个随机浮点数，如果这个浮点数小于
                pop[i][j]=1
            else:
                pop[i][j]=0
    return pop

#主程序
pop_size=10  # 种群个体数
ch_size=10  # 染色体长度
size = 100  # 迭代次数
p=[]  # 概率分布数组
for i in range(ch_size):
    p[i]=0.5  # 全部初始化为0.5
pop=species_origin(pop_size,ch_size)
#  初始化种群
for i in range(size):
# 进行迭代
    function1=function(pop,ch_size)
    # 算适应度值
    fitness1=fitness(function1)
    # 取非负
    selection(pop,fitness1)
    # 生成繁殖种群
    p=probability(pop,p,ch_size)
    # 进行概率分布生成
    pop=build(p,pop_size,ch_size)
    # 根据概率分布生成新种群
