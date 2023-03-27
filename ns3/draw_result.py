import matplotlib.pyplot as plt
import numpy as np
import math
import brewer2mpl

import matplotlib.patches as mpatches

print([1  for std in range(1,4)])
# capital 23800
nsga_linkcostXn = [2046.9191049002684, 1730.854582991454, 1813.9345895803833, 2020.3550137653563, 1913.3155087997816, 1914.568469672709, 1806.4488407791584, 1950.0725044339363, 1858.9925235870867, 2005.9649157634221, 1842.2251042149196, 1834.3697625790726]
nsga_linkcostN2 = [15326.057088411633, 12517.209417432032, 13805.817253106408, 17833.589236552292, 16341.327246261731, 14418.988406410856, 14555.344431505404, 15064.55077163362, 15019.188683489692, 17645.198501872663, 14185.490253424203, 12928.377094306637]
nsga_linkcostSr = [4801.030661532152, 3944.277692490943, 4342.900355966066, 5550.616436361701, 5096.5904724097, 4524.878915814117, 4554.2822226339, 4734.255989093871, 4702.15910865274, 5491.30034012249, 4455.030172698995, 4108.199319763914]
nsga_linkcostSe = [9122.194449958328, 8402.667240147159, 8838.828831928444, 9172.154410207544, 9000.907873494776, 9186.460633412296, 10681.551926741453, 11266.298051724663, 10120.607905148801, 9947.47216156484, 9358.515781115608, 9102.18006405334]

# 7900
nsga_linkcostXn_2 = [2743.3293898130055, 2232.0893306159132, 2417.9946671254093, 4318.21966327828, 3776.000939526269, 3237.3222250162094, 2618.544569129788, 2588.9463694840715, 2802.625530957643, 4042.1299479890595, 2584.586329649975, 2793.8219607739265]
nsga_linkcostN2_2 = [26950.04377572236, 20957.43247928854, 24009.513345419407, 47062.34214845408, 38017.997578404174, 38269.98399925891, 21123.172281918185, 24446.333880403417, 28359.29386934136, 39527.89393999553, 25969.90009925226, 28922.90578597705]
nsga_linkcostSr_2 = [8327.038032474498, 6497.613430030985, 7423.699546110172, 14456.223634053365, 11712.577266110899, 11746.98070382088, 6577.142097183988, 7567.200227651734, 8752.628799407194, 12183.942232103716, 8027.529530867465, 8920.370027262397]
nsga_linkcostSe_2 = [11137.609723821237, 9182.46609406844, 10304.143683256365, 17339.054505506127, 14890.083353182485, 12782.684140870078, 12831.137902286664, 12715.993991052785, 11584.63096955182, 15915.787377086022, 10226.902865083062, 11630.960284269868]


ground_linkcostXn = [2009.6786824936712, 2069.1273259045606, 2155.526922415268, 2117.520912748833, 2026.568744210673, 2158.2142034701355, 3565.755425576966, 3616.632038012571, 3075.176483042439, 2462.4199785603664, 2351.1058691192984, 2187.022643656865]
ground_linkcostN2 = [34265.357603186676, 35278.966914586694, 36752.09448318756, 36104.085662854806, 34553.33597988617, 36797.91307455102, 60796.726286258716, 61664.18103608005, 52432.27327943258, 41984.67241037035, 40086.74823000068, 37289.10179719964]
ground_linkcostSr = [10391.181415167966, 10698.564701834342, 11145.299739311096, 10948.787060567529, 10478.512637289925, 11159.194510250252, 18436.982902815984, 18700.043915610033, 15900.410845430206, 12732.111327272027, 12156.554092503153, 11308.150525396477]
ground_linkcostSe = [4655.554699802821, 4780.0190836664115, 4960.909208802535, 4881.338098263442, 4690.916501257105, 4966.535422649847, 7913.427747194582, 8019.945337109897, 6886.329359145707, 5603.434470163181, 5370.382187520678, 5026.850083375256]
# def draw_24_time(result_24_time):


print([sum(ground_linkcostXn)/12, sum(nsga_linkcostXn)/12,sum(nsga_linkcostXn_2)/12])
print([sum(ground_linkcostSr)/12, sum(nsga_linkcostSr)/12, sum(nsga_linkcostSr_2)/12])
print([sum(ground_linkcostN2)/12, sum(nsga_linkcostN2)/12, sum(nsga_linkcostN2_2)/12])

print([sum(ground_linkcostSe)/12, sum(nsga_linkcostSe)/12, sum(nsga_linkcostSe_2)/12])
fig = plt.figure(figsize=(9.5,3.5))

