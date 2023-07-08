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
        self.window = 10
        self.received_data = PriorityQueue(self.window)

        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.bind((self.local_ip, self.local_port))
        self.socket.setblocking(0)
        print("Servidor UDP up e escutando...")

    def listen(self):
        expected_sequence_number = 0
        #received_data = []

        while True:
            try:
                #if(self.received_data.qsize()) 
                if self.received_data.qsize() == self.window: 
                    continue

                request = self.receive_request()
                #print(f'Mensagem do Cliente: {request.__dict__}')

                if request.fyn:
                    while not self.received_data.empty(): 
                        yield self.received_data.get()
                    yield Package(fyn=True)
                    break

                # Verificar se o pacote recebido é o esperado
                if request.sequence_number == expected_sequence_number:
                    # Processamento (ou só salvar pacote no buffer) // Fila de prioridade
                    self.received_data.put((request.sequence_number, request.body))
                    # Incrementa número de sequência esperado
                    expected_sequence_number += 1
                    # Enviar response (ACK)
                    self.reply_with_ack(expected_sequence_number)

                    if random.random() <= 0.3:
                        if not self.received_data.empty():
                            yield self.received_data.get()

                    continue
                else:
                    # Enviar response (ACK) com número anterior (indica que o pacote foi recebido, mas não é o esperado)
                    self.reply_with_ack(expected_sequence_number)
                    continue
            except BlockingIOError: 
                continue

    def reply_with_ack(self, sequence_number):
        # Monta o pacote de resposta, no caso, converte ACK para string e depois para bytes
        package = Package(sequence_number)
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
