import socket

# Configurações do servidor
server_address = ('localhost', 12345)

# Cria o socket UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Associa o socket ao endereço do servidor
server_socket.bind(server_address)

print('Servidor pronto para receber mensagens.')

expected_sequence_number = 0
received_messages = []

while True:
    # Aguarda a chegada de uma mensagem
    data, address = server_socket.recvfrom(1024)
    message = data.decode()

    if message == 'FIM':
        # Recebido o sinal de encerramento do cliente
        break

    # Separa o número de sequência da mensagem
    message_parts = message.split(':')
    message_number = int(message_parts[1])
    message_content = message_parts[2]

    # Armazena a mensagem recebida
    received_messages.append((message_number, message_content))

# Ordena as mensagens com base no message_number
received_messages.sort(key=lambda x: x[0])

# Imprime as mensagens em ordem
for message_number, message_content in received_messages:
    print('Recebido:', message_number, message_content)

# Envia uma resposta de confirmação para o cliente
response = 'FIM'
server_socket.sendto(response.encode(), address)
print('Enviado: FIM')

# Fecha o socket do servidor
server_socket.close()
