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

    except Exception as e:
        print(e)


def manage_connections(config):
    s = socket.socket()
    s.bind(('127.0.0.1', config["server"]["port"]))
    s.listen(config["server"]["max_connections"])
    with s:
        while True:
            conn, address = s.accept()
            with conn:
                while True:
                    data = conn.recv(200)
                    print("Dado recebido: ", data)
                    if not data:
                        break
    print("Saindo da gestão de conexões...")


if __name__ == '__main__':
    args = parse_args()
    CONFIG = read_configuration(args.conf)
    manage_connections(CONFIG)
    print("Encerrando programa...")
