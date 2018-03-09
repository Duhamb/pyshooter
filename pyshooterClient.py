import traceback

from Mastermind import *
from NetworkSettings import *
import NetworkServer

class pyshooterClient():
    def __init__(self, name):

        try:
            self.name = raw_input("Enter a screen name: ")
            self.func_inp = raw_input
        except:
            self.name = input("Enter a screen name: ")
            self.func_inp = input
        self.name = name

        print("Mastermind console-based chat example")
        print("Ian Mallett - 2013")
        print()
        print("Commands:")
        print("/exit - exits")
        print("/update - updates the screen")
        print("<anything else> - adds as a message and updates the screen")
        print()

        self.client = None
        self.server = None

        self.already_printed_messages = [None] * scrollback

    def blocking_receive(self):
        try:
            reply = None
            while reply == None:
                reply = self.client.receive(False)
            chat_history = reply  # The entire history of the chat

            # Only prints the messages we haven't seen before.  Uses a crude method
            # based on checking equality (messages are timestamped, so even if they
            # have the same content, they'll be "different"), but a more refined
            # approach is necessary for production projects.
            for message in chat_history:
                if message not in self.already_printed_messages:
                    print(message)
                    self.already_printed_messages = self.already_printed_messages[1:] + [message]
        except MastermindError:
            self.continuing = False

    def push_update(self):
        self.client.send(["update",self.name], None)#add more parameters
        self.blocking_receive()


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
            message = self.func_inp(">>> ")
            if message == "/exit":
                self.client.send(["leave", self.name], None)
                self.blocking_receive()
                break
            elif message == "/update":
                self.client.send(["update"], None)
                self.blocking_receive()
            else:
                self.client.send(["add", "" + self.name + ": " + message], None)
                self.blocking_receive()

        self.client.disconnect()

        if self.server != None:
            self.server.accepting_disallow()
            self.server.disconnect_clients()
            self.server.disconnect()

if __name__ == "__main__":
    try:
        pyshooterClient().main()
    except:
        traceback.print_exc()
        input()
