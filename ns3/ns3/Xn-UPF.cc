#include "ns3/log.h"
#include "ns3/ipv4-address.h"
#include "ns3/ipv6-address.h"
#include "ns3/address-utils.h"
#include "ns3/nstime.h"
#include "ns3/inet-socket-address.h"
#include "ns3/inet6-socket-address.h"
#include "ns3/socket.h"
#include "ns3/udp-socket.h"
#include "ns3/simulator.h"
#include "ns3/socket-factory.h"
#include "ns3/packet.h"
#include "seq-ts-header.h"
#include "ns3/uinteger.h"

#include "Xn-UPF.h"
#include <time.h>
#include <vector>
#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#include <unistd.h>
using namespace std;
extern string target_file_name;
namespace ns3 {

NS_LOG_COMPONENT_DEFINE ("XnUPFApplication");

NS_OBJECT_ENSURE_REGISTERED (XnUPF);


TypeId
XnUPF::GetTypeId (void)
{
  static TypeId tid = TypeId ("ns3::XnUPF")
    .SetParent<Application> ()
    .SetGroupName("Applications")
    .AddConstructor<XnUPF> ()
    .AddAttribute ("Port", "Port on which we listen for incoming packets.",
                   UintegerValue (9),
                   MakeUintegerAccessor (&XnUPF::m_port),
                   MakeUintegerChecker<uint16_t> ())
    .AddAttribute ("UPFNumber", 
                   "The maximum number of packets the application will send",
                   UintegerValue (),
                   MakeUintegerAccessor (&XnUPF::m_number),
                   MakeUintegerChecker<uint16_t> ())
    .AddAttribute ("OpenLog", 
                   "open the NS_LOG_INFO",
                   UintegerValue (0),
                   MakeUintegerAccessor (&XnUPF::log_open),
                   MakeUintegerChecker<uint16_t>())
    .AddTraceSource ("Rx", "A packet has been received",
                     MakeTraceSourceAccessor (&XnUPF::m_rxTrace),
                     "ns3::Packet::TracedCallback")
    .AddTraceSource ("RxWithAddresses", "A packet has been received",
                     MakeTraceSourceAccessor (&XnUPF::m_rxTraceWithAddresses),
                     "ns3::Packet::TwoAddressTracedCallback")
  ;
  return tid;
}

XnUPF::XnUPF ()
{
  NS_LOG_FUNCTION (this);
  p_num = 1;
  cout<<"read ns3 process time nfs"<<endl;

  int n=0;
  ifstream file_nf;
  string filename3="/home/ubuntu/firstarticle/ns3_process_time_nfs.txt";
  file_nf.open(filename3,ios::in);
  string tmp;
  if(file_nf.fail())//文件打开失败:返回0
    {   
        cout<<"文件打开失败"<<endl;
    }
  while(getline(file_nf,tmp,'\n'))
  {
      n++;
  }
  file_nf.close();

  
  file_nf.open(filename3,ios::in);
  for (int k = 0; k < 3; k++)//定义行循环
	{
		for(int i=0;i<n;i++)
      {   
        if(i<n) {
              file_nf >> NF_process_time[k][i];
          }
      }
	}
  file_nf.close();
}

XnUPF::~XnUPF()
{
  NS_LOG_FUNCTION (this);
  m_socket = 0;
  m_socket6 = 0;
  
}

void
XnUPF::DoDispose (void)
{
  NS_LOG_FUNCTION (this);
  Application::DoDispose ();
}

void 
XnUPF::StartApplication (void)
{
  NS_LOG_FUNCTION (this);
  //先创建并绑定自己的socket
  if (m_socket == 0)
    {
      TypeId tid = TypeId::LookupByName ("ns3::UdpSocketFactory");
      m_socket = Socket::CreateSocket (GetNode (), tid);
      InetSocketAddress local = InetSocketAddress (Ipv4Address::GetAny (), m_port);
      if (m_socket->Bind (local) == -1)
        {
          NS_FATAL_ERROR ("Failed to bind socket");
        }
      if (addressUtils::IsMulticast (m_local))
        {
          Ptr<UdpSocket> udpSocket = DynamicCast<UdpSocket> (m_socket);
          if (udpSocket)
            {
              // equivalent to setsockopt (MCAST_JOIN_GROUP)
              udpSocket->MulticastJoinGroup (0, m_local);
            }
          else
            {
              NS_FATAL_ERROR ("Error: Failed to join multicast group");
            }
        }
    }

  if (m_socket6 == 0)
    {
      TypeId tid = TypeId::LookupByName ("ns3::UdpSocketFactory");
      m_socket6 = Socket::CreateSocket (GetNode (), tid);
      Inet6SocketAddress local6 = Inet6SocketAddress (Ipv6Address::GetAny (), m_port);
      if (m_socket6->Bind (local6) == -1)
        {
          NS_FATAL_ERROR ("Failed to bind socket");
        }
      if (addressUtils::IsMulticast (local6))
        {
          Ptr<UdpSocket> udpSocket = DynamicCast<UdpSocket> (m_socket6);
          if (udpSocket)
            {
              // equivalent to setsockopt (MCAST_JOIN_GROUP)
              udpSocket->MulticastJoinGroup (0, local6);
            }
          else
            {
              NS_FATAL_ERROR ("Error: Failed to join multicast group");
            }
        }
    }

  m_socket->SetRecvCallback (MakeCallback (&XnUPF::HandleRead, this));
  m_socket6->SetRecvCallback (MakeCallback (&XnUPF::HandleRead, this));
}

void 
XnUPF::StopApplication ()
{
  NS_LOG_FUNCTION (this);

  if (m_socket != 0) 
    {
      m_socket->Close ();
      m_socket->SetRecvCallback (MakeNullCallback<void, Ptr<Socket> > ());
    }
  if (m_socket6 != 0) 
    {
      m_socket6->Close ();
      m_socket6->SetRecvCallback (MakeNullCallback<void, Ptr<Socket> > ());
    }
}

void 
XnUPF::HandleRead (Ptr<Socket> socket)
{
  NS_LOG_FUNCTION (this << socket);

  Ptr<Packet> packet;
  Address from;
  Address localAddress;
  //Address source_address;
  
  // while ((packet = socket->RecvFrom (from)))
  //   {
  //     socket->GetSockName (localAddress);
  //     m_rxTrace (packet);
  //     m_rxTraceWithAddresses (packet, from, localAddress);
  //     if (InetSocketAddress::IsMatchingType (from))
  //       {
  //         NS_LOG_INFO ("At time " << Simulator::Now ().As (Time::S) << " server received " << packet->GetSize () << " bytes from " <<
  //                      InetSocketAddress::ConvertFrom (from).GetIpv4 () << " port " <<
  //                      InetSocketAddress::ConvertFrom (from).GetPort ());
  //       }
  //     else if (Inet6SocketAddress::IsMatchingType (from))
  //       {
  //         NS_LOG_INFO ("At time " << Simulator::Now ().As (Time::S) << " server received " << packet->GetSize () << " bytes from " <<
  //                      Inet6SocketAddress::ConvertFrom (from).GetIpv6 () << " port " <<
  //                      Inet6SocketAddress::ConvertFrom (from).GetPort ());
  //       }

  //     packet->RemoveAllPacketTags ();
  //     packet->RemoveAllByteTags ();

  //     NS_LOG_LOGIC ("Echoing packet");
  //     socket->SendTo (packet, 0, from);

      // if (InetSocketAddress::IsMatchingType (from))
      //   {
      //     NS_LOG_INFO ("At time " << Simulator::Now ().As (Time::S) << " server sent " << packet->GetSize () << " bytes to " <<
      //                  InetSocketAddress::ConvertFrom (from).GetIpv4 () << " port " <<
      //                  InetSocketAddress::ConvertFrom (from).GetPort ());
      //   }
  //     else if (Inet6SocketAddress::IsMatchingType (from))
  //       {
  //         NS_LOG_INFO ("At time " << Simulator::Now ().As (Time::S) << " server sent " << packet->GetSize () << " bytes to " <<
  //                      Inet6SocketAddress::ConvertFrom (from).GetIpv6 () << " port " <<
  //                      Inet6SocketAddress::ConvertFrom (from).GetPort ());
  //       }
  //   }
  
  while ((packet = socket->RecvFrom (from)))
    { 
      if(log_open==1){
      if (InetSocketAddress::IsMatchingType (from))
        {
          NS_LOG_INFO ("At time " << Simulator::Now ().As (Time::S) << "  "<<m_number<<" XnUPF received " << packet->GetSize () << " bytes from " <<
                       InetSocketAddress::ConvertFrom (from).GetIpv4 () << " port " <<
                       InetSocketAddress::ConvertFrom (from).GetPort ());
        }
      else if (Inet6SocketAddress::IsMatchingType (from))
        {
          NS_LOG_INFO ("At time " << Simulator::Now ().As (Time::S) << "  "<<m_number<<" XnUPF received " << packet->GetSize () << " bytes from " <<
                       Inet6SocketAddress::ConvertFrom (from).GetIpv6 () << " port " <<
                       Inet6SocketAddress::ConvertFrom (from).GetPort ());
        }
      }
      if (packet->GetSize () > 0)
        {
          uint32_t receivedSize = packet->GetSize ();
          
          SeqTsHeader seqTs;
          Time delay;
          packet->RemoveHeader (seqTs);
          //从包中提取负载信息
          //先取出所有信息
          uint8_t data[255];
          packet->CopyData(data,sizeof(data));//将包内数据写入到data内
          char a[sizeof(data)];
          for(uint32_t i=0;i<sizeof(data);i++){
              a[i]=data[i];
          }
          string strres = string(a);
          // //cout<<strres<<endl;
          // //找到空格位置（分界位置）
          // int pos = strres.find(" ");
          // string load_info = strres.substr(pos+1,sizeof(data));
          // p_num = atoi(load_info.c_str());
          // //cout<<p_num<<endl;
          // uint32_t per_receivedSize = receivedSize/p_num;
          //uint32_t currentSequenceNumber = seqTs.GetSeq ();
          if (InetSocketAddress::IsMatchingType (from))
            {
              // NS_LOG_INFO ("TraceDelay: RX " << receivedSize <<
              //              " bytes from "<< InetSocketAddress::ConvertFrom (from).GetIpv4 () <<
              //              " Sequence Number: " << currentSequenceNumber <<
              //              " Uid: " << packet->GetUid () <<
              //              " TXtime: " << seqTs.GetTs () <<
              //              " RXtime: " << Simulator::Now () <<
              //              " Delay: " << Simulator::Now () - seqTs.GetTs ());
                // if(i==0)
                // {
                //   source_address = from;
                // }
                // source_address = from;
                switch(receivedSize)
                {   
                  // XN
                  case 142:
                      {
                        usleep(NF_process_time[0][m_number]*1000);
                        uint8_t buffer[73-12];
                        uint32_t len = strres.length();
                        for(uint32_t i=0;i<len;i++)
                        {
                          buffer[i]=strres[i];//char 与 uint_8逐个赋值
                        }
                        buffer[len]='\0';
                        //InetSocketAddress dest_address = InetSocketAddress(strres.c_str(),9);

                        
                        
                        Ptr<Packet> ack_packet3 = Create<Packet>(buffer,sizeof(buffer));
                        ack_packet3->AddHeader(seqTs);
                        socket->GetSockName (localAddress);
                        m_rxTrace (ack_packet3);
                        m_rxTraceWithAddresses (ack_packet3, from, localAddress);
                        NS_LOG_LOGIC ("Echoing packet");
                        socket->SendTo (ack_packet3, 0, from);
                        if (log_open==1)
                          {
                          NS_LOG_INFO ("At time " << Simulator::Now ().As (Time::S) << "  "<<m_number<<" UPF sent " << ack_packet3->GetSize () << " bytes to " <<
                          InetSocketAddress::ConvertFrom (from).GetIpv4 () << " port " <<
                          InetSocketAddress::ConvertFrom (from).GetPort ());
                          }                        
                      }
                      break;
                      // ---------------------Xn-------------------------------------------
                  // ---------------------地面  Xn-------------------------------------------
                  case 160:
                      {
                        uint8_t buffer[139-12];
                        uint32_t len = strres.length();
                        for(uint32_t i=0;i<len;i++)
                        {
                          buffer[i]=strres[i];//char 与 uint_8逐个赋值
                        }
                        buffer[len]='\0';
                        Ptr<Packet> ack_packet3 = Create<Packet>(buffer,sizeof(buffer));
                        ack_packet3->AddHeader(seqTs);
                        socket->GetSockName (localAddress);
                        m_rxTrace (ack_packet3);
                        m_rxTraceWithAddresses (ack_packet3, from, localAddress);
                        NS_LOG_LOGIC ("Echoing packet");
                        socket->SendTo (ack_packet3, 0, from);
                        if (log_open==1)
                        {
                          NS_LOG_INFO ("At time " << Simulator::Now ().As (Time::S) << "  "<<m_number<<" UPF sent " << ack_packet3->GetSize () << " bytes to " <<
                          InetSocketAddress::ConvertFrom (from).GetIpv4 () << " port " <<
                          InetSocketAddress::ConvertFrom (from).GetPort ());
                        }
                      }
                      break;
                      // ---------------------地面  Xn-------------------------------------------

                      // ---------------------地面 sr-------------------------------------------
                  case 166:
                      {
                        uint8_t buffer[1478-12];
                        uint32_t len = strres.length();
                        for(uint32_t i=0;i<len;i++)
                        {
                          buffer[i]=strres[i];//char 与 uint_8逐个赋值
                        }
                        buffer[len]='\0';
                        Ptr<Packet> ack_packet3 = Create<Packet>(buffer,sizeof(buffer));
                        ack_packet3->AddHeader(seqTs);
                        socket->GetSockName (localAddress);
                        m_rxTrace (ack_packet3);
                        m_rxTraceWithAddresses (ack_packet3, from, localAddress);
                        NS_LOG_LOGIC ("Echoing packet");
                        socket->SendTo (ack_packet3, 0, from);
                        if (log_open==1)
                        {
                          NS_LOG_INFO ("At time " << Simulator::Now ().As (Time::S) << "  "<<m_number<<" UPF sent " << ack_packet3->GetSize () << " bytes to " <<
                          InetSocketAddress::ConvertFrom (from).GetIpv4 () << " port " <<
                          InetSocketAddress::ConvertFrom (from).GetPort ());
                        }
                      }
                      break;
                      // 模拟地面Sr
                    case 118:
                      {
                        vector<string>   destVect;
                        string strFlag = ".";
                         int pos = strres.find(strFlag, 0);
                        int startPos = 0;
                        int splitN = pos;
                        string lineText(strFlag);
                        while (pos > -1)
                        {
                            lineText = strres.substr(startPos, splitN);
                            startPos = pos + 1;
                            pos = strres.find(strFlag, pos + 1);
                            splitN = pos - startPos;
                            destVect.push_back(lineText);
                        }
                        lineText = strres.substr(startPos, strres.length() - startPos);
                        destVect.push_back(lineText);
                        // std::cout<<destVect[0]<<std::endl;
                        // std::cout<<destVect[1]<<std::endl;
                        // std::cout<<destVect[2]<<std::endl;
                        // std::cout<<destVect[3]<<std::endl;
                        int client_number = (stoi(destVect[1])-6)*256+stoi(destVect[2]);
                        // std::vector<string> res = std::split(strres, ".");
                           delay = Simulator::Now () - seqTs.GetTs ();
                           ofstream wfile;
                           wfile.open(target_file_name,ios::app);
                           wfile << client_number<<delay.As (Time::MS)<<"; ";//写入修改内容
	                        wfile.close();
                      }
                      break;
                      // ---------------------地面 sr-------------------------------------------


                      // --------------------sr-------------------------------------------
                      case 143:
                      {
                        usleep(NF_process_time[0][m_number]*1000);
                        uint8_t buffer[74-12];
                        uint32_t len = strres.length();
                        for(uint32_t i=0;i<len;i++)
                        {
                          buffer[i]=strres[i];//char 与 uint_8逐个赋值
                        }
                        buffer[len]='\0';
                        //InetSocketAddress dest_address = InetSocketAddress(strres.c_str(),9);
                        Ptr<Packet> ack_packet3 = Create<Packet>(buffer,sizeof(buffer));
                        ack_packet3->AddHeader(seqTs);
                        socket->GetSockName (localAddress);
                        m_rxTrace (ack_packet3);
                        m_rxTraceWithAddresses (ack_packet3, from, localAddress);
                        NS_LOG_LOGIC ("Echoing packet");
                        socket->SendTo (ack_packet3, 0, from);
                        if (log_open==1)
                          {
                          NS_LOG_INFO ("At time " << Simulator::Now ().As (Time::S) << "  "<<m_number<<" UPF sent " << ack_packet3->GetSize () << " bytes to " <<
                          InetSocketAddress::ConvertFrom (from).GetIpv4 () << " port " <<
                          InetSocketAddress::ConvertFrom (from).GetPort ());
                          }                        
                      }
                      break;
                      case 141:
                      {
                        usleep(NF_process_time[0][m_number]*1000);
                          vector<string>   destVect;
                          string strFlag = ".";
                          int pos = strres.find(strFlag, 0);
                          int startPos = 0;
                          int splitN = pos;
                          string lineText(strFlag);
                          while (pos > -1)
                          {
                              lineText = strres.substr(startPos, splitN);
                              startPos = pos + 1;
                              pos = strres.find(strFlag, pos + 1);
                              splitN = pos - startPos;
                              destVect.push_back(lineText);
                          }
                          lineText = strres.substr(startPos, strres.length() - startPos);
                          destVect.push_back(lineText);
                          // std::cout<<destVect[0]<<std::endl;
                          // std::cout<<destVect[1]<<std::endl;
                          // std::cout<<destVect[2]<<std::endl;
                          // std::cout<<destVect[3]<<std::endl;
                          int client_number = (stoi(destVect[1])-6)*256+stoi(destVect[2]);
                          // std::vector<string> res = std::split(strres, ".");
                            delay = Simulator::Now () - seqTs.GetTs ();
                            ofstream wfile;
                            wfile.open(target_file_name,ios::app);
                            wfile << client_number<<delay.As (Time::MS)<<"; ";//写入修改内容
                            wfile.close();             
                      }
                      break;
                    // --------------------sr-------------------------------------------

                    // --------------------n2-------------------------------------------

                  case 144:
                      {
                        usleep(NF_process_time[0][m_number]*1000);
                        uint8_t buffer[71-12];
                        uint32_t len = strres.length();
                        for(uint32_t i=0;i<len;i++)
                        {
                          buffer[i]=strres[i];//char 与 uint_8逐个赋值
                        }
                        buffer[len]='\0';
                        //InetSocketAddress dest_address = InetSocketAddress(strres.c_str(),9);
                        Ptr<Packet> ack_packet3 = Create<Packet>(buffer,sizeof(buffer));
                        ack_packet3->AddHeader(seqTs);
                        socket->GetSockName (localAddress);
                        m_rxTrace (ack_packet3);
                        m_rxTraceWithAddresses (ack_packet3, from, localAddress);
                        NS_LOG_LOGIC ("Echoing packet");
                        socket->SendTo (ack_packet3, 0, from);
                        if (log_open==1)
                          {
                          NS_LOG_INFO ("At time " << Simulator::Now ().As (Time::S) << "  "<<m_number<<" UPF sent " << ack_packet3->GetSize () << " bytes to " <<
                          InetSocketAddress::ConvertFrom (from).GetIpv4 () << " port " <<
                          InetSocketAddress::ConvertFrom (from).GetPort ());
                          }                        
                      }
                      break;

                      case 145:
                      {
                        usleep(NF_process_time[0][m_number]*1000);
                        vector<string>   destVect;
                          string strFlag = ".";
                          int pos = strres.find(strFlag, 0);
                          int startPos = 0;
                          int splitN = pos;
                          string lineText(strFlag);
                          while (pos > -1)
                          {
                              lineText = strres.substr(startPos, splitN);
                              startPos = pos + 1;
                              pos = strres.find(strFlag, pos + 1);
                              splitN = pos - startPos;
                              destVect.push_back(lineText);
                          }
                          lineText = strres.substr(startPos, strres.length() - startPos);
                          destVect.push_back(lineText);
                          // std::cout<<destVect[0]<<std::endl;
                          // std::cout<<destVect[1]<<std::endl;
                          // std::cout<<destVect[2]<<std::endl;
                          // std::cout<<destVect[3]<<std::endl;
                          int client_number = (stoi(destVect[1])-6)*256+stoi(destVect[2]);
                          // std::vector<string> res = std::split(strres, ".");
                            delay = Simulator::Now () - seqTs.GetTs ();
                            ofstream wfile;
                            wfile.open(target_file_name,ios::app);
                            wfile << client_number<<delay.As (Time::MS)<<"; ";//写入修改内容
                            wfile.close();                        
                      }
                      break;

                    // --------------------n2-------------------------------------------
                    
                    // --------------------地面n2-------------------------------------------
                    case 1630:
                      {
                        uint8_t buffer[1786-12];
                        uint32_t len = strres.length();
                        for(uint32_t i=0;i<len;i++)
                        {
                          buffer[i]=strres[i];//char 与 uint_8逐个赋值
                        }
                        buffer[len]='\0';
                        //InetSocketAddress dest_address = InetSocketAddress(strres.c_str(),9);
                        Ptr<Packet> ack_packet3 = Create<Packet>(buffer,sizeof(buffer));
                        ack_packet3->AddHeader(seqTs);
                        socket->GetSockName (localAddress);
                        m_rxTrace (ack_packet3);
                        m_rxTraceWithAddresses (ack_packet3, from, localAddress);
                        NS_LOG_LOGIC ("Echoing packet");
                        socket->SendTo (ack_packet3, 0, from);
                        if (log_open==1)
                          {
                          NS_LOG_INFO ("At time " << Simulator::Now ().As (Time::S) << "  "<<m_number<<" UPF sent " << ack_packet3->GetSize () << " bytes to " <<
                          InetSocketAddress::ConvertFrom (from).GetIpv4 () << " port " <<
                          InetSocketAddress::ConvertFrom (from).GetPort ());
                          }                        
                      }
                      break;
                      case 678:
                      {
                        uint8_t buffer[658-12];
                        uint32_t len = strres.length();
                        for(uint32_t i=0;i<len;i++)
                        {
                          buffer[i]=strres[i];//char 与 uint_8逐个赋值
                        }
                        buffer[len]='\0';
                        //InetSocketAddress dest_address = InetSocketAddress(strres.c_str(),9);
                        Ptr<Packet> ack_packet3 = Create<Packet>(buffer,sizeof(buffer));
                        ack_packet3->AddHeader(seqTs);
                        socket->GetSockName (localAddress);
                        m_rxTrace (ack_packet3);
                        m_rxTraceWithAddresses (ack_packet3, from, localAddress);
                        NS_LOG_LOGIC ("Echoing packet");
                        socket->SendTo (ack_packet3, 0, from);
                        if (log_open==1)
                          {
                          NS_LOG_INFO ("At time " << Simulator::Now ().As (Time::S) << "  "<<m_number<<" UPF sent " << ack_packet3->GetSize () << " bytes to " <<
                          InetSocketAddress::ConvertFrom (from).GetIpv4 () << " port " <<
                          InetSocketAddress::ConvertFrom (from).GetPort ());
                          }                        
                      }
                      break;
                      case 119:
                      {
                        vector<string>   destVect;
                        string strFlag = ".";
                         int pos = strres.find(strFlag, 0);
                        int startPos = 0;
                        int splitN = pos;
                        string lineText(strFlag);
                        while (pos > -1)
                        {
                            lineText = strres.substr(startPos, splitN);
                            startPos = pos + 1;
                            pos = strres.find(strFlag, pos + 1);
                            splitN = pos - startPos;
                            destVect.push_back(lineText);
                        }
                        lineText = strres.substr(startPos, strres.length() - startPos);
                        destVect.push_back(lineText);
                        // std::cout<<destVect[0]<<std::endl;
                        // std::cout<<destVect[1]<<std::endl;
                        // std::cout<<destVect[2]<<std::endl;
                        // std::cout<<destVect[3]<<std::endl;
                        int client_number = (stoi(destVect[1])-6)*256+stoi(destVect[2]);
                        // std::vector<string> res = std::split(strres, ".");
                           delay = Simulator::Now () - seqTs.GetTs ();
                           ofstream wfile;
                           wfile.open(target_file_name,ios::app);
                           wfile << client_number<<delay.As (Time::MS)<<"; ";//写入修改内容
	                        wfile.close();
                      }
                      break;
                    // --------------------地面n2-------------------------------------------

                    // --------------------se-------------------------------------------
                    case 169:
                      {
                        usleep(NF_process_time[0][m_number]*1000);
                        uint8_t buffer[112-12];
                        uint32_t len = strres.length();
                        for(uint32_t i=0;i<len;i++)
                        {
                          buffer[i]=strres[i];//char 与 uint_8逐个赋值
                        }
                        buffer[len]='\0';
                        //InetSocketAddress dest_address = InetSocketAddress(strres.c_str(),9);
                        Ptr<Packet> ack_packet3 = Create<Packet>(buffer,sizeof(buffer));
                        ack_packet3->AddHeader(seqTs);
                        socket->GetSockName (localAddress);
                        m_rxTrace (ack_packet3);
                        m_rxTraceWithAddresses (ack_packet3, from, localAddress);
                        NS_LOG_LOGIC ("Echoing packet");
                        socket->SendTo (ack_packet3, 0, from);
                        if (log_open==1)
                          {
                          NS_LOG_INFO ("At time " << Simulator::Now ().As (Time::S) << "  "<<m_number<<" UPF sent " << ack_packet3->GetSize () << " bytes to " <<
                          InetSocketAddress::ConvertFrom (from).GetIpv4 () << " port " <<
                          InetSocketAddress::ConvertFrom (from).GetPort ());
                          }                        
                      }
                      break;
                      case 146:
                      {
                        usleep(NF_process_time[0][m_number]*1000);
                          vector<string>   destVect;
                          string strFlag = ".";
                          int pos = strres.find(strFlag, 0);
                          int startPos = 0;
                          int splitN = pos;
                          string lineText(strFlag);
                          while (pos > -1)
                          {
                              lineText = strres.substr(startPos, splitN);
                              startPos = pos + 1;
                              pos = strres.find(strFlag, pos + 1);
                              splitN = pos - startPos;
                              destVect.push_back(lineText);
                          }
                          lineText = strres.substr(startPos, strres.length() - startPos);
                          destVect.push_back(lineText);
                          // std::cout<<destVect[0]<<std::endl;
                          // std::cout<<destVect[1]<<std::endl;
                          // std::cout<<destVect[2]<<std::endl;
                          // std::cout<<destVect[3]<<std::endl;
                          int client_number = (stoi(destVect[1])-6)*256+stoi(destVect[2]);
                          // std::vector<string> res = std::split(strres, ".");
                            delay = Simulator::Now () - seqTs.GetTs ();
                            ofstream wfile;
                            wfile.open(target_file_name,ios::app);
                            wfile << client_number<<delay.As (Time::MS)<<"; ";//写入修改内容
                            wfile.close();                 
                      }
                      break;
                      // ---------se-ground---
                      case 308:
                      {
                        uint8_t buffer[140-12];
                        uint32_t len = strres.length();
                        for(uint32_t i=0;i<len;i++)
                        {
                          buffer[i]=strres[i];//char 与 uint_8逐个赋值
                        }
                        buffer[len]='\0';
                        //InetSocketAddress dest_address = InetSocketAddress(strres.c_str(),9);
                        Ptr<Packet> ack_packet3 = Create<Packet>(buffer,sizeof(buffer));
                        ack_packet3->AddHeader(seqTs);
                        socket->GetSockName (localAddress);
                        m_rxTrace (ack_packet3);
                        m_rxTraceWithAddresses (ack_packet3, from, localAddress);
                        NS_LOG_LOGIC ("Echoing packet");
                        socket->SendTo (ack_packet3, 0, from);
                        if (log_open==1)
                          {
                          NS_LOG_INFO ("At time " << Simulator::Now ().As (Time::S) << "  "<<m_number<<" UPF sent " << ack_packet3->GetSize () << " bytes to " <<
                          InetSocketAddress::ConvertFrom (from).GetIpv4 () << " port " <<
                          InetSocketAddress::ConvertFrom (from).GetPort ());
                          }                        
                      }
                      break;
                      // --------------------se-------------------------------------------

                      // -------------------地面 se-------------------------------------------

                       case 238:
                        {
                              uint8_t buffer[270-12];
                            uint32_t len = strres.length();
                            for(uint32_t i=0;i<len;i++)
                            {
                              buffer[i]=strres[i];//char 与 uint_8逐个赋值
                            }
                            buffer[len]='\0';
                            //InetSocketAddress dest_address = InetSocketAddress(strres.c_str(),9);
                            Ptr<Packet> ack_packet3 = Create<Packet>(buffer,sizeof(buffer));
                            ack_packet3->AddHeader(seqTs);
                            socket->GetSockName (localAddress);
                            m_rxTrace (ack_packet3);
                            m_rxTraceWithAddresses (ack_packet3, from, localAddress);
                            NS_LOG_LOGIC ("Echoing packet");
                            socket->SendTo (ack_packet3, 0, from);
                            if (log_open==1)
                              {
                              NS_LOG_INFO ("At time " << Simulator::Now ().As (Time::S) << "  "<<m_number<<" UPF sent " << ack_packet3->GetSize () << " bytes to " <<
                              InetSocketAddress::ConvertFrom (from).GetIpv4 () << " port " <<
                              InetSocketAddress::ConvertFrom (from).GetPort ());
                              }                        
                        }
                        break;
                        case 117:
                        {
                          vector<string>   destVect;
                          string strFlag = ".";
                          int pos = strres.find(strFlag, 0);
                          int startPos = 0;
                          int splitN = pos;
                          string lineText(strFlag);
                          while (pos > -1)
                          {
                              lineText = strres.substr(startPos, splitN);
                              startPos = pos + 1;
                              pos = strres.find(strFlag, pos + 1);
                              splitN = pos - startPos;
                              destVect.push_back(lineText);
                          }
                          lineText = strres.substr(startPos, strres.length() - startPos);
                          destVect.push_back(lineText);
                          // std::cout<<destVect[0]<<std::endl;
                          // std::cout<<destVect[1]<<std::endl;
                          // std::cout<<destVect[2]<<std::endl;
                          // std::cout<<destVect[3]<<std::endl;
                          int client_number = (stoi(destVect[1])-6)*256+stoi(destVect[2]);
                          // std::vector<string> res = std::split(strres, ".");
                            delay = Simulator::Now () - seqTs.GetTs ();
                            ofstream wfile;
                            wfile.open(target_file_name,ios::app);
                            wfile << client_number<<delay.As (Time::MS)<<"; ";//写入修改内容
                            wfile.close();
                        }
                        break;
                      // -------------------地面 se-------------------------------------------

                 


                }

            }
        }
        
    }
}

} // Namespace ns3