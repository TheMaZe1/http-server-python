import socket


def main():
    print("Logs from your program will appear here!")
    server_socket = socket.create_server(("localhost", 4221))

    conn, addr = server_socket.accept() # wait for client
    request_client = conn.recv(1024).decode()
    method_http, path, version = request_client.split('\r\n')[0].split()

    headers_respone = b'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 3\r\n\r\n'
    body_responce = path.split('/')[-1].encode()

    if path == '/':
        conn.sendall(b'HTTP/1.1 200 OK\r\n\r\n')
    elif 'echo' in path:
        headers_respone = b'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 3\r\n\r\n'
        body_responce = path.lstrip('/echo/').encode() + b'\r\n'
        conn.sendall(headers_respone + body_responce)
    else:
        conn.sendall(b'HTTP/1.1 404 Not Found\r\n\r\n')

    
    conn.close()

if __name__ == "__main__":
    main()
