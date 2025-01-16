import string
import socket
import argparse
import threading


YELLOW = "\033[93m"
GREEN = "\033[92m"
RESET = "\033[00m"


def init_argparse():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Intercept communication with this simple tcp proxy script",
        epilog="""
https://github.com/barishaxxer

python main.py -lp [--local-port] -ri [--remote-ip] -rp [--remote-port]

then connect to the proxy server by: 
    telnet [proxy-servers-ip-addr] [proxy-servers-port]
        
        """,
    )
    parser.add_argument("-lp", "--local-port", required=True, type=int)
    parser.add_argument("-ri", "--remote-ip", required=True, type=str)
    parser.add_argument("-rp", "--remote-port", required=True, type=int)
    parser.add_argument("-rf", "--receive-first", action="store_true")
    args = parser.parse_args()
    return args


def main():
    args = init_argparse()

    start_proxy(args.local_port, args.remote_ip, args.remote_port, args.receive_first)


def start_proxy(local_port, remote_ip, remote_port, receive_first):
    w_response = receive_first
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("localhost", local_port))
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.listen(5)
    while True:
        client_sock, addr = sock.accept()
        thread = threading.Thread(
            target=handler, args=(client_sock, remote_ip, remote_port, w_response)
        )
        thread.start()


def receive(arg_socket):
    arg_socket.settimeout(30)
    buffer = b""
    data = arg_socket.recv(4096)
    buffer += data
    while len(data) == 4096:

        data = arg_socket.recv(4096)
        buffer += data

    return buffer


def handler(client_socket, remote_ip, remote_port, receive_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_ip, remote_port))
    if receive_first:
        data = receive(remote_socket)
        print(GREEN + "Response being sent by server to client" + RESET)
        client_socket.sendall(data)
        hexdump(data)

    while True:

        client_request = receive(client_socket)

        remote_socket.sendall(client_request)
        print(YELLOW + "Client request is being sent to the server" + RESET)
        hexdump(client_request)

        remote_response = receive(remote_socket)
        print(GREEN + "Server response is being sent to the client" + RESET)
        hexdump(remote_response)

        client_socket.sendall(remote_response)


def hexdump(data):
    partition_length = 16
    if isinstance(data, bytes):
        data = data.decode()

    data = "".join([j if j in string.printable else "." for j in data])

    for i in range(0, len(data), partition_length):
        print(f"{i:07X}", end="\n")
        hex_value = [f"{ord(b):02X}" for b in data[i : i + partition_length]]
        for n, a in enumerate(hex_value):
            if n == len(hex_value) - 1:
                print(a)
                print(data[i : i + partition_length])
            else:
                print(a, end=" ")


if __name__ == "__main__":
    main()