# 参照下方配色方案，第三参数为颜色数量，这个例子的范围是3-12，每种配色方案参数范围不相同
bmap = brewer2mpl.get_map('Set2', 'qualitative', 6)
labels = ['B-P','P-S','C-S']
x = np.arange(len(labels))/2
# colors = bmap.mpl_colors
colors = [(22/255, 6/255, 138/255),(236/255, 120/255, 83/255),(253/255, 179/255, 46/255)]
width = 0.3
plt.subplot(141)
plt.tick_params(axis='x', labelsize=6, direction='in')
plt.tick_params(axis='y', labelsize=6, direction='in')
plt.tick_params(top='on', right='on', which='both')
plt.grid(linestyle='-.',zorder=0)
plt.xticks(x, labels, fontsize=11)
plt.ylabel('Xn-Based handover overhead', fontsize=13)
plt.bar(x, [sum(ground_linkcostXn)/12, sum(nsga_linkcostXn)/12,sum(nsga_linkcostXn_2)/12], width,color = colors,zorder=10)
plt.subplot(142)
plt.ylabel('Service request overhead', fontsize=13)
plt.tick_params(axis='x', labelsize=6, direction='in')
plt.tick_params(axis='y', labelsize=6, direction='in')
plt.tick_params(top='on', right='on', which='both')
plt.grid(linestyle='-.',zorder=0)
plt.bar(x,[sum(ground_linkcostSr)/12, sum(nsga_linkcostSr)/12, sum(nsga_linkcostSr_2)/12], width,color = colors,zorder=10)
plt.xticks(x, labels, fontsize=11)
plt.subplot(143)
plt.ylabel('N2-Based handover overhead', fontsize=13)
plt.tick_params(axis='x', labelsize=6, direction='in')
plt.tick_params(axis='y', labelsize=6, direction='in')
plt.tick_params(top='on', right='on', which='both')
plt.grid(linestyle='-.',zorder=0)
plt.bar(x, [sum(ground_linkcostN2)/12, sum(nsga_linkcostN2)/12, sum(nsga_linkcostN2_2)/12], width,color = colors,zorder=10)
plt.xticks(x, labels, fontsize=11)
plt.subplot(144)
plt.ylabel('Session establishment overhead', fontsize=13)
plt.tick_params(axis='x', labelsize=6, direction='in')
plt.tick_params(axis='y', labelsize=6, direction='in')
plt.tick_params(top='on', right='on', which='both')
plt.grid(linestyle='-.',zorder=0)
plt.bar(x, [sum(ground_linkcostSe)/12, sum(nsga_linkcostSe)/12, sum(nsga_linkcostSe_2)/12], width,color = colors,zorder=10)
plt.xticks(x, labels, fontsize=11)
plt.tight_layout()
plt.show()


def compute(result_path, rate, queue, packet_number, packet_interval, type, is_ground):
    success_rate_xn = []
    delay_xn = []
    for i in range(12):
        Plan_packets = np.loadtxt('../stk/sat_load/Sat_load' + str(i) + '.txt').T.reshape(1, -1)[0]
        Plan_packets = [int(max(x / 100000, 1)) for x in Plan_packets]
        data = []
        file = open(
            result_path + '/' + str(i) + '-' + str(rate) + '-' + str(queue) + '-' + str(packet_number) + '-' + str(
                packet_interval) + '-' + str(type) + "-" + str(is_ground) + '.txt', 'r')  # 打开文件
        file_data = file.readlines()  # 读取所有行
        for row in file_data:
            tmp_list = row.split('; ')
            data.append(tmp_list)  # 将每行数据插入data中
        # print(len(data[0]))

        client_time = [[] for _ in range(960)]
        for s in data[0]:
            if len(s) > 4:
                client_time[int(s.split('+')[0])].append(float(s.split('+')[1][:-2]))

        Receive_packets = [len(s) for s in client_time]
        Success_rate = [0 for _ in range(960)]
        for s in range(960):
            if Plan_packets[s] > 0:
                Success_rate[s] = Receive_packets[s] / Plan_packets[s]
        meam_Success_rate = 0
        for s in range(960):
            meam_Success_rate += Success_rate[s] * (Plan_packets[s] / sum(Plan_packets))

        # print(meam_Success_rate)
        # print("收到总包数 = ", sum(Receive_packets))

        Average_delay = [0 for _ in range(960)]
        for s in range(960):
            if len(client_time[s]) > 0:
                Average_delay[s] = sum(client_time[s]) / len(client_time[s])
        # print(Average_delay)
        mean_Average_delay = 0
        Number_of_receive = sum(Receive_packets)
        for s in range(960):
            mean_Average_delay += Average_delay[s] * (Receive_packets[s] / Number_of_receive)
        # print(mean_Average_delay)
        delay_xn.append(mean_Average_delay), success_rate_xn.append(min(meam_Success_rate, 1))
    print(max(delay_xn),min(delay_xn))
    # return sum(delay_xn) / 12, sum(success_rate_xn) / 12
    if is_ground:
        return delay_xn,sum(success_rate_xn) / 12
    else:
        return [i+5.1 for i in delay_xn], sum(success_rate_xn) / 12

