import numpy as np  # 导入矩阵模块
import math  # 导入数学工具模块
import random  # 导入随机数模块


# Rastrigr 函数，目标函数，函数值越小说明越优化，0为最优点
def object_function1(x):
    f = 0  # 初始化变量f
    for i in range(0, len(x)):  # 从0到x数组长度的循环遍历
        f = f + (x[i] ** 2 - (10 * math.cos(2 * np.pi * x[i])) + 10)
        # 对x中每一个数做此函数处理并求和
    return f  # 返回f的值

# sphere函数
def object_function2(x):
    f = 0  # 初始化变量f
    for i in range(0, len(x)):  # 从0到x数组长度的循环遍历
        f = f + (x[i] ** 2)
        # 对x中每一个数做此函数处理并求和
    return f  # 返回f的值

# rosenbrock函数  -30,30
def object_function3(x):
    f = 0  # 初始化变量f
    for i in range(0, len(x)-1):  # 从0到x数组长度的循环遍历
        f = f + (100*(x[i+1]-x[i]**2)**2+(1-x[i])**2)
        # 对x中每一个数做此函数处理并求和
    return f  # 返回f的值

# beale  函数
def object_function4(x):
    f = 0  # 初始化变量f
    f=(1.5-x[0]+x[0]*x[1])**2+(2.25-x[0]+x[0]*x[1]**2)**2+(2.625-x[0]+x[0]*x[1]**3)**2
        # 对x中每一个数做此函数处理并求和
    return f  # 返回f的值

# styblinski_tang函数
def object_function5(x):
    f = 0  # 初始化变量f
    for i in range(0, len(x)):  # 从0到x数组长度的循环遍历
        f = f + ((x[i]**4-16*x[i]**2+5*x[i])/2)
        # 对x中每一个数做此函数处理并求和
    return f  # 返回f的值

# Ackley函数
def object_function6(x):
    f = 0  # 初始化变量f
    f=-20*math.exp(-0.2*math.sqrt(0.5*(x[0]**2+x[1]**2)))-math.exp(0.5*(math.cos(2*np.pi*x[0])+math.cos(2*np.pi*x[1])))+np.e+20
        # 对x中每一个数做此函数处理并求和
    return f  # 返回f的值

# schaffer 函数
def object_function7(x):
    f = 0  # 初始化变量f
    f=0.5+(math.cos(math.sin(abs(x[0]**2-x[1]**2)))**2-0.5)/(1+0.001*(x[0]**2+x[1]**2))**2
        # 对x中每一个数做此函数处理并求和
    return f  # 返回f的值

#himmelblau
def object_function8(x):
    f=0
    f=(x[0]**2+x[1]-11)**2+(x[0]+x[1]**2-7)**2
    return f


def initpara():
    NP = 100  # 种群数量
    F = 0.6  # 缩放因子
    CR = 0.7  # 交叉概率
    generation = 2000  # 遗传代数
    len_x = 2  # 染色体（个体）上基因个数
    value_up_range = 5.12  # 基因的取值上限
    value_down_range = -5.12  # 基因的取值下限
    return NP, F, CR, generation, len_x, value_up_range, value_down_range  # 返回一个参数列表


# 种群初始化
def initialtion(NP):
    np_list = []  # 种群，每一个成员为染色体
    for i in range(0, NP):  # 从0到种群数量大小的循环遍历
        x_list = []  # 个体，每一个成员为基因
        for j in range(0, len_x):  # 从0到基因长度的循环遍历
            x_list.append(value_down_range + random.random() * (value_up_range - value_down_range))
            # 为每一个基因取值，取值的公式的是下限+一个浮点数*（上限-下限）
        np_list.append(x_list)  # 将个体加入到种群中
    return np_list  # 返回种群矩阵


# 数组相减
def substract(a_list, b_list):
    a = len(a_list)  # 获取a数组长度
    new_list = []  # 创建新个体数组
    for i in range(0, a):  # 从0到a的遍历
        new_list.append(a_list[i] - b_list[i])  # b数组-a数组的值放入新矩阵
    return new_list  # 返回新个体数组


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


