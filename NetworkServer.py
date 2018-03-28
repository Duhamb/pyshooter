from Mastermind import *

from NetworkSettings import *

import threading
from time import gmtime, strftime


class Server(MastermindServerTCP):
    def __init__(self):
        MastermindServerTCP.__init__(self, 0.5, 0.5, 10.0)  # server refresh, connections' refresh, connection timeout

        self.players = {}
        self.zombies = {}
        self.minimaps = {}
        self.scores = {}
        self.mutex = threading.Lock()


    def add_player(self, data):

        self.mutex.acquire()
        self.players[data[0]] = data[1][data[0]]
        self.mutex.release()

    def add_minimap(self, data):

        self.mutex.acquire()
        self.minimaps[data[0]] = data[1][data[0]]
        self.mutex.release()

    def add_zombie(self, data):

        self.mutex.acquire()
        self.zombies = data
        self.mutex.release()

    def add_scores(self, data):
        self.mutex.acquire()
        self.scores = data
        self.mutex.release()

    def callback_connect(self):
        # Something could go here
        return super(Server, self).callback_connect()

    def callback_disconnect(self):
        # Something could go here
        return super(Server, self).callback_disconnect()

    def callback_connect_client(self, connection_object):
        # Something could go here
        return super(Server, self).callback_connect_client(connection_object)

    def callback_disconnect_client(self, connection_object):
        # Something could go here
        return super(Server, self).callback_disconnect_client(connection_object)

    def callback_client_receive(self, connection_object):
        # Something could go here
        return super(Server, self).callback_client_receive(connection_object)

    def callback_client_handle(self, connection_object, data):
        cmd = data[0]
        if cmd == "player":
            self.add_player(data[1])
            self.callback_client_send(connection_object, ["players", self.players])
        elif cmd == "zombie_host":
            self.add_zombie(data[1])
            self.callback_client_send(connection_object, ["zombies", self.zombies])
        elif cmd == "zombie_client":
            self.callback_client_send(connection_object, ["zombies", self.zombies])
        elif cmd == "scores_host":
            self.add_scores(data[1])
            self.callback_client_send(connection_object, ["scores", self.scores])
        elif cmd == "scores_client":
            self.callback_client_send(connection_object, ["scores", self.scores])
        elif cmd == "minimaps":
            self.add_minimap(data[1])
            self.callback_client_send(connection_object, ["minimaps", self.minimaps])

    def callback_client_send(self, connection_object, data, compression=None):
        # Something could go here
        return super(Server, self).callback_client_send(connection_object, data, compression)



if __name__ == "__main__":
    server = Server()
    server.connect(server_ip, port)
    try:
        server.accepting_allow_wait_forever()
    except:
        # Only way to break is with an exception
        pass
    server.accepting_disallow()
    server.disconnect_clients()
    server.disconnect()
