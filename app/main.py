import socket
from threading import Thread

def client_handler(connection, address):

    request_client = connection.recv(1024).decode()
    headers = request_client.split('\r\n')
    method_http, path, version = headers[0].split()
    user_agent = headers[2].split()[1]

    if path == '/':
        response = b'HTTP/1.1 200 OK\r\n\r\n'
    elif 'echo' in path:
        body_response = path[len('/echo/'):].encode()
        headers_respone = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(body_response)}\r\n\r\n'.encode()
        response = headers_respone + body_response
    elif 'user-agent' in path:
        headers_respone = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n'.encode()
        response = headers_respone + f'{user_agent}'.encode()
    else:
        response = b'HTTP/1.1 404 Not Found\r\n\r\n'

    connection.sendall(response)
    connection.close()


def main():
    print("Logs from your program will appear here!")
    server_socket = socket.create_server(("localhost", 4221))

    while True:
        conn, addr = server_socket.accept() # wait for client
        thread = Thread(target=client_handler, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    main()