rate = [1000]
queue = [5000]
packet_number = [100000]
packet_interval = [0.0001,6.7e-05, 5e-05, 4e-05,3.3e-05, 2.85e-05, 2.5e-05]
delay_bad = {}
packet_loss_bad = {}
delay_good = {}
packet_loss_good = {}
for i in rate:
    for j in queue:
        for q in packet_number:
            for p in packet_interval:
                for m in range(4):
                    for k in range(2):
                        a, b = compute('result_bad_4w', i, j, q, p, m, k)
                        aa = str(i) + '-' + str(j) + '-' + str(q) + '-' + str(p) + '-' + str(m) + '-' + str(k)
                        delay_bad[aa] = a
                        packet_loss_bad[aa] = b

                        a, b = compute('result', i, j, q, p, m, k)
                        aa = str(i) + '-' + str(j) + '-' + str(q) + '-' + str(p) + '-' + str(m) + '-' + str(k)
                        delay_good[aa] = a
                        packet_loss_good[aa] = b


x_label = ['10000 ', '','','','','','40000']
x_row = np.arange(len(x_label))
width = 0.25

fig = plt.figure(figsize=(9.5,3.5))

plt.subplot(1, 4, 1)
plt.ylabel('Xn-Based handover latency(ms)', fontsize=13)
plt.subplot(1, 4, 2)
plt.ylabel('Service request latency(ms)', fontsize=13)
plt.subplot(1, 4, 3)
plt.ylabel('N2-Based handover latency(ms)', fontsize=13)
plt.subplot(1, 4, 4)
plt.ylabel('Session establishment latency(ms)', fontsize=13)
for index in range(4):
    plt.subplot(1, 4, index+1)
    plt.tick_params(axis='x', labelsize=6, direction='in')
    plt.tick_params(axis='y', labelsize=6, direction='in')
    plt.tick_params(top='on', right='on', which='both')
    plt.grid( linestyle='-.', zorder=0)
    good = [delay_good["1000-5000-100000-0.0001-" + str(index) + "-0"],
            delay_good["1000-5000-100000-6.7e-05-" + str(index) + "-0"],
            delay_good["1000-5000-100000-5e-05-" + str(index) + "-0"],
            delay_good["1000-5000-100000-4e-05-" + str(index) + "-0"],
            delay_good["1000-5000-100000-3.3e-05-" + str(index) + "-0"],
            delay_good["1000-5000-100000-2.85e-05-" + str(index) + "-0"],
            delay_good["1000-5000-100000-2.5e-05-" + str(index) + "-0"],]

    ground = [delay_good["1000-5000-100000-0.0001-" + str(index) + "-1"],
            delay_good["1000-5000-100000-6.7e-05-" + str(index) + "-1"],
            delay_good["1000-5000-100000-5e-05-" + str(index) + "-1"],
            delay_good["1000-5000-100000-4e-05-" + str(index) + "-1"],
            delay_good["1000-5000-100000-3.3e-05-" + str(index) + "-1"],
            delay_good["1000-5000-100000-2.85e-05-" + str(index) + "-1"],
            delay_good["1000-5000-100000-2.5e-05-" + str(index) + "-1"], ]
    bad = [ delay_bad["1000-5000-100000-0.0001-" + str(index) + "-0"],
            delay_bad["1000-5000-100000-6.7e-05-" + str(index) + "-0"],
            delay_bad["1000-5000-100000-5e-05-" + str(index) + "-0"],
            delay_bad["1000-5000-100000-4e-05-" + str(index) + "-0"],
            delay_bad["1000-5000-100000-3.3e-05-" + str(index) + "-0"],
            delay_bad["1000-5000-100000-2.85e-05-" + str(index) + "-0"],
            delay_bad["1000-5000-100000-2.5e-05-" + str(index) + "-0"], ]

    print(ground)
    print(good)
    if index == 1:
        plt.boxplot(good, patch_artist=True, medianprops={'color': 'black'},
                    boxprops={'color': (236/255, 120/255, 83/255), 'facecolor': (236/255, 120/255, 83/255), 'alpha': 0.5, },
                    capprops={'color': (236/255, 120/255, 83/255)}, whiskerprops={'color': (236/255, 120/255, 83/255), }, showfliers=False, )
        plt.boxplot(ground, patch_artist=True, medianprops={'color': 'black'},
                    boxprops={'color': (22/255, 6/255, 138/255), 'facecolor': (22/255, 6/255, 138/255), 'alpha': 0.5, },
                    capprops={'color': (22/255, 6/255, 138/255)}, whiskerprops={'color': (22/255, 6/255, 138/255), },
                    showfliers=False, )
        plt.boxplot(bad, patch_artist=True, medianprops={'color': 'black'},
                    boxprops={'color': (253/255, 179/255, 46/255), 'facecolor': (253/255, 179/255, 46/255), 'alpha': 0.5, },
                    capprops={'color': (253/255, 179/255, 46/255)}, whiskerprops={'color': (253/255, 179/255, 46/255), }, showfliers=False, )

        good_patch = mpatches.Patch(color=(236/255, 120/255, 83/255), label='P-S')
        ground_patch = mpatches.Patch(color=(22/255, 6/255, 138/255), label='TCN')
        bad_patch = mpatches.Patch(color=(253/255, 179/255, 46/255), label='C-S')
        plt.legend(handles=[good_patch, ground_patch, bad_patch])
    else:
        plt.boxplot(good, patch_artist=True, medianprops={'color': 'black'},
                    boxprops={'color': (236/255, 120/255, 83/255), 'facecolor': (236/255, 120/255, 83/255), 'alpha': 0.5, },
                    capprops={'color': (236/255, 120/255, 83/255)}, whiskerprops={'color': (236/255, 120/255, 83/255), }, showfliers=False, )
        plt.boxplot(ground, patch_artist=True, medianprops={'color': 'black'},
                    boxprops={'color': (22/255, 6/255, 138/255), 'facecolor': (22/255, 6/255, 138/255), 'alpha': 0.5, },
                    capprops={'color': (22/255, 6/255, 138/255)}, whiskerprops={'color': (22/255, 6/255, 138/255), },
                    showfliers=False, )
        plt.boxplot(bad, patch_artist=True, medianprops={'color': 'black'},
                    boxprops={'color': (253/255, 179/255, 46/255), 'facecolor': (253/255, 179/255, 46/255), 'alpha': 0.5, },
                    capprops={'color': (253/255, 179/255, 46/255)}, whiskerprops={'color': (253/255, 179/255, 46/255), }, showfliers=False, )

    plt.xticks(x_row, x_label,fontsize=11)
    plt.yticks(fontsize=11)
    plt.xlabel('User request per second ',fontsize=13)

    plt.tight_layout()

