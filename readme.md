## Requires  
1. stk11.6  
2. ubuntu18.04 
3. NS3-3.33  
4. python3.8  

## Directory Structure  
* **ns3:**  
The code used by the NS3 program, including the construction of the network and the code of the app. By inputting the deployment result of nsga, obtain the process completion time and packet loss rate.
result: the running result, received packages and the time it takes for each package to complete the process
* **stk:**   
The code used by STK to build the scene, which is used to calculate the position of the satellite at each moment, the connection relationship between the satellites, the satellite and the ground, and the propagation delay between the satellites.  
---data: link information at each moment  
&emsp;|---Adjacency_Matrix.txt Satellite connection information, adjacency matrix, 960 to 60  
&emsp;|---Delay_matrix.txt Delay information, the delay between each satellite and any other satellite, 960x60, dijkstra algorithm  
&emsp;|---Delay_Matrix_origin.txt The reciprocal delay of each satellite from the connected satellite (in seconds)  
&emsp;|---hop hop information, the hops between each satellite and any other satellite  
---sat_load: The number of people loaded on each satellite at each moment, it is a 40x24 matrix  
---main: main program, create STK scene, build satellite, build ground station, calculate link information, calculate the satellite closest to the ground station  
---population: global population information, divided into 50x50.  
---Others: files used by the main program.  

* **nsga:**  
Read the stk running results and calculate the deployment position of network elements. Statistical plotting of NS3 results.  
--- main The main function, adjust global variables to control whether to run tests or calculations. Set hyperparameters. 
--- resource: the amount of resources per satellite  
--- amf_processs_time: The processing time amf runs on each satellite.  
--- smf_processs_time: The processing time of smf running on each satellite.  
--- upf_processs_time: The processing time for upf to run on each satellite.  
--- loadsum: the cumulative number of people at all times for each satellite  
--- hopMean: The average number of hops between any two satellite nodes in the total time range.  
--- delayMean: The average delay of any two satellite nodes within the total time range.  
--- P_T_time: The time consumed by the calculation process, used for nsga to calculate fitness.  
--- linkcost_compute: Calculate the linkcost of the process, used to calculate the fitness of nsga  
--- NF: Calculate the processing time of network elements.  
--- kmeans: Kmeans algorithm. Initial population used to calculate NSGA  
--- draw_result_linkcost: drawing  
--- near_core_sat: The five satellites closest to the five ground core networks at each moment.  
--- order: The core network is all on the ground, the satellites are only for transmission, the row is   each --- satellite, and the column is the satellite connected to the target core network  
--- order_Nsga: deploy amf, smf, upf in the satellite. Rows are each satellite, columns are target amf,   smf, --- upf, ground connected satellites. is the next hop location for signaling transmission.    
--- nsga2: NSGA2 code, calculate the position of the network element.  
--- resource_process: Drawings for centralized deployment and separate deployment.  
--- tools: some functions  

## Usage
1. Run main in STK to get Sat_load and link information.
1. Set compute_nsga2=True, others are False in main. Calculate the Deployment Position of NFs.
2. Set Test_nsga2=True, others are False in main. Calculate linkcost of NSGA.  
3. Set Test_nsga2=True, ground_CN = True, others are False in main. Calculate linkcost of Ground. 
4. Copy linkcost of NSGA and Ground to **draw_result_linkcost** and draw the linkcost image.
5. Copy folder order and order_nsga to NS3.  
6. Copy deployment result to NS3.
7. Run getResult.py in NS3.   
8. Use **use draw_result** in NS3 to draw the time and packet loss rate images.  

