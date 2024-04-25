import socket


def main():
    print("Logs from your program will appear here!")
    server_socket = socket.create_server(("localhost", 4221))

    conn, addr = server_socket.accept() # wait for client
    request_client = conn.recv(1024).decode()
    method_http, path, version = request_client.split('\r\n')[0].split()

    ok_res = b"HTTP/1.1 200 OK\r\n\r\n"
    not_found_res = b"HTTP/1.1 404 Not Found\r\n\r\n"

    if path == '/':
        conn.send(ok_res)
    else:
        conn.send(not_found_res)
    
    conn.close()

if __name__ == "__main__":
    main()
