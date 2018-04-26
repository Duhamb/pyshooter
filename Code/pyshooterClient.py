import traceback

import Libs.Mastermind as Mastermind
from Code.NetworkSettings import *
import Code.NetworkServer as NetworkServer
import Code.helpers as helpers

class pyshooterClient():
    def __init__(self, name):
        self.name = name

        self.client = None
        self.server = None
        self.zombies_info = {}
        self.powerups_info = {}
        self.players_info = {}
        self.powerups_clients_state = {}
        self.minimaps_info = {}
        self.scores = {}

    def start(self):
        self.client = Mastermind.MastermindClientTCP(client_timeout_connect, client_timeout_receive)
        try:
            print("Client connecting on \"" + client_ip + "\", port " + str(port) + " . . .")
            self.client.connect(client_ip, port)
        except Mastermind.MastermindError:
            print("No server found; starting server!")
            self.server = NetworkServer.Server()
            self.server.connect(server_ip, port)
            self.server.accepting_allow()

            print("Client connecting on \"" + client_ip + "\", port " + str(port) + " . . .")
            self.client.connect(client_ip, port)
        print("Client connected!")

    def start_connect(self, server_ip):
        self.client = Mastermind.MastermindClientTCP(client_timeout_connect, client_timeout_receive)
        try:
            print("Client connecting on \"" + server_ip + "\", port " + str(port) + " . . .")
            self.client.connect(server_ip, port)
            return True
        except Mastermind.MastermindError:
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
        while (reply == None or reply[0] != "players"):
            reply = self.client.receive(False)
        self.players_info = reply[1]

    def push_zombies(self, zombie_list, is_host):
        if is_host:
            self.client.send(["zombie_host", zombie_list], None)
        else:
            self.client.send(["zombie_client", zombie_list], None)

    def pull_zombies(self):
        reply = None
        while (reply == None or reply[0] != "zombies"):
            reply = self.client.receive(False)
        self.zombies_info = reply[1]

    def push_powerups(self, powerup_list, is_host):
        if is_host:
            self.client.send(["powerup_host", powerup_list], None)
        else:
            self.client.send(["powerup_client", powerup_list], None)

    def pull_powerups(self):
        reply = None
        while (reply == None or reply[0] != "powerups"):
            reply = self.client.receive(False)
        self.powerups_info = reply[1]

    def push_minimap(self, position_on_screen):
        self.client.send(["minimaps", [self.name, {self.name: position_on_screen}]], None)

    def pull_minimaps(self):
        reply = None
        while (reply == None or reply[0] != "minimaps"):
            reply = self.client.receive(False)
        self.minimaps_info = reply[1]

    def add_points(self, shooter_name):
        self.scores[shooter_name] = self.scores.get(shooter_name, 0) + 100

    def push_scores(self, is_host):
        if is_host:
            self.client.send(["scores_host", self.scores], None)
        else:
            self.client.send(["scores_client", {}], None)

    def pull_scores(self, is_host):
        reply = None
        while (reply == None or reply[0] != "scores"):
            reply = self.client.receive(False)
        if not is_host:
            self.scores = reply[1]

    def push_powerups_state(self, name, state, is_host):
        if is_host:
            self.client.send(["add_status_player", [name, state]], None)
        else:
            self.client.send(["add_status_player", [None, None]], None)

    def pull_powerups_state(self):
        reply = None
        while (reply == None or reply[0] != "powerups_states"):
            reply = self.client.receive(False)
        self.powerups_clients_state = reply[1]


    def delete_player(self):
        self.client.send(["delete_player", self.name], None)