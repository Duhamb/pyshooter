import traceback

from Mastermind import *
from NetworkSettings import *
import NetworkServer
import helpers

class pyshooterClient():
    def __init__(self, name):

        self.name = name

        self.client = None
        self.server = None

    def blocking_receive(self):
        try:
            reply = None
            while reply == None:
                reply = self.client.receive(False)
            self.players_info = reply  # The entire history of the chat


            #print(self.players_info)

        except MastermindError:
            self.continuing = False


    def start(self):
        self.client = MastermindClientTCP(client_timeout_connect, client_timeout_receive)
        try:
            print("Client connecting on \"" + client_ip + "\", port " + str(port) + " . . .")
            self.client.connect(client_ip, port)
        except MastermindError:
            print("No server found; starting server!")
            self.server = NetworkServer.Server()
            self.server.connect(server_ip, port)
            self.server.accepting_allow()

            print("Client connecting on \"" + client_ip + "\", port " + str(port) + " . . .")
            self.client.connect(client_ip, port)
        print("Client connected!")

    def start_connect(self, server_ip):
        self.client = MastermindClientTCP(client_timeout_connect, client_timeout_receive)
        try:
            print("Client connecting on \"" + server_ip + "\", port " + str(port) + " . . .")
            self.client.connect(server_ip, port)
            return True
        except MastermindError:
            print("No server found; Starting Singleplayer")
            return False

    def disconnect(self):
        self.client.disconnect()
    def push_player(self, player, can_render_bullet):
        send = player.get_server_info()
        send['is_shooting'] = can_render_bullet
        self.client.send(["player", [self.name, {self.name: send}]], None)

    def pull_players(self):
        reply = None
        while reply == None:
            reply = self.client.receive(False)
        self.players_info = reply


        #print(self.players_info)


    def main(self):

        self.client = MastermindClientTCP(client_timeout_connect, client_timeout_receive)
        try:
            print("Client connecting on \"" + client_ip + "\", port " + str(port) + " . . .")
            self.client.connect(client_ip, port)
        except MastermindError:
            print("No server found; starting server!")
            self.server = NetworkServer.Server()
            self.server.connect(server_ip, port)
            self.server.accepting_allow()

            print("Client connecting on \"" + client_ip + "\", port " + str(port) + " . . .")
            self.client.connect(client_ip, port)
        print("Client connected!")

        continuing = True
        while continuing:
            self.client.send(["new_player", [self.name, {self.name:{'peso':'1kg', 'altura':'1.20'}}]], None)
            self.blocking_receive()

        self.client.disconnect()

        if self.server != None:
            self.server.accepting_disallow()
            self.server.disconnect_clients()
            self.server.disconnect()

if __name__ == "__main__":
    try:
        pyshooterClient('Name').main()
    except:
        traceback.print_exc()
        input()
