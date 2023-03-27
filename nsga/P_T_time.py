import time
import random
import networkx as nx
import numpy as np
import main
import NF
import multiprocessing
from joblib import Parallel, delayed
def compute_sat_link_index(delay, amf_location, smf_location, upf_location,core_location_sat):
    delay_sat_vnf1_var = np.matmul(amf_location, delay)
    delay_sat_vnf2_var = np.matmul(smf_location, delay)
    delay_vnf1_vnf2_var = np.matmul(smf_location, delay_sat_vnf1_var.T)
    delay_vnf2_vnf3_var = np.matmul(upf_location, delay_sat_vnf2_var.T)

    delay_ground_vnf2_var = np.matmul(core_location_sat, delay_sat_vnf2_var.T)

    # delay_sat_vnf1_min_var = np.min(delay_sat_vnf1_var, axis=0)
    vnf1_index_var = np.argmin(delay_sat_vnf1_var, axis=0)
    # delay_vnf1_vnf2__min_var = np.min(delay_vnf1_vnf2_var, axis=0)
    vnf2_index_var = np.argmin(delay_vnf1_vnf2_var, axis=0)
    # delay_vnf2_vnf3__min_var = np.min(delay_vnf2_vnf3_var, axis=0)
    vnf3_index_var = np.argmin(delay_vnf2_vnf3_var, axis=0)

    ground_index_var = np.argmin(delay_ground_vnf2_var, axis=0)

    # 每个VNF部署节点
    vnf1_location_var = np.argmax(amf_location, 1)
    # print('vnf1_location_var',vnf1_location_var)
    vnf2_location_var = np.argmax(smf_location, 1)
    vnf3_location_var = np.argmax(upf_location, 1)
    # print('vnf1_location_var', vnf1_location_var)
    ground_location_var = np.argmax(core_location_sat, 1)

    sat_link_index = np.zeros((delay.shape[0], 4)).astype(np.uint32)
    sat_link_index_for_ns3 = np.zeros((delay.shape[0], 4)).astype(np.uint32)
    # 消息路径
    for s in range(delay.shape[0]):
        sat_link_index[s][0] = vnf1_location_var[vnf1_index_var[s]]
        sat_link_index[s][1] = vnf2_location_var[vnf2_index_var[vnf1_index_var[s]]]
        sat_link_index[s][2] = vnf3_location_var[vnf3_index_var[vnf2_index_var[vnf1_index_var[s]]]]
        sat_link_index[s][3] = ground_location_var[ground_index_var[vnf2_index_var[vnf1_index_var[s]]]]

        sat_link_index_for_ns3[s][0] = vnf1_index_var[s]
        sat_link_index_for_ns3[s][1] = vnf2_index_var[vnf1_index_var[s]]
        sat_link_index_for_ns3[s][2] = vnf3_index_var[vnf2_index_var[vnf1_index_var[s]]]
        sat_link_index_for_ns3[s][3] = ground_index_var[vnf2_index_var[vnf1_index_var[s]]]
    print(list(vnf2_index_var))
    print(list(vnf3_index_var))
    print(list(ground_index_var))
    print(list(np.argmin(delay_vnf1_vnf2_var.T, axis=0)))
    return sat_link_index,sat_link_index_for_ns3

