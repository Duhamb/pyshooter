try:    name = raw_input("Enter a screen name: ")
except: name = input("Enter a screen name: ")

import pygame
from pygame.locals import *
import traceback
pygame.display.init()
pygame.font.init()

from Mastermind import *
from NetworkSettings import *
import NetworkServer

screen_size = [400,300]
icon = pygame.Surface((1,1)); icon.set_alpha(0); pygame.display.set_icon(icon)
pygame.display.set_caption("Mastermind Chat Example - Ian Mallett - v.1.02 - 2013")
surface = pygame.display.set_mode(screen_size,RESIZABLE)

pygame.key.set_repeat(400, 25)

client = None
server = None

log = [None]*scrollback

message = ""
to_send = [
    ["introduce",name]
]

font = pygame.font.SysFont("Times New Roman",12)

def get_input():
    global surface, screen_size, message
    keys_pressed = pygame.key.get_pressed()
    for event in pygame.event.get():
        if   event.type == QUIT: return False
        elif event.type == KEYDOWN:
            if   event.key == K_ESCAPE: return False
            elif event.key == K_RETURN:
                if message != "":
                    to_send.append(["add",""+name+": "+message])
                    message = ""
            elif event.key == K_BACKSPACE:
                if len(message) > 0:
                    message = message[:-1]
            else:
                try: message += str(event.unicode)
                except: pass
        elif event.type == VIDEORESIZE:
            surface = pygame.display.set_mode(event.size,RESIZABLE)
            screen_size = event.size
    return True

def send_next_blocking():
    global log, to_send, continuing
    try:
        if len(to_send) == 0:
            client.send(["update"],None)
        else:
            client.send(to_send[0],None)
            to_send = to_send[1:]

        reply = None
        while reply == None:
            reply = client.receive(False)
        log = reply
    except MastermindError:
        continuing = False
    
def draw():
    surface.fill((255,255,255))

    x = 8

    y = screen_size[1] - 40
    for msg in log[::-1]:
        if msg == None: break
        surf_msg = font.render(msg,True,(0,0,0))
        surface.blit(surf_msg,(x,y))
        y -= 15

    surf_msg = font.render(message,True,(0,0,0))
    surface.blit(surf_msg,(x+1,screen_size[1]-20+3))

    pygame.draw.rect(surface,(128,128,128),(0,screen_size[1]-20,screen_size[0],20),1)
    
    pygame.display.flip()

def main():
    global client, server, continuing

    client = MastermindClientTCP(client_timeout_connect,client_timeout_receive)
    try:
        print("Client connecting on \""+client_ip+"\", port "+str(port)+" . . .")
        client.connect(client_ip,port)
    except MastermindError:
        print("No server found; starting server!")
        server = NetworkServer.ServerChat()
        server.connect(server_ip,port)
        server.accepting_allow()

        print("Client connecting on \""+client_ip+"\", port "+str(port)+" . . .")
        client.connect(client_ip,port)
    print("Client connected!")
        
    clock = pygame.time.Clock()
    continuing = True
    while continuing:
        if not get_input():
            to_send.append(["leave",name])
            send_next_blocking()
            break
        send_next_blocking()
        draw()
        clock.tick(60)
    pygame.quit()

    client.disconnect()

    if server != None:
        server.accepting_disallow()
        server.disconnect_clients()
        server.disconnect()
if __name__ == "__main__":
    try:
        main()
    except:
        traceback.print_exc()
        pygame.quit()
        input()

