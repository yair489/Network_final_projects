from scapy.all import*
import time

global i #for determine new ip 
i=1

def dhcp_offer(pkt):
    global i
    print("got a packet")
    #first thing we need to chek if DHCP layer is in the pkt 
    #second thing we check if the pkt is a DHCP discover packet by check if the second number in the tuple is 1

    if DHCP in pkt and pkt[DHCP].options[0][1] == 1:
        print("it is a DISCOVERY packet!")
        
        determine_ip= "10.0.0." + str(i)
        i+=1
        if(i==254):
            i=0 
        #we determine the ip address below like the book
        server_ip = "223.1.2.5" #IP address of the DHCP server that is making the offer
        broadcast_ip = "255.255.255.255" #dest
        router = "192.168.1.1" 
        subnet_mask = "255.255.255.0"
        life_time = 3600 #how much time the cleint have 

        print("create OFFER packet..")
        # Create the Ethernet, IP, UDP and BOOTP layers
        ether_pkt = Ether(dst="ff:ff:ff:ff:ff:ff")
        ip_pkt = IP(src=server_ip, dst=broadcast_ip)
        udp_pkt = UDP(sport =67 , dport =68)
        bootp_pkt = BOOTP(op=2, yiaddr=determine_ip, siaddr=server_ip, giaddr="0.0.0.0", xid=pkt[BOOTP].xid) 
        # Create the DHCP OFFER message
        dhcp_offer = DHCP(options=[("message-type","offer"), 
                                    ("lease_time", life_time),
                                    ("subnet_mask", subnet_mask),
                                    ("router", router),
                                    "end"])
        offer_pkt = ether_pkt/ip_pkt/udp_pkt/bootp_pkt/dhcp_offer
        print("DONE!")

        time.sleep(1)
        sendp(offer_pkt, iface="enp0s3")
        print("The offer packet has been sent!")


        sniff(filter="udp and port 68", prn=dhcp_ack, count=1, iface="enp0s3")

def dhcp_ack(pkt):
    print("got a packet")
    if DHCP in pkt and pkt[DHCP].options[0][1] == 3:
        print("it is a REQUEST packet!")

        requested_ip = pkt[BOOTP].yiaddr
        server_ip = "192.168.1.1" 
        broadcast_ip = "255.255.255.255"
        router = "10.0.0.18" 
        subnet_mask = "255.255.255.0"
        life_time = 3600

        print("create ACK packet..")
        # Create the DHCP ACK message
        dhcp_ack = DHCP(options=[("message-type", "ack"),
                                # ("server_id", server_ip),
                                ("lease_time", life_time),
                                ("subnet_mask", subnet_mask),
                                ("router", router),
                                "end"])
        # Create the Ethernet, IP, UDP and BOOTP layers
        ether_pkt = Ether(dst="ff:ff:ff:ff:ff:ff")
        ip_pkt = IP(src=server_ip, dst=broadcast_ip)
        udp_pkt = UDP(sport=67, dport=68)
        bootp_pkt = BOOTP(op=2, yiaddr=requested_ip, siaddr= pkt[BOOTP].siaddr, giaddr = "0.0.0.0", xid=pkt[BOOTP].xid)

        # combine the dhcp offer packet
        ack_pkt = ether_pkt/ip_pkt/udp_pkt/bootp_pkt/dhcp_ack
        print("DONE!")
        
        time.sleep(1)
        sendp(ack_pkt , iface = "enp0s3")
        print("The ack packet has been sent!")




if __name__ == '__main__':
    print('running server')
    sniff(filter="udp and port 68", prn=dhcp_offer, iface="enp0s3")