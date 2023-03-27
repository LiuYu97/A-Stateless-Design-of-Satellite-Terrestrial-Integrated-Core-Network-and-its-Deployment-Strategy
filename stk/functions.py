import math
import os
import random
from satellite_settings import *
from start_stk import Start_STK

os.environ['CUDA_VISIBLE_DEVICES'] = '0'


import time

startTime = time.time()
import networkx as nx
from tqdm import tqdm
import pandas as pd
import numpy as np
from comtypes.gen import STKObjects, STKUtil, AgStkGatorLib
from comtypes.client import CreateObject, GetActiveObject, GetEvents, CoGetObject, ShowEvents
from ctypes import *
import comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0
from comtypes import GUID
from comtypes import helpstring
from comtypes import COMMETHOD
from comtypes import dispid
from ctypes.wintypes import VARIANT_BOOL
from ctypes import HRESULT
from comtypes import BSTR
from comtypes.automation import VARIANT
from comtypes.automation import _midlSAFEARRAY
from comtypes import CoClass
from comtypes import IUnknown
import comtypes.gen._00DD7BD4_53D5_4870_996B_8ADB8AF904FA_0_1_0
import comtypes.gen._8B49F426_4BF0_49F7_A59B_93961D83CB5D_0_1_0
from comtypes.automation import IDispatch
import comtypes.gen._42D2781B_8A06_4DB2_9969_72D6ABF01A72_0_1_0
from comtypes import DISPMETHOD, DISPPROPERTY, helpstring


def Get_Population():
    A = np.zeros([50, 50])
    f = open('population.txt')  # 打开数据文件文件
    lines = f.readlines()  # 把全部数据文件读到一个列表lines中
    A_row = 0  # 表示矩阵的行，从0行开始
    for line in lines:  # 把lines中的数据逐行读取出来
        list = line.strip('\n').split(' ')  # 处理逐行数据：strip表示把头尾的'\n'去掉，split表示以空格来分割行数据，然后把处理后的行数据返回到list列表中
        A[A_row, :] = list[0:50]  # 把处理后的数据放到方阵A中。list[0:3]表示列表的0,1,2列数据放到矩阵A中的A_row行
        A_row += 1  # 然后方阵A的下一行接着读
    return A.astype(int)

def Gateway_Position_And_Load_Matrix(Gateway_Load):
    Gateway_Position_Matrix = np.zeros((50, 50, 3))
    lat = 82.26
    lon = -176.4
    for i in range(Gateway_Position_Matrix.shape[0]):
        for j in range(Gateway_Position_Matrix.shape[1]):
            Gateway_Position_Matrix[i][j][0] = lat - i * 3.48
            Gateway_Position_Matrix[i][j][1] = lon + j * 7.2
            Gateway_Position_Matrix[i][j][2] = Gateway_Load[i][j]
    # print(Gateway_Position_Matrix[47][-1])
    return Gateway_Position_Matrix


def Compute_Satellite_Position(current_time, sat):
    satLLADP = sat.DataProviders.GetDataPrvTimeVarFromPath('LLA State/Fixed')
    results_LLA = satLLADP.ExecSingleElements(current_time, ElementNames=["Lat", "Lon", "Alt"])
    Lat = results_LLA.DataSets.GetDataSetByName('Lat').GetValues()
    Lon = results_LLA.DataSets.GetDataSetByName('Lon').GetValues()
    Alt = results_LLA.DataSets.GetDataSetByName('Alt').GetValues()
    return Lat[0], Lon[0], Alt[0]


