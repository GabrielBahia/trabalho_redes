from providers.UDPServer import UDPServer


if __name__ == '__main__':
    server = UDPServer()
    for i in server.listen():
        while False:#not i.empty():
            print(i.get())