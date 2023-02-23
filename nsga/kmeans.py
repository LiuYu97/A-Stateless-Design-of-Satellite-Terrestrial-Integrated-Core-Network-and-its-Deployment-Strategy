import copy

import numpy as np
import matplotlib.pyplot as plt
import  networkx as nx
import random


def K_means(center,K,nodes,Sat_load,delay):
    # print('center',center)
    Cluster = [[] for _ in range(K)]
    for i in nodes:
        l = []
        for m in range(K):
            l.append(delay[i][center[m]])
        Cluster[l.index(min(l))].append(i)
    # print(Cluster)
    center_new = []
    for i in range(K):
        tmp = []
        for m in range(len(Cluster[i])):
            l = []
            for j in Cluster[i]:
                l.append(Sat_load[j]*delay[j][Cluster[i][m]])
            tmp.append(sum(l))
        center_new.append(Cluster[i][tmp.index(min(tmp))])
    # print('center_new',center_new)
    k = 0
    for i in range(K):
        if delay[center[i]][center_new[i]] > 0:
            center[i] = center_new[i]
            k = 1
    if k == 0:
        return 0, center, Cluster
    else:
        return 1, center, Cluster


def K_means_smf_nsga(center,K,nodes,Sat_load,delay):
    # print('center',center)
    Cluster = [[] for _ in range(K)]
    for i in nodes:
        l = []
        for m in range(K):
            l.append(delay[i][center[m]])
        Cluster[l.index(min(l))].append(i)
    # print('Cluster',Cluster)
    center_new = []
    for i in range(K):
        tmp = []
        for m in range(len(Cluster[i])):
            l = []
            for j in Cluster[i]:
                l.append(Sat_load[nodes.index(j)]*delay[j][Cluster[i][m]])
            tmp.append(sum(l))
        center_new.append(Cluster[i][tmp.index(min(tmp))])
    # print('center_new',center_new)
    k = 0
    for i in range(K):
        if delay[center[i]][center_new[i]] > 0:
            center[i] = center_new[i]
            k = 1
    if k == 0:
        return 0, center, Cluster
    else:
        return 1, center, Cluster
# ok,center_smf,Cluster_smf = K_means_smf(center_smf,smf_num, copy.deepcopy(center_amf), LoadAmf, delay)
def K_means_smf_v2(center,K,nodes,Sat_load,delay):
    # print('center',center)
    Cluster = [[] for _ in range(K)]
    for i in nodes:
        l = []
        for m in range(K):
            l.append(delay[i][center[m]])
        Cluster[l.index(min(l))].append(i)
    # print('Cluster',Cluster)
    center_new = []
    loc = list(filter(lambda x:x not in nodes,[i for i in range(960)]))
    for i in range(K):
        tmp = []
        for m in loc:
            l = []
            for j in Cluster[i]:
                l.append(Sat_load[nodes.index(j)]*delay[j][m])
            tmp.append(sum(l))
        # set_lst = set(list(tmp))
        # if len(set_lst) != len(tmp):
        #     print('chongfu--------------------------')
        center_new.append(loc[tmp.index(min(tmp))])
    # print('center_new',center_new)
    k = 0
    for i in range(K):
        if delay[center[i]][center_new[i]] > 0:
            center[i] = center_new[i]
            k = 1
    if k == 0:
        return 0, center, Cluster
    else:
        return 1, center, Cluster

def K_means_upf(center,K,nodes,Sat_load,delay,center_amf):
    # print('center',center)
    Cluster = [[] for _ in range(K)]
    for i in nodes:
        l = []
        for m in range(K):
            l.append(delay[i][center[m]])
        Cluster[l.index(min(l))].append(i)
    print('Cluster',Cluster)
    center_new = []
    loc = list(filter(lambda x:x not in nodes,[i for i in range(960)]))
    loc = list(filter(lambda x: x not in center_amf, loc))
    for i in range(K):
        tmp = []
        for m in loc:
            l = []
            for j in Cluster[i]:
                l.append(Sat_load[nodes.index(j)]*delay[j][m])
            tmp.append(sum(l))
        # set_lst = set(list(tmp))
        # if len(set_lst) != len(tmp):
        #     print('chongfu--------------------------')
        center_new.append(loc[tmp.index(min(tmp))])
    print('center_new',center_new)
    k = 0
    for i in range(K):
        if delay[center[i]][center_new[i]] > 0:
            center[i] = center_new[i]
            k = 1
    if k == 0:
        return 0, center, Cluster
    else:
        return 1, center, Cluster

