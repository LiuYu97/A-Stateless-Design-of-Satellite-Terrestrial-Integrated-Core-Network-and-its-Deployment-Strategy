import  numpy as np
import random
import os
import matplotlib.pyplot as plt
import networkx as nx
import copy
import main
import pandas as pd
import time
import kmeans

class NSGA2_Distribute():

    def __init__(self, MAX_AMF_NUMBER, MAX_SMF_NUMBER, MAX_UPF_NUMBER,SAT_NUMBER):
        self.SAT_NUMBER = SAT_NUMBER
        self.sat_index = [i for i in range(self.SAT_NUMBER)]
        self.DNA_SIZE = MAX_AMF_NUMBER + MAX_SMF_NUMBER + MAX_UPF_NUMBER
        self.MAX_AMF_NUMBER = MAX_AMF_NUMBER
        self.MAX_SMF_NUMBER = MAX_SMF_NUMBER
        self.MAX_UPF_NUMBER = MAX_UPF_NUMBER
        self.NF_NUMBER = [i + 1 for i in range(self.MAX_AMF_NUMBER)]
        self.POP_SIZE = 100
        self.P0 = np.zeros((self.POP_SIZE, self.DNA_SIZE),int)
        self.cross_rate = 0.7
        self.mutation = 0.01



        self.initializeDistribute()
        np.savetxt('initial.txt',self.P0,fmt='%d')
        self.Q0 = copy.deepcopy(self.P0)
        self.merge = np.zeros((2 * self.POP_SIZE, self.DNA_SIZE),int)
        self.merge_len = 2 * self.POP_SIZE
        self.merge_capital = []
        self.merge_performance = []
        self.NDFSet = []
        # print(self.Q0)


    def initializeDistribute(self):
        for r in range(self.POP_SIZE):
            print('r',r)
            avail_number = copy.deepcopy(self.NF_NUMBER)
            avail_index = copy.deepcopy(self.sat_index)
            # amf
            p = []
            sump =0
            for i in range(1,self.MAX_AMF_NUMBER+1):
                sump = sump+i
                p.append(sump)
            p = [i /sum(p) for i in p]
            amf_number = np.random.choice(a=avail_number, p=p)
            for i in range(amf_number):
                self.P0[r][i] = random.choice(avail_index)
                avail_index.remove(self.P0[r][i])
            for j in range(amf_number, self.MAX_AMF_NUMBER):
                self.P0[r][j] = 999
            # smf
            smf_potential = []
            for k in range(amf_number):
                distance = []
                for m in avail_index:
                    # distance.append(nx.dijkstra_path_length(main.G, self.P0[r][k], m))
                    distance.append(main.delayMean[self.P0[r][k]][m])
                # print('min(distance)', distance)
                smf_potential.append(avail_index[distance.index(min(distance))])
            assert len(set(smf_potential)) <= amf_number, 'smf部署位置大于amf数量'
            avail_number = list(filter(lambda x: x <= len(smf_potential), avail_number))
            smf_number = random.choice(avail_number)

            amf_smf_dis = np.full_like(np.zeros((amf_number,smf_number)),9999)
            # amf_nearest_smf = [999 for _ in range(amf_number)]
            # print('amfnumber',amf_number,smf_number)
            i=0
            smf_avail_index = copy.deepcopy(avail_index)
            while i<smf_number:
                self.P0[r][self.MAX_AMF_NUMBER + i] = random.choice(smf_avail_index)
                smf_avail_index.remove(self.P0[r][self.MAX_AMF_NUMBER + i])
                # print('amfnumber', self.P0[r])
                for  a in range(amf_number):
                    # amf_smf_dis[a][i] = nx.dijkstra_path_length(main.G, self.P0[r][a], self.P0[r][self.MAX_AMF_NUMBER + i])
                    amf_smf_dis[a][i] = main.delayMean[self.P0[r][a]][self.P0[r][self.MAX_AMF_NUMBER + i]]
                np.argmin(amf_smf_dis, axis=1)
                tmp = list(np.argmin(amf_smf_dis, axis=1))
                if set([i for i in range(i+1)]) <= set(tmp):
                    # amf_nearest_smf = copy.deepcopy(tmp)
                    avail_index.remove(self.P0[r][self.MAX_AMF_NUMBER + i])
                    i=i+1
                else:
                    print('重新部署smf')
                    if len(smf_avail_index) == 0:
                        smf_number = i
                        print('无法再额外部署smf。修改smf数量')
            for j in range(smf_number, self.MAX_SMF_NUMBER):
                self.P0[r][self.MAX_AMF_NUMBER + j] = 999

            # upf
            upf_potential = []
            for k in range(smf_number):
                distance = []
                for m in avail_index:
                    # distance.append(nx.dijkstra_path_length(main.G, self.P0[r][self.MAX_AMF_NUMBER + k], m))
                    distance.append(main.delayMean[self.P0[r][self.MAX_AMF_NUMBER + k]][m])

                upf_potential.append(avail_index[distance.index(min(distance))])
            assert len(set(upf_potential)) <= smf_number, 'smf部署位置大于amf数量'
            avail_number = list(filter(lambda x: x <= len(upf_potential), avail_number))
            upf_number = random.choice(avail_number)

            smf_upf_dis = np.full_like(np.zeros((smf_number, upf_number)), 9999)
            smf_nearest_upf = [999 for _ in range(amf_number)]
            i = 0
            upf_avail_index = copy.deepcopy(avail_index)
            while i < upf_number:
                self.P0[r][self.MAX_AMF_NUMBER + self.MAX_SMF_NUMBER + i] = random.choice(upf_avail_index)
                upf_avail_index.remove(self.P0[r][self.MAX_AMF_NUMBER + self.MAX_SMF_NUMBER + i])
                for s in range(smf_number):
                    # smf_upf_dis[s][i] = nx.dijkstra_path_length(main.G, self.P0[r][self.MAX_AMF_NUMBER + s], self.P0[r][self.MAX_AMF_NUMBER + self.MAX_SMF_NUMBER + i])
                    smf_upf_dis[s][i] = main.delayMean[self.P0[r][self.MAX_AMF_NUMBER + s]][self.P0[r][self.MAX_AMF_NUMBER + self.MAX_SMF_NUMBER + i]]
                np.argmin(smf_upf_dis, axis=1)
                tmp = list(np.argmin(smf_upf_dis, axis=1))
                if set([i for i in range(i+1)]) <= set(tmp):
                    smf_nearest_upf = copy.deepcopy(tmp)
                    avail_index.remove(self.P0[r][self.MAX_AMF_NUMBER + self.MAX_SMF_NUMBER + i])
                    i = i + 1
                else:
                    print('重新部署upf')
                    if len(upf_avail_index) == 0:
                        upf_number = i
                        print('无法再额外部署upf。修改upf数量')
            for j in range(upf_number, self.MAX_UPF_NUMBER):
                self.P0[r][self.MAX_AMF_NUMBER + self.MAX_SMF_NUMBER + j] = 999

            if random.random() < 0.5:
                self.P0[r][:amf_number],self.P0[r][self.MAX_AMF_NUMBER:self.MAX_AMF_NUMBER+smf_number],self.P0[r][self.MAX_AMF_NUMBER + self.MAX_SMF_NUMBER :self.MAX_AMF_NUMBER + self.MAX_SMF_NUMBER +upf_number] = kmeans.nf_kmeans_nsga(amf_number,smf_number,upf_number)
                print('kmeans',self.P0[r])

    # 将编码后的DNA翻译回来（解码）
    def translateDNA(self, l_amf, l_smf, l_upf):
        amf = np.zeros((len(l_amf), self.SAT_NUMBER))
        smf = np.zeros((len(l_smf), self.SAT_NUMBER))
        upf = np.zeros((len(l_upf), self.SAT_NUMBER))
        for i in range(len(l_amf)):
            amf[i][int(l_amf[i])] = 1
        for i in range(len(l_smf)):
            smf[i][int(l_smf[i])] = 1
        for i in range(len(l_upf)):
            upf[i][int(l_upf[i])] = 1
        return amf, smf, upf

    def getnflen(self, var):
        amf = len(list(filter(lambda x:x!=999,var[:self.MAX_AMF_NUMBER])))
        smf = len(list(filter(lambda x:x!=999,var[self.MAX_AMF_NUMBER:self.MAX_AMF_NUMBER + self.MAX_SMF_NUMBER])))
        upf = len(list(filter(lambda x:x!=999,var[self.MAX_SMF_NUMBER + self.MAX_AMF_NUMBER:self.MAX_SMF_NUMBER + self.MAX_AMF_NUMBER + self.MAX_UPF_NUMBER])))
        return amf, smf, upf

    # 得到适应度
    def get_fitness(self, index):
        l_amf = list(filter(lambda x: x != 999, self.merge[index][:self.MAX_AMF_NUMBER]))
        l_smf = list(filter(lambda x: x != 999,
                            self.merge[index][self.MAX_AMF_NUMBER:self.MAX_AMF_NUMBER + self.MAX_SMF_NUMBER]))
        l_upf = list(filter(lambda x: x != 999, self.merge[index][
                                                self.MAX_SMF_NUMBER + self.MAX_AMF_NUMBER:self.MAX_SMF_NUMBER + self.MAX_AMF_NUMBER + self.MAX_UPF_NUMBER]))
        amf, smf, upf = self.translateDNA(l_amf, l_smf, l_upf)
        # print('amf,smf,upf', amf, smf, upf)
        if len(l_smf) == 0 or len(l_amf) == 0 or len(l_upf) == 0:
            print('11111111111', self.merge[index])
        capital, performance, result,_,_,_,_ = main.F(len(l_amf), len(l_smf), len(l_upf), amf, smf, upf)
        return capital, performance, 1 / result

    # 得到适应度
    def get_var_fitness(self,var, index):
        l_amf = list(filter(lambda x: x != 999, var[index][:self.MAX_AMF_NUMBER]))
        l_smf = list(filter(lambda x: x != 999,
                            var[index][self.MAX_AMF_NUMBER:self.MAX_SMF_NUMBER + self.MAX_SMF_NUMBER]))
        l_upf = list(filter(lambda x: x != 999, var[index][
                                                self.MAX_SMF_NUMBER + self.MAX_AMF_NUMBER:self.MAX_SMF_NUMBER + self.MAX_AMF_NUMBER + self.MAX_UPF_NUMBER]))
        amf, smf, upf = self.translateDNA(l_amf, l_smf, l_upf)
        # print('amf,smf,upf', amf, smf, upf)
        if len(l_smf) == 0 or len(l_amf) == 0 or len(l_upf) == 0:
            print('11111111111', var[index])
        capital, performance, result,_,_,_,_ = main.F(len(l_amf), len(l_smf), len(l_upf), amf, smf, upf)
        return capital, performance, 1 / result

    # 染色体交叉
    def crossover(self):
        for i in range(self.POP_SIZE):
            tmp = copy.deepcopy(self.Q0[i])
            if np.random.rand() < self.cross_rate:
                a = np.random.randint(0, self.POP_SIZE)
                position = random.randrange(0, self.DNA_SIZE)
                tmp11 = self.Q0[i][:position]
                tmp12 = copy.deepcopy(self.Q0[i][position:])
                tmp21 = self.Q0[a][:position]
                tmp22 = copy.deepcopy(self.Q0[a][position:])
                set_lst = set(list(self.Q0[i]))
                self.Q0[i] = copy.deepcopy(np.append(tmp11, tmp22))
                m = list(filter(lambda x: x != 999, self.Q0[i]))
                set_lst = set(list(m))
                # 防止网元部署在同一个节点上。
                if not len(set_lst) == len(list(m)):
                    self.Q0[i] = np.append(tmp11, tmp12)
            amf,s,u = self.getnflen(self.Q0[i])
            if not u<=s<=amf:
                self.Q0[i] = tmp
                # print('交叉失败')
            # 防止一个网元实例都没有部署
            if len(list(filter(lambda x: x == 999, self.Q0[i][:self.MAX_AMF_NUMBER]))) == self.MAX_AMF_NUMBER or len(
                    list(filter(lambda x: x == 999, self.Q0[i][
                                                    self.MAX_AMF_NUMBER:self.MAX_AMF_NUMBER + self.MAX_SMF_NUMBER]))) == self.MAX_AMF_NUMBER or len(
                list(filter(lambda x: x == 999, self.Q0[i][
                                                self.MAX_AMF_NUMBER + self.MAX_SMF_NUMBER:
                                                self.MAX_AMF_NUMBER + self.MAX_SMF_NUMBER + self.MAX_UPF_NUMBER]))) == self.MAX_AMF_NUMBER:
                self.Q0[i] = tmp
            # if self.invaliddistribute(np.array([self.Q0[i]]))!=0:
            #     print(self.Q0[i],self.Q0[a],position)
        return self.Q0

    # 基因变异
    def mutate(self):
        for i in range(self.POP_SIZE):
            tmp = copy.deepcopy(self.Q0[i])
            a = [i for i in self.sat_index]
            a = list(filter(lambda x: x not in self.Q0[i], a))
            a.append(999)
            for point in range(self.DNA_SIZE):
                if np.random.rand() < self.mutation:
                    self.Q0[i][point] = random.choice(a)
            # 防止一个网元实例都没有部署
            if len(list(filter(lambda x: x == 999, self.Q0[i][:self.MAX_AMF_NUMBER]))) == self.MAX_AMF_NUMBER or len(
                    list(filter(lambda x: x == 999, self.Q0[i][
                                                    self.MAX_AMF_NUMBER:self.MAX_AMF_NUMBER + self.MAX_SMF_NUMBER]))) == self.MAX_AMF_NUMBER or len(
                list(filter(lambda x: x == 999, self.Q0[i][
                                                self.MAX_AMF_NUMBER + self.MAX_SMF_NUMBER:
                                                self.MAX_AMF_NUMBER + self.MAX_SMF_NUMBER + self.MAX_UPF_NUMBER]))) == self.MAX_AMF_NUMBER:
                self.Q0[i] = tmp
        return self.Q0

    def combine(self):
        self.merge = copy.deepcopy(np.append(self.P0, self.Q0, axis=0))
        return self.merge

    def fnds(self):
        # define the dominate set Sp
        dominateList = [set() for i in range(self.merge_len)]
        # define the dominated set
        dominatedList = [set() for i in range(self.merge_len)]

        for i in range(self.merge_len):
            m,n,_ = self.get_fitness(i)
            self.merge_capital.append(m)
            self.merge_performance.append(n)
        # qqq = 0
        for i in range(self.merge_len):
            for j in range(self.merge_len):
                if self.merge_capital[i] < self.merge_capital[j] and self.merge_performance[i] < self.merge_performance[
                    j]:
                    dominateList[i].add(j)
                elif self.merge_capital[i] < self.merge_capital[j] and self.merge_performance[i] == self.merge_performance[
                    j]:
                    dominateList[i].add(j)
                elif self.merge_capital[i] == self.merge_capital[j] and self.merge_performance[i] < self.merge_performance[
                    j]:
                    dominateList[i].add(j)
                elif self.merge_capital[i] > self.merge_capital[j] and self.merge_performance[i] > \
                        self.merge_performance[j]:
                    dominatedList[i].add(j)
                elif self.merge_capital[i] == self.merge_capital[j] and self.merge_performance[i] > \
                        self.merge_performance[j]:
                    dominatedList[i].add(j)
                elif self.merge_capital[i] > self.merge_capital[j] and self.merge_performance[i] == \
                        self.merge_performance[j]:
                    dominatedList[i].add(j)
                # elif i != j and self.merge_capital[i] == self.merge_capital[j] and self.merge_performance[i] == \
                #         self.merge_performance[j]:
        #             print('222222222222222222',self.merge[i],self.merge[j])
        #             qqq = qqq+1
        # print('qqq',qqq)
        # compute dominated degree Np
        for i in range(self.merge_len):
            dominatedList[i] = len(dominatedList[i])

        # create list to save the non-dominated front information
        NDFSet2 = []
        # compute non-dominated front
        while max(dominatedList) >= 0:
            front = []
            for i in range(self.merge_len):
                if dominatedList[i] == 0:
                    front.append(i)
            NDFSet2.append(front)
            for i in range(self.merge_len):
                dominatedList[i] = dominatedList[i] - 1
        self.NDFSet = NDFSet2
        return NDFSet2

    def crowdedDistance(self, Front):
        # create distance list to save the information of crowded for every entity in front
        distance = pd.Series([float(0) for i in range(len(Front))], index=Front)
        capitalList = []
        performance = []
        for i in Front:
            capitalList.append(self.merge_capital[i])
            performance.append(self.merge_performance[i])
        # print('capitalList', capitalList)
        # print('preformance', performance)
        capitalSer = pd.Series(capitalList, index=Front)
        performanceSer = pd.Series(performance, index=Front)
        # sort value
        capitalSer.sort_values(ascending=False, inplace=True)
        # print('capitalSer', capitalSer)
        performanceSer.sort_values(ascending=False, inplace=True)
        # print('performanceSer', performanceSer)
        # set the distance for the entities which have the min and max value in every objective
        distance[capitalSer.index[0]] = 10000
        distance[capitalSer.index[-1]] = 10000
        distance[performanceSer.index[0]] = 10000
        distance[performanceSer.index[-1]] = 10000

        aaa = (max(capitalList) - min(capitalList)) if not max(capitalList) == min(capitalList) else 1
        bbb = (max(performanceSer) - min(performanceSer)) if not max(performanceSer) == min(performanceSer) else 1
        for i in range(1, len(Front) - 1):
            distance[capitalSer.index[i]] = distance[capitalSer.index[i]] + (
                    capitalSer[capitalSer.index[i - 1]] - capitalSer[capitalSer.index[i + 1]]) / (
                                                aaa)
            distance[performanceSer.index[i]] += (performanceSer[performanceSer.index[i - 1]] - performanceSer[
                performanceSer.index[i + 1]]) / (bbb)

        distance.sort_values(ascending=False, inplace=True)
        return distance

    def crowdedCompareOperator(self):
        newPopulation = []
        # save the information of the entity the new population have
        count = 0
        # save the information of the succession of the front
        number = 0
        while count < self.POP_SIZE:
            if count + len(self.NDFSet[number]) <= self.POP_SIZE:
                if number == 0:
                    # save the information of the first non-dominated front
                    firstFront = [i for i in self.NDFSet[number]]
                for i in self.NDFSet[number]:
                    newPopulation.append(self.merge[i])
                count += len(self.NDFSet[number])
                number += 1
            else:
                if number == 0:
                    firstFront = [i for i in range(self.POP_SIZE)]
                n = self.POP_SIZE - count
                distance = self.crowdedDistance(self.NDFSet[number])
                for i in range(n):
                    newPopulation.append(self.merge[distance.index[i]])
                number += 1
                count += n
        return np.array(newPopulation), firstFront

    def defrepet(self):
        for i in range(self.merge_len):
            for j in range(i):
                tmp = copy.deepcopy(self.merge[i])
                while((self.merge[j][0:self.MAX_AMF_NUMBER] == self.merge[i][0:self.MAX_AMF_NUMBER]).all() and (
                        self.merge[j][
                        self.MAX_AMF_NUMBER:self.MAX_AMF_NUMBER + self.MAX_SMF_NUMBER] ==
                        self.merge[i][ self.MAX_AMF_NUMBER:self.MAX_AMF_NUMBER + self.MAX_SMF_NUMBER]).all() and (
                        self.merge[j][
                        self.MAX_AMF_NUMBER + self.MAX_SMF_NUMBER:
                        self.MAX_AMF_NUMBER + self.MAX_SMF_NUMBER + self.MAX_UPF_NUMBER] ==
                        self.merge[i][
                        self.MAX_AMF_NUMBER + self.MAX_SMF_NUMBER:
                        self.MAX_AMF_NUMBER + self.MAX_SMF_NUMBER + self.MAX_UPF_NUMBER]).all()):
                    # print('repeatrepeatrepeatrepeatrepeatrepeatrepeat')
                    a = [i for i in self.sat_index]
                    a = list(filter(lambda x: x not in self.merge[i], a))
                    a.append(999)
                    for point in range(self.DNA_SIZE):
                        if np.random.rand() < self.mutation:
                            self.merge[i][point] = random.choice(a)
                    # 防止一个网元实例都没有部署
                    if len(list(filter(lambda x: x == 999, self.merge[i][:self.MAX_AMF_NUMBER]))) == self.MAX_AMF_NUMBER or len(
                            list(filter(lambda x: x == 999, self.merge[i][
                                                            self.MAX_AMF_NUMBER:self.MAX_AMF_NUMBER + self.MAX_SMF_NUMBER]))) == self.MAX_AMF_NUMBER or len(
                        list(filter(lambda x: x == 999, self.merge[i][
                                                        self.MAX_AMF_NUMBER + self.MAX_SMF_NUMBER:
                                                        self.MAX_AMF_NUMBER + self.MAX_SMF_NUMBER + self.MAX_UPF_NUMBER]))) == self.MAX_AMF_NUMBER:
                        self.merge[i] = tmp

    def invaliddistribute(self,input):
        for i in range(input.shape[0]):
            ok=0
            amf = list(filter(lambda x: x != 999, input[i][:self.MAX_AMF_NUMBER]))
            smf = list(filter(lambda x: x != 999, input[i][self.MAX_AMF_NUMBER:self.MAX_AMF_NUMBER + self.MAX_SMF_NUMBER]))
            upf = list(filter(lambda x: x != 999, input[i][self.MAX_SMF_NUMBER + self.MAX_AMF_NUMBER:self.MAX_SMF_NUMBER + self.MAX_AMF_NUMBER + self.MAX_UPF_NUMBER]))
            amf_number, smf_number,upf_number = len(amf),len(smf),len(upf)

            amf_smf_dis = np.full_like(np.zeros((amf_number, smf_number)), 9999)
            for a in range(amf_number):
                for s in range(smf_number):
                    try :
                        amf_smf_dis[a][s] = nx.dijkstra_path_length(G, input[i][a], input[i][self.MAX_AMF_NUMBER + s])
                    except:
                        print('44444444444444444',input[i])
            np.argmin(amf_smf_dis, axis=1)
            tmp = list(np.argmin(amf_smf_dis, axis=1))
            if not set([i for i in range(smf_number)]) <= set(tmp):
                print('smf无效布局')
                ok=1

            smf_upf_dis = np.full_like(np.zeros((smf_number, upf_number)), 9999)
            for s in range(smf_number):
                for u in range(upf_number):
                    try :
                        smf_upf_dis[s][u] = nx.dijkstra_path_length(G, input[i][self.MAX_AMF_NUMBER +s], input[i][self.MAX_AMF_NUMBER +self.MAX_SMF_NUMBER+ u])
                    except:
                        print('44444444444444444',input[i])

            np.argmin(smf_upf_dis, axis=1)
            tmp = list(np.argmin(smf_upf_dis, axis=1))
            if not set([i for i in range(upf_number)]) <= set(tmp):
                print('upf无效布局')
                ok=2
        return ok
