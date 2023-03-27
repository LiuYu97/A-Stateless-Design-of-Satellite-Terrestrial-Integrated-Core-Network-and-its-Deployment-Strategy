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

#include "Xn-SMF.h"
#include <time.h>
#include <vector>
#include <iostream>
#include <string>
#include <sstream>
#include <fstream> 
#include <unistd.h>

using namespace std;
namespace ns3 {

// int liuyu=0;
NS_LOG_COMPONENT_DEFINE ("XnSMFApplication");

NS_OBJECT_ENSURE_REGISTERED (XnSMF);


TypeId
XnSMF::GetTypeId (void)
{
  static TypeId tid = TypeId ("ns3::XnSMF")
    .SetParent<Application> ()
    .SetGroupName("Applications")
    .AddConstructor<XnSMF> ()
    .AddAttribute ("Port", "Port on which we listen for incoming packets.",
                   UintegerValue (9),
                   MakeUintegerAccessor (&XnSMF::m_port),
                   MakeUintegerChecker<uint16_t> ())
    .AddTraceSource ("Rx", "A packet has been received",
                     MakeTraceSourceAccessor (&XnSMF::m_rxTrace),
                     "ns3::Packet::TracedCallback")
    .AddTraceSource ("RxWithAddresses", "A packet has been received",
                     MakeTraceSourceAccessor (&XnSMF::m_rxTraceWithAddresses),
                     "ns3::Packet::TwoAddressTracedCallback")
    .AddAttribute ("UPFAddress", 
                   "The destination Address of the outbound packets",
                   AddressValue (),
                   MakeAddressAccessor (&XnSMF::UPF_address),
                   MakeAddressChecker ())
    .AddAttribute ("UPFPort", 
                   "The destination port of the outbound packets",
                   UintegerValue (0),
                   MakeUintegerAccessor (&XnSMF::UPF_port),
                   MakeUintegerChecker<uint16_t> ())
    .AddAttribute ("SMFNumber", 
                   "The maximum number of packets the application will send",
                   UintegerValue (),
                   MakeUintegerAccessor (&XnSMF::m_number),
                   MakeUintegerChecker<uint16_t> ())
    .AddAttribute ("Ground_address", 
                   "The destination Address of the outbound packets",
                   AddressValue (),
                   MakeAddressAccessor (&XnSMF::Ground_address),
                   MakeAddressChecker ())
    .AddAttribute ("AMFPort", 
                   "The destination port of the outbound packets",
                   UintegerValue (9),
                   MakeUintegerAccessor (&XnSMF::AMF_port),
                   MakeUintegerChecker<uint16_t> ())
     .AddAttribute ("OpenLog", 
                   "open the NS_LOG_INFO",
                   UintegerValue (0),
                   MakeUintegerAccessor (&XnSMF::log_open),
                   MakeUintegerChecker<uint16_t>())
    
  ;
  return tid;
}

XnSMF::XnSMF ()
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

XnSMF::~XnSMF()
{
  NS_LOG_FUNCTION (this);
  m_socket = 0;
  m_socket6 = 0;
  
}

void
XnSMF::DoDispose (void)
{
  NS_LOG_FUNCTION (this);
  Application::DoDispose ();
}

void 
XnSMF::StartApplication (void)
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

  m_socket->SetRecvCallback (MakeCallback (&XnSMF::HandleRead, this));
  m_socket6->SetRecvCallback (MakeCallback (&XnSMF::HandleRead, this));
}

