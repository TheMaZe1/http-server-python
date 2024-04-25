import socket
from threading import Thread
import os
import sys

def client_handler(connection, address, dir=''):

    request_client = connection.recv(1024).decode()
    headers = request_client.split('\r\n')
    method_http, path, version = headers[0].split()

    if path == '/':
        response = b'HTTP/1.1 200 OK\r\n\r\n'
    elif 'echo' in path:
        body_response = path[len('/echo/'):].encode()
        headers_respone = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(body_response)}\r\n\r\n'.encode()
        response = headers_respone + body_response
    elif 'user-agent' in path:
        user_agent = headers[2].split()[1]
        headers_respone = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n'.encode()
        response = headers_respone + f'{user_agent}'.encode()
    elif 'files' in path:
        filename = path[len('/files/'):]
        if os.path.exists(dir + '/' + filename):
            with open(dir + '/' + filename, 'rb') as f:
                data = f.read()
                headers_respone = f'HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(data)}\r\n\r\n'.encode()
                response = headers_respone + data
        else:
            response = b'HTTP/1.1 404 Not Found\r\n\r\n'
    else:
        response = b'HTTP/1.1 404 Not Found\r\n\r\n'

    connection.sendall(response)
    connection.close()


def main():
    print("Logs from your program will appear here!")
    server_socket = socket.create_server(("localhost", 4221))
    dir = ''
    if len(sys.argv) > 2:
        dir = sys.argv[2]

    while True:
        conn, addr = server_socket.accept() # wait for client
        if dir:
            thread = Thread(target=client_handler, args=(conn, addr, dir))
        else:
            thread = Thread(target=client_handler, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    main()
