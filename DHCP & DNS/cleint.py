from scapy.all import*
import time
import socket

def dhcp_discover():
    print("#####DHCP#####")
    cleint_ip = "0.0.0.0" 
    broadcast_ip = "255.255.255.255" #dest
    subnet_mask = "255.255.255.0"
    life_time = 3600 #how much time the cleint have 
    
    print("create DISCOVER packet..")
    # Create the Ethernet, IP, UDP and BOOTP layers
    ether_pkt = Ether(dst="ff:ff:ff:ff:ff:ff")
    ip_pkt = IP(src=cleint_ip, dst=broadcast_ip)
    udp_pkt = UDP(sport =68 , dport =67)
    bootp_pkt =BOOTP(chaddr="16:10:87:64:c2:1f", xid=0x87654321) 
    # Create the DHCP OFFER message
    dhcp_discover = DHCP(options=[("message-type","discover"), 
                                ("lease_time", life_time),
                                ("subnet_mask", subnet_mask),
                                "end"])
    discover_pkt = ether_pkt/ip_pkt/udp_pkt/bootp_pkt/dhcp_discover
    print("DONE!")

    time.sleep(1)
    sendp(discover_pkt)
    print("The discovery packet has been sent!")
    sniff(filter="udp and port 67", prn=dhcp_request, count=1, iface="enp0s3")


def dhcp_request(pkt):
    client_ip = pkt[BOOTP].yiaddr
  
    broadcast_ip = "255.255.255.255" #dest
    subnet_mask = "255.255.255.0"
    life_time = 3600 #how much time stay up 
   
    print("create REQUEST packet..")

    # Create the Ethernet, IP, UDP and BOOTP layers
    ether_pkt = Ether(dst="ff:ff:ff:ff:ff:ff")
    ip_pkt = IP(src="0.0.0.0", dst=broadcast_ip)
    udp_pkt = UDP(sport =68 , dport =67)
    bootp_pkt =BOOTP(chaddr="16:10:87:64:c2:1f", yiaddr=client_ip, xid=pkt[BOOTP].xid) 
    # Create the DHCP REQUEST message
    dhcp_request = DHCP(options=[("message-type","request"), 
                                    ("lease_time", life_time),
                                    ("subnet_mask", subnet_mask),
                                    "end"])
    request_pkt = ether_pkt/ip_pkt/udp_pkt/bootp_pkt/dhcp_request
    print("DONE!")

    time.sleep(1)
    sendp(request_pkt)
    print("The request packet has been sent!")
    sniff(filter="udp and port 67", count=1, iface="enp0s3")

def dns():
    print("#####DNS#####")
    server_address = ('localhost', 53)
    dns_req = DNS(rd=1, qd=DNSQR(qname='hello.world'))

    # create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # s.bind(server_address)
    # send DNS request data
    s.sendto(dns_req.__bytes__(), server_address)
    # parse data as DNS
    resp = DNS(s.recv(1024))
    # print IP address
    print(resp[DNSRR].rrname)


if __name__ == '__main__':
    dhcp_discover() #for run part 1 -DHCP
    dns() #for run part 2 -DNS
