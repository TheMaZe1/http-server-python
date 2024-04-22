import socket


def main():
    print("Logs from your program will appear here!")
    server_socket = socket.create_server(("localhost", 4221))

    conn, addr = server_socket.accept() # wait for client
    http_response = b'HTTP/1.1 200 OK\r\n\r\n'
    conn.send(http_response)
    conn.close()

if __name__ == "__main__":
    main()
