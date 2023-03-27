import subprocess
import json
import os
import threading
import time


def run_ns3(slot,rate,queue,packet_number,packet_interval,procedure_type,is_ground):
    target_file_name = "/home/ubuntu/firstarticle/result/"
    target_file_name = target_file_name + str(slot) +"-"+ str(rate) +"-"+ str(queue)+"-"+ str(packet_number)+"-"+ str(packet_interval) +"-"+ str(procedure_type) +"-"+ str(is_ground)+".txt"
    command = "scratch/XnNsag.cc --slot="
    command = command + str(slot) + " --rate=" + str(rate) +" --queue=" + str(queue) + " --procedure_type=" + str(procedure_type) + " --is_ground=" + str(is_ground) + " --target_file_name=" + "\""+target_file_name + "\""
    command = command +" --packet_number=" + str(packet_number) + " --packet_interval=" + str(packet_interval)
    command = './waf --run '+"\"" + command +"\""+ "  2>&1 &"
    print(command)
    run_status = os.system('echo %s | sudo -S %s' % ("123",command))


def fourProcedure(rate,queue,packet_number,packet_interval,is_ground):
    for i in range(12):
        slot = i
        run_ns3(slot,rate,queue,packet_number,packet_interval,0,is_ground)
        time.sleep(wait_time)
    for i in range(12):
        slot = i
        run_ns3(slot,rate,queue,packet_number,packet_interval,1,is_ground)
        time.sleep(wait_time)
    for i in range(12):
        slot = i
        run_ns3(slot,rate,queue,packet_number,packet_interval,2,is_ground)
        time.sleep(wait_time)
    for i in range(12):
        slot = i
        run_ns3(slot,rate,queue,packet_number,packet_interval,3,is_ground)
        time.sleep(wait_time)


wait_time = 80
if __name__ == '__main__':
    slot = 8
    rate = [1000]
    queue = [5000]
    packet_number = [100000]
    packet_interval = [0.0001, 0.000067, 0.00005, 0.00004, 0.000033, 0.0000285, 0.000025]
    for i in rate:
        for j in queue:
            for q in packet_number:
                for p in packet_interval:
                    is_ground = 0
                    fourProcedure(i,j,q,p,is_ground)

                    is_ground = 1
                    fourProcedure(i,j,q,p,is_ground)
    # rate = [50]
    # queue = [1000,3000,5000]
    # packet_number = [100000]
    # packet_interval = [0.001]
    # for i in rate:
    #     for j in queue:
    #         for q in packet_number:
    #             for p in packet_interval:
    #                 is_ground = 0
    #                 fourProcedure(i,j,q,p,is_ground)

    #                 is_ground = 1
    #                 fourProcedure(i,j,q,p,is_ground)

    


    # run_ns3(slot,rate,queue,3,0)
    # time.sleep(2)
    # run_ns3(slot,rate,queue,3,1)
    # time.sleep(2)

    # run_ns3(slot,rate,queue,2,0)
    # time.sleep(2)
    # run_ns3(slot,rate,queue,2,1)
    # time.sleep(2)

    # run_ns3(slot,rate,queue,1,0)
    # time.sleep(2)
    # run_ns3(slot,rate,queue,1,1)
    # time.sleep(2)

    # run_ns3(slot,rate,queue,0,0)
    # time.sleep(2)
    # run_ns3(slot,rate,queue,0,1)
    # time.sleep(2)

    print("okk")




#     command = "scratch/XnNsag.cc --slot=" + str(slot) + " --rate=" + str(rate) +" --queue=" + str(queue) + " --procedure_type=" + str(procedure_type) + " --is_ground=" + str(is_ground)
#     command = './waf --run '+"\"" + command +"\""
#     print(command)
#     run_status = os.system('echo %s | sudo -S %s' % ("123",command))
#     filename = str(slot) +"-"+ str(rate) +"-"+ str(queue) +"-"+ str(procedure_type) +"-"+ str(is_ground)+".txt"
#     if run_status == 0:
#         subprocess.Popen("cp /home/ubuntu/firstarticle/result_delay_of_client.txt /home/ubuntu/firstarticle/result/" +filename, stdout=subprocess.PIPE, shell=True)

# #函数 将得到的保存时延的二位列表写到文件中
# def Save_list(list1,filename):
#     file2 = open(filename + '.txt','w')
#     for i in range(len(list1)):
#         for j in range(len(list1[i])):
#             file2.write(str(list1[i][j]))
#             file2.write('\t')
#         file2.write('\n')
#     file2.close()

# #完成读取c++输出并保存到二位列表在写入文件
# screen_str = subprocess.Popen("./waf --run scratch/liuyu_distribute_ground.cc", stdout=subprocess.PIPE, shell=True)

# #screen_str.wait()

# string = screen_str.stdout.read()
# print(string)
# split_string = string.split()

# #创建一个空的内含有80个空列表的二位列表
# delay = [[] for i in range(80)]

# for d in split_string:
#     s = d.decode("utf-8")
#     if s[0]=="N":
#         index1 = s.find("Number")
#         index2 = s.find("Client")
#         delay[int(s[index1+6:index2])].append(float(s[index2+6:-2]))
#         print(delay[int(s[index1+6:index2])])
# print(delay)
# Save_list(delay,'delay')

# each_average_delay = [0 for i in range(80)]
# each_packet_num = [0 for i in range(80)]
# each_packet_loss = [0 for i in range(80)]
# for i in range(80):
#     if(delay[i]==[]):
#         continue
#     sum = 0.0
#     capacity = 0
#     for j in delay[i]:
#         sum += j
#         capacity += 1
#     each_average_delay[i] = sum/capacity
#     each_packet_num[i] = capacity
# print(each_average_delay)

# all_average_delay = 0
# all_average_loss = 0

# n = 0
# for i in range(8):
#     for j in range(10):
#         if(Sat_load[j][i]!=0):
#             all_average_delay += each_average_delay[n] * (Sat_load[j][i]/total_load)
#             each_packet_loss[n] = (Sat_load[j][i]-each_packet_num[n])/Sat_load[j][i]
#             all_average_loss += each_packet_loss[n] * (Sat_load[j][i]/total_load)
#         else:
#             each_packet_loss[n] = -1
#         n += 1
# print(each_packet_loss)
# print(all_average_delay)
# print(all_average_loss)
    

        

