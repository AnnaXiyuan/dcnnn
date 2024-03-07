from flask import Flask, request
import requests
import socket

app = Flask(__name__)




def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

@app.route('/fibonacci', methods=['GET'])
def fib():
    number = int(request.args.get('number'))
    result = fibonacci(number)
    return str(result)


@app.route('/register', methods=['PUT'])
def register():
    hostname = request.json['hostname']
    fs_ip = request.json['fs_ip']
    fs_port = request.json['fs_port']

    # Register with AS using UDP
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        message = f'{hostname},{fs_ip},{fs_port}'
        sock.sendto(message.encode(), ('0.0.0.0', int(53533)))

    return 'Registered successfully', 200

def register(hostname, fs_ip, fs_port):
    # Register with AS using UDP
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        message = f'{hostname},{fs_ip},{fs_port}'
        sock.sendto(message.encode(), ('0.0.0.0', int(53533)))

    return 'Registered successfully', 200

if __name__ == '__main__':
    (register('fibonacci.com', '127.0.0.1', '9090'))
    app.run(debug=True, port=9090)