# @profile
def suanfa(MAX_AMF_NUMBER, MAX_SMF_NUMBER, MAX_UPF_NUMBER):
    # 迭代次数G
    G_MAX = 200
    a = NSGA2_Distribute(MAX_AMF_NUMBER, MAX_SMF_NUMBER, MAX_UPF_NUMBER,960)
    for G in range(G_MAX):
        start_time = time.time()
        a.merge_capital.clear()
        a.merge_performance.clear()
        a.crossover()
        a.mutate()
        a.combine()
        a.defrepet()
        # 非支配排序
        dfset = a.fnds()
        a.P0, firstFront = a.crowdedCompareOperator()
        # if G % 20 == 0:
        #     x = []
        #     y = []
        #     for i in dfset[0]:
        #         x.append(a.get_fitness(i)[0])
        #         y.append(a.get_fitness(i)[1])
        #     print('dfset[0]', len(a.merge_performance))
        #     c = []
        #     p = []
        #     for i in range(a.POP_SIZE):
        #         m,n,_ = a.get_var_fitness(a.P0, i)
        #         c.append(m)
        #         p.append(n)
        #     fig = plt.figure()
        #     plt.scatter(p, c, color='g', marker='v')
        #     plt.scatter(a.merge_performance, a.merge_capital, color='b', marker='.')
        #     plt.scatter(y, x, color='red', marker='.', s=10)
        #     # figure_save_path = "./file_fig"
        #     # if not os.path.exists(figure_save_path):
        #     #     os.makedirs(figure_save_path)  # 如果不存在目录figure_save_path，则创建
        #     # plt.savefig(os.path.join(figure_save_path, 'nspg2'+str(G)+'.png'))  # 第一个是指存储路径，第二个是图片名字
        #     plt.show()

        a.Q0 = copy.deepcopy(a.P0)
        stop_time = time.time()
        print('G', G,'time',stop_time-start_time)
        print('firstFront numbers', len(firstFront))
    opl = []
    for i in firstFront:
        opl.append(a.merge[i])
    opl = np.array(opl)
    capital = []
    performance = []
    result = []
    for i in range(len(firstFront)):
        c,p,_= a.get_var_fitness(opl,i)
        capital.append(c)
        performance.append(p)
        result.append(capital[i]+2.5*performance[i])
    x = [i for i in range(len(firstFront))]
    fig = plt.figure()
    plt.scatter(performance, capital)
    figure_save_path = "./file_fig"
    if not os.path.exists(figure_save_path):
        os.makedirs(figure_save_path)  # 如果不存在目录figure_save_path，则创建
    plt.savefig(os.path.join(figure_save_path, 'nspa2result.png'))  # 第一个是指存储路径，第二个是图片名字
    # plt.show()
    print('------------')
    for i in opl:
        print(i)
    print('------------')
    print(capital)
    print(performance)
    print('min result=',min(result),'amf.smf,upf',opl[result.index(min(result))])




if __name__ == '__main__':
    MAX_AMF_NUMBER = 15
    MAX_SMF_NUMBER = 15
    MAX_UPF_NUMBER = 15
    start_time = time.time()
    suanfa(MAX_AMF_NUMBER, MAX_SMF_NUMBER, MAX_UPF_NUMBER)
    stop_time = time.time()
    print('time = ', stop_time - start_time)



