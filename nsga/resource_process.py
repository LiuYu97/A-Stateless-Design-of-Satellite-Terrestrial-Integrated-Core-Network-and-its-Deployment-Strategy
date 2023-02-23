

import matplotlib.pyplot as plt
# 各实验数据
# ue 500 cpu 5 -1 不够500
# ue 500 cpu 5 -2 102-564
# 55-572
# 77-292

# ue 500 cpu 10 -1 77-78
# 52-100
# 77-114

# ue 500 cpu 15 -1 77-200
# 53 -134
# 77-186

# ue 500 cpu 20 -1 54-354
# 61-172
# 52-168
# 76-194

# blade ue 500 cpu 20 -1 3.714-52-198
# 3.01-77-124
# 2.669-52-124
# 3.498-77-152
# 2.448-52-166
if __name__ == '__main__':
    y1 = []
    y2 = []
    time_cpu5 = (102+55+77)/3
    time_cpu20 = (61 + 52 + 76) / 3
    time_cpu20_blade = (52 + 77 + 77) / 3
    y1.append(time_cpu5)
    y1.append(time_cpu20_blade)
    y1.append(time_cpu20)

    expire_cpu5 = (564+572+292)/3
    expire_cpu20 = (172 + 168 + 194) / 3
    expire_cpu20_blade = (198 + 124 + 162) / 3
    print(time_cpu5,time_cpu20,time_cpu20_blade)
    y2.append(expire_cpu5)
    y2.append(expire_cpu20_blade)
    y2.append(expire_cpu20)
    print(expire_cpu5,expire_cpu20,expire_cpu20_blade)
    # fig = plt.figure()


    x = [1, 2, 3]
    x_label = ['5', 'balde_20', '20']
    # ax = fig.add_subplot(111)

    plt.rcParams['xtick.direction'] = 'in'  # 将x周的刻度线方向设置向内
    plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度方向设置向内
    plt.rcParams['axes.labelsize'] = 16  # xy轴label的size
    plt.rcParams['xtick.labelsize'] = 12  # x轴ticks的size
    plt.rcParams['ytick.labelsize'] = 14  # y轴ticks的size
    # plt.rcParams['legend.fontsize'] = 12  # 图例的size

    # 设置柱形的间隔
    width = 0.3  # 柱形的宽度
    x1_list = []
    x2_list = []
    for i in range(len(y1)):
        x1_list.append(i)
        x2_list.append(i + width)

    # 创建图层
    fig, ax1 = plt.subplots()

    # 设置左侧Y轴对应的figure
    ax1.set_ylabel('Execution time(s)')
    ax1.set_ylim(0, 100)
    for a, b in enumerate(y1):  # 柱子上的数字显示
        plt.text(a+0.15, b, '%.2f' % b, ha='center', va='bottom', fontsize=10)

    ax1.set_xlabel('CPU', fontsize=15, fontweight='bold')
    ax1.bar(x1_list, y1, width=width, color='lightseagreen', align='edge',edgecolor="k", hatch="X")

    ax1.set_xticklabels(ax1.get_xticklabels())  # 设置共用的x轴

    # 设置右侧Y轴对应的figure
    ax2 = ax1.twinx()
    ax2.set_ylabel('Expire number')
    ax2.set_ylim(100, 500)
    for a, b in enumerate(y2):  # 柱子上的数字显示
        plt.text(a+0.45, b, '%d' % b, ha='center', va='bottom', fontsize=10)
    ax2.bar(x2_list, y2, width=width, color='tab:blue', align='edge', edgecolor="k", hatch=".",tick_label=x_label)
    plt.tight_layout()
    plt.show()


    # plt.tick_params(top='on', right='on', which='both')
    # plt.grid(axis="y", ls='--')
    # plt.xticks(x, x_label)  # 绘制x刻度标签
    # plt.xlabel('CPU ', fontsize=15)

    # plt.ylabel('', fontsize=15)
    # # 设置网格刻度
    # # plt.ylim(0, 6900)
    # plt.bar(x, y1, width=0.35, alpha=1, color="r", edgecolor="k", hatch=".....")
    #
    #
    # # plt.legend()
    # plt.show()



    #