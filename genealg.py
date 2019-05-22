# 目标求解2*sin(x)+cos(x)最大值
import random  # 导入random模块，使可调用random静态方法生成随机数
import math  # 有关数学计算的模块
import matplotlib.pyplot as plt
# 初始化生成一个种群，其中population_size为种群中的个体数，chromosome_length为个体染色体大小（即二进制编码长度）
def species_origin(population_size,chromosome_length):
    population=[[]]
    # 二维列表，包含染色体和基因
    for i in range(population_size):  # 生成种群
        temporary=[]
        # 染色体暂存器
        for j in range(chromosome_length):
            temporary.append(random.randint(0,1))
            # 随机产生0，1序列，组成一个染色体
        population.append(temporary)
            # 将染色体添加到种群中
    return population[1:]
            # 将种群返回，种群是个二维数组，个体和染色体两维，去掉第一个空项

# 从二进制到十进制
# 参数为种群,染色体长度
def translation(population,chromosome_length):
    temporary=[]
    # 存储十进制数
    for i in range(len(population)):
        total=0
        # 每个染色体二进制序列的十进制表示
        for j in range(chromosome_length):
            total+=population[i][j]*(math.pow(2,j))
            # 从第一个基因开始，每位对2求幂，再求和
        temporary.append(total)
        # 一个染色体编码完成，由一个二进制数编码为一个十进制数
    return temporary
   # 返回种群中所有个体编码完成后的十进制数

"""此处为适应度计算，适应度直接采用原函数2*sin(x)+cos(x)的值"""




#此函数作用为为适应度划分区间，第一个值为第一个区间，第二值为原数组中第一个值+第二个值，
# 这个值与第一个值之间的大小即为原数组中第二个值大小，以此类推，
def cumsum(fitness1):
    for i in range(len(fitness1)-2,-1,-1):
        # 此处为倒计数，从倒数第二个开始
        total=0
        j=0
        while(j<=i):
            total+=fitness1[j]
            j+=1
        fitness1[i]=total
    fitness1[len(fitness1)-1]=1
#选择
#fitness1为经筛选后的非负适应度值
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
    #作为两个数组的下标
    new_pop = population
    #创建一个新的个体数组
    # 轮盘赌方式
    while newin < pop_len:
        if (ms[newin] < new_fitness[fitin]):
            new_pop[newin] = population[fitin]
            newin += 1
        else:
            fitin += 1
    #如果随机数在某个区间便取该区间序号的个体，例如得到的适应度值为[1,2,3,4],则得到的适应度值区间为[0.1,0.3,0.6,1],
    # 若随机数取到了0.2，则取第二个区间的数即2代表的个体入新种群
    population = new_pop


def crossover(population):
    pop_len = len(population)
    for i in range(pop_len - 1):
        cpoint = random.randint(0, len(population[0]))
        # 在种群个数内随机生成单点交叉点
        temporary1 = []
        temporary2 = []

        temporary1.extend(pop[i][0:cpoint])
        temporary1.extend(pop[i + 1][cpoint:len(population[i])])
        # 将tmporary1作为暂存器，暂时存放第i个染色体中的前0到cpoint个基因，
        # 然后再把第i+1个染色体中的后cpoint到第i个染色体中的基因个数，补充到temporary2后面

        temporary2.extend(pop[i + 1][0:cpoint])
        temporary2.extend(pop[i][cpoint:len(pop[i])])
        # 将tmporary2作为暂存器，暂时存放第i+1个染色体中的前0到cpoint个基因，
        # 然后再把第i个染色体中的后cpoint到第i个染色体中的基因个数，补充到temporary2后面
        population[i] = temporary1
        population[i + 1] = temporary2
        # 第i个染色体和第i+1个染色体基因重组/交叉完成