void 
XnSMF::StopApplication ()
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
XnSMF::HandleRead (Ptr<Socket> socket)
{
  NS_LOG_FUNCTION (this << socket);

  Ptr<Packet> packet;
  Address from;
  Address localAddress;
  
  Address AMF_address;
  
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
          NS_LOG_INFO ("At time " << Simulator::Now ().As (Time::S) << "  "<<m_number<<" XnSMF received " << packet->GetSize () << " bytes from " <<
                       InetSocketAddress::ConvertFrom (from).GetIpv4 () << " port " <<
                       InetSocketAddress::ConvertFrom (from).GetPort ());
        }
      else if (Inet6SocketAddress::IsMatchingType (from))
        {
          NS_LOG_INFO ("At time " << Simulator::Now ().As (Time::S) <<  "  "<<m_number<<" XnSMF received " << packet->GetSize () << " bytes from " <<
                       Inet6SocketAddress::ConvertFrom (from).GetIpv6 () << " port " <<
                       Inet6SocketAddress::ConvertFrom (from).GetPort ());
        }
      }
      if (packet->GetSize () > 0)
        {
          uint32_t receivedSize = packet->GetSize ();
          
          SeqTsHeader seqTs;
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
          //cout<<strres<<endl;
          //找到空格位置（分界位置）
          // int pos = strres.find(" ");
          // string load_info = strres.substr(pos+1,sizeof(data));
          // p_num = atoi(load_info.c_str());
          //cout<<p_num<<endl;
          //uint32_t per_receivedSize = receivedSize/p_num;
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
                usleep(NF_process_time[0][m_number]*1000);
                switch(receivedSize)
                {       
                  // ---------------------------------------XN-----------------------------//
                        case 554:
                        {
                          
                          // uint8_t data[255];
                          // packet->CopyData(data,sizeof(data));//将包内数据写入到data内
                          // //cout <<packet->GetUid ()<<" "<<"receive : '" << data <<"' from "<<InetSocketAddress::ConvertFrom (from).GetIpv4 ()<< endl;  
    
                          // char a[sizeof(data)];
                          // for(uint32_t i=0;i<sizeof(data);i++){
                          //   a[i]=data[i];
                          // }
                          // string strres = string(a);
                          //cout<<"接受到的字符串为 "<<strres<<endl;
                          smf_back_amf.insert(std::pair<std::string,Address>(strres,from) );
                          uint8_t buffer[142-12];
                          uint32_t len = strres.length();
                          for(uint32_t i=0;i<len;i++)
                          {
                            buffer[i]=strres[i];//char 与 uint_8逐个赋值
                          }
                          buffer[len]='\0';
                          //InetSocketAddress dest_address = InetSocketAddress(strres.c_str(),9);
                          Ptr<Packet> p1 = Create<Packet>(buffer,sizeof(buffer));
                          p1->AddHeader(seqTs);
                          socket->GetSockName (localAddress);
                          m_rxTrace (p1);
                          m_rxTraceWithAddresses (p1, InetSocketAddress (Ipv4Address::ConvertFrom (UPF_address),UPF_port), localAddress);
                          socket->SendTo(p1,0,InetSocketAddress (Ipv4Address::ConvertFrom (UPF_address),UPF_port));
                          if(log_open==1)
                          {
                          NS_LOG_INFO ("At time " << Simulator::Now ().As (Time::S) <<  "  "<<m_number<<" XnSMF sent " << p1->GetSize () << " bytes to " <<
                          Ipv4Address::ConvertFrom (UPF_address)<< " port " << UPF_port);
                          }
                        }
                        break;
                        case 73:
                       //收到的包大小为108
                        //回复398
                        {
                            //NS_LOG_INFO("source_address:"<<source_address);
                            // uint8_t data[255];
                            //   packet->CopyData(data,sizeof(data));//将包内数据写入到data内
                            //   cout <<packet->GetUid ()<<" "<<"receive : '" << data <<"' from "<<InetSocketAddress::ConvertFrom (from).GetIpv4 ()<< endl;  
        
                            //   char a[sizeof(data)];
                            //   for(uint32_t i=0;i<sizeof(data);i++){
                            //     a[i]=data[i];
                            //   }
                            //   string strres = string(a);
                            //   cout<<"接受到的字符串为 "<<strres<<endl;
                            //   InetSocketAddress source_address = InetSocketAddress(strres.c_str(),49153);
                              
                              // uint8_t data[255];
                              // packet->CopyData(data,sizeof(data));//将包内数据写入到data内
                              // //cout <<packet->GetUid ()<<" "<<"receive : '" << data <<"' from "<<InetSocketAddress::ConvertFrom (from).GetIpv4 ()<< endl;  
        
                              // char a[sizeof(data)];
                              // for(uint32_t i=0;i<sizeof(data);i++){
                              //   a[i]=data[i];
                              // }
                              // string strres = string(a);

                              uint8_t buffer[294-12];
                              uint32_t len = strres.length();
                              for(uint32_t i=0;i<len;i++)
                              {
                                buffer[i]=strres[i];//char 与 uint_8逐个赋值
                              }
                              buffer[len]='\0';
                              Ptr<Packet> p2 = Create<Packet>(buffer,sizeof(buffer));
                              p2->AddHeader(seqTs);
                              socket->GetSockName (localAddress);
                              m_rxTrace (p2);

                              AMF_address = smf_back_amf[strres];
                              // cout<<InetSocketAddress::ConvertFrom (AMF_address).GetIpv4 ()<<endl;
                              // cout<<InetSocketAddress::ConvertFrom (AMF_address).GetIpv4 ()<<endl;
                              m_rxTraceWithAddresses (p2,InetSocketAddress (InetSocketAddress::ConvertFrom (AMF_address).GetIpv4 (), AMF_port),localAddress);
                              NS_LOG_LOGIC ("Echoing packet");
                              socket->SendTo(p2,0,InetSocketAddress (InetSocketAddress::ConvertFrom (AMF_address).GetIpv4 (), AMF_port));
                              if(log_open==1)
                              {
                              NS_LOG_INFO ("At time " << Simulator::Now ().As (Time::S) <<"  " <<m_number<<" XnSMF sent " << p2->GetSize () << " bytes to " <<
                            InetSocketAddress::ConvertFrom (AMF_address).GetIpv4 ()<< " port " << AMF_port);
                              }
                          }
                          break;
                          // ---------------------------------------XN-----------------------------//

                          // ---------------------------------------sr-----------------------------//
                          case 365:
                        {
                             smf_back_amf.insert(std::pair<std::string,Address>(strres,from) );
                              uint8_t buffer[143-12];
                              uint32_t len = strres.length();
                              for(uint32_t i=0;i<len;i++)
                              {
                                buffer[i]=strres[i];//char 与 uint_8逐个赋值
                              }
                              buffer[len]='\0';
                              //InetSocketAddress dest_address = InetSocketAddress(strres.c_str(),9);
                              
                              
                              Ptr<Packet> p1 = Create<Packet>(buffer,sizeof(buffer));
                              p1->AddHeader(seqTs);
                              socket->GetSockName (localAddress);
                              m_rxTrace (p1);
                              m_rxTraceWithAddresses (p1, InetSocketAddress (Ipv4Address::ConvertFrom (UPF_address),UPF_port), localAddress);
                              socket->SendTo(p1,0,InetSocketAddress (Ipv4Address::ConvertFrom (UPF_address),UPF_port));
                              if(log_open==1)
                              {
                              NS_LOG_INFO ("At time " << Simulator::Now ().As (Time::S) <<  "  "<<m_number<<" XnSMF sent " << p1->GetSize () << " bytes to " <<
                              Ipv4Address::ConvertFrom (UPF_address)<< " port " << UPF_port);
                              }
                          }
                          break;
                          case 74:
                        {
                              uint8_t buffer[167-12];
                              uint32_t len = strres.length();
                              for(uint32_t i=0;i<len;i++)
                              {
                                buffer[i]=strres[i];//char 与 uint_8逐个赋值
                              }
                              buffer[len]='\0';
                              Ptr<Packet> p2 = Create<Packet>(buffer,sizeof(buffer));
                              p2->AddHeader(seqTs);
                              socket->GetSockName (localAddress);
                              m_rxTrace (p2);

                              AMF_address = smf_back_amf[strres];
                              // cout<<InetSocketAddress::ConvertFrom (AMF_address).GetIpv4 ()<<endl;
                              // cout<<InetSocketAddress::ConvertFrom (AMF_address).GetIpv4 ()<<endl;
                              m_rxTraceWithAddresses (p2,InetSocketAddress (InetSocketAddress::ConvertFrom (AMF_address).GetIpv4 (), AMF_port),localAddress);
                              NS_LOG_LOGIC ("Echoing packet");
                              socket->SendTo(p2,0,InetSocketAddress (InetSocketAddress::ConvertFrom (AMF_address).GetIpv4 (), AMF_port));
                              if(log_open==1)
                              {
                              NS_LOG_INFO ("At time " << Simulator::Now ().As (Time::S) <<"  " <<m_number<<" XnSMF sent " << p2->GetSize () << " bytes to " <<
                            InetSocketAddress::ConvertFrom (AMF_address).GetIpv4 ()<< " port " << AMF_port);
                              }
                          }
                          break;
                           case 366:
                        {
                             smf_back_amf.insert(std::pair<std::string,Address>(strres,from) );
                              uint8_t buffer[141-12];
                              uint32_t len = strres.length();
                              for(uint32_t i=0;i<len;i++)
                              {
                                buffer[i]=strres[i];//char 与 uint_8逐个赋值
                              }
                              buffer[len]='\0';
                              //InetSocketAddress dest_address = InetSocketAddress(strres.c_str(),9);
                              
                              
                              Ptr<Packet> p1 = Create<Packet>(buffer,sizeof(buffer));
                              p1->AddHeader(seqTs);
                              socket->GetSockName (localAddress);
                              m_rxTrace (p1);
                              m_rxTraceWithAddresses (p1, InetSocketAddress (Ipv4Address::ConvertFrom (UPF_address),UPF_port), localAddress);
                              socket->SendTo(p1,0,InetSocketAddress (Ipv4Address::ConvertFrom (UPF_address),UPF_port));
                              if(log_open==1)
                              {
                              NS_LOG_INFO ("At time " << Simulator::Now ().As (Time::S) <<  "  "<<m_number<<" XnSMF sent " << p1->GetSize () << " bytes to " <<
                              Ipv4Address::ConvertFrom (UPF_address)<< " port " << UPF_port);
                              }
                          }
                          break;

                        //   case 72:
                        // {
                        //       uint8_t buffer[168-12];
                        //       uint32_t len = strres.length();
                        //       for(uint32_t i=0;i<len;i++)
                        //       {
                        //         buffer[i]=strres[i];//char 与 uint_8逐个赋值
                        //       }
                        //       buffer[len]='\0';
                        //       Ptr<Packet> p2 = Create<Packet>(buffer,sizeof(buffer));
                        //       p2->AddHeader(seqTs);
                        //       socket->GetSockName (localAddress);
                        //       m_rxTrace (p2);

                        //       AMF_address = smf_back_amf[strres];
                        //       // cout<<InetSocketAddress::ConvertFrom (AMF_address).GetIpv4 ()<<endl;
                        //       // cout<<InetSocketAddress::ConvertFrom (AMF_address).GetIpv4 ()<<endl;
                        //       m_rxTraceWithAddresses (p2,InetSocketAddress (InetSocketAddress::ConvertFrom (AMF_address).GetIpv4 (), AMF_port),localAddress);
                        //       NS_LOG_LOGIC ("Echoing packet");
                        //       socket->SendTo(p2,0,InetSocketAddress (InetSocketAddress::ConvertFrom (AMF_address).GetIpv4 (), AMF_port));
                        //       if(log_open==1)
                        //       {
                        //       NS_LOG_INFO ("At time " << Simulator::Now ().As (Time::S) <<"  " <<m_number<<" XnSMF sent " << p2->GetSize () << " bytes to " <<
                        //     InetSocketAddress::ConvertFrom (AMF_address).GetIpv4 ()<< " port " << AMF_port);
                        //       }
                        //   }
                        //   break;
                          // ---------------------------------------XN-----------------------------//

                          // ---------------------------------------n2-----------------------------//
                          case 374:
                          {  
                            smf_back_amf.insert(std::pair<std::string,Address>(strres,from) );
                            uint8_t buffer[191-12];
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
                              NS_LOG_INFO ("At time " << Simulator::Now ().As (Time::S) << "  "<<m_number<<" Client sent " << ack_packet3->GetSize () << " bytes to " <<
                              InetSocketAddress::ConvertFrom (from).GetIpv4 () << " port " <<
                              InetSocketAddress::ConvertFrom (from).GetPort ());
                              }                        
                          }
                          break;

                          case 381:
                          {  
                              uint8_t buffer[144-12];
                              uint32_t len = strres.length();
                              for(uint32_t i=0;i<len;i++)
                              {
                                buffer[i]=strres[i];//char 与 uint_8逐个赋值
                              }
                              buffer[len]='\0';
                              //InetSocketAddress dest_address = InetSocketAddress(strres.c_str(),9);
                              
                              
                              Ptr<Packet> p1 = Create<Packet>(buffer,sizeof(buffer));
                              p1->AddHeader(seqTs);
                              socket->GetSockName (localAddress);
                              m_rxTrace (p1);
                              m_rxTraceWithAddresses (p1, InetSocketAddress (Ipv4Address::ConvertFrom (UPF_address),UPF_port), localAddress);
                              socket->SendTo(p1,0,InetSocketAddress (Ipv4Address::ConvertFrom (UPF_address),UPF_port));
                              if(log_open==1)
                              {
                              NS_LOG_INFO ("At time " << Simulator::Now ().As (Time::S) <<  "  "<<m_number<<" XnSMF sent " << p1->GetSize () << " bytes to " <<
                              Ipv4Address::ConvertFrom (UPF_address)<< " port " << UPF_port);
                              }                   
                          }
                          break;
                          case 71:
                        {
                              uint8_t buffer[169-12];
                              uint32_t len = strres.length();
                              for(uint32_t i=0;i<len;i++)
                              {
                                buffer[i]=strres[i];//char 与 uint_8逐个赋值
                              }
                              buffer[len]='\0';
                              Ptr<Packet> p2 = Create<Packet>(buffer,sizeof(buffer));
                              p2->AddHeader(seqTs);
                              socket->GetSockName (localAddress);
                              m_rxTrace (p2);

                              AMF_address = smf_back_amf[strres];
                              // cout<<InetSocketAddress::ConvertFrom (AMF_address).GetIpv4 ()<<endl;
                              // cout<<InetSocketAddress::ConvertFrom (AMF_address).GetIpv4 ()<<endl;
                              m_rxTraceWithAddresses (p2,InetSocketAddress (InetSocketAddress::ConvertFrom (AMF_address).GetIpv4 (), AMF_port),localAddress);
                              NS_LOG_LOGIC ("Echoing packet");
                              socket->SendTo(p2,0,InetSocketAddress (InetSocketAddress::ConvertFrom (AMF_address).GetIpv4 (), AMF_port));
                              if(log_open==1)
                              {
                              NS_LOG_INFO ("At time " << Simulator::Now ().As (Time::S) <<"  " <<m_number<<" XnSMF sent " << p2->GetSize () << " bytes to " <<
                            InetSocketAddress::ConvertFrom (AMF_address).GetIpv4 ()<< " port " << AMF_port);
                              }
                          }
                          break;
                          case 352:
                          {  
                            
                              uint8_t buffer[145-12];
                              uint32_t len = strres.length();
                              for(uint32_t i=0;i<len;i++)
                              {
                                buffer[i]=strres[i];//char 与 uint_8逐个赋值
                              }
                              buffer[len]='\0';
                              //InetSocketAddress dest_address = InetSocketAddress(strres.c_str(),9);
                              
                              
                              Ptr<Packet> p1 = Create<Packet>(buffer,sizeof(buffer));
                              p1->AddHeader(seqTs);
                              socket->GetSockName (localAddress);
                              m_rxTrace (p1);
                              m_rxTraceWithAddresses (p1, InetSocketAddress (Ipv4Address::ConvertFrom (UPF_address),UPF_port), localAddress);
                              socket->SendTo(p1,0,InetSocketAddress (Ipv4Address::ConvertFrom (UPF_address),UPF_port));
                              if(log_open==1)
                              {
                              NS_LOG_INFO ("At time " << Simulator::Now ().As (Time::S) <<  "  "<<m_number<<" XnSMF sent " << p1->GetSize () << " bytes to " <<
                              Ipv4Address::ConvertFrom (UPF_address)<< " port " << UPF_port);
                              }                   
                          }
                          break;
                        //   case 75:
                        // {
                        //       uint8_t buffer[156-12];
                        //       uint32_t len = strres.length();
                        //       for(uint32_t i=0;i<len;i++)
                        //       {
                        //         buffer[i]=strres[i];//char 与 uint_8逐个赋值
                        //       }
                        //       buffer[len]='\0';
                        //       Ptr<Packet> p2 = Create<Packet>(buffer,sizeof(buffer));
                        //       p2->AddHeader(seqTs);
                        //       socket->GetSockName (localAddress);
                        //       m_rxTrace (p2);

                        //       AMF_address = smf_back_amf[strres];
                        //       // cout<<InetSocketAddress::ConvertFrom (AMF_address).GetIpv4 ()<<endl;
                        //       // cout<<InetSocketAddress::ConvertFrom (AMF_address).GetIpv4 ()<<endl;
                        //       m_rxTraceWithAddresses (p2,InetSocketAddress (InetSocketAddress::ConvertFrom (AMF_address).GetIpv4 (), AMF_port),localAddress);
                        //       NS_LOG_LOGIC ("Echoing packet");
                        //       socket->SendTo(p2,0,InetSocketAddress (InetSocketAddress::ConvertFrom (AMF_address).GetIpv4 (), AMF_port));
                        //       if(log_open==1)
                        //       {
                        //       NS_LOG_INFO ("At time " << Simulator::Now ().As (Time::S) <<"  " <<m_number<<" XnSMF sent " << p2->GetSize () << " bytes to " <<
                        //     InetSocketAddress::ConvertFrom (AMF_address).GetIpv4 ()<< " port " << AMF_port);
                        //       }
                        //   }
                        //   break;

                          // ---------------------------------------n2-----------------------------//

                          // ---------------------------------------Se-----------------------------//
                          case 811:
                          {  
                              smf_back_amf.insert(std::pair<std::string,Address>(strres,from) );
                              uint8_t buffer[308-12];
                              uint32_t len = strres.length();
                              for(uint32_t i=0;i<len;i++)
                              {
                                buffer[i]=strres[i];//char 与 uint_8逐个赋值
                              }
                              buffer[len]='\0';
                              //InetSocketAddress dest_address = InetSocketAddress(strres.c_str(),9);
                              
                              
                              Ptr<Packet> p1 = Create<Packet>(buffer,sizeof(buffer));
                              p1->AddHeader(seqTs);
                              socket->GetSockName (localAddress);
                              m_rxTrace (p1);
                              // cout<<Ipv4Address::ConvertFrom (Ground_address)<<endl;
                              m_rxTraceWithAddresses (p1, InetSocketAddress (Ipv4Address::ConvertFrom (Ground_address),UPF_port), localAddress);
                              socket->SendTo(p1,0,InetSocketAddress (Ipv4Address::ConvertFrom (Ground_address),UPF_port));
                              if(log_open==1)
                              {
                              NS_LOG_INFO ("At time " << Simulator::Now ().As (Time::S) <<  "  "<<m_number<<" XnSMF sent " << p1->GetSize () << " bytes to " <<
                              Ipv4Address::ConvertFrom (Ground_address)<< " port " << UPF_port);
                              }                   
                          }
                          break;
                          case 140:
                          {  
                              smf_back_amf.insert(std::pair<std::string,Address>(strres,from) );
                              uint8_t buffer[169-12];
                              uint32_t len = strres.length();
                              for(uint32_t i=0;i<len;i++)
                              {
                                buffer[i]=strres[i];//char 与 uint_8逐个赋值
                              }
                              buffer[len]='\0';
                              //InetSocketAddress dest_address = InetSocketAddress(strres.c_str(),9);
                              
                              
                              Ptr<Packet> p1 = Create<Packet>(buffer,sizeof(buffer));
                              p1->AddHeader(seqTs);
                              socket->GetSockName (localAddress);
                              m_rxTrace (p1);
                              m_rxTraceWithAddresses (p1, InetSocketAddress (Ipv4Address::ConvertFrom (UPF_address),UPF_port), localAddress);
                              socket->SendTo(p1,0,InetSocketAddress (Ipv4Address::ConvertFrom (UPF_address),UPF_port));
                              if(log_open==1)
                              {
                              NS_LOG_INFO ("At time " << Simulator::Now ().As (Time::S) <<  "  "<<m_number<<" XnSMF sent " << p1->GetSize () << " bytes to " <<
                              Ipv4Address::ConvertFrom (UPF_address)<< " port " << UPF_port);
                              }                   
                          }
                          break;
                          case 112:
                        {
                              uint8_t buffer[1057-12];
                              uint32_t len = strres.length();
                              for(uint32_t i=0;i<len;i++)
                              {
                                buffer[i]=strres[i];//char 与 uint_8逐个赋值
                              }
                              buffer[len]='\0';
                              Ptr<Packet> p2 = Create<Packet>(buffer,sizeof(buffer));
                              p2->AddHeader(seqTs);
                              socket->GetSockName (localAddress);
                              m_rxTrace (p2);

                              AMF_address = smf_back_amf[strres];
                              // cout<<InetSocketAddress::ConvertFrom (AMF_address).GetIpv4 ()<<endl;
                              // cout<<InetSocketAddress::ConvertFrom (AMF_address).GetIpv4 ()<<endl;
                              m_rxTraceWithAddresses (p2,InetSocketAddress (InetSocketAddress::ConvertFrom (AMF_address).GetIpv4 (), AMF_port),localAddress);
                              NS_LOG_LOGIC ("Echoing packet");
                              socket->SendTo(p2,0,InetSocketAddress (InetSocketAddress::ConvertFrom (AMF_address).GetIpv4 (), AMF_port));
                              if(log_open==1)
                              {
                              NS_LOG_INFO ("At time " << Simulator::Now ().As (Time::S) <<"  " <<m_number<<" XnSMF sent " << p2->GetSize () << " bytes to " <<
                            InetSocketAddress::ConvertFrom (AMF_address).GetIpv4 ()<< " port " << AMF_port);
                              }
                          }
                          break;
                          case 472:
                          {  
                              uint8_t buffer[146-12];
                              uint32_t len = strres.length();
                              for(uint32_t i=0;i<len;i++)
                              {
                                buffer[i]=strres[i];//char 与 uint_8逐个赋值
                              }
                              buffer[len]='\0';
                              //InetSocketAddress dest_address = InetSocketAddress(strres.c_str(),9);
                              
                              
                              Ptr<Packet> p1 = Create<Packet>(buffer,sizeof(buffer));
                              p1->AddHeader(seqTs);
                              socket->GetSockName (localAddress);
                              m_rxTrace (p1);
                              m_rxTraceWithAddresses (p1, InetSocketAddress (Ipv4Address::ConvertFrom (UPF_address),UPF_port), localAddress);
                              socket->SendTo(p1,0,InetSocketAddress (Ipv4Address::ConvertFrom (UPF_address),UPF_port));
                              if(log_open==1)
                              {
                              NS_LOG_INFO ("At time " << Simulator::Now ().As (Time::S) <<  "  "<<m_number<<" XnSMF sent " << p1->GetSize () << " bytes to " <<
                              Ipv4Address::ConvertFrom (UPF_address)<< " port " << UPF_port);
                              }                   
                          }
                          break;
                        //   case 76:
                        // {
                        //       uint8_t buffer[170-12];
                        //       uint32_t len = strres.length();
                        //       for(uint32_t i=0;i<len;i++)
                        //       {
                        //         buffer[i]=strres[i];//char 与 uint_8逐个赋值
                        //       }
                        //       buffer[len]='\0';
                        //       Ptr<Packet> p2 = Create<Packet>(buffer,sizeof(buffer));
                        //       p2->AddHeader(seqTs);
                        //       socket->GetSockName (localAddress);
                        //       m_rxTrace (p2);

                        //       AMF_address = smf_back_amf[strres];
                        //       // cout<<InetSocketAddress::ConvertFrom (AMF_address).GetIpv4 ()<<endl;
                        //       // cout<<InetSocketAddress::ConvertFrom (AMF_address).GetIpv4 ()<<endl;
                        //       m_rxTraceWithAddresses (p2,InetSocketAddress (InetSocketAddress::ConvertFrom (AMF_address).GetIpv4 (), AMF_port),localAddress);
                        //       NS_LOG_LOGIC ("Echoing packet");
                        //       socket->SendTo(p2,0,InetSocketAddress (InetSocketAddress::ConvertFrom (AMF_address).GetIpv4 (), AMF_port));
                        //       if(log_open==1)
                        //       {
                        //       NS_LOG_INFO ("At time " << Simulator::Now ().As (Time::S) <<"  " <<m_number<<" XnSMF sent " << p2->GetSize () << " bytes to " <<
                        //     InetSocketAddress::ConvertFrom (AMF_address).GetIpv4 ()<< " port " << AMF_port);
                        //       }
                        //   }
                        //   break;
                          // ---------------------------------------Se-----------------------------//

                }
                          
                    
                        


                

            }
        }
        
    }
}


} // Namespace ns3