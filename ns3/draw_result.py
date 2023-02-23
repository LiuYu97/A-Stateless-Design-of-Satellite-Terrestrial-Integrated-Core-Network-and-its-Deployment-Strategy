
import matplotlib.pyplot as plt
import numpy as np
import math



def compute(rate,queue,type,is_ground):
    success_rate_xn = []
    delay_xn = []
    for i in range(12):
        Plan_packets = np.loadtxt('../stk_compute/sat_load/Sat_load' + str(i) + '.txt').T.reshape(1, -1)[0]
        Plan_packets = [int(i / 100000) for i in Plan_packets]
        data = []
        file = open('result/' + str(i) + '-' + str(rate) + '-' + str(queue) +'-' + str(type) + "-" + str(is_ground) + '.txt', 'r')  #打开文件
        file_data = file.readlines() #读取所有行
        for row in file_data:
            tmp_list = row.split('; ')
            data.append(tmp_list) #将每行数据插入data中
        # print(len(data[0]))

        client_time = [[] for i in range(960)]
        for i in data[0]:
            if len(i)>4:
                client_time[int(i.split('+')[0])].append(float(i.split('+')[1][:-2]))

        Receive_packets = [len(i) for i in client_time]
        Success_rate = [0 for i in range(960)]
        for i in range(960):
            if Plan_packets[i] > 0:
                Success_rate[i] = Receive_packets[i] / Plan_packets[i]
        meam_Success_rate = 0
        for i in range(960):
            meam_Success_rate += Success_rate[i] * (Plan_packets[i] / sum(Plan_packets))

        print(meam_Success_rate)
        # print("收到总包数 = ", sum(Receive_packets))

        Average_delay = [0 for i in range(960)]
        for i in range(960):
            if len(client_time[i]) > 0:
                Average_delay[i] = sum(client_time[i]) / len(client_time[i])
        # print(Average_delay)
        mean_Average_delay = 0
        Number_of_receive = sum(Receive_packets)
        for i in range(960):
            mean_Average_delay += Average_delay[i] * (Receive_packets[i] / Number_of_receive)
        # print(mean_Average_delay)
        delay_xn.append(mean_Average_delay) , success_rate_xn.append(min(meam_Success_rate,1))
    return sum(delay_xn)/12,sum(success_rate_xn)/12

rate = [5000,2000,700]
queue = [10000,5000]
delay = {}
packet_loss = {}
for i in rate:
    for j in queue:
        for m in range(4):
            for k in range(2):
                a,b = compute(i,j,m,k)
                aa = str(i) + '-' + str(j) + '-' + str(m) +'-' + str(k)
                delay[aa] = a
                packet_loss[aa] = b

# packet_loss_bar_nsga = []
# packet_loss_bar_ground = []
# for i in rate:
#     for j in queue:
#         for m in range(4):
#             packet_loss_bar_nsga.append(packet_loss[str(i)+'-'+str(j)+'-' + str(m) + "-0"])
#             packet_loss_bar_ground.append(packet_loss[str(i)+'-'+str(j)+'-' + str(m) + "-1"])
# print(packet_loss_bar_nsga)
# print(packet_loss_bar_ground)

# x_width = range(0,1)


x = [i for i in range(12)]
x_label = ['NSGA', 'Ground']
width = 0.4
fig, ax = plt.subplots(2, 4, sharex=True)

