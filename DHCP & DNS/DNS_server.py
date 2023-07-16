'''Run with:
python ./dns_server.py
'''
from scapy.all import *
import socketserver

#maps domain names to IP addresses
DNS_HOSTS = {
    b'hello.world.': b'10.0.0.17', 
    b'foo.bar.': b'1.2.3.4'
}


class MyUDPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request[0].strip()
        sock = self.request[1]
        pkt = DNS(data)
        qname = pkt[DNSQR].qname
        
        print('handling dns query from client {} for domain name {}'.format(self.client_address[0], qname))
        
        if qname in DNS_HOSTS:
            pkt[DNS].an = DNSRR(rrname=qname, rdata=DNS_HOSTS[qname])
            pkt[DNS].ancount = 1
        else:
            #  if the requested domain name is not found in the DNS_HOSTS dictionary, we creates a default DNS response packet
            qid = pkt[DNS].id
            pkt = DNS(b'\x00\x00\x81\x83\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x01\x00\x00\x06\x00\x01\x00\x00*0\x00@\x01a\x0croot-servers\x03net\x00\x05nstld\x0cverisign-grs\x03com\x00x\x94\xfdT\x00\x00\x07\x08\x00\x00\x03\x84\x00\t:\x80\x00\x01Q\x80')
            pkt[DNS].id = qid
            pkt[DNSQR].qname = qname
        
        pkt[DNS].qr = 1 #for declare the packet as response packet

        sock.sendto(pkt.__bytes__(), self.client_address)

if __name__ == "__main__":
    #beacuse it a local server
    HOST, PORT = "localhost", 53

    print('running server')

    with socketserver.UDPServer((HOST, PORT), MyUDPHandler) as server:
        server.serve_forever() #start the server and handling requests
