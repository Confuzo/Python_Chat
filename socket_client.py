import socket
import select
import sys
from s_des import SimpleDes
from rc4 import RC4
from diffie_hellman import DiffieHellman


class Client:
    __port = 5354
    __key: str

    def __init__(self, q, alpha):
        self.__tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__s_des = SimpleDes()
        self.__rc4 = RC4()
        self.__encryption = None
        self.__diffie_hellman = DiffieHellman(q, alpha)

    def connect(self, host: str):
        dest = (host, self.__port)

        self.__tcp.connect(dest)

        sockets_list = [sys.stdin, self.__tcp]

        while True:
            read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])

            for socks in read_sockets:
                if socks == self.__tcp:
                    socks: socket.socket
                    messages: list = socks.recv(2048).decode().split("\x02")
                    controls = messages[1].split(" ")
                    if controls[0] == "\dh_end":
                        kp = controls[1]
                        self.__key = self.__diffie_hellman.calculate_sessionkey(int(kp))
                        print("Chave de diffie hellman trocadas!")
                        self.__key = bin(self.__key)[2:].zfill(10)[-10:]
                    elif controls[0] == "\dh_begin":
                        kp = controls[1]
                        y = self.__diffie_hellman.calculate_pubkey()
                        self.__key = self.__diffie_hellman.calculate_sessionkey(int(kp))
                        print("Chave de diffie hellman trocadas!")
                        self.__key = bin(self.__key)[2:].zfill(10)[-10:]
                        msg = "\dh_end " + str(y)
                        self.__tcp.send(bytes(msg.encode()))
                    else: 
                        decrypted_message = self.__verify_encryption(messages[1])
                        print(messages[0] + decrypted_message)
                else:
                    message: str = sys.stdin.readline()[:-1]
                    self.__erase_line()
                    if message[:5] == "\exit":
                        exit(1)
                    if message == "\dh_begin":
                        y = self.__diffie_hellman.calculate_pubkey()
                        msg = "\dh_begin " + str(y)
                        self.__tcp.send(bytes(msg.encode()))
                    else:    
                        if self.__encryption:
                            encrypted_message: str = self.__encryption(message, True)

                            self.__tcp.send(bytes(encrypted_message.encode()))
                        else:
                            self.__tcp.send(bytes(message.encode()))

                    sys.stdout.write("<You> {}".format(self.__verify_start_encryption(message) + "\n"))
                    sys.stdout.flush()

    def __use_s_des(self, message: str, encrypt: bool):

        if encrypt:
            execute = self.__s_des.encrypt
        else:
            execute = self.__s_des.decrypt

        bin_message = list(format(ord(x), 'b') for x in message)

        s_des_message = self.__execute_s_des(bin_message, execute)

        return self.__binary_list_to_ascii(s_des_message)

    def __execute_s_des(self, bin_message, execute: SimpleDes.encrypt) -> list:
        s_des_message = list()
        for byte in bin_message:
            byte: str
            s_des_message.append(execute(byte.zfill(8), self.__key))

        return s_des_message

    @staticmethod
    def __binary_list_to_ascii(text: list) -> str:
        return "".join([chr(int(i, 2)) for i in text])

    def __verify_encryption(self, message: str):
        if self.__encryption is None:

            return self.__verify_start_encryption(message)
        else:
            decrypt_message = self.__encryption(message, False)

            return self.__verify_start_encryption(decrypt_message)

    def __use_rc4(self, message: str, encrypt: bool):
        return self.__rc4.execute(message, self.__key)

    def __start_encryption(self, message: str) -> bool:
        commands = message.split(" ")
        if commands[0] == "\crypt":
            type_encryption = commands[1]
            if type_encryption == "sdes":
                self.__encryption = self.__use_s_des
                return True
                '''if self.__have_quotes(commands[2]):
                    key = commands[2][1:-1]
                    self.__encryption = self.__use_s_des
                    if len(key) < 10:
                        self.__key = key.zfill(10)
                    else:
                        self.__key = key[:10]
                    return True
                return False'''

            elif type_encryption == "rc4":
                self.__encryption = self.__use_rc4
                '''if self.__have_quotes(commands[2]):
                    self.__encryption = self.__use_rc4
                    #self.__key = commands[2][1:-1]
                    return True
                return False'''

            elif type_encryption == "none":
                self.__encryption = None
                return True
            else:
                return False
        return False

    def __check_type_encryption(self, message: str):
        if self.__start_encryption(message):
            if self.__encryption == self.__use_s_des:
                return "Cifra Simple DES ativada"
            elif self.__encryption == self.__use_rc4:
                return "Cifra RC4 ativada"
            else:
                return "Comunicação sem cifra"
        else:
            return message

    def __verify_start_encryption(self, message: str):
        if self.__start_encryption(message):
            return self.__check_type_encryption(message)

        return message

    def __erase_line(self):
        CURSOR_UP_ONE = '\x1b[1A'
        ERASE_LINE = '\x1b[2K'
        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(ERASE_LINE)

    @staticmethod
    def __have_quotes(command: str) -> bool:
        if command[0] == command[-1] == "\"":
            return True
        return False

    def __del__(self):
        print("saindo do chat...")
        self.__tcp.close()


def start_client():
    if len(sys.argv) != 4:
        print("digite o ip do server que deseja conectar seguido do q e alpha, e nada mais !!")
        exit(1)

    client = Client(int(sys.argv[2]), int(sys.argv[3]))

    try:
        client.connect(sys.argv[1])
    except KeyboardInterrupt:
        exit(2)


if __name__ == '__main__':
    start_client()
