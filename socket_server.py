import socket
import _thread


class Server:
    __port = 5354
    __clients = list()

    def __init__(self):
        self.__tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        orig = ("", self.__port)

        self.__tcp.bind(orig)
        self.__tcp.listen(10)

    def __chat_room(self, connection: socket.socket, addr: tuple):

        connection.send(bytes("Bem vindo !!\n".encode()))
        connection.send(bytes("comandos /des /rc4 /exit\n".encode()))
        connection.send(bytes("/exit para sair do chat\n".encode()))
        connection.send(bytes("/des para iniciar o simple des\n".encode()))
        connection.send(bytes("/rc4 para iniciar o rc4 \n".encode()))
        connection.send(bytes("exemplo: /des a\n".encode()))
        connection.send(bytes("exemplo: /rc4 segredo\n".encode()))
        connection.send(bytes("observe que o segundo parametro: a e segredo\n".encode()))
        connection.send(bytes("represeta a chave, no caso do Simple DES\n".encode()))
        connection.send(bytes("a chave só pode ter 1 caracter \n".encode()))
        connection.send(bytes("o RC4 pode ter até 256 caracters \n".encode()))

        while True:

            msg = connection.recv(2048)

            if not msg:
                break

            msg_to_seed = "<{}, {}> {}".format(addr[0], addr[1], msg.decode()).encode()

            self.__broadcast(msg_to_seed, connection)

            print(addr, msg.decode())

        print("Finalizando conexão do cliente {}".format(addr))
        self.__remove_connection(connection)

    def __broadcast(self, message: bytes, connection: socket.socket):
        for client in self.__clients:
            client: socket.socket
            if client != connection:
                try:
                    client.send(message)
                except:
                    self.__remove_connection(client)

    def run(self):
        while True:
            con, client = self.__tcp.accept()

            self.__clients.append(con)
            print("Conectado ao ", client)

            _thread.start_new_thread(self.__chat_room, (con, client))

    def __remove_connection(self, conection: socket.socket):
        if conection in self.__clients:
            self.__clients.remove(conection)
            conection.close()


def start_server():
    server = Server()
    server.run()


if __name__ == '__main__':
    start_server()