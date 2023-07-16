import socket
import sys
import urlvalidator

ip = ''
Port = 20287
redirect_port = 30776
# redirect_ip = '10.0.2.15' #change to your ip tcp_server
redirect_ip = '10.0.2.15' #change to your ip tcp_server
# redirect_ip=''
redirect_url = f'http://{redirect_ip}:{redirect_port}'






# class MyTCPHandler(socketserver.BaseRequestHandler):
#     def handle(self):
#         request = HTTP(
#             self.request.recv(1024).strip()
#         )
#         print("{} wrote:".format(self.client_address[0]))
#         print(request[HTTP])
#         if request.Method == b'GET':
#             if request.Path == b'/':
#                 response = HTTP() / HTTPResponse(
#                     Status_Code=b'302',
#                     Reason_Phrase=b'Found',
#                     Location=b'http://localhost:8081/'
#                 )
#         self.request.sendall(response.__bytes__())

# check_url.
def check_url(url: str):
    validator = urlvalidator.URLValidator()
    try:
        validator(url)
        return True
    except urlvalidator.exceptions.ValidationError as exception:
        print(exception)
        return False


def get_url():
    action_mode = input('Enter 1 to choose a URL or any other number to redirect url: ')
    #For submission we don't want to use the digit 1
    if action_mode == '1':
        url = input('Enter the URL to redirect to: ')
        if not check_url(url):
            print('Invalid URL')
            sys.exit()
    else:
        url = redirect_url
    # if no URL was entered, redirect to localhost
    return url


if __name__ == '__main__':
    redirect_url = get_url()
  
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print('Failed to create socket. error' + e.__str__() + ' exiting now')
        sys.exit()
    try:
        sock.bind(('', 20287))
    except OSError as e:
        print('Cannot Bind Socket to this address.\nerror : ' + e.__str__() + '\nexiting now')
        sock.close()
        sys.exit()

    # listen to 10 connections at a time
    sock.listen(10)

    while True:
        try:
            #connections from client
            client_sock, address = sock.accept()
            print('Connected with ' + address[0] + ':' + str(address[1]))
            data = client_sock.recv(1024)
            print(data.decode())
            if data:
                #  response
                response = f"HTTP/1.1 301 Moved Permanently\r\nLocation: {redirect_url}\r\nContent-Type: " \
                           f"text/html\r\nContent-Length: 0\r\n\r\n "
                print(response)
                client_sock.send(response.encode())
        except Exception as e:
            print('Error Occurred while handling client request exiting now')
            print(e.__str__())
            client_sock.close()
            sock.close()
            sys.exit()