def Create_Ground_and_Target_Area(gateway_poseiton_and_load,scenario,stkRoot,Target_Area):
    print('create gateway')
    for i in range(gateway_poseiton_and_load.shape[0]):
        for j in range(gateway_poseiton_and_load.shape[1]):
            target_name = 'Gateway' + '_' + str(i) + '_' + str(j)
            gateway = scenario.Children.New(STKObjects.eTarget, target_name)
            gateway2 = gateway.QueryInterface(STKObjects.IAgTarget)
            gateway2.Position.AssignGeodetic(gateway_poseiton_and_load[i][j][0], gateway_poseiton_and_load[i][j][1], 0)
    print('create gateway done')
    print('create Target_Area')
    for i in range(len(Target_Area)):
        target_name = 'CoreNetwork' + '_' + str(i)
        print(target_name)
        corenetwork = scenario.Children.New(STKObjects.eTarget, target_name)
        corenetwork2 = corenetwork.QueryInterface(STKObjects.IAgTarget)
        corenetwork2.Position.AssignGeodetic(Target_Area[i][1], Target_Area[i][2], 0)
    print('create Target_Area done')
    Ground_list = stkRoot.CurrentScenario.Children.GetElements(STKObjects.eTarget)
    ground_dic = {}
    for target in Ground_list:
        ground_dic[target.InstanceName] = target
        # print(target.InstanceName)
    return ground_dic

def Create_Sat_Dic(sat_list, orbitNum, satsNum):
    # 创建卫星的字典，方便根据名字对卫星进行查找
    sat_dic = {}
    print('Creating Satellite Dictionary')
    for sat in tqdm(sat_list):
        sat_dic[sat.InstanceName] = sat
    Plane_num = []
    for i in range(0, orbitNum):
        Plane_num.append(i)
    Sat_num = []
    for i in range(0, satsNum):
        Sat_num.append(i)
    print("sat_dic len", len(sat_dic))
    print("Total satellite number:", len(sat_dic))
    print("plane_num", Plane_num)
    print("Sat_num", Sat_num)
    return sat_dic

def Get_nearest_sat_for_target_area(sat_position,stkRoot,Target_Area,satsNum,orbitNum):
    Ground_list = stkRoot.CurrentScenario.Children.GetElements(STKObjects.eTarget)
    # sat_list = stkRoot.CurrentScenario.Children.GetElements(STKObjects.eSatellite)
    nearest_sat_tmp = []
    for target in Ground_list:

        if target.InstanceName[:4] == "Core":
            distance = []
            distance2 = []
            core_num = int(target.InstanceName.split('_')[1])

            for sat in sat_position:
                sat_name = sat[0]
                # print(sat_name)
                # print(sat[2],Target_Area[core_num][2])
                x = abs(sat[2] - Target_Area[core_num][2])
                y = abs(sat[1] - Target_Area[core_num][1])
                z = abs(abs(sat[2] - Target_Area[core_num][2]) - 180)
                if y <= 360 / (satsNum * 2) + 0.0001:
                    if x <= 360 / (orbitNum * 2 * 2) + 0.0001:
                        distance.append([sat_name, x, y])
                    if z <= 360 / (orbitNum * 2 * 2) + 0.0001:
                        distance2.append([sat_name, sat[2], sat[1]])
                # print(distance)
            if len(distance) == 1:
                print('near ',distance[0][0])
                now_plane_num = int(distance[0][0].split('_')[0][3:])
                now_sat_num = int(distance[0][0].split('_')[1])

                x = now_plane_num * satsNum + now_sat_num
                print(x)
                nearest_sat_tmp.append(x)
                # return distance[0][0]
            elif len(distance2) == 1:
                print('near ', distance2[0][0])
                now_plane_num = int(distance2[0][0].split('_')[0][3:])
                now_sat_num = int(distance2[0][0].split('_')[1])
                x = now_plane_num * satsNum + now_sat_num
                print(x)
                nearest_sat_tmp.append(x)
                # return distance2[0][0]
            else:
                print(distance)
                print(Target_Area[core_num][1], Target_Area[core_num][2])
                print(distance2)
                print('compute nearest sat for gateway error')
    print(nearest_sat_tmp)
        # nearest_sat.append(nearest_sat_tmp)
    # print(nearest_sat)
    return nearest_sat_tmp

