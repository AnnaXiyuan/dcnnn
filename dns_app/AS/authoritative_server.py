import socket
import json

dns_records = {}

def udp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(('0.0.0.0', 53533))
        while True:
            data, addr = sock.recvfrom(1024)
            parts = data.decode().split(',')
            hostname = parts[0]
            print("message received:", parts)
            if len(parts) == 3:  # hostname, IP, and port provided
                fs_ip, fs_port = parts[1], parts[2]
                dns_records[hostname] = (fs_ip, fs_port)
                print(f'Registered {hostname} -> {fs_ip}:{fs_port}')
            elif len(parts) == 2:  # only hostname provided
                if hostname in dns_records:
                    print("目前存的东西", dns_records)
                    fs_ip, fs_port = dns_records[hostname]
                    response = f"{fs_ip},{fs_port}"
                    sock.sendto(response.encode(), addr)
                    print(f'Returned {hostname} -> {fs_ip}:{fs_port}')
                else:
                    print(f'Hostname {hostname} not found')
            else:
                print('Invalid data format')



def main():
    udp_server()

if __name__ == '__main__':
    main()
