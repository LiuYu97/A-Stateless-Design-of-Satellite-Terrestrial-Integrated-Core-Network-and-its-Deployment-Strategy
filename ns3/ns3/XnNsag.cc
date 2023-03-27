#include <vector>
#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#include <string>
#include <cassert>
#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
#include "ns3/ipv4-global-routing-helper.h"
#include "ns3/nstime.h"
#include "ns3/flow-monitor.h"
#include "ns3/flow-monitor-module.h"
#include <stdint.h>
#include "ns3/ipv4-nix-vector-helper.h"
// #include "ns3/ipv4-fw-cuda-routing.h"
// #include "ns3/ipv4-fw-cuda-helper.h"
//#include "ns3/delay-jitter-estimation.h"

// Default Network Topology
//
//       10.1.1.0
// n0 -------------- n1
//    point-to-point
//
using namespace ns3;
using namespace std;

NS_LOG_COMPONENT_DEFINE ("TcpServer");
void MacTxCallback(std::string context,Ptr<const Packet> packet){
  NS_LOG_UNCOND("time:"<<Simulator::Now().GetSeconds()<<" size:"<<packet->GetSize()<<" "<<context);
}
void MacRxCallback(std::string context,Ptr<const Packet> packet){
  NS_LOG_UNCOND("time:"<<Simulator::Now().GetSeconds()<<" size:"<<packet->GetSize()<<" "<<context);
}
void RxPacketCall(std::string context,Ptr<const Packet> packet, const Address &address){
  NS_LOG_UNCOND ("At time " << Simulator::Now ().GetSeconds ()
                       << "s packet sink received "
                       <<  packet->GetSize () << " bytes from "
                       << InetSocketAddress::ConvertFrom(address).GetIpv4 ()
                       << " port " << InetSocketAddress::ConvertFrom (address).GetPort ()
                       );
}
int CountLines(string filename)
{
    ifstream ReadFile;
    int n=0;
    string tmp;
    ReadFile.open(filename,ios::in);//ios::in 表示以只读的方式读取文件
    if(ReadFile.fail())//文件打开失败:返回0
    {   
        cout<<"文件打开失败"<<endl;
        return 0;
    }
    else//文件存在
    {
        while(getline(ReadFile,tmp,'\n'))
        {
            n++;
        }
        ReadFile.close();
        return n;
    }
}
double delay_Matrix[1000][1000];
double error_Matrix[1000][1000];
int SMF_choose_Matrix[100][100];
int UPF_choose_Matrix[100][100];
int AMF_choose_Matrix[1000][100];
int Sat_Matrix[5000][5000];
int load_Matrix[100][100];
double rate_Matrix[1000][1000];
int logSwitch_amf = 0;
int logSwitch_smf = 0;
int logSwitch_upf = 0;
int logSwitch_client = 0;
//int delay[100][100];
int orbitsNum = 24;
int satsNum = 40;
int totalSatsNum = orbitsNum * satsNum;
int NFs_index[960][4];

extern string target_file_name;