plt.show()
#
#
fig = plt.figure(figsize=(9.5,3.5))
plt.subplot(1, 4, 1)
plt.ylabel('Xn-Based handover reliability', fontsize=13)
plt.subplot(1, 4, 2)
plt.ylabel('Service request reliability', fontsize=13)
plt.subplot(1, 4, 3)
plt.ylabel('N2-Based handover reliability', fontsize=13)
plt.subplot(1, 4, 4)
plt.ylabel('Session establishment reliability', fontsize=13)
for index in range(4):
    plt.subplot(1, 4, index+1)
    # plt.ylim(0.55, 1.02)
    plt.tick_params(axis='x', labelsize=6, direction='in')
    plt.tick_params(axis='y', labelsize=6, direction='in')
    plt.tick_params(top='on', right='on', which='both')
    plt.grid(linestyle='-.', zorder=0)
    good = [packet_loss_good["1000-5000-100000-0.0001-" + str(index) + "-0"],
            packet_loss_good["1000-5000-100000-6.7e-05-" + str(index) + "-0"],
            packet_loss_good["1000-5000-100000-5e-05-" + str(index) + "-0"],
            packet_loss_good["1000-5000-100000-4e-05-" + str(index) + "-0"],
            packet_loss_good["1000-5000-100000-3.3e-05-" + str(index) + "-0"],
            packet_loss_good["1000-5000-100000-2.85e-05-" + str(index) + "-0"],
            packet_loss_good["1000-5000-100000-2.5e-05-" + str(index) + "-0"], ]
    bad = [ packet_loss_bad["1000-5000-100000-0.0001-" + str(index) + "-0"],
            packet_loss_bad["1000-5000-100000-6.7e-05-" + str(index) + "-0"],
            packet_loss_bad["1000-5000-100000-5e-05-" + str(index) + "-0"],
            packet_loss_bad["1000-5000-100000-4e-05-" + str(index) + "-0"],
            packet_loss_bad["1000-5000-100000-3.3e-05-" + str(index) + "-0"],
            packet_loss_bad["1000-5000-100000-2.85e-05-" + str(index) + "-0"],
            packet_loss_bad["1000-5000-100000-2.5e-05-" + str(index) + "-0"], ]
    ground = [packet_loss_good["1000-5000-100000-0.0001-" + str(index) + "-1"],
              packet_loss_good["1000-5000-100000-6.7e-05-" + str(index) + "-1"],
              packet_loss_good["1000-5000-100000-5e-05-" + str(index) + "-1"],
              packet_loss_good["1000-5000-100000-4e-05-" + str(index) + "-1"],
              packet_loss_good["1000-5000-100000-3.3e-05-" + str(index) + "-1"],
              packet_loss_good["1000-5000-100000-2.85e-05-" + str(index) + "-1"],
              packet_loss_good["1000-5000-100000-2.5e-05-" + str(index) + "-1"], ]

    print(ground)
    print(good)
    # print(bad)
    if index == 0:
        plt.plot(x_row,ground, color=(22/255, 6/255, 138/255), zorder=10, marker='s',  label = 'TCN', )
        plt.plot(x_row,good, color=(236/255, 120/255, 83/255), zorder=10, marker='o',  label = 'P-S', )
        plt.plot(x_row,bad, color=(253/255, 179/255, 46/255), zorder=10, marker='D',  label = 'C-S', )
        plt.legend()
    else:
        plt.plot(x_row, ground, color=(22/255, 6/255, 138/255), zorder=10,marker='s',)
        plt.plot(x_row, good, color=(236/255, 120/255, 83/255), zorder=10,marker='o',)
        plt.plot(x_row, bad, color=(253/255, 179/255, 46/255), zorder=10, marker='D', )
    # plt.bar(x_row + 0.5 * width, bad, width, color=(253/255, 179/255, 46/255), zorder=10)
    # for a, b in zip(x_row + 0.5 * width, ground):
    #     plt.text(a, b, '%.0f' % b, ha='center', va='bottom', fontsize=7)
    # for a, b in zip(x_row - 1.5 * width, good):
    #     plt.text(a, b, '%.0f' % b, ha='center', va='bottom', fontsize=7)
    # for a, b in zip(x_row - 0.5 * width, bad):
    #     plt.text(a, b, '%.0f' % b, ha='center', va='bottom', fontsize=7)
    plt.xticks(x_row, x_label,fontsize=11)
    plt.yticks(fontsize=11)
    plt.xlabel('User request per second ',fontsize=13)

    plt.tight_layout()

