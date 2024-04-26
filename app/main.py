import socket
from threading import Thread
import os
import sys

def client_handler(connection, address):

    data = connection.recv(4096).decode()
    headers = data.split('\r\n')
    method_http, path, version = headers[0].split()
    if method_http == 'GET':
        response =get_handler(connection, data)
    elif method_http == 'POST':
        response = post_handler(connection, data)
    
    connection.sendall(response)
    connection.close()

def get_handler(connection, data):

    headers = data.split('\r\n')
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
        dir = ''
        if len(sys.argv) > 2:
            dir = sys.argv[2]
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
    return response


def post_handler(connection, data):

    headers = data.split('\r\n')
    method_http, path, version = headers[0].split()

    dir = ''
    if len(sys.argv) > 2:
        dir = sys.argv[2]

    filename = path[len('/files/'):]
    if os.path.exists(dir):
        with open(dir + '/' + filename, 'wb') as f:
            f.write(data.split('\r\n\r\n')[1])
            headers_respone = f'HTTP/1.1 201 OK\r\n\r\n'.encode()
            response = headers_respone
    else:
        os.mkdir(dir)
        with open(dir + '/' + filename, 'wb') as f:
            f.write(data.split('\r\n\r\n')[1])
            headers_respone = f'HTTP/1.1 201 OK\r\n\r\n'.encode()
            response = headers_respone
    return response

def main():
    server_socket = socket.create_server(("localhost", 4221))

    while True:
        conn, addr = server_socket.accept() # wait for client
        thread = Thread(target=client_handler, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    main()
