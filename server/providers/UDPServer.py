import socket
import json


class UDPServer:
    def __init__(self, local_ip="127.0.0.1", local_port=20001, buffer_size=1024):
        self.local_ip = local_ip
        self.local_port = local_port
        self.buffer_size = buffer_size

        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.bind((self.local_ip, self.local_port))
        self.socket.setblocking(0)
        print("Servidor UDP up e escutando...")

    def listen(self):

        expected_sequence_number = 0
        received_data = []

        while True:
            try: 
                request = self.receive_request()
                print("Mensagem do Cliente: {}".format(request))
                # Verificar se o pacote recebido é o esperado
                if request["sequence_number"] == expected_sequence_number:
                    # Processamento (ou só salvar pacote no buffer)
                    received_data.append(request["body"])
                    # Incrementa número de sequência esperado
                    expected_sequence_number += 1
                    # Enviar response (ACK)
                    self.reply_with_ack(self, expected_sequence_number)
                    continue
                else:
                    # Enviar response (ACK) com número anterior (indica que o pacote foi recebido, mas não é o esperado)
                    self.reply_with_ack(self, expected_sequence_number)
                    continue

            except BlockingIOError: 
                continue

    def reply_with_ack(self, sequence_number):
        # Monta o pacote de resposta, no caso, converte ACK para string e depois para bytes
        package_encoded = (json.dumps({"sequence_number": sequence_number})).encode()
        # Envia o pacote de resposta
        self.socket.sendto(package_encoded, self.client_address)

    def receive_request(self):
        request_encoded, address = self.socket.recvfrom(self.buffer_size)
        self.client_address = address

        request_decoded = request_encoded.decode()
        request = json.loads(request_decoded)

        return request

    def response(self, body: dict):
        response_body = json.dumps(body)
        response_body_encoded = str.encode(response_body)

        self.socket.sendto(response_body_encoded, self.client_address)