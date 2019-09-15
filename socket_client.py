import socket
import select
import sys
from s_des import SimpleDes
from rc4 import RC4


class Client:
    __port = 5354
    __key = str()

    def __init__(self, args):
        self.__tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if(args[1] == "sdes" or args[1] == "rc4"):
            if(args[1] == "sdes"):
                self.__encryption = SimpleDes()
            else:
                self.__encryption = RC4()
        else:
            self.__encryption = None

    def connect(self, host: str):
        dest = (host, self.__port)

        self.__tcp.connect(dest)

        sockets_list = [sys.stdin, self.__tcp]

        while True:
            read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])

            for socks in read_sockets:
                if socks == self.__tcp:
                    message= socks.recv(2048).decode()
                    if(self.__encryption is None):
                        print(message)
                    else:
                        #print(message)
                        print(self.decrypt(message))
                    '''decrypted_message = self.__verify_encryption(message[19:])
                    print(message[:19] + decrypted_message)'''
                else:
                    message= sys.stdin.readline()
                    if(self.__encryption is None):
                        self.__tcp.send(bytes(message.encode()))
                        sys.stdout.write("<You> {}".format(message))
                        sys.stdout.flush()
                    else:
                        copy = message
                        m = self.encrypt(message)
                        self.__tcp.send(bytes(m.encode()))
                        sys.stdout.write("<You> {}".format(copy))
                        sys.stdout.flush()
                    '''if message[:5] == "/exit":
                        exit(1)

                    if self.__encryption:
                        encrypted_message = self.__encryption(message, True)
                        self.__start_encryption(message)
                        self.__tcp.send(bytes(encrypted_message.encode()))
                    else:
                        self.__start_encryption(message)
                        self.__tcp.send(bytes(message.encode()))'''


    '''def __use_s_des(self, message: str, encrypt: bool):

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
           
            s_des_message.append(execute(byte.zfill(8), self.__key))

        return s_des_message

    @staticmethod
    def __binary_list_to_ascii(text: list) -> str:
        return "".join([chr(int(i, 2)) for i in text])

    '''
    def decrypt(self, message: str):
        if(sys.argv[1] == "sdes"):
            message_de = ""
            for m in message:
                m = bin(ord(m))
                m = m[2:].zfill(8)
                d = self.__encryption.decrypt(m, sys.argv[2])
                message_de += chr(int(d,2))
            return message_de
        else:
            return self.__encryption.execute(message, sys.argv[2])

    def encrypt(self, message: str):
        if(sys.argv[1] == "sdes"):
            message_en = ""
            for m in message:
                m =  bin(ord(m))
                m = m[2:].zfill(8)
                d = self.__encryption.encrypt(m, sys.argv[2])
                message_en += chr(int(d,2))
            return message_en
        else:
            return self.__encryption.execute(message, sys.argv[2])
    '''def __use_rc4(self, message: str, encrypt: bool):
        return self.__rc4.execute(message, self.__key)

    def __start_encryption(self, message: str) -> bool:

        if len(message) >= 6:
            type_encryption = message[:4]
            key = message[5:6]
            if type_encryption == "/des":
                self.__encryption = self.__use_s_des
                self.__key = format(ord(key), "b").zfill(10)
                return True
            elif type_encryption == "/rc4":
                self.__encryption = self.__use_rc4
                self.__key = key
                return True
            else:
                return False

        return False

    def __check_type_encryption(self, message: str):
        if self.__start_encryption(message):
            if self.__encryption == self.__use_s_des:
                return "Cifra Simple DES ativada"
            else:
                return "Cifra RC4 ativada"
        else:
            return message

    def __verify_start_encryption(self, message: str):
        if self.__start_encryption(message):
            return self.__check_type_encryption(message)

        return message'''

    def __del__(self):
        print("saindo do chat...")
        self.__tcp.close()


def start_client():
    if len(sys.argv) < 2:
        print("O padrão deve ser script, encription, key (Apenas para as criptografias rc4 e s-des)")
        exit(1)

    client = Client(sys.argv)

    try:
        client.connect("")
    except KeyboardInterrupt:
        exit(2)


if __name__ == '__main__':
    start_client()
