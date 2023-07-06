import socket
import json
from math import ceil
from sys import path, getsizeof
path.append('..')

from trabalho_redes.entities.Package import Package
# from entities.Package import Package


class UDPClient:
    def __init__(self, server_address="127.0.0.1", server_port=20001, buffer_size=1024):
        self.server_address = server_address
        self.server_port = server_port
        self.buffer_size = buffer_size
        self.window_size = 10
        self.next_sequence_number = 0
        self.sent_packages = {}

        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.setblocking(0)

    @property
    def max_sequence_number(self) -> int:
        return self.window_size * 2 - 1

    def send_package(self, package: Package) -> None:
        package_dump = package.to_json_str()
        package_encoded = str.encode(package_dump)

        self.socket.sendto(package_encoded, (self.server_address, self.server_port))

        self.sent_packages[package.sequence_number] = package

        self.next_sequence_number += 1
        if self.next_sequence_number > self.max_sequence_number:
            self.next_sequence_number = 0
    
    def receive(self) -> Package:
        response_encoded, address = self.socket.recvfrom(self.buffer_size)
        response_decoded = response_encoded.decode()
        response = json.loads(response_decoded)
        package = Package(**response)

        return package

    def send_file(self, file: str):
        while True:
            # Envia pacotes dentro da janela e verifica timeout dos pacotes
            
            #chunk = self.get_file_chunk(file)
            
            # package = Package(self.next_sequence_number)
            # self.send_package(package)

            try:
                # Recebe responses (ACKs)
                response = self.receive()
                print(f'response: {response.__dict__}')

                ack_number = response.sequence_number
                if ack_number in self.sent_packages:
                    del self.sent_packages[ack_number]

                    # Reajusta a janela de acordo com os ACKs recebidos
            
            except BlockingIOError:
                continue

    @staticmethod
    def get_file_chunk(file: str) -> str:
        max_package_size = 1024
        empty_package_size = Package.empty_package_size()
        body_size = max_package_size - empty_package_size
        file_size = getsizeof(file)
        chunks_amount = ceil(file_size / body_size)

        for chunk_index in range(chunks_amount):
            start_index = chunk_index * body_size
            stop_index = (chunk_index + 1) * body_size
            yield file[start_index:stop_index]
