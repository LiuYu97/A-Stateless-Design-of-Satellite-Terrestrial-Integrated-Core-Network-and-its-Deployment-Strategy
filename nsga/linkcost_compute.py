import time
import random
import networkx as nx
import numpy as np
import main
import NF
def LinkCost(LoadSat, delay, hop, LINK_COST_3, LINK_COST_4, LINK_COST_5, amf_location, smf_location,
             upf_location,core_location_sat,sat_link_hop):
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
    # # hop_sat_vnf1_var = np.matmul(amf_location, hop)
    # # hop_sat_vnf2_var = np.matmul(smf_location, hop)
    # # hop_vnf1_vnf2_var = np.matmul(smf_location, hop_sat_vnf1_var.T)
    # # hop_vnf2_vnf3_var = np.matmul(upf_location, hop_sat_vnf2_var.T)
    # #
    # # hop_ground_vnf2_var = np.matmul(core_location_sat, hop_sat_vnf2_var.T)
    # # 每个VNF部署节点
    # # 每个VNF部署节点
    # vnf1_location_var = np.argmax(amf_location, 1)
    # # print('vnf1_location_var',vnf1_location_var)
    # vnf2_location_var = np.argmax(smf_location, 1)
    # vnf3_location_var = np.argmax(upf_location, 1)
    # # print('vnf1_location_var', vnf1_location_var)
    # ground_location_var = np.argmax(core_location_sat, 1)
    #
    # # sat_link_hop = np.zeros((delay.shape[0], 5))
    # # 0 sat-amf 1 amf-smf  2 smf-upf 3 smf-ground
    # sat_link_hop = np.zeros((delay.shape[0], 4)).astype(np.uint32)
    #
    # for s in range(delay.shape[0]):
    #     sat_link_hop[s][0] = vnf1_location_var[vnf1_index_var[s]]
    #     sat_link_hop[s][1] = vnf2_location_var[vnf2_index_var[vnf1_index_var[s]]]
    #     sat_link_hop[s][2] = vnf3_location_var[vnf3_index_var[vnf2_index_var[vnf1_index_var[s]]]]
    #     sat_link_hop[s][3] = ground_location_var[ground_index_var[vnf2_index_var[vnf1_index_var[s]]]]


    trass_hop = np.zeros((delay.shape[0], 5))
    for s in range(delay.shape[0]):
        trass_hop[s][0] = hop[s][sat_link_hop[s][0]]
        trass_hop[s][1] = hop[sat_link_hop[s][0]][sat_link_hop[s][1]]
        trass_hop[s][2] = hop[sat_link_hop[s][1]][sat_link_hop[s][2]]
        trass_hop[s][3] = hop[sat_link_hop[s][1]][sat_link_hop[s][3]] + 1


    business_3 = np.zeros((delay.shape[0]))
    business_4 = np.zeros((delay.shape[0]))
    business_5 = np.zeros((delay.shape[0]))
    business_session = np.zeros((delay.shape[0]))
    reliability_3 = np.zeros((delay.shape[0]))
    reliability_4 = np.zeros((delay.shape[0]))
    reliability_5 = np.zeros((delay.shape[0]))
    reliability_session = np.zeros((delay.shape[0]))
    Z = 0
    R = 0
    Z_3 = 0
    Z_4 = 0
    Z_5 = 0
    Z_s = 0
    for i in range(delay.shape[0]):
        if LoadSat[i] != 0:
            # reliability_3[i] = 0.999 ** (2 * trass_hop[i][0] + 2 * trass_hop[i][1] + 2 * trass_hop[i][2])
            # reliability_4[i] = 0.999 ** (7 * trass_hop[i][0] + 6 * trass_hop[i][1] + 4 * trass_hop[i][2])
            # reliability_5[i] = 0.999 ** (3 * trass_hop[i][0] + 2 * trass_hop[i][1] + 2 * trass_hop[i][2])
            # reliability_session[i] = 0.999 ** (
            #             3 * trass_hop[i][0] + 6 * trass_hop[i][1] + 4 * trass_hop[i][2] + 2 * trass_hop[i][3])
            reliability_3[i] = (2 * trass_hop[i][0] + 2 * trass_hop[i][1] + 2 * trass_hop[i][2])
            reliability_4[i] = (7 * trass_hop[i][0] + 6 * trass_hop[i][1] + 4 * trass_hop[i][2])
            reliability_5[i] = (3 * trass_hop[i][0] + 2 * trass_hop[i][1] + 2 * trass_hop[i][2])
            reliability_session[i] = (3 * trass_hop[i][0] + 6 * trass_hop[i][1] + 4 * trass_hop[i][2] + 2 * trass_hop[i][3])

            business_3[i] = LINK_COST_3[0] * trass_hop[i][0] + \
                            LINK_COST_3[1] * trass_hop[i][1] + \
                            LINK_COST_3[2] * trass_hop[i][2] + \
                            LINK_COST_3[3] * trass_hop[i][2] + \
                            LINK_COST_3[4] * trass_hop[i][1] + \
                            LINK_COST_3[5] * trass_hop[i][0]
            business_4[i] = LINK_COST_4[0] * trass_hop[i][0] + \
                            LINK_COST_4[1] * trass_hop[i][1] + \
                            LINK_COST_4[2] * trass_hop[i][1] + \
                            LINK_COST_4[3] * trass_hop[i][0] + \
                            LINK_COST_4[4] * trass_hop[i][0] + \
                            LINK_COST_4[5] * trass_hop[i][1] + \
                            LINK_COST_4[6] * trass_hop[i][2] + \
                            LINK_COST_4[7] * trass_hop[i][2] + \
                            LINK_COST_4[8] * trass_hop[i][1] + \
                            LINK_COST_4[9] * trass_hop[i][0] + \
                            LINK_COST_4[10] * trass_hop[i][0] + \
                            LINK_COST_4[11] * trass_hop[i][1] + \
                            LINK_COST_4[12] * trass_hop[i][2] + \
                            LINK_COST_4[13] * trass_hop[i][2] + \
                            LINK_COST_4[14] * trass_hop[i][1] + \
                            LINK_COST_4[15] * trass_hop[i][0] + \
                            LINK_COST_4[16] * trass_hop[i][0]
            business_5[i] = LINK_COST_5[0] * trass_hop[i][0] + \
                            LINK_COST_5[1] * trass_hop[i][1] + \
                            LINK_COST_5[2] * trass_hop[i][2] + \
                            LINK_COST_5[3] * trass_hop[i][2] + \
                            LINK_COST_5[4] * trass_hop[i][1] + \
                            LINK_COST_5[5] * trass_hop[i][0] + \
                            LINK_COST_5[6] * trass_hop[i][0]
            business_session[i] = \
                            main.LINK_COST_6[0] * trass_hop[i][0] + \
                            main.LINK_COST_6[1] * trass_hop[i][1] + \
                            main.LINK_COST_6[2] * trass_hop[i][3] + \
                            main.LINK_COST_6[3] * trass_hop[i][3] + \
                            main.LINK_COST_6[4] * trass_hop[i][1] + \
                            main.LINK_COST_6[5] * trass_hop[i][2] + \
                            main.LINK_COST_6[6] * trass_hop[i][2] + \
                            main.LINK_COST_6[7] * trass_hop[i][1] + \
                            main.LINK_COST_6[8] * trass_hop[i][1] + \
                            main.LINK_COST_6[9] * trass_hop[i][0] + \
                            main.LINK_COST_6[10] * trass_hop[i][0] + \
                            main.LINK_COST_6[11] * trass_hop[i][1] + \
                            main.LINK_COST_6[12] * trass_hop[i][2] + \
                            main.LINK_COST_6[13] * trass_hop[i][2] + \
                            main.LINK_COST_6[14] * trass_hop[i][1]

        if main.youzhuangtai:
            Z += LoadSat[i] * (0.743 * business_3[i] + 0.107 * business_4[i] + 0.1 * business_5[i]+ 0.05 * business_session[i])
            R += LoadSat[i] * (0.743 * reliability_3[i] + 0.107 * reliability_4[i] + 0.1 * reliability_5[i] + 0.05 *
                               reliability_session[i])
        else:
            if main.ground_CN:
                business_3[i] = business_3[i] + LINK_COST_3[0] + LINK_COST_3[5]
                business_4[i] = business_4[i] + LINK_COST_4[0]+ LINK_COST_4[9] + LINK_COST_4[15] + LINK_COST_4[16]
                business_5[i] = business_5[i] + LINK_COST_5[0] + LINK_COST_5[5] + LINK_COST_5[6]
                business_session[i] = business_session[i] + main.LINK_COST_6[0] + main.LINK_COST_6[9] +main.LINK_COST_6[10]+ main.LINK_COST_6[2] +main.LINK_COST_6[3]

            Z += LoadSat[i] * (0.847 * business_3[i] + 0.003 * business_4[i] + 0.1 * business_5[i] + 0.05 * business_session[i])
            R += LoadSat[i] * (0.847 * reliability_3[i] + 0.003 * reliability_4[i] + 0.1 * reliability_5[i] + 0.05 *
                               reliability_session[i])
            Z_3 += LoadSat[i] * business_3[i]
            Z_4 += LoadSat[i] * business_4[i]
            Z_5 += LoadSat[i] * business_5[i]
            Z_s += LoadSat[i] * business_session[i]

    return Z, R,Z_3,Z_4,Z_5,Z_s
