import socket


def main():
    print("Logs from your program will appear here!")
    server_socket = socket.create_server(("localhost", 4221))

    conn, addr = server_socket.accept() # wait for client
    request_client = conn.recv(1024).decode()
    method_http, path, version = request_client.split('\r\n')[0].split()


    if path == '/':
        response = b'HTTP/1.1 200 OK\r\n\r\n'
    elif 'echo' in path:
        body_responce = path.lstrip('/echo/').encode()
        headers_respone = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(body_responce)}\r\n\r\n'.encode()
        response = headers_respone + body_responce
    else:
        response = b'HTTP/1.1 404 Not Found\r\n\r\n'

    conn.sendall(response)
    conn.close()

if __name__ == "__main__":
    main()