# 变异，参数为种群矩阵
def mutation(np_list):
    v_list = []  # 创建新种群矩阵
    for i in range(0, NP):  # 从0到个体数量大小的遍历
        r1 = random.randint(0, NP - 1)  # 取小于种群大小的随机正整数
        while r1 == i:  # 当r1==i的时候做下列操作
            r1 = random.randint(0, NP - 1)  # 重新取r1
        r2 = random.randint(0, NP - 1)  # 取 r2同r1
        while r2 == r1 | r2 == i:  # 当r2取得与r1或i一样的值时
            r2 = random.randint(0, NP - 1)  # 重新取r2
        r3 = random.randint(0, NP - 1)  # 取r3
        while r3 == r2 | r3 == r1 | r3 == i:  # 当r3取得与r1或r2或i一样的值时
            r3 = random.randint(0, NP - 1)  # 重新取r3
        # 取三个随机个体
        v_list.append(add(np_list[r1], multiply(F, substract(np_list[r2], np_list[r3]))))
        # 对三个个体数组做 r1+F*（r2-r3）操作加入到新种群
    return v_list  # 返回新种群矩阵


# 交叉，参数为原种群矩阵以及变异种群矩阵
def crossover(np_list, v_list):
    u_list = []  # 创建一个种群矩阵
    for i in range(0, NP): # 从0到种群大小的遍历
        vv_list = []  # 创建一个临时个体矩阵
        for j in range(0, len_x):  # 从0到染色体长度的遍历
            if (random.random() <= CR) | (j == random.randint(0, len_x - 1)):
            # 取一个随机浮点数如果小于交叉概率或者取一个小于基因长度的正整数等于当前遍历值
                vv_list.append(v_list[i][j])  # 将变异种群此位置的基因加入到临时个体数组
            else:
                vv_list.append(np_list[i][j]) # 否则将原种群的基因加入到临时个体数组
        u_list.append(vv_list)   # 将新个体加入到新种群中
    return u_list  # 返回新种群


# 选择，参数为变异交叉后的新种群以及原种群
def selection(u_list, np_list):
    for i in range(0, NP):  # 从0到种群个数的遍历
        if object_function8(u_list[i]) <= object_function8(np_list[i]):
        # 对两个种群的个体用目标函数进行评价，如果新种群个体比原种群个体的目标函数值更小或者相等
            np_list[i] = u_list[i]  # 则将新种群的个体赋给原种群数组
        else:
            np_list[i] = np_list[i] # 否则保持原种群
    return np_list # 返回np_list矩阵


# 主函数
NP, F, CR, generation, len_x, value_up_range, value_down_range = initpara()
# 参数初始化
np_list = initialtion(NP)   # 种群初始化
min_x = []  # 储存取得函数值的位置值，此处即为x的值
min_f = []  # 目标函数值数组
for i in range(0, generation):  # 做遗传代数的遍历
    v_list = mutation(np_list)  # 原种群做变异得到变异种群v
    u_list = crossover(np_list, v_list)  # 变异种群与原种群做交叉得到交叉种群u
    np_list = selection(u_list, np_list)  # 在交叉种群和原种群中做选择操作，得到结果数组即为np_list
    for i in range(0, NP):  # 做NP次数的遍历
        xx = []  # 创建一个数组
        xx.append(object_function8(np_list[i]))  # 向xx数组中加入原数组中每个个体的目标函数值
        min_f.append(min(xx))  # 向min_f数组中添加xx数组中的最小值
        min_x.append(np_list[xx.index(min(xx))])  # 向min_x中添加原数组中取得最小目标函数值的位置
# 输出
min_ff = min(min_f)  # 取得最小的函数值
min_xx = min_x[min_f.index(min_ff)]  # 取得最小值时x的位置
print('the minimum point is x ')  # x位置的输出
print(min_xx)  # 输出x的位置
print('the minimum value is y ')  # 最小值的输出
print(min_ff)  # 输出算法结果