def Get_nearest_sat_for_gateway(gateway_poseiton_and_load,target, sat_position,orbitNum,  satsNum):
    # print(target.InstanceName.split('_'))
    row = int(target.InstanceName.split('_')[1])
    col = int(target.InstanceName.split('_')[2])
    gateway_lat = gateway_poseiton_and_load[row][col][0]
    gateway_lon = gateway_poseiton_and_load[row][col][1]
    distance = []
    distance2 = []
    lat_ok = 0
    x,y,z=0,0,0
    text = []
    for sat in sat_position:
        sat_name = sat[0]
        x = min(abs(sat[2] - gateway_lon), abs(abs(sat[2] - gateway_lon) - 360))
        y = abs(sat[1] - gateway_lat)
        if y <= 360 / (satsNum * 2) + 0.001:
            lat_ok = 1
            text.append([sat_name, x, y, sat[1], sat[2]])

    # print(distance)
    if len(text)<1:
        print(text)
    # print(len(text))
    q = [text[i][1] for i in range(len(text))]
    return text[q.index(min(q))][0]
    # if len(distance) == 1:
    #     return distance[0][0]
    # elif len(distance) >= 2:
    #
    #     return distance[q.index(min(q))][0]
    # elif len(distance2) == 1:
    #     return distance2[0][0]
    # elif len(distance2) >= 2:
    #     q = [distance2[i][1] for i in range(len(distance2))]
    #     return distance2[q.index(min(q))][0]
    # else:
    #     print(distance)
    #     print(gateway_lat,gateway_lon)
    #     print(distance2)
    #     print(text)
        # if lat_ok == 0:
        #     print('Get_nearest_sat_for_gateway error, not suitable lat')
        # elif lat_ok == 1:
        #     print('Get_nearest_sat_for_gateway error, not suitable lon')
        # print('compute nearest sat for gateway error')


        #
        # if abs(gateway_lat)<72 :
        #
        #     if y <= 360 / (satsNum * 2) + 1:
        #         lat_ok=1
        #         text.append([sat_name,x,y,z,sat[1],sat[2] ])
        #         if  x<= 360 / (orbitNum * 2 * 2) + 0.0001:
        #             lat_ok = 2
        #             distance.append([sat_name, x, y])
        #         if  z<= 360 / (orbitNum * 2 * 2) + 0.0001:
        #             lat_ok = 2
        #             distance2.append([sat_name,  x, y])
        # else:
        #     y = abs(sat[1] - gateway_lat)
        #     #     if ppp>=7:
        #     #         y = abs(abs(sat[1]) - 90) + abs(90 - gateway_lat)
        #     # if np.sign(gateway_lon) == np.sign(sat[2]):
        #     #     y = abs(sat[1] - gateway_lat)
        #     # else:
        #     if y <= 360 / (satsNum * 2) + 1:
        #         lat_ok=1
        #         text.append([sat_name,x,y,z,sat[1],sat[2] ])
                # if  x<= 360 / (orbitNum * 2 ) + 0.0001:
                #     lat_ok = 2
                #     distance.append([sat_name, x, y])
                # if  z<= 360 / (orbitNum * 2) + 0.0001:
                #     lat_ok = 2
                #     distance2.append([sat_name,  x, y])

def Get_Satellite_Load_Matrix(gateway_poseiton_and_load,n,sat_position,scenario2,stkRoot,orbitNum,  satsNum):
    print('Get_Satellite_Load_Matrix')
    Sat_Load_Matrix = np.zeros(( orbitNum,  satsNum))
    Ground_list =  stkRoot.CurrentScenario.Children.GetElements(STKObjects.eTarget)
    for target in Ground_list:
        if target.InstanceName[:7] == "Gateway":
            # print('Get_nearest_sat_for_gateway')
            closest_sat_name = Get_nearest_sat_for_gateway(gateway_poseiton_and_load,target, sat_position,orbitNum,  satsNum)
            # print(closest_sat_name)
            # print('Get_nearest_sat_for_gateway ok')
            now_plane_num = int(closest_sat_name.split('_')[0][3:])
            now_sat_num = int(closest_sat_name.split('_')[1])
            # print(now_plane_num, " ", now_sat_num)
            # print(gateway_poseiton_and_load[int(target.InstanceName.split('_')[1])][int(target.InstanceName.split('_')[2])][2])
            Sat_Load_Matrix[now_plane_num][now_sat_num] +=\
                gateway_poseiton_and_load[int(target.InstanceName.split('_')[1])][int(target.InstanceName.split('_')[2])][2]
    # print('Get_Satellite_Load_Matrix OK')
    return Sat_Load_Matrix


