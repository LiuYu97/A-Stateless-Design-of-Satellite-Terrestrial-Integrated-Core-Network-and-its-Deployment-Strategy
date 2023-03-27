#include "ns3/log.h"
#include "ns3/ipv4-address.h"
#include "ns3/ipv6-address.h"
#include "ns3/nstime.h"
#include "ns3/inet-socket-address.h"
#include "ns3/inet6-socket-address.h"
#include "ns3/socket.h"
#include "ns3/simulator.h"
#include "ns3/socket-factory.h"
#include "ns3/packet.h"
#include "ns3/uinteger.h"
#include "seq-ts-header.h"
#include "ns3/trace-source-accessor.h"
#include "Xn-Client.h"
#include <time.h>
#include <vector>
#include <iostream>
#include <string>
#include <sstream>
#include <fstream>

using namespace std;
std::string target_file_name;
namespace ns3 {
int  liuyu_client=0;
// extern string target_name;

NS_LOG_COMPONENT_DEFINE ("XnClientApplication");

NS_OBJECT_ENSURE_REGISTERED (XnClient);

TypeId
XnClient::GetTypeId (void)
{
  static TypeId tid = TypeId ("ns3::XnClient")
    .SetParent<Application> ()
    .SetGroupName("Applications")
    .AddConstructor<XnClient> ()
    .AddAttribute ("MaxPackets", 
                   "The maximum number of packets the application will send",
                   UintegerValue (0),
                   MakeUintegerAccessor (&XnClient::m_count),
                   MakeUintegerChecker<uint32_t> ())
    .AddAttribute ("ClientNumber", 
                   "the code of client",
                   UintegerValue (),
                   MakeUintegerAccessor (&XnClient::m_number),
                   MakeUintegerChecker<uint16_t> ())
    
    .AddAttribute ("BeginTime", 
                   "the time to send",
                   UintegerValue (2),
                   MakeUintegerAccessor (&XnClient::m_time),
                   MakeUintegerChecker<uint16_t>())
    .AddAttribute ("OpenLog", 
                   "open the NS_LOG_INFO",
                   UintegerValue (0),
                   MakeUintegerAccessor (&XnClient::log_open),
                   MakeUintegerChecker<uint16_t>())
    .AddAttribute ("Interval", 
                   "The time to wait between packets",
                   TimeValue (Seconds (0)),
                   MakeTimeAccessor (&XnClient::m_interval),
                   MakeTimeChecker ())
    // .AddAttribute ("dest_address", 
                   
    //                AdressValXnClient (),
    //                MakeTimeAccessor (&UdpEchoClient::dest_address),
    //                MakeTimeChecker ())
    .AddAttribute ("ClientLoad", 
                   "the number of people under the sat",
                   UintegerValue (1),
                   MakeUintegerAccessor (&XnClient::m_load),
                   MakeUintegerChecker<uint32_t>())
    .AddAttribute ("RemoteAddress", 
                   "The destination Address of the outbound packets",
                   AddressValue (),
                   MakeAddressAccessor (&XnClient::m_peerAddress),
                   MakeAddressChecker ())
    .AddAttribute ("RemotePort", 
                   "The destination port of the outbound packets",
                   UintegerValue (0),
                   MakeUintegerAccessor (&XnClient::m_peerPort),
                   MakeUintegerChecker<uint16_t> ())
    .AddAttribute ("PacketSize", "Size of echo data in outbound packets",
                   UintegerValue (112),
                   MakeUintegerAccessor (&XnClient::SetDataSize,
                                         &XnClient::GetDataSize),
                   MakeUintegerChecker<uint32_t> ())
    .AddTraceSource ("Tx", "A new packet is created and is sent",
                     MakeTraceSourceAccessor (&XnClient::m_txTrace),
                     "ns3::Packet::TracedCallback")
    .AddTraceSource ("Rx", "A packet has been received",
                     MakeTraceSourceAccessor (&XnClient::m_rxTrace),
                     "ns3::Packet::TracedCallback")
    .AddTraceSource ("TxWithAddresses", "A new packet is created and is sent",
                     MakeTraceSourceAccessor (&XnClient::m_txTraceWithAddresses),
                     "ns3::Packet::TwoAddressTracedCallback")
    .AddTraceSource ("RxWithAddresses", "A packet has been received",
                     MakeTraceSourceAccessor (&XnClient::m_rxTraceWithAddresses),
                     "ns3::Packet::TwoAddressTracedCallback")
    
  ;
  return tid;
}

XnClient::XnClient ()
{
  NS_LOG_FUNCTION (this);
  m_sent = 0;
  m_socket = 0;
  m_sendEvent = EventId ();
  m_data = 0;
  m_dataSize = 0;
  TotalReceived=0;
  
  //dest_address = "10.1.2.2";
  
  
}

XnClient::~XnClient()
{
  NS_LOG_FUNCTION (this);
  m_socket = 0;

  delete [] m_data;
  m_data = 0;
  m_dataSize = 0;
}

// void
// XnClient::GetMyAddress(string address)
// {
//   NS_LOG_FUNCTION(this<<m_address);
//   m_address = address;
// }

void 
XnClient::SetRemote (Address ip, uint16_t port)
{
  NS_LOG_FUNCTION (this << ip << port);
  m_peerAddress = ip;
  m_peerPort = port;
}

void 
XnClient::SetRemote (Address addr)
{
  NS_LOG_FUNCTION (this << addr);
  m_peerAddress = addr;
}

void
XnClient::DoDispose (void)
{
  NS_LOG_FUNCTION (this);
  Application::DoDispose ();
}

void 
XnClient::StartApplication (void)
{
  NS_LOG_FUNCTION (this);

  if (m_socket == 0)
    {
      TypeId tid = TypeId::LookupByName ("ns3::UdpSocketFactory");
      m_socket = Socket::CreateSocket (GetNode (), tid);
      if (Ipv4Address::IsMatchingType(m_peerAddress) == true)
        {
          if (m_socket->Bind () == -1)
            {
              NS_FATAL_ERROR ("Failed to bind socket");
            }
          m_socket->Connect (InetSocketAddress (Ipv4Address::ConvertFrom(m_peerAddress), m_peerPort));
        }
      else if (Ipv6Address::IsMatchingType(m_peerAddress) == true)
        {
          if (m_socket->Bind6 () == -1)
            {
              NS_FATAL_ERROR ("Failed to bind socket");
            }
          m_socket->Connect (Inet6SocketAddress (Ipv6Address::ConvertFrom(m_peerAddress), m_peerPort));
        }
      else if (InetSocketAddress::IsMatchingType (m_peerAddress) == true)
        {
          if (m_socket->Bind () == -1)
            {
              NS_FATAL_ERROR ("Failed to bind socket");
            }
          m_socket->Connect (m_peerAddress);
        }
      else if (Inet6SocketAddress::IsMatchingType (m_peerAddress) == true)
        {
          if (m_socket->Bind6 () == -1)
            {
              NS_FATAL_ERROR ("Failed to bind socket");
            }
          m_socket->Connect (m_peerAddress);
        }
      else
        {
          NS_ASSERT_MSG (false, "Incompatible address type: " << m_peerAddress);
        }
    }
  
  //注册回调调用handleRead函数
  m_socket->SetRecvCallback (MakeCallback (&XnClient::HandleRead, this));
  m_socket->SetAllowBroadcast (true);
  //调用发送函数
  ScheduleTransmit (Seconds (m_time));
  
}

void 
XnClient::StopApplication ()
{
  NS_LOG_FUNCTION (this);

  if (m_socket != 0) 
    {
      m_socket->Close ();
      m_socket->SetRecvCallback (MakeNullCallback<void, Ptr<Socket> > ());
      m_socket = 0;
    }

  Simulator::Cancel (m_sendEvent);
}

void 
XnClient::SetDataSize (uint32_t dataSize)
{
  NS_LOG_FUNCTION (this << dataSize);

  //
  // If the client is setting the echo packet data size this way, we infer
  // that she doesn't care about the contents of the packet at all, so 
  // neither will we.
  //
  delete [] m_data;
  m_data = 0;
  m_dataSize = 0;
  m_size = dataSize;
}

uint32_t 
XnClient::GetDataSize (void) const
{
  NS_LOG_FUNCTION (this);
  return m_size;
}

void 
XnClient::SetFill (std::string fill)
{
  NS_LOG_FUNCTION (this << fill);

  uint32_t dataSize = fill.size () + 1;

  if (dataSize != m_dataSize)
    {
      delete [] m_data;
      m_data = new uint8_t [dataSize];
      m_dataSize = dataSize;
    }

  memcpy (m_data, fill.c_str (), dataSize);

  //
  // Overwrite packet size attribute.
  //
  m_size = dataSize;
}

void 
XnClient::SetFill (uint8_t fill, uint32_t dataSize)
{
  NS_LOG_FUNCTION (this << fill << dataSize);
  if (dataSize != m_dataSize)
    {
      delete [] m_data;
      m_data = new uint8_t [dataSize];
      m_dataSize = dataSize;
    }

  memset (m_data, fill, dataSize);

  //
  // Overwrite packet size attribute.
  //
  m_size = dataSize;
}

void 
XnClient::SetFill (uint8_t *fill, uint32_t fillSize, uint32_t dataSize)
{
  NS_LOG_FUNCTION (this << fill << fillSize << dataSize);
  if (dataSize != m_dataSize)
    {
      delete [] m_data;
      m_data = new uint8_t [dataSize];
      m_dataSize = dataSize;
    }

  if (fillSize >= dataSize)
    {
      memcpy (m_data, fill, dataSize);
      m_size = dataSize;
      return;
    }

  //
  // Do all but the final fill.
  //
  uint32_t filled = 0;
  while (filled + fillSize < dataSize)
    {
      memcpy (&m_data[filled], fill, fillSize);
      filled += fillSize;
    }

  //
  // Last fill may be partial
  //
  memcpy (&m_data[filled], fill, dataSize - filled);

  //
  // Overwrite packet size attribute.
  //
  m_size = dataSize;
}
//规划发送函数
void 
XnClient::ScheduleTransmit (Time dt)
{
  NS_LOG_FUNCTION (this << dt);
  //利用Schedule安排send发送事件
  //string str = "hello world";
  if(m_count!=0)
  {
  m_sendEvent = Simulator::Schedule (dt, &XnClient::Send, this);
  }
}
//发送函数
void 
XnClient::Send (void)
{
  NS_LOG_FUNCTION (this);
  duration = Time(1000000000.0);
  NS_ASSERT (m_sendEvent.IsExpired ());
  SeqTsHeader seqTs;
  Ptr<Packet> p;
  int z = m_number/256;
  int m = m_number%256;
  //cout<<z<<endl;
  //cout<<m<<endl;
  string m_address = "10.";
  m_address.append(to_string(z+6));
  m_address.append(".");
  m_address.append(to_string(m));
  m_address.append(".2");
  //NS_LOG_INFO(m_address);
  uint8_t buffer[m_size-12];
  uint32_t len = m_address.length();//存储的地址都为9位
  //cout<<len<<endl;
  for(uint32_t i=0;i<len;i++)
  {
    buffer[i]=m_address[i];//char 与 uint_8逐个赋值
  }
  //buffer[len]='\0';
  // buffer[len] = ' ';
  // string load = to_string(m_load);
  // //cout<<load<<endl;
  // uint32_t len1 = load.length();
  // for(uint32_t i =len+1,j =0;i<len+len1+1;i++,j++)
  // {
  //   buffer[i] = load[j];
  // }
  buffer[len]='\0';
  //cout<<buffer<<endl;
  if (m_dataSize)
    {
      //
      // If m_dataSize is non-zero, we have a data buffer of the same size that we
      // are expected to copy and send.  This state of affairs is created if one of
      // the Fill functions is called.  In this case, m_size must have been set
      // to agree with m_dataSize
      //
      NS_ASSERT_MSG (m_dataSize == m_size, "UdpEchoClient::Send(): m_size and m_dataSize inconsistent");
      NS_ASSERT_MSG (m_data, "UdpEchoClient::Send(): m_dataSize but no m_data");
      
      //seqTs.SetSeq(m_sent);
      //NS_LOG_INFO("header time "<<seqTs.GetTs());
      p = Create<Packet>(buffer,sizeof(buffer));
      //p = Create<Packet>(89);
      p->AddHeader(seqTs);
    }
  else
    {
      //
      // If m_dataSize is zero, the client has indicated that it doesn't care
      // about the data itself either by specifying the data size by setting
      // the corresponding attribute or by not calling a SetFill function.  In
      // this case, we don't worry about it either.  But we do allow m_size
      // to have a valXnClient different from the (zero) m_dataSize.
      //
      //seqTs.SetSeq(m_sent);
      //NS_LOG_INFO("header time "<<seqTs.GetTs());
      p = Create<Packet>(buffer,sizeof(buffer));
      //p = Create<Packet>(89-12);
      p->AddHeader(seqTs);
    }
  Address localAddress;
  m_socket->GetSockName (localAddress);
  // call to the trace sinks before the packet is actually sent,
  // so that tags added to the packet can be sent as well
  m_txTrace (p);
  if (Ipv4Address::IsMatchingType (m_peerAddress))
    {
      m_txTraceWithAddresses (p, localAddress, InetSocketAddress (Ipv4Address::ConvertFrom (m_peerAddress), m_peerPort));
    }
  else if (Ipv6Address::IsMatchingType (m_peerAddress))
    {
      m_txTraceWithAddresses (p, localAddress, Inet6SocketAddress (Ipv6Address::ConvertFrom (m_peerAddress), m_peerPort));
    }
  //发送
  m_socket->Send (p);
  start = Simulator::Now ();
  ++m_sent;

  
  if (Ipv4Address::IsMatchingType (m_peerAddress) && log_open==1)
    {
      cout<<"m_address"<<m_address<<endl;
      NS_LOG_INFO ("At time " << Simulator::Now ().As (Time::S) <<  "  "<<m_number<<" XnClient sent " << p->GetSize() << " bytes to " <<
                   Ipv4Address::ConvertFrom (m_peerAddress) << " port " << m_peerPort<<"localAddress"<<InetSocketAddress::ConvertFrom (localAddress).GetIpv4 ());
    }
  else if (Ipv6Address::IsMatchingType (m_peerAddress))
    {
      NS_LOG_INFO ("At time " << Simulator::Now ().As (Time::S) << " client sent " << p->GetSize() << " bytes to " <<
                   Ipv6Address::ConvertFrom (m_peerAddress) << " port " << m_peerPort);
    }
  else if (InetSocketAddress::IsMatchingType (m_peerAddress) && log_open==1)
    {
      NS_LOG_INFO ("At time " << Simulator::Now ().As (Time::S) << "  "<< m_number<<" XnClient sent " << p->GetSize() << " bytes to " <<
                   InetSocketAddress::ConvertFrom (m_peerAddress).GetIpv4 () << " port " << InetSocketAddress::ConvertFrom (m_peerAddress).GetPort ());
    }
  else if (Inet6SocketAddress::IsMatchingType (m_peerAddress))
    {
      NS_LOG_INFO ("At time " << Simulator::Now ().As (Time::S) << " client sent " << p->GetSize() << " bytes to " <<
                   Inet6SocketAddress::ConvertFrom (m_peerAddress).GetIpv6 () << " port " << Inet6SocketAddress::ConvertFrom (m_peerAddress).GetPort ());
    }
  
  if (m_sent < m_count) 
    {
      
      ScheduleTransmit (m_interval);
    }
   
}

void
XnClient::HandleRead (Ptr<Socket> socket)
{
  NS_LOG_FUNCTION (this << socket);
  Ptr<Packet> packet;
  Address from;
  Address localAddress;
 
  while ((packet = socket->RecvFrom (from)))
    { 
      
      if (InetSocketAddress::IsMatchingType (from) && log_open)
        {
          NS_LOG_INFO ("At time " << Simulator::Now ().As (Time::S) <<"  "<<m_number<< " XnClient received " << packet->GetSize () << " bytes from " <<
                       InetSocketAddress::ConvertFrom (from).GetIpv4 () << " port " <<
                       InetSocketAddress::ConvertFrom (from).GetPort ());
        }
      else if (Inet6SocketAddress::IsMatchingType (from) && log_open)
        {
          NS_LOG_INFO ("At time " << Simulator::Now ().As (Time::S) <<"  "<<m_number<< " XnClient received " << packet->GetSize () << " bytes from " <<
                       Inet6SocketAddress::ConvertFrom (from).GetIpv6 () << " port " <<
                       Inet6SocketAddress::ConvertFrom (from).GetPort ());
        }
      
      // socket->GetSockName (localAddress);
      // m_rxTrace (packet);
      // m_rxTraceWithAddresses (packet, from, localAddress);
      if (packet->GetSize () > 0)
        {
          // liuyu_client+=1;
          //     std::cout<<"liuyu_client"<<liuyu_client<<endl;

          uint32_t receivedSize = packet->GetSize ();
          //uint32_t per_receivedSize = receivedSize/m_load;
          SeqTsHeader seqTs;
          Time delay;
          packet->RemoveHeader (seqTs);
          uint32_t currentSequenceNumber = seqTs.GetSeq ();

          uint8_t data[255];
          packet->CopyData(data,sizeof(data));//将包内数据写入到data内
          char a[sizeof(data)];
          for(uint32_t i=0;i<sizeof(data);i++){
              a[i]=data[i];
          }
          string strres = string(a);

          if (InetSocketAddress::IsMatchingType (from))
             {
              // NS_LOG_INFO ("TraceDelay: RX " << receivedSize <<
              //              " bytes from "<< InetSocketAddress::ConvertFrom (from).GetIpv4 () <<
              //              " Sequence Number: " << currentSequenceNumber <<
              //              " Uid: " << packet->GetUid () <<
              //              " TXtime: " << seqTs.GetTs () <<
              //              " RXtime: " << Simulator::Now () <<
              //              " Delay: " << Simulator::Now () - seqTs.GetTs ());
                switch(receivedSize)
                {
                  //----------------------------------xn----------------------//
                    case 139:
                        //创建一个packet类型变量 并设置指针ack_packet
                        {  
                          
                          if(log_open==1)
                          {
                            NS_LOG_INFO ("TraceDelay: RX " << receivedSize <<
                           " bytes from "<< InetSocketAddress::ConvertFrom (from).GetIpv4 () <<
                           " Sequence Number: " << currentSequenceNumber <<
                           " Uid: " << packet->GetUid () <<
                           " TXtime: " << seqTs.GetTs () <<
                           " RXtime: " << Simulator::Now () <<
                           " Delay: " << Simulator::Now () - seqTs.GetTs ());
                          }
                           delay = Simulator::Now () - seqTs.GetTs ();
                           //cout<<m_number << "\t" ;
                          //  cout<<"Number"<<m_number <<"Client"<<std::fixed<<delay.As (Time::MS)<<endl;
                           TotalReceived++;
                           ofstream wfile;
                          //  cout<<target_file_name << endl;
                           wfile.open(target_file_name,ios::app);
                           wfile << m_number<<delay.As (Time::MS)<<"; ";
	                         wfile.close();
                           //cout<<m_number<<"客户端成功接收率:"<<double(TotalReceived)/double(m_count)<<endl;
                           //cout<<(duration).As(Time::S)<<endl;
                            
                          
                        }
                        break;
                     //----------------------------------xn----------------------//  
                        //----------------------------------sr----------------------//
                     case 1478:
                        {  
                          uint8_t buffer[118-12];
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
                        //----------------------------------sr----------------------//

                        //----------------------------------n2----------------------//

                        case 1786:
                        {  
                          uint8_t buffer[678-12];
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
                        case 658:
                        {  
                          uint8_t buffer[119-12];
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
                        //----------------------------------n2----------------------//

                        //----------------------------------se----------------------//
                        case 270:
                        {  
                          uint8_t buffer[117-12];
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
                        //----------------------------------se----------------------//

                }

                

            }
        }
    }
}

} // Namespace ns3