def nf_kmeans_nsga(amf_num,smf_num,upf_num):
    amf_num = amf_num
    smf_num = smf_num
    upf_num = upf_num
    nodes = 960
    center_amf = []
    center_smf = []
    sat_index = [i for i in range(nodes)]
    for i in range(amf_num):
        tmp = random.choice(sat_index)
        center_amf.append(tmp)
        sat_index.remove(tmp)
    LoadSat = np.loadtxt('./loadsum.txt').T.reshape(1, -1)[0]
    a = sum(LoadSat)/100000
    LoadSat = [x / a for x in LoadSat]
    delay = np.loadtxt('./delayMean.txt')
    hop = np.loadtxt('./hopMean.txt')
    while True:
        ok,center_amf,Cluster = K_means(center_amf,amf_num, [i for i in range(nodes)], LoadSat, delay)
        if ok == 0:
            break
    LoadAmf = []
    print('center_amf', center_amf)
    for i in range(amf_num):
        tmp = 0
        for j in Cluster[i]:
            tmp = tmp + LoadSat[j]
        LoadAmf.append(tmp)
    print(LoadAmf)
    center_smf = []
    for i in range(smf_num):
        center_smf.append(center_amf[i])
    while True:
        ok,center_smf,Cluster_smf = K_means_smf_nsga(center_smf,smf_num, copy.deepcopy(center_amf), LoadAmf, delay)
        if ok == 0:
            break
    print(center_smf)
    LoadSmf = []
    for i in range(smf_num):
        tmp = 0
        for j in Cluster_smf[i]:
            tmp = tmp + LoadAmf[center_amf.index(j)]
        LoadSmf.append(tmp)
    print(LoadSmf)
    center_upf = []
    for i in range(upf_num):
        center_upf.append(center_smf[i])
    while True:
        ok, center_upf, Cluster_upf = K_means_smf_nsga(center_upf, upf_num, center_smf, LoadSmf, delay)
        if ok == 0:
            break
    print(center_upf)
    LoadUpf = []
    for i in range(upf_num):
        tmp = 0
        for j in Cluster_upf[i]:
            tmp = tmp + LoadAmf[center_smf.index(j)]
        LoadUpf.append(tmp)
    print(LoadUpf)
    center_upf_result = []
    for i in center_upf:
        if i-2>int(i/40)*40:
            center_upf_result.append(i-2)
        elif i+2 < int(i/40)*40+40:
            center_upf_result.append(i+2)
    center_smf_result = []
    for s in center_smf:
        if s in center_upf:
            if s-2 in center_upf_result:
                center_smf_result.append(s - 1)
            elif s+2 in center_upf_result:
                center_smf_result.append(s + 1)
        elif (s-1)>(int(s/40)*40):
            center_smf_result.append(s - 1)
        elif (s+1)< int(s/40)*40+40:
            center_smf_result.append(s + 1)
    center_amf_result = center_amf
    print(center_amf_result)
    print(center_smf_result)
    print(center_upf_result)
    # for i in center_amf:
    #     print(int(i/40)*40,int(i/40)*40+40)
    return center_amf_result,center_smf_result,center_upf_result

def nf_kmeans(amf_num,smf_num,upf_num):
    amf_num = amf_num
    smf_num = smf_num
    upf_num = upf_num
    nodes = 960
    center_amf = []
    center_smf = []
    sat_index = [i for i in range(nodes)]
    for i in range(amf_num):
        tmp = random.choice(sat_index)
        center_amf.append(tmp)
        sat_index.remove(tmp)
    LoadSat = np.loadtxt('./loadsum.txt').T.reshape(1, -1)[0]/100000
    a = sum(LoadSat)/100000
    LoadSat = [x / a for x in LoadSat]
    delay = np.loadtxt('./delayMean.txt')
    hop = np.loadtxt('./hopMean.txt')

    while True:
        ok,center_amf,Cluster = K_means(center_amf,amf_num, [i for i in range(nodes)], LoadSat, delay)
        if ok == 0:
            break
    LoadAmf = []
    print('center_amf', center_amf)
    for i in range(amf_num):
        tmp = 0
        for j in Cluster[i]:
            tmp = tmp + LoadSat[j]
        LoadAmf.append(tmp)
    print(LoadAmf)
    center_smf = []
    for i in range(smf_num):
        center_smf.append(center_amf[i])
    while True:
        ok,center_smf,Cluster_smf = K_means_smf_v2(center_smf,smf_num, copy.deepcopy(center_amf), LoadAmf, delay)
        if ok == 0:
            break
    # print('center_smf',center_smf,Cluster_smf)
    LoadSmf = []
    for i in range(smf_num):
        tmp = 0
        for j in Cluster_smf[i]:
            tmp = tmp + LoadAmf[center_amf.index(j)]
        LoadSmf.append(tmp)
    # print(LoadSmf)
    center_upf = []
    print('center_smf', center_smf)
    for i in range(upf_num):
        center_upf.append(center_smf[i])
    print('center_upf1111', center_upf)
    while True:
        ok, center_upf, Cluster_upf = K_means_upf(center_upf, upf_num, center_smf, LoadSmf, delay,center_amf)
        if ok == 0:
            break
    # print(center_upf)
    print('center_smf', center_smf, Cluster_upf)
    LoadUpf = []
    for i in range(upf_num):
        tmp = 0
        for j in Cluster_upf[i]:
            tmp = tmp + LoadAmf[center_smf.index(j)]
        LoadUpf.append(tmp)
    print(center_amf)
    print(center_smf)
    print(center_upf)



# print(nf_kmeans(3,3,3))
