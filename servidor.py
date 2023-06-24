import socket

# Configurações do servidor
server_address = ('localhost', 12345)

# Cria o socket UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Associa o socket ao endereço do servidor
server_socket.bind(server_address)

print('Servidor pronto para receber mensagens.')

while True:
    print('Esperando por clientes...')
    # Aguarda a chegada de uma mensagem
    data, address = server_socket.recvfrom(1024)
    print('Mensagem recebida do cliente:', data.decode())

    # Envia uma resposta para o cliente
    response = 'Olá, cliente!'
    server_socket.sendto(response.encode(), address)
