from os import path

from providers.UDPClient import UDPClient


if __name__ == '__main__':
    client = UDPClient()

    filename = 'test1.txt'
    with open(path.join(path.curdir, 'test_data', filename), 'r') as file:
        file_content = file.read()
        client.send_file(file_content)