for i in range(2):
    for j in range(4):
        ax[i,j].tick_params(axis='x', labelsize=6, direction='in')
        ax[i, j].tick_params(axis='y', labelsize=6, direction='in')
        # ax[i, j].set_yticks([])
        # ax[i, j].xaxis.set_visible(False)
        if i ==0:
            # ax[i, j].set_ylim(10,100)
            ax[i, j].bar(np.arange(len(x_label)) - 1.5 * width,
                [delay["5000-10000-" + str(j) + "-0"], delay["5000-10000-" + str(j) + "-1"]], width, )
            ax[i, j].bar(np.arange(len(x_label)) - 0.5 * width,
                         [delay["2000-10000-" + str(j) + "-0"], delay["2000-10000-" + str(j) + "-1"]], width, )
            ax[i, j].bar(np.arange(len(x_label)) + 0.5 * width,
                         [delay["2000-5000-" + str(j) + "-0"], delay["2000-5000-" + str(j) + "-1"]], width, )
            ax[i, j].bar(np.arange(len(x_label)) + 1.5 * width,
                         [delay["5000-5000-" + str(j) + "-0"], delay["5000-5000-" + str(j) + "-1"]], width, )
            ax[i, j].bar(np.arange(len(x_label)) + 2.5 * width,
                         [delay["700-10000-" + str(j) + "-0"], delay["700-10000-" + str(j) + "-1"]], width, )
            ax[i, j].bar(np.arange(len(x_label)) + 3.5 * width,
                         [delay["700-5000-" + str(j) + "-0"], delay["700-5000-" + str(j) + "-1"]], width, )
            # ax[i, j].plot(x, delay["5000-10000-" + str(j) + "-0"], color='red')
            # ax[i, j].plot(x, delay["5000-10000-" + str(j) + "-1"], color='blue')
            # ax[i, j].plot(x, delay["2000-10000-" + str(j) + "-0"], color='tomato')
            # ax[i, j].plot(x, delay["2000-10000-" + str(j) + "-1"], color='cornflowerblue')
            # ax[i, j].plot(x, delay["5000-5000-" + str(j) + "-0"], color='tomato')
            # ax[i, j].plot(x, delay["5000-5000-" + str(j) + "-1"], color='cornflowerblue')

        if i ==1:
            # ax[i, j].set_ylim(-0.05, 0.5)
            # ax[i, j].plot(x, delay["5000-10000-" + str(j) + "-0"], color='red')
            # ax[i, j].plot(x, delay["5000-10000-" + str(j) + "-1"], color='blue')
            # ax[i, j].plot(x, delay["2000-10000-" + str(j) + "-0"], color='red')
            # ax[i, j].plot(x, delay["2000-10000-" + str(j) + "-1"], color='blue')
            #
            # ax[i, j].plot(x, delay["2000-5000-" + str(j) + "-0"], color='tomato')
            # ax[i, j].plot(x, delay["2000-5000-" + str(j) + "-1"], color='cornflowerblue')
            ax[i, j].set_ylim(0.5, 1.09)
            ax[i, j].bar(np.arange(len(x_label)) - 1.5 * width,
                [packet_loss["5000-10000-" + str(j) + "-0"], packet_loss["5000-10000-" + str(j) + "-1"]], width, )
            ax[i, j].bar(np.arange(len(x_label)) - 0.5 * width,
                 [packet_loss["2000-10000-" + str(j) + "-0"], packet_loss["2000-10000-" + str(j) + "-1"]], width, )
            ax[i, j] .bar(np.arange(len(x_label)) + 0.5 * width,
                 [packet_loss["2000-5000-" + str(j) + "-0"], packet_loss["2000-5000-" + str(j) + "-1"]], width, )
            ax[i, j] .bar(np.arange(len(x_label)) + 1.5 * width,
                 [packet_loss["5000-5000-" + str(j) + "-0"], packet_loss["5000-5000-" + str(j) + "-1"]], width, )
            ax[i, j].bar(np.arange(len(x_label)) + 2.5 * width,
                         [packet_loss["700-10000-" + str(j) + "-0"], packet_loss["700-10000-" + str(j) + "-1"]], width, )
            ax[i, j].bar(np.arange(len(x_label)) + 3.5 * width,
                         [packet_loss["700-5000-" + str(j) + "-0"], packet_loss["700-5000-" + str(j) + "-1"]], width, )

ax[0,0].set_ylabel('Delay')
ax[1,0].set_ylabel('Packet Loss')
ax[1,0].set_xlabel('Time slot')
ax[1,1].set_xlabel('Time slot')
ax[1,2].set_xlabel('Time slot')
ax[1,3].set_xlabel('Time slot')
plt.tight_layout()
plt.show()



# fig, ax = plt.subplots(1, 4)
# for j in range(4):
#
#     ax[j].set_xlabel('Time slot')
#     ax[j].bar(np.arange(len(x_label))- 1.5*width, [packet_loss["5000-10000-" + str(j) + "-0"], packet_loss["5000-10000-" + str(j) + "-1"]],width,)
#     ax[j].bar(np.arange(len(x_label))- 0.5*width, [packet_loss["2000-10000-" + str(j) + "-0"], packet_loss["2000-10000-" + str(j) + "-1"]],width,)
#     ax[j].bar(np.arange(len(x_label)) + 0.5 * width, [packet_loss["2000-5000-" + str(j) + "-0"], packet_loss["2000-5000-" + str(j) + "-1"]],width,)
#     ax[j].bar(np.arange(len(x_label)) + 1.5 * width, [packet_loss["5000-5000-" + str(j) + "-0"], packet_loss["5000-5000-" + str(j) + "-1"]],width,)
    # ax[j].set_xticks(np.arange(len(x_label)), labels=x_label)



# ax[0,0].plot(x, delay["5000-10000-0-0"], color='red')
# ax[0,0].plot(x, delay["5000-10000-0-1"], color='blue')