plt.show()
# #


# rate = [50,100,150]
# queue = [1000]
# packet_number = [100000]
# packet_interval = [0.001]
# delay = {}
# packet_loss = {}
# delay_good = {}
# packet_loss_good = {}
# for i in rate:
#     for j in queue:
#         for q in packet_number:
#             for p in packet_interval:
#                 for m in range(4):
#                     for k in range(2):
#                         a, b = compute('result', i, j, q, p, m, k)
#                         aa = str(i) + '-' + str(j) + '-' + str(q) + '-' + str(p) + '-' + str(m) + '-' + str(k)
#                         delay[aa] = a
#                         packet_loss[aa] = b
#
#
# x_label = ['50\nS', '50\nT', '100\nS','100\nT','150\nS','150\nT']
# x_row = np.arange(len(x_label))
# width = 0.25
# fig = plt.figure(figsize=(9.5,3.5))
# # delay = [1,2,3,4,5,6]
# # loss = [1,2,3,4,5,6]
# for index in range(4):
#     # plt.subplot(1, 4, index+1)
#     ax = fig.add_subplot(1, 4, index+1)
#     #
#     ax.tick_params(axis='x', labelsize=6, direction='in')
#     ax.tick_params(axis='y', labelsize=6, direction='in')
#     ax.tick_params(top='on', right='on', which='both')
#     ax.grid(axis='y', linestyle='-.', zorder=0)
#     delay_result = [delay["50-1000-100000-0.001-" + str(index) + "-0"], delay["50-1000-100000-0.001-" + str(index) + "-1"],
#             delay["100-1000-100000-0.001-" + str(index) + "-0"], delay["100-1000-100000-0.001-" + str(index) + "-1"],
#             delay["150-1000-100000-0.001-" + str(index) + "-0"], delay["150-1000-100000-0.001-" + str(index) + "-1"],
#             ]
#     loss = [packet_loss["50-1000-100000-0.001-" + str(index) + "-0"],packet_loss["50-1000-100000-0.001-" + str(index) + "-1"],
#             packet_loss["100-1000-100000-0.001-" + str(index) + "-0"],packet_loss["100-1000-100000-0.001-" + str(index) + "-1"],
#             packet_loss["150-1000-100000-0.001-" + str(index) + "-0"],packet_loss["150-1000-100000-0.001-" + str(index) + "-1"],
#             ]
#     print(delay_result)
#     print(loss)
#     ax.bar(x_row -width , delay_result, width, color = (236/255, 120/255, 83/255), zorder=10)
#
#
#     ax1 = ax.twinx()
#     ax1.bar(x_row, loss, width, color=(22/255, 6/255, 138/255), zorder=10)
#     ax.set_xticks(x_row)
#
#     ax1.set_ylim(0.5,1.02)
#
#     # ax.set_xlabel('User request per second ')
#     if index ==0:
#         ax.set_ylabel('Xn-Based handover delay(ms)', fontsize=13)
#         ax1.set_ylabel('Xn-Based handover reliability', fontsize=13)
#         ax1.set_yticks([])
#     elif index ==1:
#         ax.set_ylabel('Service request delay(ms)', fontsize=13)
#         ax1.set_ylabel('Service request reliability', fontsize=13)
#         ax1.set_yticks([])
#     elif index == 2:
#         ax.set_ylabel('N2-Based handover delay(ms)', fontsize=13)
#         ax1.set_ylabel('N2-Based handover reliability', fontsize=13)
#         ax1.set_yticks([])
#     elif index == 3:
#         ax.set_ylabel('Session establishment delay(ms)', fontsize=13)
#         ax1.set_ylabel('Session establishment reliability', fontsize=13)
#     ax.set_xticklabels(x_label)
#     ax1.set_xticklabels(x_label)
#     plt.setp(ax.get_xticklabels(), fontsize=9)
#     plt.setp(ax1.get_xticklabels(), fontsize=9)
#     plt.tight_layout()
#     # plt.legend()
# plt.show()

