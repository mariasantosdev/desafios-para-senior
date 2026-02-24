#!/usr/bin/python3

import socket
import argparse
import json
import time

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

    except e:
        print(e)


def connect_to_backend(backend):
    sock = socket.socket()
    sock.connect((backend["ip"], backend["port"]))
    # TODO antes de retornar ver se o backend de fato esta alive ou tirar ele do LB
    return sock


def manage_connections(config):
    for backend in config["backends"]:
        try:
            sock = connect_to_backend(backend)
            for i in range(10):
                sock.send("Mandando para o backend ".encode())
                time.sleep(3)
        finally:
            sock.close()

    s = socket.socket()
    s.bind(('127.0.0.1', config["server"]["port"]))
    s.listen(config["server"]["max_connections"])
    try:
        conn, address = s.accept()
        while True:
            data = conn.recv(200)
            print(data)
    finally:
        conn.close()
        s.close()
    print("Saindo da gestão de conexões...")


if __name__ == '__main__':
    args = parse_args()
    CONFIG = read_configuration(args.conf)
    manage_connections(CONFIG)
    print("Encerrando programa...")