def TransTime_PTime(LoadSat, delay, AMF_NUMBER, SMF_NUMBER, UPF_NUMBER, amf_location, smf_location, upf_location,
                    resource_sat,core_location_sat,sat_link_index):
    # 单位都是ms
    # 链路的时间都是 1ms
    # aaa = time.time()
    # delay_sat_vnf1_var = np.matmul(amf_location, delay)
    # delay_sat_vnf2_var = np.matmul(smf_location, delay)
    # delay_vnf1_vnf2_var = np.matmul(smf_location, delay_sat_vnf1_var.T)
    # delay_vnf2_vnf3_var = np.matmul(upf_location, delay_sat_vnf2_var.T)
    #
    # delay_ground_vnf2_var = np.matmul(core_location_sat, delay_sat_vnf2_var.T)
    #
    # # delay_sat_vnf1_min_var = np.min(delay_sat_vnf1_var, axis=0)
    # vnf1_index_var = np.argmin(delay_sat_vnf1_var, axis=0)
    # # delay_vnf1_vnf2__min_var = np.min(delay_vnf1_vnf2_var, axis=0)
    # vnf2_index_var = np.argmin(delay_vnf1_vnf2_var, axis=0)
    # # delay_vnf2_vnf3__min_var = np.min(delay_vnf2_vnf3_var, axis=0)
    # vnf3_index_var = np.argmin(delay_vnf2_vnf3_var, axis=0)
    #
    # ground_index_var = np.argmin(delay_ground_vnf2_var, axis=0)
    #
    # # 每个VNF部署节点
    # vnf1_location_var = np.argmax(amf_location, 1)
    # # print('vnf1_location_var',vnf1_location_var)
    # vnf2_location_var = np.argmax(smf_location, 1)
    # vnf3_location_var = np.argmax(upf_location, 1)
    # # print('vnf1_location_var', vnf1_location_var)
    # ground_location_var = np.argmax(core_location_sat, 1)
    #
    #
    # sat_link_index = np.zeros((delay.shape[0], 4)).astype(np.uint32)
    # # 消息路径
    # for s in range(delay.shape[0]):
    #     sat_link_index[s][0] = vnf1_location_var[vnf1_index_var[s]]
    #     sat_link_index[s][1] = vnf2_location_var[vnf2_index_var[vnf1_index_var[s]]]
    #     sat_link_index[s][2] = vnf3_location_var[vnf3_index_var[vnf2_index_var[vnf1_index_var[s]]]]
    #     sat_link_index[s][3] = ground_location_var[ground_index_var[vnf2_index_var[vnf1_index_var[s]]]]
    # print(vnf1_index_var[959])
    # print(vnf1_location_var[vnf1_index_var[959]])
    # print(sat_link_index[959][0])

    trass_time = np.zeros((delay.shape[0], 5))
    for s in range(delay.shape[0]):
        trass_time[s][0] = delay[s][sat_link_index[s][0]]
        trass_time[s][1] = delay[sat_link_index[s][0]][ sat_link_index[s][1]]
        trass_time[s][2] = delay[sat_link_index[s][1]][ sat_link_index[s][2]]
        trass_time[s][3] = delay[sat_link_index[s][1]][ sat_link_index[s][3]]
        # print(delay[s, sat_link_index[s][0]])
        # print('1111',sat_link_index[959][0])
    # print('compute time ok', time.time() - aaa)
    business_3 = np.zeros((delay.shape[0]))
    business_4 = np.zeros((delay.shape[0]))
    business_5 = np.zeros((delay.shape[0]))
    business_session = np.zeros((delay.shape[0]))
    Z = 0
    for s in range(delay.shape[0]):
        if LoadSat[s] !=0:
            business_3[s] = 2 * trass_time[s][0] + 2 * trass_time[s][1] + 2 * trass_time[s][2] + 2 * main.amf_process_time[
                sat_link_index[s][0]] \
                            + 2 * main.smf_process_time[sat_link_index[s][1]] + 1 * main.upf_process_time[
                                sat_link_index[s][2]]
            business_4[s] = 7 * trass_time[s][0] + 7 * main.amf_process_time[sat_link_index[s][0]] + 6 * \
                            trass_time[s][1] + \
                            5 * main.smf_process_time[sat_link_index[s][1]] + 4 * trass_time[s][
                                2] + 2 * main.upf_process_time[sat_link_index[s][2]]
            business_5[s] = 3 * trass_time[s][0] + 2 * trass_time[s][1] + 2 * trass_time[s][2] + 2 * main.amf_process_time[
                sat_link_index[s][0]] + \
                            2 * main.smf_process_time[sat_link_index[s][1]] + 1 * main.upf_process_time[
                                sat_link_index[s][2]]

            business_session[s] = 3 * trass_time[s][0] + 6 * trass_time[s][1] + 4 * trass_time[s][2] + 3 * \
                                  main.amf_process_time[sat_link_index[s][0]] + \
                                  5 * main.smf_process_time[sat_link_index[s][1]] + 2 * main.upf_process_time[
                                      sat_link_index[s][2]] + 2 * trass_time[s][3]

        if main.youzhuangtai:
            Z += LoadSat[s] * (0.743 * business_3[s] + 0.107 * business_4[s] + 0.1 * business_5[s] + 0.05 * (business_session[s]+4))
        else:
            Z += LoadSat[s] * (0.847 * business_3[s] + 0.003 * business_4[s] + 0.1 * business_5[s] + 0.05 * (business_session[s]+4) )
    return Z
