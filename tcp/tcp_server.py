import os
import socket
import sys
import os

file_name = 'file_to_download.txt'


# function to read the file contents
def get_file(file_name):
    with open(file_name, 'r') as f:
        contents = f.read()
        #we sened the file to client 
        f.close()

    return contents


def create_msg(param, file_tosened):
    #  response 
    responseee = f'HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Disposition: attachment; filename="{file_name}"\r\nContent-Length: {len(file_tosened)}\r\n'
    responseee+=file_tosened
    
    return responseee



if __name__ == '__main__':
    file_tosened = get_file(file_name)

    # creating socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print('Failed to create socket. Error code: ' + e.__str__() + ' exiting now')
        sys.exit()

    # binding socket to the desired port and ip
    try:
        sock.bind(('', 30776))
    except OSError as e:
        print('Cannot Bind . error : ' + e.__str__() + ' exit')
        sock.close()
        sys.exit()

    sock.listen(10)
    while True:
        try:
            client_sock, address = sock.accept()
            print('Connected with ' + address[0] + ':' + str(address[1]))
            request = client_sock.recv(1024)

            if request:
                #answer = create_msg(request, file_tosened)
                answer = create_msg(request.decode(), file_tosened)
                #print(before sened)
                client_sock.send(answer.encode())
                print('sened answer')
            client_sock.close()

        except Exception as e:
            print(e.__str__())
            #print(xceptione)
            print('error , exit')
            client_sock.close()
            sock.close()
            sys.exit()
