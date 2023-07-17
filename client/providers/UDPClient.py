import socket
import json
from math import ceil
from sys import getsizeof
from queue import PriorityQueue
import time
from Package import Package


class UDPClient:
    def __init__(self, server_address="127.0.0.1", server_port=20001, buffer_size=1024):
        self.server_address = server_address
        self.server_port = server_port
        self.buffer_size = buffer_size
        self.window_size = 10
        self.window_start = 0
        self.next_sequence_number = 0
        self.sent_packages = {}
        self.package_buffer = PriorityQueue(self.window_size)

        self.rwnd_size_server = 10

        self.start_time = time.perf_counter_ns()

        self.socket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.setblocking(0)

    @property
    def max_sequence_number(self) -> int:
        return self.window_size * 2 - 1

    def send_package(self, package: Package) -> None:
        # Gera pacote encodado
        package_dump = package.to_json_str()
        package_encoded = str.encode(package_dump)

        # Envia pacote e adiciona na lista de pacotes enviados
        self.socket.sendto(
            package_encoded, (self.server_address, self.server_port))

        self.sent_packages[package.sequence_number] = package

        # Incrementa o número de sequência
        self.next_sequence_number += 1

        # Verifica se o número de sequência é válido e zera se necessário
        if (self.next_sequence_number > self.max_sequence_number):
            self.next_sequence_number = 0

    def show_timer(self):
        current_time = time.perf_counter_ns()
        elapsed_time = current_time - self.start_time
        print(f"Tempo decorrido: {elapsed_time:.2f} nanosegundos")

    def receive(self) -> Package:
        response_encoded, address = self.socket.recvfrom(self.buffer_size)
        response_decoded = response_encoded.decode()
        response = json.loads(response_decoded)
        package = Package(**response)

        return package

    def send_file(self, file: str):
        file_chunk_generator = self.get_file_chunk_generator(file)
        end_of_file = False

        while not end_of_file:
            try:
                # Envia pacotes dentro da janela e verifica timeout dos pacotes
                file_chunk = next(file_chunk_generator)
                package = Package(self.next_sequence_number, file_chunk)

                # print(f"espaco livre do buffer do server {self.rwnd_size_server }")
                # Verifica se pode enviar pacote (ainda há espaço na janela)
                if ((self.next_sequence_number - self.window_start) < self.window_size and self.rwnd_size_server > 0):
                    # Envia pacote se ainda for possível
                    # print(f"if do send file do client {self.next_sequence_number}")
                    self.send_package(package)
                else:
                    # Verifica timeout dos pacotes
                    while (self.next_sequence_number - self.window_start >= self.window_size):
                        # print("while do send file do client")
                        # Espera resposta
                        self.receive_acks()

            except StopIteration:
                # self.send_package(Package(fyn=True))
                end_of_file = True

            try:
                # Recebe responses (ACKs)
                self.receive_acks()

            except BlockingIOError:
                # print("except do blocking io")
                continue

    def receive_acks(self):
        # Espera resposta e pega número de ACK
        response = self.receive()
        received_ack_number = response.sequence_number

        self.rwnd_size_server = response.rwnd

        # Verifica se o ACK recebido é válido
        if received_ack_number in self.sent_packages:
            # Checa se o pacote foi enviado e apaga
            del self.sent_packages[received_ack_number]

            # Reajusta a janela de acordo com o número de ACKs recebidos
            if (received_ack_number == self.window_start):
                # print("if do receive ack do client")
                while ((self.next_sequence_number - self.window_start) >= self.window_size):
                    # print("while do receive ack do client")
                    self.window_start += 1
        self.show_timer()

    @staticmethod
    def get_file_chunk_generator(file: str):
        max_package_size = 1024
        base_char_size = getsizeof(str.encode(' '))
        max_package_length = max_package_size - base_char_size
        body_length = max_package_length - Package.empty_package_length()
        chunks_amount = ceil(len(file) / body_length)

        for chunk_index in range(chunks_amount):
            start_index = chunk_index * body_length
            stop_index = (chunk_index + 1) * body_length
            yield file[start_index:stop_index]
