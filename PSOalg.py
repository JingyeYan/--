import numpy as np  # 导入矩阵模块
import random  # 导入随机数模块


class PSO():
    # PSO类构造函数，参数为粒子群中的粒子数量，搜索维度，迭代次数
    def __init__(self, pN, dim, max_iter):
        self.w = 0.8  # 惯性常数
        self.c1 = 2  # 个体认知常数
        self.c2 = 2  # 社会经验常数
        self.r1 = random.random()  # 随机浮点数1
        self.r2 = random.random()  # 随机浮点数2
        self.pN = pN  # 粒子数量
        self.dim = dim  # 搜索维度
        self.max_iter = max_iter  # 迭代次数
        self.X = np.zeros((self.pN, self.dim))  # 所有粒子的位置,大小为pN*dim
        self.V = np.zeros((self.pN, self.dim))  # 所有粒子的速度
        self.pbest = np.zeros((self.pN, self.dim))  # 个体经历的最佳位置
        self.gbest = np.zeros((1, self.dim))  # 全局最佳位置
        self.p_fit = np.zeros(self.pN)  # 每个个体的历史最佳适应值
        self.fit = 1e10  # 全局最佳适应值

    # 目标函数x^2，当x取0时取得最小值0
    def function(self, x):
        sum = 0  # 每个维度搜索最优值的和
        length = len(x)  # 搜索维度，即x数组的长度
        x = x ** 2  # 目标函数 x^2
        for i in range(length):  # 从0到维度数的遍历
            sum += x[i]  # 对结果求和
        return sum  # 返回最后的和

    # 粒子群初始化
    def init_Population(self):
        for i in range(self.pN):  # 从0到粒子群粒子数量的遍历
            for j in range(self.dim): # 从0到每个粒子的搜索维度的遍历
                self.X[i][j] = random.uniform(0, 1)
                # 随机产生一个0到1之间的实数，作为粒子位置
                self.V[i][j] = random.uniform(0, 1)
                # 随机产生一个0到1之间的实数，作为粒子速度
            self.pbest[i] = self.X[i]  # 将此位置设为个体经历最佳位置
            tmp = self.function(self.X[i])  # 计算此粒子的适应值
            self.p_fit[i] = tmp  # 存入个体历史最佳适应值数组
            if (tmp < self.fit):  # 当tmp小于全局最佳适应值（即优于）
                self.fit = tmp  # 将tmp作为全局最佳适应值
                self.gbest = self.X[i] # 当前位置为历史最佳位置

    # 迭代函数
    def iterator(self):
        fitness = []  # 创建适应值数组
        for t in range(self.max_iter):  # 迭次次数的循环
            for i in range(self.pN):  # 粒子群数量的循环，更新gbest\pbest
                temp = self.function(self.X[i])  # 当前粒子适应值
                if (temp < self.p_fit[i]):
                    # 如果当前粒子适应值小于粒子历史最佳适应值
                    self.p_fit[i] = temp   # 更新数组
                    self.pbest[i] = self.X[i]  # 更新个体经历最佳位置
                    if (self.p_fit[i] < self.fit):
                        # 如果当前个体历史最佳适应值优于全局最优适应值
                        self.gbest = self.X[i]  # 更新全局最佳位置
                        self.fit = self.p_fit[i] # 更新全局最优适应值
            for i in range(self.pN):
            # 粒子群数量次的循环
                self.V[i] = self.w * self.V[i] + self.c1 * self.r1 * (self.pbest[i] - self.X[i]) + \
                            self.c2 * self.r2 * (self.gbest - self.X[i])
                # 做wv+c1*rand1*(pbest(i)-x(i))+c2*rand2*(gbest(i)-x(i))
                self.X[i] = self.X[i] + self.V[i]
                # 更新粒子位置
            fitness.append(self.fit)
            # 将此次迭代的全局最优适应值放入临时适应值数组
            print(self.fit)  # 输出最优值
        return fitness  #返回此适应值数组


my_pso = PSO(pN=30, dim=5, max_iter=100)
# 创建pso类对象，初始化粒子数为30，维度为5，迭代次数为100
my_pso.init_Population()
# 粒子群初始化
fitness = my_pso.iterator()
# 开始迭代