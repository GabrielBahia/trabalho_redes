from os import path

from providers.UDPServer import UDPServer


if __name__ == '__main__':
    server = UDPServer()

    packages = []
    for package in server.listen():
        if package.fyn:
            break

        packages.append(package)

    filename = 'test1.txt'
    with open(path.join(path.curdir, 'test_data', filename), 'w+') as file:
        for package in packages:
            file.write(package.body)
