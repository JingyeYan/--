import random

W1 = 165  # 背包总容量
w1 = [23, 31, 29, 44, 53, 38, 63, 85, 89, 82]  # 每个物品所占容量
v1 = [92, 57, 49, 68, 60, 43, 67, 84, 87, 72]  # 每个物品的价值
n1 = 10  # 物品个数
W2 = 26
w2 = [12, 7, 11, 8, 9]
v2 = [24, 13, 23, 15, 16]
n2 = 5
W3 = 190
w3 = [56, 59, 80, 64, 75, 17]
v3 = [50, 50, 64, 46, 50, 5]
n3 = 6
W4 = 50
w4 = [31, 10, 20, 19, 4, 3, 6]
v4 = [70, 20, 39, 37, 7, 5, 10]
n4 = 7


def initpop(pop_size, gene_size):
    pop = [[]]
    for i in range(pop_size):
        temp = []  # 临时染色体数组
        for j in range(gene_size):
            temp.append(random.randint(0, 1))
        pop.append(temp)
    return pop[1:]


# 适应值函数,ge为一个染色体
def fitness(v, w, pop, W):
    weight = 0  # 物品当前总质量
    value = 0  # 物品当前总价值
    all_value = []  # 每一个个体的总价值
    for i in range(len(pop)):
        for j in range(len(pop[i])):
            if (pop[i][j] == 1):
                if weight + w[j] <= W:
                    weight = weight + w[j]
                    value = value + v[j]
                else:
                    value = 0  # 如果超重则适应度为0
                    break

        all_value.append(value)
        weight = 0
        value = 0
    return all_value


# 轮盘赌选择
def select(pop, all_value, n):
    new_fitness = []
    sum_value = sum(all_value)
    # 化成概率存入新适应值数组
    for i in range(n):
        new_fitness.append(all_value[i] / sum_value)
    # 化成概率值区间
    for i in range(len(new_fitness) - 2, -1, -1):
        temp = 0
        j = 0
        while (j <= i):
            temp = temp + new_fitness[j]
            j = j + 1
        new_fitness[i] = temp
    new_fitness[len(new_fitness) - 1] = 1

    alive = []  # 存活的个体
    # 产生随机数
    for i in range(len(pop)):
        alive.append(random.random())
    alive.sort()

    fitin = 0
    popin = 0
    new_pop = pop
    while popin < len(pop):
        if (alive[popin] < new_fitness[fitin]):
            new_pop[popin] = pop[fitin]
            popin += 1
        else:
            fitin += 1
    pop = new_pop


# 单点杂交，设定交叉概率pc为1
def crossover1(pop):
    for i in range(len(pop) - 1):
        cpoint = random.randint(0, len(pop[0]))
        temporary1 = []
        temporary2 = []

        temporary1.extend(pop[i][0:cpoint])
        temporary1.extend(pop[i + 1][cpoint:len(pop[i])])

        temporary2.extend(pop[i + 1][0:cpoint])
        temporary2.extend(pop[i][cpoint:len(pop[i])])

        pop[i] = temporary1
        pop[i + 1] = temporary2


def crossover2(pop, pc):
    a = int(len(pop) / 2)
    parents_one = pop[:a]
    parents_two = pop[a:]
    random.shuffle(parents_one)
    random.shuffle(parents_two)
    new_pop = []
    for i in range(a):
        r = random.random()
        if r <= pc:
            point1 = random.randint(0, (len(parents_one[i]) - 1))
            point2 = random.randint(point1, len(parents_one[i]))
            off_one = parents_one[i][:point1] + parents_two[i][point1:point2] + parents_one[i][point2:]
            off_two = parents_two[i][:point1] + parents_one[i][point1:point2] + parents_two[i][point2:]
        else:
            off_one = parents_one[i]
            off_two = parents_two[i]
        new_pop.append(off_one)
        new_pop.append(off_two)
    return new_pop


# 变异因子为pm
def mutation(pop, pm):
    px = len(pop)
    py = len(pop[0])
    # 染色体/个体中基因的个数
    for i in range(px):
        if (random.random() < pm):
            # 如果小于阈值就变异
            mpoint = random.randint(0, py - 1)
            if (pop[i][mpoint] == 1):
                pop[i][mpoint] = 0
            else:
                pop[i][mpoint] = 1


def best(pop, all_value):
    px = len(pop)
    bestindividual = pop[0]
    bestfitness = all_value[0]
    for i in range(1, px):
        # 循环找出最大的适应度，适应度最大的也就是最好的个体
        if (all_value[i] > bestfitness):
            bestfitness = all_value[i]
            bestindividual = pop[i]
    return bestindividual, bestfitness


pop_size = 200
pm = 0.5
pc = 0.7

pop = initpop(pop_size, n1)
all_value = fitness(v1, w1, pop, W1)
for i in range(500):
    select(pop, all_value, pop_size)
    # crossover1(pop)
    pop = crossover2(pop, pc)
    mutation(pop, pm)
    all_value = fitness(v1, w1, pop, W1)
bestin, bestfit = best(pop, all_value)
# 309 1111010000

"""
pop=initpop(pop_size,n2)
all_value=fitness(v2,w2,pop,W2)
for i in range(500):
    select(pop,all_value,pop_size)
    #crossover1(pop)
    pop=crossover2(pop,pc)
    mutation(pop,pm)
    all_value = fitness(v2, w2, pop, W2)
bestin, bestfit=best(pop,all_value)
# 51 01110
"""

"""
pop=initpop(pop_size,n3)
all_value=fitness(v3,w3,pop,W3)
for i in range(500):
    select(pop,all_value,pop_size)
    #crossover1(pop)
    pop=crossover2(pop,pc)
    mutation(pop,pm)
    all_value = fitness(v3, w3, pop, W3)
bestin, bestfit=best(pop,all_value)
# 150 110010
"""

"""
pop=initpop(pop_size,n4)
all_value=fitness(v4,w4,pop,W4)
for i in range(500):
    select(pop,all_value,pop_size)
    #crossover1(pop)
    pop=crossover2(pop,pc)
    mutation(pop,pm)
    all_value = fitness(v4, w4, pop, W4)
bestin, bestfit=best(pop,all_value)
# 107 1001000
"""
print(bestfit)
print(bestin)
