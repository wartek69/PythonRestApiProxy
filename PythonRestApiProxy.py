import socket
import logging
import time
import requests
import argparse

from threading import Thread

class TcpServer:
    def __init__(self, host, port, backend_api_url):
        self.host = host
        self.port = port
        self.backend_api_url = backend_api_url
        
    def init_server_connection(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.s:
            self.s.bind((self.host, self.port))
            logging.info('listening for connections on {}:{}...'.format(self.host, self.port))
            while True:
                self.s.listen()
                self.conn, addr = self.s.accept()
                thread = Thread(target = self.receive_message, args = (self.conn,addr))
                thread.start()
                logging.info('connection accepted from {}'.format(addr))

    def receive_message(self, connection, addr):       
        while True:
            data = ""
            if(connection is not None ):
                data = connection.recv(1024)
            logging.info("received: {}".format(data))
            if(data == b""):
                logging.info("{} closed connection".format(addr))
                return
            else:
                r = requests.post(self.backend_api_url, json={"p_messagedata": data.decode("utf-8")})

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--endpoint", help="rest endpoint to post the data to", default="")
    parser.add_argument("-p", "--port", help="port to listen on (default 9999)", default=9999)
    parser.add_argument("-i", "--ip", help="ip to listen on (default 0.0.0.0)", default="0.0.0.0")
    args = parser.parse_args()

    return args.endpoint, int(args.port), args.ip

if __name__== '__main__':
    logging.basicConfig(level=logging.INFO,
            format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s')
    endpoint, port, ip = parse_args()
    pythonProxy = TcpServer(ip, port, endpoint)
    pythonProxy.init_server_connection()