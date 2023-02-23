##Requires
stk11.6
 ubuntu18.04
Install NS3-3.33
python3.8

ns3: The code used by the NS3 program, including the construction of the network and the code of the app. By inputting the deployment result of nsga, obtain the process completion time and packet loss rate.
result: the running result, received packages and the time it takes for each package to complete the process
stk: The code used by STK to build the scene, which is used to calculate the position of the satellite at each moment, the connection relationship between the satellites, the satellite and the ground, and the propagation delay between the satellites.
data: link information at each moment
Adjacency_Matrix.txt Satellite connection information, adjacency matrix, 960 to 60
Delay_matrix.txt Delay information, the delay between each satellite and any other satellite, 960x60, dijkstra algorithm
Delay_Matrix_origin.txt The reciprocal delay of each satellite from the connected satellite (in seconds)
hop hop information, the hops between each satellite and any other satellite
sat_load: The number of people loaded on each satellite at each moment, it is a 40x24 matrix
main: main program, create STK scene, build satellite, build ground station, calculate link information, calculate the satellite closest to the ground station
population: global population information, divided into 50x50.
Others: files used by the main program.

nsga: Read the stk running results and calculate the deployment position of network elements. Statistical plotting of NS3 results.
main The main function, adjust global variables to control whether to run tests or calculations. Set hyperparameters. If you want to use NSGAII to calculate the deployment location, then compute_nsga2=True, others are False. If you want to test, set Test_nsga2 to True and others to False. In the test, linkcost results are available. Copy the linkcost result to draw_result_linkcost and draw the linkcost image. Then copy the deployment result to NS3, use NS3 to obtain the time and packet loss rate results, and use draw_result in NS3 to draw the time and packet loss rate images.
resource: the amount of resources per satellite
amf_processs_time: The processing time amf runs on each satellite.
smf_processs_time: The processing time of smf running on each satellite.
upf_processs_time: The processing time for upf to run on each satellite.
loadsum: the cumulative number of people at all times for each satellite
hopMean: The average number of hops between any two satellite nodes in the total time range.
delayMean: The average delay of any two satellite nodes within the total time range.
P_T_time: The time consumed by the calculation process, used for nsga to calculate fitness.
linkcost_compute: Calculate the linkcost of the process, used to calculate the fitness of nsga
NF: Calculate the processing time of network elements.
kmeans: Kmeans algorithm. Initial population used to calculate NSGA
draw_result_linkcost: drawing
near_core_sat: The five satellites closest to the five ground core networks at each moment.
order: The core network is all on the ground, the satellites are only for transmission, the row is each satellite, and the column is the satellite connected to the target core network
order_Nsga: deploy amf, smf, upf in the satellite. Rows are each satellite, columns are target amf, smf, upf, ground connected satellites. is the next hop location for signaling transmission.
nsga2: NSGA2 code, calculate the position of the network element.
resource_process: Drawings for centralized deployment and separate deployment.
tools: some functions
