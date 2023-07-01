import socket
import json
from sys import path
path.append('..')

from trabalho_redes.entities.Package import Package

class UDPClient:
    def __init__(self, server_addess="127.0.0.1", server_port=20001, buffer_size=1024):
        self.server_address = server_addess
        self.server_port = server_port
        self.buffer_size = buffer_size
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.setblocking(0)

    def send_package(self, package: Package) -> None:
        package_dump = package.to_json_str()
        package_encoded = str.encode(package_dump)

        self.socket.sendto(package_encoded, (self.server_address, self.server_port))
    
    def receive(self):
        response_encoded, address = self.socket.recvfrom(self.buffer_size)
        response_decoded = response_encoded.decode()
        response = json.loads(response_decoded)
        return response

    def listen(self):
        while True:
            # Envia pacotes dentro da janela
            # self.send_package(package1)
            # self.send_package(package2)

            # Recebe responses (ACKs)
            try:
                response = self.receive()
            except BlockingIOError:
                continue
            # Reajusta a janela de acordo com os ACKs recebidos
            