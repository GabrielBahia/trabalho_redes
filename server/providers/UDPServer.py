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
        while True:
            try: 
                request = self.receive_request()
                print("Mensagem do Cliente: {}".format(request))
            except BlockingIOError: 
                continue
            # Processamento (ou só salvar pacote no buffer...)
            
            # Enviar response (ACK)


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
