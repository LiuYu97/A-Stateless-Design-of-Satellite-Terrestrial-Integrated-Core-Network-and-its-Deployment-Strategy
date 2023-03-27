#include "Xn-helper.h"
#include "ns3/Xn-Client.h"
#include "ns3/Xn-AMF.h"
#include "ns3/Xn-SMF.h"
#include "ns3/Xn-UPF.h"
#include "ns3/uinteger.h"
#include "ns3/names.h"

namespace ns3 {

XnUPFHelper::XnUPFHelper (uint16_t port)
{
  m_factory.SetTypeId (XnUPF::GetTypeId ());
  SetAttribute ("Port", UintegerValue (port));
}

void 
XnUPFHelper::SetAttribute (
  std::string name, 
  const AttributeValue &value)
{
  m_factory.Set (name, value);
}

ApplicationContainer
XnUPFHelper::Install (Ptr<Node> node) const
{
  return ApplicationContainer (InstallPriv (node));
}

ApplicationContainer
XnUPFHelper::Install (std::string nodeName) const
{
  Ptr<Node> node = Names::Find<Node> (nodeName);
  return ApplicationContainer (InstallPriv (node));
}

ApplicationContainer
XnUPFHelper::Install (NodeContainer c) const
{
  ApplicationContainer apps;
  for (NodeContainer::Iterator i = c.Begin (); i != c.End (); ++i)
    {
      apps.Add (InstallPriv (*i));
    }

  return apps;
}

Ptr<Application>
XnUPFHelper::InstallPriv (Ptr<Node> node) const
{
  Ptr<Application> app = m_factory.Create<XnUPF> ();
  node->AddApplication (app);

  return app;
}



// XnAMFHelper::XnAMFHelper (uint16_t port)
// {
//   m_factory.SetTypeId (XnAMF::GetTypeId ());
//   SetAttribute ("Port", UintegerValue (port));
// }

XnAMFHelper::XnAMFHelper (Address SMF_address, uint16_t SMF_port)
{
  m_factory.SetTypeId (XnAMF::GetTypeId ());
  SetAttribute ("SMFAddress", AddressValue (SMF_address));
  SetAttribute ("SMFPort", UintegerValue (SMF_port));
  
  
}

void 
XnAMFHelper::SetAttribute (
  std::string name, 
  const AttributeValue &value)
{
  m_factory.Set (name, value);
}

ApplicationContainer
XnAMFHelper::Install (Ptr<Node> node) const
{
  return ApplicationContainer (InstallPriv (node));
}

ApplicationContainer
XnAMFHelper::Install (std::string nodeName) const
{
  Ptr<Node> node = Names::Find<Node> (nodeName);
  return ApplicationContainer (InstallPriv (node));
}

ApplicationContainer
XnAMFHelper::Install (NodeContainer c) const
{
  ApplicationContainer apps;
  for (NodeContainer::Iterator i = c.Begin (); i != c.End (); ++i)
    {
      apps.Add (InstallPriv (*i));
    }

  return apps;
}

Ptr<Application>
XnAMFHelper::InstallPriv (Ptr<Node> node) const
{
  Ptr<Application> app = m_factory.Create<XnAMF> ();
  node->AddApplication (app);

  return app;
}


// XnSMFHelper::XnSMFHelper (uint16_t port)
// {
//   m_factory.SetTypeId (XnSMF::GetTypeId ());
//   SetAttribute ("Port", UintegerValue (port));
// }

XnSMFHelper::XnSMFHelper (Address UPF_address, uint16_t UPF_port)
{
  m_factory.SetTypeId (XnSMF::GetTypeId ());
  SetAttribute ("UPFAddress", AddressValue (UPF_address));
  SetAttribute ("UPFPort", UintegerValue (UPF_port));
  // SetAttribute ("AMFAddress", AddressValue (AMF_address));
  // SetAttribute ("AMFPort", UintegerValue (AMF_port));
  //SetAttribute ("Port", UintegerValue (port));
}

void 
XnSMFHelper::SetAttribute (
  std::string name, 
  const AttributeValue &value)
{
  m_factory.Set (name, value);
}

ApplicationContainer
XnSMFHelper::Install (Ptr<Node> node) const
{
  return ApplicationContainer (InstallPriv (node));
}

ApplicationContainer
XnSMFHelper::Install (std::string nodeName) const
{
  Ptr<Node> node = Names::Find<Node> (nodeName);
  return ApplicationContainer (InstallPriv (node));
}

ApplicationContainer
XnSMFHelper::Install (NodeContainer c) const
{
  ApplicationContainer apps;
  for (NodeContainer::Iterator i = c.Begin (); i != c.End (); ++i)
    {
      apps.Add (InstallPriv (*i));
    }

  return apps;
}

Ptr<Application>
XnSMFHelper::InstallPriv (Ptr<Node> node) const
{
  Ptr<Application> app = m_factory.Create<XnSMF> ();
  node->AddApplication (app);

  return app;
}





XnClientHelper::XnClientHelper (Address address, uint16_t port)
{
  m_factory.SetTypeId (XnClient::GetTypeId ());
  SetAttribute ("RemoteAddress", AddressValue (address));
  SetAttribute ("RemotePort", UintegerValue (port));
}

XnClientHelper::XnClientHelper (Address address)
{
  m_factory.SetTypeId (XnClient::GetTypeId ());
  SetAttribute ("RemoteAddress", AddressValue (address));
}

void 
XnClientHelper::SetAttribute (
  std::string name, 
  const AttributeValue &value)
{
  m_factory.Set (name, value);
}

// void 
// XnClientHelper::GetMyAddress(Ptr<Application> app,std::string address)
// {
//   app->GetObject<XnClient>()->GetMyAddress(address);
// }

void
XnClientHelper::SetFill (Ptr<Application> app, std::string fill)
{
  app->GetObject<XnClient>()->SetFill (fill);
}

void
XnClientHelper::SetFill (Ptr<Application> app, uint8_t fill, uint32_t dataLength)
{
  app->GetObject<XnClient>()->SetFill (fill, dataLength);
}

void
XnClientHelper::SetFill (Ptr<Application> app, uint8_t *fill, uint32_t fillLength, uint32_t dataLength)
{
  app->GetObject<XnClient>()->SetFill (fill, fillLength, dataLength);
}

ApplicationContainer
XnClientHelper::Install (Ptr<Node> node) const
{
  return ApplicationContainer (InstallPriv (node));
}

ApplicationContainer
XnClientHelper::Install (std::string nodeName) const
{
  Ptr<Node> node = Names::Find<Node> (nodeName);
  return ApplicationContainer (InstallPriv (node));
}

ApplicationContainer
XnClientHelper::Install (NodeContainer c) const
{
  ApplicationContainer apps;
  for (NodeContainer::Iterator i = c.Begin (); i != c.End (); ++i)
    {
      apps.Add (InstallPriv (*i));
    }

  return apps;
}

Ptr<Application>
XnClientHelper::InstallPriv (Ptr<Node> node) const
{
  Ptr<Application> app = m_factory.Create<XnClient> ();
  node->AddApplication (app);

  return app;
}

} // namespace ns3
