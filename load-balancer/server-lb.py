#!/usr/bin/python3

import socket
import argparse
import json
import time
import threading

CONFIG = None
BACKEND_CONNECTIONS = []
CLIENT_CONNECTIONS = []
CLIENT_SOCKET = None

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

def direct_data_to_backend(connection, backend_sockets, index):
    backend_index = 0
    num_backends = len(backend_sockets)
    with connection:
        while True:
            data = connection.recv(200)
            if not data:
                break
            print(f"Repassando dados pro backend {backend_index}: ", data)
            backend_sockets[backend_index].send(data)
            backend_index = (backend_index + 1) % num_backends
    print(f"Encerrando conexão {index}...")

# TODO: encerrar todas as conexões em caso de shutdown do LB
def manage_connections(config):
    global BACKEND_CONNECTIONS, CLIENT_CONNECTIONS, CLIENT_SOCKET
    BACKEND_CONNECTIONS = [connect_to_backend(backend) for backend in config["backends"]]
    threads = []

    CLIENT_SOCKET = socket.socket()
    CLIENT_SOCKET.bind(('127.0.0.1', config["server"]["port"]))
    CLIENT_SOCKET.listen(config["server"]["max_connections"])
    with CLIENT_SOCKET:
        while True:
            conn, address = CLIENT_SOCKET.accept()
            CLIENT_CONNECTIONS.append(conn)
            print("Conexão aceita no endereço ", address)
            t = threading.Thread(target=direct_data_to_backend, args=(conn, BACKEND_CONNECTIONS, len(threads)))
            t.start()
            threads.append(t)
    for thread in threads:
        thread.join()
    print("Saindo da gestão de conexões...")

# TODO: gerenciar corretamente as conexões em caso de shutdown do LB, ele tá ficando preso e não encerra de vdd
if __name__ == '__main__':
    try:
        args = parse_args()
        CONFIG = read_configuration(args.conf)
        manage_connections(CONFIG)
    except KeyboardInterrupt as e:
        print("Recebi sinal de encerramento de programa. Encerrando...")
    finally:
        print("Fechando conexões com backends...")
        for conn in BACKEND_CONNECTIONS:
            conn.close()
        print("Fechando conexões com clientes...")
        for conn in CLIENT_CONNECTIONS:
            conn.close()
        print("Fechando socket do cliente...")
        CLIENT_SOCKET.close()
        print("Tchau!")
