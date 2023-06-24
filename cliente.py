import socket

# Configurações do servidor
server_address = ('localhost', 12345)

# Cria o socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    # Envia uma mensagem para o servidor
    message = 'Olá, servidor!'
    client_socket.sendto(message.encode(), server_address)

    # Aguarda a resposta do servidor
    data, server = client_socket.recvfrom(1024)
    print('Resposta do servidor:', data.decode())

finally:
    # Fecha o socket
    client_socket.close()
