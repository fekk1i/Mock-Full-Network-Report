import datetime
import netmiko
import time
from scapy.all import *
import random

# Enter the IP addresses of the routers in a list
routers = ['192.168.44.130', '192.168.44.140', '192.168.44.150', '192.168.44.160', '192.168.44.170', '192.168.44.180']

#Enter the IP addresses of the switch in a list
switches = ['192.168.44.120']

# Set the username and password for the routers
username = 'admin'
password = 'cisco'


while True:
    # Connect to each router and retrieve the OSPF priority value
    router_priorities = {}
    for router in routers:
        connection = netmiko.ConnectHandler(ip=router, username=username, password=password, device_type='cisco_ios')
        if isinstance(connection, netmiko.base_connection.BaseConnection):
            print(f'Successfully connected to router {router}')
        else:
            print(f'Failed to connect to router {router}')
        connection.secret = password
        connection.enable()
        priority = random.randint(1, 255)
        print(f'Setting OSPF priority on router {router} to {priority}')
        command = f'router ospf 1 priority {priority}'
        # Use the send_config_set method to apply the configuration change
        output = connection.send_config_set([command])
        router_priorities[router] = priority
        connection.disconnect()

    # Check if the routers list is empty
    if not router_priorities:
        print("Error: the router_priorities dictionary is empty")
        exit()

    # Determine the router with the highest OSPF priority
    designated_router = max(router_priorities, key=router_priorities.get)
    print(f'{datetime.now()}: Designated router is {designated_router} with priority {router_priorities[designated_router]}')

    # Connect to each router and check for unknown MAC addresses
    # Connect to each router and check for unknown MAC addresses
    threat_detected = False
    while True:
        for switch in switches:
            connection = netmiko.ConnectHandler(ip=switch, username=username, password=password,
                                                device_type='cisco_ios')
            command = 'show mac address-table'
            output = connection.send_command(command)
            lines = output.split('\n')
            for line in lines:
                # print the MAC address check
                print(f'Checking MAC address on router {switch}: {line}')
                if 'Dynamic' in line:
                    # Extract the MAC address from the line
                    mac_address = line.split()[1]
                    # Set the flag indicating that a threat has been detected
                    threat_detected = True
                    print(f'{datetime.datetime.now()}: Unknown MAC address detected on router {switch}: {line}')
                    # Block the MAC address with the mac access-list extended and deny commands
                    command = f'mac access-list extended BLOCK_THREAT_{switch} deny any host {mac_address}'
                    connection.send_config_set([command])
                    print(f'{datetime.now()}: MAC address {mac_address} blocked on router {switch}')
                    # Start scapy locally and capture packets on the router with the detected threat
                    packets = sniff(iface="Ethernet", filter="host " + switch)
                    # Save the packets to a file
                    wrpcap("captured_packets.pcap", packets)
                    print(f'{datetime.datetime.now()}: Packets saved to captured_packets.pcap')
            connection.disconnect()

            if threat_detected:
                # Restart all the routers
                for router in routers:
                    connection = netmiko.ConnectHandler(ip=router, username=username, password=password,
                                                        device_type='cisco_ios')
                    connection.send_command('reload')
                    connection.disconnect()
                print(f'{datetime.datetime.now()}: All routers restarted due to threat detection')

            # Wait for one day before repeating the process
            time.sleep(3600)
    time.sleep(86400)