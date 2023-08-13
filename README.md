# Mock-Full-Network-Report

KonnectiCo is an internet service provider (ISP) that aims always to provide secured
services to their clients. One of their subdomains consists of 6 routers connected to a
switch where the routers use single area OSPF protocol over this multiaccess network
and each one serves a group of customers

1. The ISP Head Quarter Manager (IHQM) consulted you as a professional network
administrator to implement and secure the communication over the multiaccess
network by admitting all security concerns related to the OSPF routing protocol,
and switch port security and any other additional security measurement
considering the CIA triad.

3. The IHQM requested you to build a security network thread or tool that will be
considered in SDN in later stages. This thread will perform SSH connection to all
company routers and switches considering networking automation using python,
where all these routers are connected together via a switch over a multiaccess
network using single area OSPF protocol. The main aim of this tool is to change
the configuration of the switch whenever unknown traffic is detected over the
multiaccess network. Another process considered by the network tool is changing
the Designated Router (DR) on daily basis over the shared network to avoid the
same DR election whenever the shared switch is restarted. The threat is detected
by the thread over the shared network if unknown source and destination mac
addresses are detected or other than OSPF routing information or network control
PDUs are circulating over the network. A mac address is considered unknown if it
doesn’t belong to any of the router interfaces over the shared multi-access
network. Once a threat is detected the thread will change the operating VLAN
connecting the routers over the multi-access network to another one and forward
a copy to VLAN 88 which is connected to a server having an AI application that
inspects the PDU over several layers, to enhance the future defense.

The thread works as follows:
• The thread extracts the source and destination mac addresses of any PDU
circulating over the multiaccess network.

• The thread compares it with the trusted mac addresses of the routers’
interfaces connected to the switch to confirm that it is sent locally.

• The thread extracts the information from the routing packet to verify that
the packet is a valid routing PDU from the trusted OSPF domain.

• In case of a PDU that doesn’t comply with the above requirements, the
thread will forward the PDU to the AI application for further inspection.

Standing from the above requirements, you are requested to prepare a detailed report
illustrating the topology where you have the freedom to consider any virtual environment
(GNS3, Virtual Box, …) to implement the requested tasks from the IHQM. The detailed
report should be delivered considering the planning, used devices and their models,
configuration, budget estimation, commented code snippets, and all technical information.

You should make valid assumptions in a way that they are oriented to the requested tasks.