int
main (int argc, char *argv[])
{
    time_t start_time = time(nullptr);
    
    int  slot = 0; 
    int  procedure_type = 0; 
    int  is_ground = 1;
    int rate_num = 800;
    int queue_num = 500;
    int packet_number = 100000;
    double packet_interval = 0.001;
    target_file_name = "/home/ubuntu/firstarticle/result_delay_of_client.txt";
    CommandLine cmd;
    cmd.AddValue("slot", "Time slot", slot);
    cmd.AddValue("rate", "rate", rate_num);
    cmd.AddValue("queue", "queue", queue_num);
    cmd.AddValue("procedure_type", "procedure_type", procedure_type);
    cmd.AddValue("is_ground", "is_ground", is_ground);
    cmd.AddValue("target_file_name", "target_file_name", target_file_name);
    cmd.AddValue("packet_number", "packet_number", packet_number);
    cmd.AddValue("packet_interval", "packet_interval", packet_interval);
    cmd.Parse (argc, argv);
    

    Time::SetResolution (Time::NS);
    LogComponentEnable ("XnAMFApplication", LOG_LEVEL_INFO);
    LogComponentEnable ("XnSMFApplication", LOG_LEVEL_INFO);
    LogComponentEnable ("XnUPFApplication", LOG_LEVEL_INFO);
    LogComponentEnable ("XnClientApplication", LOG_LEVEL_INFO);

    cout<<"Time slot="<<slot<<endl;
    cout<<"rate="<<rate_num<<endl;
    cout<<"queue="<<queue_num<<endl;
    cout<<"procedure_type="<<procedure_type<<"  (0-xn 1-sr 2-n2 3-se)  "<<endl;
    cout<<"is_ground="<<is_ground<<"  (0-NSGA 1-Ground)  "<<endl;
    cout<<"target_file_name="<<target_file_name<<"  (default:/home/ubuntu/firstarticle/result_delay_of_client.txt)  "<<endl;
    cout<<"packet_number="<<packet_number<<endl;
    cout<<"packet_interval="<<packet_interval<<endl;
    ofstream file_writer(target_file_name, ios_base::out);

    int send_packet_size = 160;
    switch (procedure_type)
    {
    case 0:
        send_packet_size = 160;
        break;
    case 1:
        send_packet_size = 166;
        break;
    case 2:
        send_packet_size = 1630;
        break;
    case 3:
        send_packet_size = 238;
        break;
    }
    int near_core_sat[24][5]= 
        {{696, 737, 535, 577, 658},
        {791, 832, 630, 672, 753},
        {846, 887, 686, 727, 808},
        {941, 9, 781, 822, 904},
        {65, 104, 876, 918, 23},
        {121, 160, 931, 39, 118},
        {216, 255, 56, 95, 174},
        {311, 350, 152, 190, 269},
        {366, 405, 207, 245, 324},
        {462, 501, 302, 340, 419},
        {557, 596, 397, 436, 515},
        {612, 651, 453, 491, 570},
        {707, 746, 548, 586, 665},
        {763, 802, 603, 641, 720},
        {858, 897, 698, 737, 816},
        {953, 5, 794, 832, 911},
        {60, 100, 849, 887, 62},
        {155, 196, 944, 36, 157},
        {210, 251, 50, 91, 212},
        {305, 346, 145, 186, 307},
        {361, 401, 200, 242, 363},
        {456, 497, 295, 337, 458},
        {551, 592, 391, 432, 553},
        {606, 647, 486, 487, 608},
        };

    // vector<int> amf_location{797, 354, 792, 61, 52, 609, 657, 337, 807, 893, 449, 365, 251, 271, 600, 210, 148, 117, 554, 87, 298, 163, 838, 903, 174, 506, 561, 695, 465, 91, 568, 845, 576, 593};
    // vector<int> smf_location{601, 353, 791, 60, 51, 608, 656, 902, 806, 173, 260, 364, 250, 505, 837, 853, 147, 116, 553, 162, 297, 409, 244, 311, 545, 88};
    // vector<int> upf_location{602, 552, 790, 59, 50, 607, 655, 901, 805, 172, 296, 161, 249, 504, 836, 852, 146, 115, 529, 404, 352};
    vector<int> amf_location{648, 656, 148, 670, 184, 244, 227, 752, 173, 435, 188};
    vector<int> smf_location{751, 647, 655, 187, 902, 434, 243, 702, 174};
    vector<int> upf_location{750, 646, 654, 186, 283, 433, 214};
    vector<int> ground_core_location(near_core_sat[slot],near_core_sat[slot]+5);
    


    // int amf_chose_smf[] = { 14, 1, 2, 3, 4, 5, 6, 20, 8, 15, 5, 11, 12, 23, 0, 25, 16, 17, 18, 25, 20, 19, 14, 7, 9, 13, 0, 6, 13, 4, 5, 8, 6, 18};
    // int smf_chose_upf[] = { 0, 20, 2, 3, 4, 5, 6, 7, 8, 9, 10, 19, 12, 13, 14, 15, 16, 17, 1, 11, 10, 18, 19, 20, 13, 12};
    // int smf_chose_ground[] = {2, 4, 4, 2, 2, 2, 0, 1, 0, 2, 3, 2, 2, 3, 0, 0, 4, 4, 4, 2, 3, 2, 2, 4, 3, 2};
    int amf_chose_smf[] = { 1, 2, 3, 0, 3, 6, 3, 0, 8, 5, 3};
    int smf_chose_upf[] = { 0, 1, 2, 3, 0, 5, 4, 0, 6};
    int smf_chose_ground[] = {4, 2, 0, 4, 1, 4, 2, 4, 2};


    int upf_number = upf_location.size();
    int smf_number = smf_location.size();
    int amf_number = amf_location.size();
    int ground_core_number = ground_core_location.size();
    std::cout<<"amf_number"<<amf_number<<"  smf_number="<<smf_number<<"  upf_number"<<upf_number<<std::endl;

    

    int LINES;
    int cols;  
    cout<<"read Delay_Matrix_origin"<<endl;
    ifstream file;
    string filename = "/home/ubuntu/firstarticle/data/" +std::to_string(slot)+ "Delay_Matrix_origin.txt";
    file.open(filename,ios::in);
    LINES=CountLines(filename);
    cols= LINES;
    int num=0;
    while(!file.eof()) //读取数据到数组
    {
        for(int i=0;i<cols;i++)
        {   if(i<cols) {
                file >> delay_Matrix[num][i];
            }
        }
        num++;
    }
    file.close();

    //将人数矩阵读入
    cout<<"read Sat_load"<<endl;
    ifstream file3;
    string filename3="/home/ubuntu/firstarticle/sat_load/Sat_load" +to_string(slot)+ ".txt";
    file3.open(filename3,ios::in);
    LINES=CountLines(filename3);
    cols= orbitsNum;
    num=0;
    while(!file3.eof()) //读取数据到数组
    {
        for(int i=0;i<cols;i++)
        {   if(i<cols) {
                file3 >> load_Matrix[num][i];
            }
        }
        num++;
    }
    file3.close();

    
    ifstream file4;
    string filename4;
    if(is_ground)
    {
        filename4 = "/home/ubuntu/firstarticle/order_ground/" +to_string(slot)+ "order.txt";
        cout<<"read order_ground"<<endl;
    }
    else
    {
        filename4 = "/home/ubuntu/firstarticle/order_Nsga/" +to_string(slot)+ "order.txt";
        cout<<"read order_Nsga"<<endl;
    }

    
    file4.open(filename4,ios::in);
    LINES=CountLines(filename4);
    // cout<<"The number of 0order lines is:"<<LINES<<endl;
    cols= 4;
    num=0;
    while(!file4.eof()) //读取数据到数组
    {
        for(int i=0;i<cols;i++)
        {   if(i<cols) {
                file4 >> NFs_index[num][i];
            }
        }
        num++;
    }
    file4.close();

    
    cout<<"create topology"<<endl;
    //所有节点
    cout<<"总节点数量: "<<totalSatsNum*2+amf_number+smf_number+upf_number+ground_core_number<<endl;
    NodeContainer nodes;
    nodes.Create (totalSatsNum*2+amf_number+smf_number+upf_number+ground_core_number);
    
    InternetStackHelper stack;
    
    Ipv4NixVectorHelper nixRouting;
    stack.SetRoutingHelper (nixRouting);

    stack.Install (nodes);
    Ipv4AddressHelper address;

    //卫星网络建立
    NodeContainer node[10000];
    PointToPointHelper pointToPoint[10000];
    NetDeviceContainer devices[10000];
    Ipv4InterfaceContainer interfaces[10000];
    Ptr<RateErrorModel>em=CreateObject<RateErrorModel> ();
    //创建信道数n
    for(int n =0,m=0,z=10, i=0;i<totalSatsNum;i++)
    {
        for(int j=i;j<totalSatsNum;j++)
        {
            if(delay_Matrix[i][j]!=0)
            {
                //符合条件进入设置一对点到点信道
                //将构成当前信道的两点放入容器中
                // j 列 i 行
                node[n].Add(nodes.Get(i));
                node[n].Add(nodes.Get(j));
                //准备设置该信道的信道参数
                //将时延读出并以字符串的形式读到delay_num中
                double delay_num = 1.0/delay_Matrix[i][j];
                //cout<<"第"<<n<<"条信道时延"<<de<<endl;
                string delay = to_string(delay_num)+ "s";            
                //cout<<"第"<<n<<"个信道的延时是"<<delay<<endl;
                //读出当前链路带宽
                // double rate_num = rate_Matrix[i][j]/500000000;                          
                string rate = to_string(rate_num) + "Mbps";
                string queue = to_string(queue_num) + "p";
                //cout<<rate<<endl;
                //将时延已经数据传输速率传入当前信道中
                pointToPoint[n].SetDeviceAttribute("DataRate", StringValue (rate));
                pointToPoint[n].SetChannelAttribute ("Delay", StringValue (delay.c_str()));
                pointToPoint[n].SetQueue ("ns3::DropTailQueue", "MaxSize", StringValue (queue)); 
                //将此信道的两点装上网络设备 完成信道网络设备的安装
                devices[n] = pointToPoint[n].Install(node[n]);                
                //添加错误概率
                Ptr<RateErrorModel>em=CreateObject<RateErrorModel> ();
                em->SetAttribute("ErrorRate",DoubleValue(0));
                devices[n].Get(1)->SetAttribute("ReceiveErrorModel",PointerValue (em));  
                //给刚生成的卫星节点的网络设备分配地址
                if(m==256)
                {
                    z += 1;
                    m = 0;
                }
                string address_string("10.");
                address_string.append(to_string(z));
                address_string.append(".");
                address_string.append(to_string(m));
                address_string.append(".0");
                //cout<<"第"<<n<<"条信道地址"<<address_string<<endl;
                string mask_string("255.255.255.0");
                address.SetBase (ns3::Ipv4Address(address_string.c_str()),ns3::Ipv4Mask(mask_string.c_str()));
                interfaces[n] = address.Assign (devices[n]);
                
                //n+1表示已经完成了一个信道（包括两点容器，两点信道以及网络设备）
                n++;
                m++;
            }
        }
    }
    //建立客户端节点
    NodeContainer node_client[2000];
    PointToPointHelper pointToPoint_client;
    NetDeviceContainer devices_client[2000];
    Ipv4InterfaceContainer interfaces_client[2000];
    ApplicationContainer clientApps;
    for(int n=0, m=0,z=6,j=totalSatsNum;j<totalSatsNum*2;j++)
    {
           
        //i是卫星
        node_client[n].Add(nodes.Get(j-totalSatsNum));
        //j是客户端
        node_client[n].Add(nodes.Get(j));
        pointToPoint_client.SetDeviceAttribute("DataRate", StringValue ("10000000Mbps"));
        pointToPoint_client.SetChannelAttribute ("Delay", StringValue ("0.01ms"));
        pointToPoint_client.SetQueue ("ns3::DropTailQueue", "MaxSize", StringValue ("99999999p")); 
        devices_client[n] = pointToPoint_client.Install(node_client[n]);
        //给生成的客户端节点的网络设备分配ip
        if(m==255)
        {
            z+=1;
            m=0;
        }
        string address_string("10.");
        address_string.append(to_string(z));
        address_string.append(".");
        address_string.append(to_string(m));//从10.6.0.0开始
        address_string.append(".0");
        string mask_string("255.255.255.0");
        address.SetBase (ns3::Ipv4Address(address_string.c_str()),ns3::Ipv4Mask(mask_string.c_str()));
        interfaces_client[n] = address.Assign (devices_client[n]);    
        n++;   
        m++;

    }
    NodeContainer node_AMF[100];
    PointToPointHelper pointToPoint_AMF;
    NetDeviceContainer devices_AMF[100];
    Ipv4InterfaceContainer interfaces_AMF[100];
    ApplicationContainer AMFApps;

    //建立SMF节点
    NodeContainer node_SMF[100];
    PointToPointHelper pointToPoint_SMF;
    NetDeviceContainer devices_SMF[100];
    Ipv4InterfaceContainer interfaces_SMF[100];
    ApplicationContainer SMFApps;

    NodeContainer node_UPF[100];
    PointToPointHelper pointToPoint_UPF;
    NetDeviceContainer devices_UPF[100];
    Ipv4InterfaceContainer interfaces_UPF[100];
    ApplicationContainer UPFApps;

    NodeContainer node_GROUND[100];
    PointToPointHelper pointToPoint_GROUND;
    NetDeviceContainer devices_GROUND[100];
    Ipv4InterfaceContainer interfaces_GROUND[100];
    ApplicationContainer GROUNDApps;
    //  建立GROUND节点 
    for(int n=0, j=0;j<ground_core_number;j++)
    {   
        //i是卫星
        node_GROUND[n].Add(nodes.Get(ground_core_location[j]));
        //j是AMF
        node_GROUND[n].Add(nodes.Get(totalSatsNum*2+amf_number+smf_number+upf_number+j));
        pointToPoint_GROUND.SetDeviceAttribute("DataRate", StringValue (to_string(rate_num) + "Mbps"));
        pointToPoint_GROUND.SetChannelAttribute ("Delay", StringValue ("4ms"));
        pointToPoint_GROUND.SetQueue ("ns3::DropTailQueue", "MaxSize", StringValue (to_string(queue_num) + "p")); 
        devices_GROUND[n] = pointToPoint_GROUND.Install(node_GROUND[n]);
        //em->SetAttribute("ErrorRate",DoubleValue(error_Matrix[i][cols-1]));
        //device_server.Get(1)->SetAttribute("ReceiveErrorModel",PointerValue (em)); 
        //给生成的UPF节点的网络设备分配ip
        string address_string("10.88.");
        address_string.append(to_string(n));
        address_string.append(".0");
        string mask_string("255.255.255.0");
        address.SetBase (ns3::Ipv4Address(address_string.c_str()),ns3::Ipv4Mask(mask_string.c_str()));
        interfaces_GROUND[n] = address.Assign (devices_GROUND[n]);   
        // 给每个UPF安装应用
        XnUPFHelper UPF (9);
        UPF.SetAttribute ("UPFNumber", UintegerValue (n));
        UPF.SetAttribute ("OpenLog", UintegerValue (logSwitch_upf));
        GROUNDApps = UPF.Install (node_GROUND[n].Get (1));
        // cout<<n<<interfaces_GROUND[0].GetAddress (1)<<endl;
        n++;            
    }

    if(!is_ground)
    {
        for(int n=0, j=0;j<amf_number;j++)
        {
            //i是卫星
            node_AMF[n].Add(nodes.Get(amf_location[j]));
            //j是AMF
            node_AMF[n].Add(nodes.Get(totalSatsNum*2+j));
            pointToPoint_AMF.SetDeviceAttribute("DataRate", StringValue ("10000000Mbps"));
            pointToPoint_AMF.SetChannelAttribute ("Delay", StringValue ("0.01ms"));
            pointToPoint_AMF.SetQueue ("ns3::DropTailQueue", "MaxSize", StringValue ("99999999p")); 
            devices_AMF[n] = pointToPoint_AMF.Install(node_AMF[n]);
            //em->SetAttribute("ErrorRate",DoubleValue(error_Matrix[i][cols-1]));
            //device_server.Get(1)->SetAttribute("ReceiveErrorModel",PointerValue (em));        
            //给生成的AMF节点的网络设备分配ip
            string address_string("10.5.");
            address_string.append(to_string(n));
            address_string.append(".0");
            string mask_string("255.255.255.0");
            address.SetBase (ns3::Ipv4Address(address_string.c_str()),ns3::Ipv4Mask(mask_string.c_str()));
            interfaces_AMF[n] = address.Assign (devices_AMF[n]);                               
            n++;                
        }
    
        for(int n=0, j=0;j<smf_number;j++)
        {
            //i是卫星
            node_SMF[n].Add(nodes.Get(smf_location[j]));
            node_SMF[n].Add(nodes.Get(totalSatsNum*2+amf_number+j));
            pointToPoint_SMF.SetDeviceAttribute("DataRate", StringValue ("10000000Mbps"));
            pointToPoint_SMF.SetChannelAttribute ("Delay", StringValue ("0.01ms"));
            pointToPoint_SMF.SetQueue ("ns3::DropTailQueue", "MaxSize", StringValue ("99999999p")); 
            devices_SMF[n] = pointToPoint_SMF.Install(node_SMF[n]);
            //em->SetAttribute("ErrorRate",DoubleValue(error_Matrix[i][cols-1]));
            //device_server.Get(1)->SetAttribute("ReceiveErrorModel",PointerValue (em));        
            //给生成的AMF节点的网络设备分配ip
            string address_string("10.4.");
            address_string.append(to_string(n));
            address_string.append(".0");
            string mask_string("255.255.255.0");
            address.SetBase (ns3::Ipv4Address(address_string.c_str()),ns3::Ipv4Mask(mask_string.c_str()));
            interfaces_SMF[n] = address.Assign (devices_SMF[n]);   
            n++;
        }
        for(int n=0, j=0;j<upf_number;j++)
        {   
            //i是卫星
            node_UPF[n].Add(nodes.Get(upf_location[j]));
            node_UPF[n].Add(nodes.Get(totalSatsNum*2+amf_number+smf_number+j));
            pointToPoint_UPF.SetDeviceAttribute("DataRate", StringValue ("10000000Mbps"));
            pointToPoint_UPF.SetChannelAttribute ("Delay", StringValue ("0.01ms"));
            pointToPoint_UPF.SetQueue ("ns3::DropTailQueue", "MaxSize", StringValue ("99999999p")); 
            devices_UPF[n] = pointToPoint_UPF.Install(node_UPF[n]);
            //em->SetAttribute("ErrorRate",DoubleValue(error_Matrix[i][cols-1]));
            //device_server.Get(1)->SetAttribute("ReceiveErrorModel",PointerValue (em));  
            //给生成的UPF节点的网络设备分配ip
            string address_string("10.3.");
            address_string.append(to_string(n));
            address_string.append(".0");
            string mask_string("255.255.255.0");
            address.SetBase (ns3::Ipv4Address(address_string.c_str()),ns3::Ipv4Mask(mask_string.c_str()));
            interfaces_UPF[n] = address.Assign (devices_UPF[n]);   
            // 给每个UPF安装应用
            XnUPFHelper UPF (9);
            UPF.SetAttribute ("UPFNumber", UintegerValue (n));
            UPF.SetAttribute ("OpenLog", UintegerValue (logSwitch_upf));
            UPFApps = UPF.Install (node_UPF[n].Get (1));
            // cout<<n<<interfaces_UPF[0].GetAddress (1)<<endl;
            n++; 
        }
        for(int n=0;n<smf_number;n++)
        {
            //给每个SMF安装应用
            XnSMFHelper SMF (interfaces_UPF[smf_chose_upf[n]].GetAddress (1), 9);
            SMF.SetAttribute ("SMFNumber", UintegerValue (n));
            SMF.SetAttribute ("Ground_address",AddressValue (interfaces_GROUND[smf_chose_ground[n]].GetAddress(1)));
            SMF.SetAttribute ("OpenLog", UintegerValue (logSwitch_smf));
            SMFApps = SMF.Install (node_SMF[n].Get (1));
        }
        for(int n=0;n<amf_number;n++)
        {
            XnAMFHelper AMF (interfaces_SMF[amf_chose_smf[n]].GetAddress (1), 9);
            AMF.SetAttribute ("AMFNumber", UintegerValue (n));
            AMF.SetAttribute ("OpenLog", UintegerValue (logSwitch_amf));
            AMFApps = AMF.Install (node_AMF[n].Get(1));
        }

    }

    if(is_ground)
    {
        for(int y=0,n=0,i=0;y<orbitsNum;y++)
        {
            for(int x=0;x<satsNum;x++)
            {   
                XnClientHelper Client (interfaces_GROUND[NFs_index[i][0]].GetAddress(1), 9);
                Client.SetAttribute ("MaxPackets", UintegerValue (max(int(load_Matrix[x][y]/packet_number),1)));
                Client.SetAttribute ("ClientNumber",UintegerValue (n));
                Client.SetAttribute ("Interval",TimeValue (Seconds (packet_interval)));
                Client.SetAttribute ("PacketSize",UintegerValue (send_packet_size));
                Client.SetAttribute ("OpenLog", UintegerValue (logSwitch_client));      
                Client.SetAttribute ("BeginTime",UintegerValue (2));
                //Client.SetAttribute ("ClientLoad",UintegerValue (load_Matrix[x][y]));
                clientApps = Client.Install (node_client[n].Get(1));
                n++;
                i++;
            }
        }
    }
    else
    {
        for(int y=0,n=0,i=0;y<orbitsNum;y++)
        {
            for(int x=0;x<satsNum;x++)
            {   
                XnClientHelper Client (interfaces_AMF[NFs_index[i][0]].GetAddress(1), 9);
                Client.SetAttribute ("MaxPackets", UintegerValue (max(int(load_Matrix[x][y]/packet_number),1)));
                Client.SetAttribute ("ClientNumber",UintegerValue (n));
                Client.SetAttribute ("Interval",TimeValue (Seconds (packet_interval)));
                Client.SetAttribute ("PacketSize",UintegerValue (send_packet_size));
                Client.SetAttribute ("OpenLog", UintegerValue (0));      
                Client.SetAttribute ("BeginTime",UintegerValue (2));
                //Client.SetAttribute ("ClientLoad",UintegerValue (load_Matrix[x][y]));
                clientApps = Client.Install (node_client[n].Get(1));
                n++;
                i++;
            }
        }
    }    

    // std::cout<<"start routing"<<std::endl;
    // Ipv4GlobalRoutingHelper::PopulateRoutingTables ();
    // time_t end_time_of_routing = time(nullptr);
    // std::cout<<"time for routing"<<end_time_of_routing-start_time<<std::endl;
    std::cout<<"Start All Apps"<<std::endl;

    AMFApps.Start (Seconds (1.0));
    AMFApps.Stop (Seconds (210.0));

    SMFApps.Start (Seconds (1.0));
    SMFApps.Stop (Seconds (205.0));

    UPFApps.Start (Seconds (1.0));
    UPFApps.Stop (Seconds (200.0));

    
    clientApps.Start (Seconds (1.0));
    clientApps.Stop (Seconds (230.0));

    //pointToPoint_client.EnablePcapAll ("pcap_data/SatelliteNet");    
    // Ptr<FlowMonitor> flowMonitor;
    // FlowMonitorHelper flowHelper;
    // flowMonitor = flowHelper.InstallAll();
    // AsciiTraceHelper ascii;
    // Ptr<OutputStreamWrapper> stream = ascii.CreateFileStream ("SatelliteNet.tr");
    // pointToPoint_client.EnableAsciiAll (stream);
    Simulator::Stop (Seconds(230.0));
    Simulator::Run ();
    // flowMonitor->SerializeToXmlFile("NameOfFile.xml", true, true);
    Simulator::Destroy ();
    NS_LOG_INFO ("Done.");
    time_t end_time_of_simulation = time(nullptr);
    std::cout<<"time for simulation"<<end_time_of_simulation-start_time<<std::endl;
    return 0;
}
    // ifstream file7;
    // char filename7[512]="/home/ubuntu/firstarticle/data/0Rate_Matrix.txt";
    // file7.open(filename7,ios::in);
    // LINES=CountLines(filename7);
    // cols= LINES;
    // num=0;
    // while(!file7.eof()) //读取数据到数组
    // {
    //     for(int i=0;i<cols;i++)
    //     {   if(i<cols) {
    //             file7 >> rate_Matrix[num][i];
    //         }
    //     }
    //     num++;
    // }
    // file7.close();  