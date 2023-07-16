import socket
import json
import random
from queue import PriorityQueue

from Package import Package


class UDPServer:
    def __init__(self, local_ip="127.0.0.1", local_port=20001, buffer_size=1024):
        self.local_ip = local_ip
        self.local_port = local_port
        self.buffer_size = buffer_size
        self.window_size = 10
        self.window_start = 0
        self.packages_buffer = PriorityQueue(self.window_size)
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.bind((self.local_ip, self.local_port))
        self.socket.setblocking(0)
        print("Servidor UDP up e escutando...")

    def listen(self):
        expected_sequence_number = 0

        while True:
            try:
                # Checa se fila do buffer está lotada: DropTail (descarta novos pacotes)
                if self.packages_buffer.qsize() == self.window_size: 
                    continue

                request = self.receive_request()

                # Simulação de perda de pacote(10% de chance)
                if random.random() <= 0.1:
                    continue

                if request.fyn:
                    while not self.packages_buffer.empty(): 
                        yield self.packages_buffer.get()[1]
                    yield Package(fyn=True)
                    break

                # Verificar se o pacote recebido é o esperado
                if request.sequence_number == expected_sequence_number:
                    # Processamento (salva pacote no buffer (uso de fila de prioridade para ordenar de acordo com número de sequência))
                    self.packages_buffer.put((request.sequence_number, request))

                    # Enviar response (ACK)
                    self.reply_with_ack(expected_sequence_number)

                    # Incrementa número de sequência esperado
                    expected_sequence_number += 1

                    # Simulação de consumo da aplicação(30% de chance)
                    if random.random() <= 0.3:
                        if not self.packages_buffer.empty():
                            yield self.packages_buffer.get()[1]
                    continue

                else:
                    # Enviar response (ACK) com número anterior (indica que o pacote foi recebido, mas não é o esperado)
                    self.reply_with_ack(expected_sequence_number)
                    continue
            except BlockingIOError: 
                continue

    def reply_with_ack(self, sequence_number):
        # Monta o pacote de resposta, no caso, converte ACK para string e depois para bytes
        rwnd = self.window_size - self.packages_buffer.qsize()
        package = Package(sequence_number, rwnd=rwnd)
        package_encoded = str.encode(package.to_json_str())

        # Envia o pacote de resposta
        self.socket.sendto(package_encoded, self.client_address)

    def receive_request(self) -> Package:
        request_encoded, address = self.socket.recvfrom(self.buffer_size)
        self.client_address = address

        request_decoded = request_encoded.decode()
        request = json.loads(request_decoded)
        package = Package(**request)

        return package

    def response(self, body: dict):
        response_body = json.dumps(body)
        response_body_encoded = str.encode(response_body)

        self.socket.sendto(response_body_encoded, self.client_address)
