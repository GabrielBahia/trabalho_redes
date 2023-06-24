import socket
import random

# Configurações do servidor
server_address = ('localhost', 12345)

# Cria o socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Mensagens a serem enviadas
messages = [
    '1: Mensagem 1',
    '2: Mensagem 2',
    '3: Mensagem 3'
]

# Embaralha a ordem das mensagens
random.shuffle(messages)

# Envia as mensagens para o servidor
for i, message in enumerate(messages):
    sequence_number = i
    message_with_sequence = f'{sequence_number}: {message}'
    client_socket.sendto(message_with_sequence.encode(), server_address)
    print('Enviado:', message_with_sequence)

# Envia o sinal de encerramento para o servidor
client_socket.sendto('FIM'.encode(), server_address)
print('Enviado: FIM')

# Fecha o socket do cliente
client_socket.close()