# rate = [50]
# queue = [1000,3000,5000]
# packet_number = [100000]
# packet_interval = [0.001]
# delay = {}
# packet_loss = {}
# delay_good = {}
# packet_loss_good = {}
# for i in rate:
#     for j in queue:
#         for q in packet_number:
#             for p in packet_interval:
#                 for m in range(4):
#                     for k in range(2):
#                         a, b = compute('result', i, j, q, p, m, k)
#                         aa = str(i) + '-' + str(j) + '-' + str(q) + '-' + str(p) + '-' + str(m) + '-' + str(k)
#                         delay[aa] = a
#                         packet_loss[aa] = b
#
# x_label = ['1000\nS', '1000\nT', '3000\nS','3000\nT','5000\nS','5000\nT']
# x_row = np.arange(len(x_label))
# width = 0.25
# fig = plt.figure(figsize=(9.5,3.5))
# # delay = [1,2,3,4,5,6]
# # loss = [1,2,3,4,5,6]
# for index in range(4):
#     # plt.subplot(1, 4, index+1)
#     ax = fig.add_subplot(1, 4, index+1)
#     #
#     ax.tick_params(axis='x', labelsize=6, direction='in')
#     ax.tick_params(axis='y', labelsize=6, direction='in')
#     ax.tick_params(top='on', right='on', which='both')
#     ax.grid(axis='y', linestyle='-.', zorder=0)
#     delay_result = [delay["50-1000-100000-0.001-" + str(index) + "-0"],delay["50-1000-100000-0.001-" + str(index) + "-1"],
#             delay["50-3000-100000-0.001-" + str(index) + "-0"], delay["50-3000-100000-0.001-" + str(index) + "-1"],
#             delay["50-5000-100000-0.001-" + str(index) + "-0"],delay["50-5000-100000-0.001-" + str(index) + "-1"],
#             ]
#     loss = [packet_loss["50-1000-100000-0.001-" + str(index) +    "-0"],packet_loss["50-1000-100000-0.001-" + str(index) + "-1"],
#             packet_loss["50-3000-100000-0.001-" + str(index) + "-0"],packet_loss["50-3000-100000-0.001-" + str(index) + "-1"],
#             packet_loss["50-5000-100000-0.001-" + str(index) + "-0"],packet_loss["50-5000-100000-0.001-" + str(index) + "-1"],
#             ]
#     print(delay_result)
#     print(loss)
#     ax.bar(x_row - width, delay_result, width, color=(236/255, 120/255, 83/255), zorder=10)
#
#     ax1 = ax.twinx()
#     ax1.bar(x_row, loss, width, color=(22/255, 6/255, 138/255), zorder=10)
#
#     ax1.set_ylim(0.5, 1.02)
#
#     # ax.set_xlabel('User request per second ')
#     if index == 0:
#         ax.set_ylabel('Xn-Based handover delay(ms)', fontsize=13)
#         ax1.set_ylabel('Xn-Based handover reliability', fontsize=13)
#         ax1.set_yticks([])
#     elif index == 1:
#         ax.set_ylabel('Service request delay(ms)', fontsize=13)
#         ax1.set_ylabel('Service request reliability', fontsize=13)
#         ax1.set_yticks([])
#     elif index == 2:
#         ax.set_ylabel('N2-Based handover delay(ms)', fontsize=13)
#         ax1.set_ylabel('N2-Based handover reliability', fontsize=13)
#         ax1.set_yticks([])
#     elif index == 3:
#         ax.set_ylabel('Session establishment delay(ms)', fontsize=13)
#         ax1.set_ylabel('Session establishment reliability', fontsize=13)
#     ax.set_xticks(x_row)
#     ax.set_xticklabels(x_label)
#     ax1.set_xticks(x_row)
#     ax1.set_xticklabels(x_label)
#     plt.setp(ax.get_xticklabels(), fontsize=9)
#     plt.setp(ax1.get_xticklabels(), fontsize=9)
#     plt.tight_layout()
#     # plt.legend()
# plt.show()