# plt.tight_layout()
# plt.show()
# fig=plt.figure()
# plt.rcParams['xtick.direction'] = 'in'  # 将x周的刻度线方向设置向内
# plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度方向设置向内
# # plt.rcParams['axes.labelsize'] = 16  # xy轴label的size
# # plt.rcParams['xtick.labelsize'] = 12  # x轴ticks的size
# # plt.rcParams['ytick.labelsize'] = 14  # y轴ticks的size
# # plt.rcParams['legend.fontsize'] = 12  # 图例的size
#
# ax1=fig.add_subplot(241)
#
# # ax1.set_ylim(0, 100)
#
# # plt.tick_params(axis='both',which='major',labelsize=14)
# ax1.set_xlabel('Time slot', fontsize=15, fontweight='bold')
# plt.xticks(x,x, color='black')
#
# ax1.
# ax1.plot(x, delay_xn_ground_5000_10000, color='green')
# ax1.set_xticklabels(ax1.get_xticklabels())  # 设置共用的x轴
#
#
# # 设置右侧Y轴对应的figure
# ax2=fig.add_subplot(122)
# ax2.set_ylabel('Success Rate', color='blue')
# ax2.set_ylim(-0.1, 1)
# ax2.set_xlabel('Time slot', fontsize=15, fontweight='bold')
# plt.xticks(x,x, color='black')
# ax2.plot(x, success_rate_xn_nsga_5000_10000, color='blue')
# ax2.plot(x, success_rate_xn_ground_5000_10000, color='green')
# plt.show()



#
# plt.rcParams['xtick.direction'] = 'in'#将x周的刻度线方向设置向内
# plt.rcParams['ytick.direction'] = 'in'#将y轴的刻度方向设置向内
# plt.tick_params(top='on', right='on', which='both')
# plt.grid()# 设置xtick和ytick的方向：in、out、inout
# # plt.plot(x, result_24_time, color="fuchsia", linestyle='solid',label='Svenario 3', linewidth=1, marker='P',markerfacecolor='none',markersize='5',)
# plt.plot(x, ground_tptime, color="red", linestyle='solid',label='Svenario 5', linewidth=1, marker='o',markerfacecolor='none',markersize='5',)
# plt.plot(x, nsga_tptime, color="blue", linestyle='solid', label='Svenario 1', linewidth=1, marker='^',markerfacecolor='none',markersize='5',)
# # plt.plot(x, nsga_tptime2, color="green", linestyle='solid', label='Svenario 4', linewidth=1, marker="s",markerfacecolor='none',markersize='5',)
# # plt.plot(x, kmeans_tptime, color="darkorange", linestyle='solid', label='Svenario 2', linewidth=1, marker="x",markerfacecolor='none',markersize='5',)
# # plt.ylim(2300, 11500)
# plt.xlabel('Time Solt', fontsize=15)
# plt.ylabel('Average Communication Overheads', fontsize=15)
# plt.legend(loc='upper center', ncol=3, markerscale=2.5, fontsize=11)
# plt.show()
# # plt.ylim(50, 330)
# # plt.xlabel('Time Slot', fontsize=15)
# # plt.ylabel('Average CPP delay(ms)', fontsize=15)
# # plt.legend(loc='upper center', ncol=3, markerscale=2.5, fontsize=11)
# # plt.show()
# #
# # plt.rcParams['xtick.direction'] = 'in'  # 将x周的刻度线方向设置向内
# # plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度方向设置向内
# # plt.tick_params(top='on', right='on', which='both')
# # plt.grid()
# plt.plot(x, ground_linkcost, color="fuchsia", linestyle='solid', label='Svenario 3', linewidth=1, marker='o',
#          markerfacecolor='none', markersize='5', )
# plt.plot(x, nsga_linkcost, color="blue", linestyle='solid', label='Svenario 5', linewidth=1, marker='o',
#          markerfacecolor='none', markersize='5', )
# # plt.plot(x, nsga_linkcost2, color="blue", linestyle='solid', label='Svenario 1', linewidth=1, marker='H',
# #          markerfacecolor='none', markersize='5', )
# # plt.plot(x, kmeans_linkcost_rccmm, color="green", linestyle='solid', label='Svenario 4', linewidth=1, marker="s",
# #          markerfacecolor='none', markersize='5', )
# # plt.plot(x, kmeans_linkcost, color="darkorange", linestyle='solid', label='Svenario 2', linewidth=1, marker="s",
# #          markerfacecolor='none', markersize='5', )
# plt.show()
#
#
# plt.plot(x, ground_rel, color="darkorange", linestyle='solid', alpha=0.3, linewidth=1,markerfacecolor='none',markersize='5',)
# plt.plot(x, nsga_rel, color="blue", linestyle='solid', alpha=0.3, linewidth=1,markerfacecolor='none',markersize='5',)
#
#
# plt.xlabel('Time Solt', fontsize=15)
# plt.ylabel('Average CPP Reliability', fontsize=15)
# plt.legend(loc='upper center',ncol=3,markerscale=2.5,fontsize=11)
# plt.show()