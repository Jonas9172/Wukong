import socket


class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "178.79.191.185"
        self.port = 5555
        self.addr = (self.host, self.port)
        self.connect()
        self.id = None

    def connect(self):
        self.client.connect(self.addr)

    def get_id(self):
        id_request = "id r"
        self.client.send(str.encode(id_request))
        self.id = self.client.recv(2048).decode()

    def send(self, data):
        """
        :param data: str
        :return: str
        """
        try:
            self.client.send(str.encode(data))
            reply = self.client.recv(2048).decode()
            return reply
        except socket.error as e:
            return str(e)

    def reach(self, data):
        self.client.send(str.encode(data))
        reply = self.client.recv(2048).decode()
        return reply

    def leave(self, data):
        self.client.send(str.encode(data))
        self.client.close()