# fig, ax = plt.subplots(2, 4, sharex=True)
#
# for i in range(2):
#     for j in range(4):
#         ax[i, j].tick_params(axis='x', labelsize=6, direction='in')
#         ax[i, j].tick_params(axis='y', labelsize=6, direction='in')
#         # ax[i, j].set_yticks([])
#         # ax[i, j].xaxis.set_visible(False)
#         if i == 0:
#             # ax[i, j].set_ylim(10,100)
#             ax[i, j].bar(x_row - 1.5 * width,
#                          [delay_good["100-1000-100000-0.01-" + str(j) + "-0"],
#                           delay_good["100-1000-100000-0.001-" + str(j) + "-0"],
#                           delay_good["100-1000-100000-0.0001-" + str(j) + "-0"]], width, label='23800')
#             ax[i, j].bar(x_row - 0.5 * width,
#                          [delay["100-1000-100000-0.01-" + str(j) + "-0"],
#                           delay["100-1000-100000-0.001-" + str(j) + "-0"],
#                           delay["100-1000-100000-0.0001-" + str(j) + "-0"]], width, label='7900' )
#             ax[i, j].bar(x_row + 0.5 * width,
#                          [delay["100-1000-100000-0.01-" + str(j) + "-1"],
#                           delay["100-1000-100000-0.001-" + str(j) + "-1"],
#                           delay["100-1000-100000-0.0001-" + str(j) + "-1"]], width, label='TCN' )
#
#             # ax[i, j].bar(x_row + 0.5 * width,
#             #              [delay["100-1000-100000-0.0001-" + str(j) + "-0"], delay["100-1000-100000-0.0001-" + str(j) + "-1"]], width, )
#             # ax[i, j].bar(x_row + 1.5 * width,
#             #              [delay["100-1000-100000-0.01-" + str(j) + "-0"], delay["100-1000-100000-0.01-" + str(j) + "-1"]], width, )
#             # ax[i, j].bar(x_row + 2.5 * width,
#             #              [delay["100-1000-100000-0.01-" + str(j) + "-0"], delay["100-1000-100000-0.01-" + str(j) + "-1"]], width, )
#             # ax[i, j].bar(x_row + 3.5 * width,
#             #              [delay["100-1000-100000-0.01-" + str(j) + "-0"], delay["100-1000-100000-0.01-" + str(j) + "-1"]], width, )
#             # ax[i, j].plot(x, delay["100-1000-100000-0.01-" + str(j) + "-0"], color='red')
#             # ax[i, j].plot(x, delay["100-1000-100000-0.01-" + str(j) + "-1"], color='blue')
#             # ax[i, j].plot(x, delay["100-1000-100000-0.001-" + str(j) + "-0"], color='tomato')
#             # ax[i, j].plot(x, delay["100-1000-100000-0.001-" + str(j) + "-1"], color='cornflowerblue')
#             # ax[i, j].plot(x, delay["100-1000-100000-0.0001-" + str(j) + "-0"], color='black')
#             # ax[i, j].plot(x, delay["100-1000-100000-0.0001-" + str(j) + "-1"], color='green')
#
#         if i == 1:
#             # ax[i, j].set_ylim(-0.05, 0.5)
#             # ax[i, j].plot(x, delay["5000-10000-" + str(j) + "-0"], color='red')
#             # ax[i, j].plot(x, delay["5000-10000-" + str(j) + "-1"], color='blue')
#             # ax[i, j].plot(x, delay["2000-10000-" + str(j) + "-0"], color='red')
#             # ax[i, j].plot(x, delay["100-1000-100000-0.01-" + str(j) + "-1"], color='blue')
#             #
#             # ax[i, j].plot(x, delay["2000-5000-" + str(j) + "-0"], color='tomato')
#             # ax[i, j].plot(x, delay["2000-5000-" + str(j) + "-1"], color='cornflowerblue')
#             ax[i, j].set_ylim(0.4, 1.09)
#             # ax[i, j].plot(x, packet_loss["100-1000-100000-0.01-" + str(j) + "-0"], color='red')
#             # ax[i, j].plot(x, packet_loss["100-1000-100000-0.01-" + str(j) + "-1"], color='blue')
#             # ax[i, j].plot(x, packet_loss["100-1000-100000-0.001-" + str(j) + "-0"], color='tomato')
#             # ax[i, j].plot(x, packet_loss["100-1000-100000-0.001-" + str(j) + "-1"], color='cornflowerblue')
#             # ax[i, j].plot(x, packet_loss["100-1000-100000-0.0001-" + str(j) + "-0"], color='black')
#             # ax[i, j].plot(x, packet_loss["100-1000-100000-0.0001-" + str(j) + "-1"], color='green')
#             ax[i, j].bar(x_row - 1.5 * width,
#                          [packet_loss_good["100-1000-100000-0.01-" + str(j) + "-0"],
#                           packet_loss_good["100-1000-100000-0.001-" + str(j) + "-0"],
#                           packet_loss_good["100-1000-100000-0.0001-" + str(j) + "-0"]], width, )
#
#             ax[i, j].bar(x_row - 0.5 * width,
#                          [packet_loss["100-1000-100000-0.01-" + str(j) + "-0"],
#                           packet_loss["100-1000-100000-0.001-" + str(j) + "-0"],
#                           packet_loss["100-1000-100000-0.0001-" + str(j) + "-0"]], width, )
#             ax[i, j].bar(x_row + 0.5 * width,
#                          [packet_loss["100-1000-100000-0.01-" + str(j) + "-1"],
#                           packet_loss["100-1000-100000-0.001-" + str(j) + "-1"],
#                           packet_loss["100-1000-100000-0.0001-" + str(j) + "-1"]], width, )
#
#             # ax[i, j] .bar(x_row + 0.5 * width,
#             #      [packet_loss["100-1000-100000-0.0001-" + str(j) + "-0"], packet_loss["100-1000-100000-0.0001-" + str(j) + "-1"]], width, )
#             # ax[i, j] .bar(x_row + 1.5 * width,
#             #      [packet_loss["5000-5000-" + str(j) + "-0"], packet_loss["5000-5000-" + str(j) + "-1"]], width, )
#             # ax[i, j].bar(x_row + 2.5 * width,
#             #              [packet_loss["700-10000-" + str(j) + "-0"], packet_loss["700-10000-" + str(j) + "-1"]], width, )
#             # ax[i, j].bar(x_row + 3.5 * width,
#             #              [packet_loss["700-5000-" + str(j) + "-0"], packet_loss["700-5000-" + str(j) + "-1"]], width, )
#
# ax[0, 0].set_ylabel('Delay')
# ax[1, 0].set_ylabel('Packet Loss')
# # ax[1, 0].set_xlabel('Time slot')
# # ax[1, 1].set_xlabel('Time slot')
# # ax[1, 2].set_xlabel('Time slot')
# # ax[1, 3].set_xlabel('Time slot')
# ax[1, 0].set_xticks(x_row,x_label)
# # ax[1, 1].set_xlabel('Time slot')
# # ax[1, 2].set_xlabel('Time slot')
# # ax[1, 3].set_xlabel('Time slot')
# plt.tight_layout()
# plt.legend()
# # plt.title()
# plt.show()

# fig, ax = plt.subplots(1, 4)
# for j in range(4):
#
#     ax[j].set_xlabel('Time slot')
#     ax[j].bar(x_row- 1.5*width, [packet_loss["5000-10000-" + str(j) + "-0"], packet_loss["5000-10000-" + str(j) + "-1"]],width,)
#     ax[j].bar(x_row- 0.5*width, [packet_loss["2000-10000-" + str(j) + "-0"], packet_loss["2000-10000-" + str(j) + "-1"]],width,)
#     ax[j].bar(x_row + 0.5 * width, [packet_loss["2000-5000-" + str(j) + "-0"], packet_loss["2000-5000-" + str(j) + "-1"]],width,)
#     ax[j].bar(x_row + 1.5 * width, [packet_loss["5000-5000-" + str(j) + "-0"], packet_loss["5000-5000-" + str(j) + "-1"]],width,)
# ax[j].set_xticks(x_row, labels=x_label)


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
