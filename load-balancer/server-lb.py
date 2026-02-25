#!/usr/bin/python3

import socket
import argparse
import json
import time
import threading

CONFIG = None

def parse_args():
    parser = argparse.ArgumentParser(description='Majão load balancer')
    parser.add_argument('--conf', help='Configuration file to be used')
    return parser.parse_args()


def read_configuration(filename):
    try:
        with open(filename) as file:
            raw_config = file.read()
            return json.loads(raw_config)
    except Exception as e:
        print(e)

def connect_to_backend(backend):
    sock = socket.socket()
    sock.connect((backend["ip"], backend["port"]))
    # TODO antes de retornar ver se o backend de fato esta alive ou tirar ele do LB
    return sock

def direct_data_to_backend(connection, backend_socket):
    while True:
        data = connection.recv(200)
        if not data:
            return
        print("Repassando dados pro backend: ", data)
        backend_socket.send(data)

def manage_connections(config):
    backend_sockets = [connect_to_backend(backend) for backend in config["backends"]]

    client_socket = socket.socket()
    client_socket.bind(('127.0.0.1', config["server"]["port"]))
    client_socket.listen(config["server"]["max_connections"])
    with client_socket:
        while True:
            conn, address = client_socket.accept()
            print("Conexão aceita no endereço ", address)
            with conn:
                t = threading.Thread(target=direct_data_to_backend, args=(conn, backend_sockets[0]))
                t.start()
                t.join()
    print("Saindo da gestão de conexões...")


if __name__ == '__main__':
    args = parse_args()
    CONFIG = read_configuration(args.conf)
    manage_connections(CONFIG)
    print("Encerrando programa...")
