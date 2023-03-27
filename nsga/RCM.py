import queue
import time
import threading
import  random
import matplotlib.pyplot as plt
import numpy as np
import  copy
# 场景分析
# UE3的行为。但是UE3切换的时间点可能在更新上下文后，这个比较简单，也可能在更新上下文前，这样就需要等待。
# 一个线程，发送请求
# 发送信令，可能切换，也可能 不是切换，但是我关注的是切换。用户发生切换后就不再发起信令，因为网元已经切换，其他信令正常执行就行了。
# 所以个应该一个用户一个线程。
# AMF可能会宕机。宕机后网元上下文全部丢失。假设网元宕机后会在周围卫星立马启动新网元。用户在新网元处完成重新接入。重新接入会花费很长的时间。时间是多少。

# UE最少间隔多长时间产生一次信令。
# 然后每次random是否信令，以及那哪种信令。
# 一共多少个ue

# 每秒切换用户数



# AMF数量与AMF之间传输时间挂钩，也就与有状态完成时间挂钩
# 无状态不依赖于网元数量

ue_number_per_second = 100
total_second = 10
us_state = {}
def Client(user_per_second):
    index = 0

    while True:


        # for i in range(100):
        message = str(index)+"-"+"handover" +"-"+ str(time.time())
        gnb_amf.put(message)
        time.sleep(0.001)
        index = index + 1
        # for i in range(index, 1000):
        #     if random.random() > 0.7:
        #         us_state[i] = 'modify'
        #         client_udsf.put(str(i)+"-"+"modify")
        #     else:
        #         us_state[i] = 'initial'
        # if time.time()-start_time >10:
        if index > 600:
            gnb_amf.put("over")
            break




def Client_receive():

    while True:
        aa = amf_gnb.get()
        if aa=='over':
            break
        ue_index = aa.split('-')[0]
        print(aa)
        ue_procedure_time = time.time() - float(aa.split('-')[2])
        time_of_each_ue.append(ue_procedure_time)
        print(ue_procedure_time)

    print(time_of_each_ue)
    global program_over
    program_over = 1
    all_ue_complete_time_span = time.time()-start_time
    print('all_ue_complete_time_span',all_ue_complete_time_span)
    print('mean_ue_complete_time', sum(time_of_each_ue)/len(time_of_each_ue))
    # np.savetxt('time_of_each_ue',np.array(time_of_each_ue))

# 一个线程，模拟有状态AFM。接受请求，发送response
# 等待时间根据AMF数量不同而不同

def Stateful_AMF():
    while True:
        aa=gnb_amf.get()
        if aa=='over':
            amf_gnb.put('over')
            break
        index  = aa.split('-')[0]
        print(aa)
        # time.sleep(float(random.uniform(1 ,  3)/1000))
        time.sleep(AMF_AMF_time)
        message_amf_gnb = str(index) +"-"+ 'response'+"-"+aa.split('-')[2]
        amf_gnb.put(message_amf_gnb)
        # print(aa)


# 一个线程，模拟无状态AMF。接受请求，如果没有过向UDSF获取
def Stateless_AMF():

    while True:
        aa=gnb_amf.get()
        if aa=='over':
            amf_gnb.put('over')
            break

        index  = aa.split('-')[0]
        if index in local_context:
            print('ue in Stateless_AMF')
            # time.sleep(float(1/1000))
            message_amf_gnb = str(index) + "-" + 'response' + "-" + aa.split('-')[2]
            amf_gnb.put(message_amf_gnb)
        else:
            print('ue not in Stateless_AMF')
            should_but_no_response.append(index)
            should_but_no_response.append(aa.split('-')[2])
            message_amf_udsf = str(index) + "-" + 'context_request' + "-" + aa.split('-')[2]
            amf_udsf.put(message_amf_udsf)

def Stateless_AMF_receive():
    while True:

        aa = udsf_amf.get()
        print('AMF reveive request from UDSF')
        for i in aa:
            local_context[i.split('-')[0]] = time.time()
        print('AMF send response to gNB')
        for _ in range(int(len(should_but_no_response)/2)):
            if str(should_but_no_response[0]) in local_context:
                amf_gnb.put(str(should_but_no_response[0]) + "-" + 'response' + "-" + should_but_no_response[1])
                should_but_no_response.pop(0)
                should_but_no_response.pop(0)


# 一个线程，模拟UDSF
def UDSF():
    yifasongfangwei = 0
    while True:

        aa = amf_udsf.get()
        if yifasongfangwei > int(aa.split('-')[0]):
            print('UDSF reveive request, but UDSF ignore')

        else:
            first = 0
            time.sleep(0.226)
            print('UDSF reveive request')
            message_udsf_amf = []
            # message_udsf_amf.append(str(aa.split('-')[0]) + "-" + 'context_response'+ "-" +  aa.split('-')[2])
            yifasongfangwei = int(aa.split('-')[0]) + 100
            for i in range(int(aa.split('-')[0]),yifasongfangwei):
                message_udsf_amf.append(str(i) + "-" + 'context_response')

            print('UDSF rsend response')
            udsf_amf.put(message_udsf_amf)


# 变量-每秒用户请求数。
# 持续时间不算变量，10s吧
start_time = time.time()
gnb_amf = queue.Queue()
amf_gnb = queue.Queue()
amf_udsf = queue.Queue()
udsf_amf = queue.Queue()

client_udsf = queue.Queue()

time_of_each_ue = []
local_context = {}
should_but_no_response = []
AMF_AMF_time = 0.010 # 单位 S
other_procedure = {}
program_over = 0
if __name__ == '__main__':
    # gnb-amf
    thread = threading.Thread(target=Client,args=(4000,))
    thread.start()
    thread = threading.Thread(target=Client_receive)
    thread.start()
    # thread = threading.Thread(target=Stateful_AMF)
    # thread.start()
    thread = threading.Thread(target=Stateless_AMF)
    thread.start()
    thread = threading.Thread(target=Stateless_AMF_receive)
    thread.start()
    thread = threading.Thread(target=UDSF)
    thread.start()

    while True:
        if program_over == 1:
            plt.scatter([i for i in range(len(time_of_each_ue))], time_of_each_ue)

            plt.show()
            break
        else:
            time.sleep(1)
            print('-----------------------program_over,',program_over)

    # UDSF
    # 有状态AMF
    # 客户端