import numpy as np


# 建立“蚂蚁”类
class Ant(object):
    def __init__(self, path):  # 构造函数
        self.path = path  # 蚂蚁当前迭代整体路径
        self.length = self.calc_length(path)  # 蚂蚁当前迭代整体路径长度

    # 计算整体路径长度，path=[A, B, C, D, A]注意路径闭环
    def calc_length(self, path_):
        length_ = 0  # 长度
        for i in range(len(path_) - 1):  # 路径节点数组的遍历
            delta = (path_[i].x - path_[i + 1].x, path_[i].y - path_[i + 1].y)
            # x，y坐标的变化量
            length_ += np.linalg.norm(delta)  # 长度累和，累加项为√（deltax^2+deltay^2）
        return length_  # 返回总长度

    @staticmethod  # 静态方法
    def calc_len(A, B):  # 静态方法，计算城市A与城市B之间的距离
        return np.linalg.norm((A.x - B.x, A.y - B.y))
        # 计算此项二范数即两点距离公式


# 建立“城市”类
class City(object):
    def __init__(self, x, y):  # 构造函数
        self.x = x  # x坐标
        self.y = y  # y坐标


# 建立“路径”类
class Path(object):
    def __init__(self, A):  # A为起始城市
        self.path = [A, A]  # 路径节点数组头尾节点都为A

    def add_path(self, B):  # 追加路径信息，方便计算整体路径长度
        self.path.append(B)  # 添加B城市节点
        self.path[-1], self.path[-2] = self.path[-2], self.path[-1]
        # path数组末尾两节点交换，即将新加的节点存入倒数第二位

