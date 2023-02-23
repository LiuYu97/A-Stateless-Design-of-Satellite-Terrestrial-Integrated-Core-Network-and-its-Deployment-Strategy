需要安装stk11.6
需要ubuntu18.04 
安装NS3-3.33
python3.8

ns3: NS3程序用到的代码，包括网络的构建以及app的代码。通过输入nsga的部署结果，获取流程完成时间以及丢包率。
	result: 运行结果，收到的包以及每个包完成流程消耗的时间
stk: STK构建场景用到的代码，用来计算每个时刻卫星的位置以及卫星之间、卫星与地面的连接关系，还有卫星之间的传播时延。
	data: 每个时刻的链路信息
		Adjacency_Matrix.txt 卫星连接信息，邻接矩阵，960下60
		Delay_matrix.txt 时延信息，每个卫星距离其他任意卫星的时延，960x60，dijkstra算法
		Delay_Matrix_origin.txt 每个卫星距离连接卫星的时延倒数（单位秒）
		hop 跳数信息，每个卫星距离其他任意卫星的跳数
	sat_load: 每个时刻每个卫星的人数负载，是个40x24的矩阵
	main: 主程序，建立STK场景，构建卫星，构建地面站，计算链路信息，计算距离地面站最近的卫星
	population: 全球人数信息，分成50x50。
	其他：主程序用到的文件。

nsga: 读取stk运行结果，计算网元的部署位置。对NS3的结果进行统计绘图。
	main 主函数，调整全局变量控制运行测试还是计算。设置超参数。如果想要使用NSGAII计算部署位置，则compute_nsga2 = True，其他均为False。如果想要测试，则将Test_nsga2设为True，其他未False。在测试中，可以获得linkcost结果。将linkcost结果复制到draw_result_linkcost中，绘制linkcost图像。再将部署结果复制到NS3中，使用NS3获得时间以及丢包率结果，使用NS3中的draw_result绘制时间以及丢包率图像。
	resource: 每个卫星的资源量
	amf_processs_time: amf在每个卫星上运行的处理时间。
smf_processs_time: smf在每个卫星上运行的处理时间。
upf_processs_time: upf在每个卫星上运行的处理时间。
	loadsum: 每个卫星所有时刻的人数累计
	hopMean: 任意两个卫星节点在总时刻范围内的平均跳数。
	delayMean: 任意两个卫星节点在总时刻范围内的平均时延。
	P_T_time: 计算流程的消耗时间，用于nsga计算适应度。
	linkcost_compute: 计算流程的linkcost，用于计算nsga的适应度
	NF: 计算网元的处理时间。
	kmeans：Kmeans算法。用于计算NSGA的初始种群
	draw_result_linkcost: 画图
	near_core_sat: 每个时刻离5个地面核心网最近的五个卫星。
	order: 核心网全部在地面，卫星只做传输，行是每个卫星，列是目标核心网连接的卫星
	order_Nsga: 卫星中部署amf、smf、upf。行是每个卫星，列是目标amf, smf, upf, 地面连接的卫星。是信令传输的下一跳位置。
	nsga2: NSGA2代码，计算网元位置。
	resource_process: 集中部署分开部署的画图。
	tools: 一些函数