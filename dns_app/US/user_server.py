from flask import Flask, request, jsonify
import logging
import requests
from socket import socket, AF_INET, SOCK_DGRAM, gethostbyname
app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

def send_udp_request(hostname, number, as_ip, as_port):
    message = f"{hostname},{number}"
    as_ip = gethostbyname('localhost')
    with socket(AF_INET, SOCK_DGRAM) as client_socket:
        client_socket.sendto(message.encode(), (as_ip, as_port))
        response, _ = client_socket.recvfrom(2048)
    return response.decode()

@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')
   
    
    if not all([hostname, fs_port, number, as_ip, as_port]):
        return jsonify("Required parameters are not given"), 400
  
    logging.info(f"Request received: {hostname}, {fs_port}, {number}, {as_ip}, {as_port}")

    as_response = send_udp_request(hostname, number, as_ip, int(as_port))
    logging.info(f"Response from AS: {as_response}")
    ip, port = as_response.split(",")


    fs_response = requests.get(f"http://{ip}:{port}/fibonacci?number={number}")
    logging.info(fs_response)
    return jsonify(fs_response.json()), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
