## Requires  
1. stk11.6 (windows)  
3. NS3-3.33 (ubuntu18.04)  
4. python3.8  

## Usage
1. Build connection between `python` and `stk11.6`.
1. Run `main` in STK to obtain the `Sat_load` and `data` for each time slot.
1. Set `Test_nsga2=True`, `ground_CN=True`, and others to `False` in `main`. Run `main` Calculate the linkcost of B-P.
1. Copy the deployment result of linkcost to `draw_result`.
1. Copy `order`, `Sat_load`, and `data` to `NS3-3.33`.
1. Copy the deployment result to `XnNsga.cc` in `NS3`.
1. Modify path of files in `XnNsga.cc` of `NS3`.  
1. Set the path of result in `NS3`.
1. Set `compute_nsga2=True` and others to `False` in `main`. Run `main` to calculate the Pareto Front of NFs stored in `opl.txt`.
1. Set `Test_nsga2=True` and others to `False` in `main`. Select the deployment of P-S with more NF instances from `opl.txt`. Run `main` to calculate the linkcost of P-S.
1. Copy the result of linkcost to `draw_git result`.
1. Copy the files in `ns3/ns3` to `NS3-3.33`.
1. Copy `order_nsga`, `Sat_load`, `data`, `amf_processs_time`, `smf_processs_time`, `upf_processs_time`, and `ns3_process_time_nfs` to `NS3-3.33`.
1. Modify path of files in `XnNsga.cc` of `NS3`.  
1. Copy the deployment result to `XnNsga.cc` in `NS3`.
1. Set the path of result in `NS3`.  
1. Run `getResult.py` in `ns3/ns3`.
1. Copy the result to `ns3` folder and rename it `result_P-S_B-P`.
1. Set `Test_nsga2=True` and others to `False` in `main`. Select the deployment of C-S with fewer NF instances from `opl.txt`. Run `main` Calculate the linkcost of C-S.
1. Copy the result of  linkcost to `draw_result`.
1. Copy `order_nsga`, `Sat_load`, `data`, `amf_processs_time`, `smf_processs_time`, `upf_processs_time`, and `ns3_process_time_nfs` to `NS3-3.33`.
1. Copy the deployment result to `XnNsga.cc` in `NS3`.
1. Modify path of files in `XnNsga.cc` of `NS3`.
1. Set the path of result in `NS3`.
1. Run getResult.py in `ns3/ns3`.
1. Copy the result to `ns3` folder and rename it `result_C-S`.  
1. Use `draw_result` in `NS3` to draw the time and packet loss rate images.  



## Directory Structure  
* **ns3:**  
The code used by the NS3 program, including the construction of the network and the app code. By inputting the deployment result of NSGA, obtain the process completion time and packet loss rate.
---ns3: the code of AMF, SMF, UPF and client used in NS3.  
---result_P-S_B-P: the running result of P-S and B-P, received packages and the time it takes for each package to complete the process.  
---result_C-S: the running result of C-S.  
---draw_result.py Draw the picture of figure 10, figure 11, figure 12.
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
Read the stk running results and calculate the deployment position of NF instances. Statistical plotting of NS3 results.  
--- main The main function, adjust global variables to control whether to run tests or calculations. Set hyperparameters. 
--- resource: the amount of resources per satellite  
--- amf_processs_time: The processing time amf runs on each satellite.  
--- smf_processs_time: The processing time of smf running on each satellite.  
--- upf_processs_time: The processing time for upf to run on each satellite.  
--- loadsum: the cumulative number of people at all times for each satellite.
--- ns3_process_time_nfs: The processing time of each NF instance. The first row represents AMF, the second represents SMF, and the third represents UPF. 
--- hopMean: The average number of hops between any two satellite nodes in the total time range.  
--- delayMean: The average delay of any two satellite nodes within the total time range.  
--- P_T_time: The time consumed by the calculation process, used for nsga to calculate fitness.  
--- linkcost_compute: Calculate the linkcost of the process, used to calculate the fitness of nsga  
--- NF: Calculate the processing time of network elements.  
--- kmeans: Kmeans algorithm. Initial population used to calculate NSGA
--- near_core_sat: The five satellites closest to the five ground core networks at each moment.  
--- order: The core network is all on the ground, the satellites are only for transmission, the row is each satellite, and the column is the satellite connected to the target core network  
--- order_Nsga: deploy amf, smf, upf in the satellite. Rows are each satellite, columns are target amf, smf, upf, ground connected satellites. is the next hop location for signaling transmission.    
--- nsga2: NSGA2 code, calculate the position of the network element.    
--- tools: some functions.  
--- RCM: RCM mechanism simulation.    
--- RCM_DRAW: Draw result of RCM mechanism.  
--- opl.txt: Pareto Front.  