# 构建“蚁群算法”
class ACO(object):
    def __init__(self, ant_num=50, maxIter=300, alpha=1, beta=5, rho=0.1, Q=1):
        # 类构造函数，参数含义如下
        self.ants_num = ant_num  # 蚂蚁个数
        self.maxIter = maxIter  # 蚁群最大迭代次数
        self.alpha = alpha  # 信息启发式因子
        self.beta = beta  # 期望启发式因子
        self.rho = rho  # 信息素挥发速度
        self.Q = Q  # 信息素强度
        ###########################
        self.deal_data('coordinates.dat')
        # 提取所有城市的坐标信息，文件信息后面给出
        ###########################
        self.path_seed = np.zeros(self.ants_num).astype(int)
        # 记录一次迭代过程中每个蚂蚁的初始城市下标,大小为蚂蚁数量
        self.ants_info = np.zeros((self.maxIter, self.ants_num))
        # 记录每次迭代后所有蚂蚁的路径长度信息，大小为迭代次数*蚂蚁数
        self.best_path = np.zeros(self.maxIter)
        # 记录每次迭代后整个蚁群的“历史”最短路径长度，大小为迭代次数*1
        ########################### 
        self.solve()  # 完成算法的迭代更新

    # 读取城市坐标数据
    def deal_data(self, filename):
        with open(filename, 'rt') as f:  # 打开文件
            temp_list = list(line.split() for line in f)
            # 临时存储提取出来的坐标信息
        self.cities_num = len(temp_list)  # 1. 获取城市个数
        self.cities = list(City(float(item[0]), float(item[1])) for item in temp_list)  # 2. 构建城市列表
        self.city_dist_mat = np.zeros((self.cities_num, self.cities_num))  # 3. 构建城市距离矩阵
        for i in range(self.cities_num):  # 城市个数次的循环
            A = self.cities[i]  # 提取城市节点
            for j in range(i, self.cities_num):  # 从当前城市到最后的遍历
                B = self.cities[j] # 其他城市
                self.city_dist_mat[i][j] = self.city_dist_mat[j][i] = Ant.calc_len(A, B)
                # 计算A，B间的距离，存入城市距离矩阵
        self.phero_mat = np.ones((self.cities_num, self.cities_num))  # 4. 初始化信息素矩阵
        self.eta_mat = 1 / (self.city_dist_mat + np.diag([np.inf] * self.cities_num))  # 5. 初始化启发函数矩阵

    # 算法执行
    def solve(self):
        iterNum = 0  # 当前迭代次数
        while iterNum < self.maxIter:
            # 当当前迭代次数小于最大迭代次数
            self.random_seed()  # 使整个蚁群产生随机的起始点
            delta_phero_mat = np.zeros((self.cities_num, self.cities_num))
            # 初始化每次迭代后信息素矩阵的增量
            for i in range(self.ants_num):  # 蚂蚁个数次的遍历
                city_index1 = self.path_seed[i]  # 每只蚂蚁访问的第一个城市下标
                ant_path = Path(self.cities[city_index1])  # 记录每只蚂蚁访问过的城市
                tabu = [city_index1]  # 记录每只蚂蚁访问过的城市下标，禁忌城市下标列表
                non_tabu = list(set(range(self.cities_num)) - set(tabu)) # 非禁止，即可以走
                for j in range(self.cities_num - 1):  # 对余下的城市进行访问
                    up_proba = np.zeros(self.cities_num - len(tabu))  # 初始化状态迁移概率的分子
                    for k in range(self.cities_num - len(tabu)): # 在剩余可行城市中，求迁移概率
                        up_proba[k] = np.power(self.phero_mat[city_index1][non_tabu[k]], self.alpha) * \
                                      np.power(self.eta_mat[city_index1][non_tabu[k]], self.beta)
                        # 分子为信息素浓度^信息启发因子*启发函数^期望启发因子
                    proba = up_proba / sum(up_proba)
                    # 每条可能子路径上的状态迁移概率，部分除以整体
                    while True:  # 提取出下一个城市的下标
                        random_num = np.random.rand()
                        #产生[0,1)浮点数
                        index_need = np.where(proba > random_num)[0]
                        # 取出概率大于随机数的城市在proba中的坐标
                        if len(index_need) > 0:
                        # 如果存在这样的城市
                            city_index2 = non_tabu[index_need[0]]
                            # 取出城市节点坐标
                            break  # 退出循环
                    ant_path.add_path(self.cities[city_index2])
                    # 蚂蚁访问此节点
                    tabu.append(city_index2)
                    # 禁止表（已访问）添加此节点
                    non_tabu = list(set(range(self.cities_num)) - set(tabu))
                    # 更新非禁止表
                    city_index1 = city_index2
                    # 更新蚂蚁当前访问城市坐标
                self.ants_info[iterNum][i] = Ant(ant_path.path).length
                # 记录此蚂蚁的路径长度信息
                if iterNum == 0 and i == 0:  # 完成对最佳路径城市的记录
                    # 如果是第一代第一只蚂蚁
                    self.best_cities = ant_path.path
                    # 记录最佳路径城市
                else:
                    if self.ants_info[iterNum][i] < Ant(self.best_cities).length: self.best_cities = ant_path.path
                    # 如果此路径长度比已记录的要小，则记录最佳城市
                tabu.append(tabu[0])  # 每次迭代完成后，使禁忌城市下标列表形成完整闭环
                for l in range(self.cities_num): # 城市个数次数的遍历
                    # 更新信息素增量矩阵
                    delta_phero_mat[tabu[l]][tabu[l + 1]] += self.Q / self.ants_info[iterNum][i]

            self.best_path[iterNum] = Ant(self.best_cities).length
            # 记录当前代数最佳路径长度

            self.update_phero_mat(delta_phero_mat)  # 更新信息素矩阵
            iterNum += 1 # 迭代次数+1

    # 更新信息素矩阵，参数为信息素增量矩阵
    def update_phero_mat(self, delta):
        self.phero_mat = (1 - self.rho) * self.phero_mat + delta
        # 信息素浓度=（1-信息挥发速度）*信息素浓度+信息素变量

    # 产生随机的起始点下表，尽量保证所有蚂蚁的起始点不同
    def random_seed(self):
        if self.ants_num <= self.cities_num:  # 蚂蚁数 <= 城市数
            self.path_seed[:] = np.random.permutation(range(self.cities_num))[:self.ants_num]
            # 在城市数范围内生成蚂蚁个数的数的随机序列
        else:  # 蚂蚁数 > 城市数
            self.path_seed[:self.cities_num] = np.random.permutation(range(self.cities_num))
            # 先生成城市个数的随机数列放入此数组的前城市个数项
            temp_index = self.cities_num
            # 取当前下标
            while temp_index + self.cities_num <= self.ants_num:
            # 如果两倍的城市个数仍然小于蚂蚁数
                self.path_seed[temp_index:temp_index + self.cities_num] = np.random.permutation(range(self.cities_num))
                # 则再用随机数列填充
                temp_index += self.cities_num
                # 更新下标
            temp_left = self.ants_num % self.cities_num
            # 蚂蚁数对城市数取余
            if temp_left != 0:
                # 继续填充随机数列，范围同上
                self.path_seed[temp_index:] = np.random.permutation(range(self.cities_num))[:temp_left]

ACO()
# 执行算法