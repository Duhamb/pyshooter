import pygame as pg
from pyshooterClient import *
from textbox import TextBox
import constants

KEY_REPEAT_SETTING = (200, 70)


class Menu():
    def __init__(self):
        #load menu images
        self.MENU_IMAGE = pg.image.load("Assets/Images/menu/background.png")
        self.MENU_IMAGE = pg.transform.scale(self.MENU_IMAGE, (800, 600))
        self.SINGLE_OFF = pg.image.load("Assets/Images/menu/button_singleplayer_off.png")
        self.SINGLE_OFF = pg.transform.scale(self.SINGLE_OFF, (200, 50))
        self.SINGLE_ON = pg.image.load("Assets/Images/menu/button_singleplayer_on.png")
        self.SINGLE_ON = pg.transform.scale(self.SINGLE_ON, (200, 50))
        self.MULTI_OFF = pg.image.load("Assets/Images/menu/button_multiplayer_off.png")
        self.MULTI_OFF = pg.transform.scale(self.MULTI_OFF, (200, 50))
        self.MULTI_ON = pg.image.load("Assets/Images/menu/button_multiplayer_on.png")
        self.MULTI_ON = pg.transform.scale(self.MULTI_ON, (200, 50))
        self.SERVER_OFF = pg.image.load("Assets/Images/menu/button_create_server_off.png")
        self.SERVER_OFF = pg.transform.scale(self.SERVER_OFF, (200, 50))
        self.SERVER_ON = pg.image.load("Assets/Images/menu/button_create_server_on.png")
        self.SERVER_ON = pg.transform.scale(self.SERVER_ON, (200, 50))
        self.CONNECT_OFF = pg.image.load("Assets/Images/menu/button_connect_off.png")
        self.CONNECT_OFF = pg.transform.scale(self.CONNECT_OFF, (200, 50))
        self.CONNECT_ON = pg.image.load("Assets/Images/menu/button_connect_on.png")
        self.CONNECT_ON = pg.transform.scale(self.CONNECT_ON, (200, 50))

        #### new menu
        self.is_selected = False
        self.switch_sound = pg.mixer.Sound('Assets/Sounds/switch_sound.wav')
        self.switch_sound.set_volume(1)
        self.options_width = 300 #background options width
        self.spacing = 50 #space between the center of two options
        self.first_option_position = constants.SCREEN_SIZE[0]/2, constants.SCREEN_SIZE[1]/2 #center position of first menu option
        self.font_text = pg.font.Font("Assets/Fonts/BebasNeue-Regular.otf", 35)
        
        ### single player
        self.single_off = self.font_text.render("SINGLEPLAYER", 1, constants.WHITE)
        self.rect_single = self.single_off.get_rect()
        
        self.surface_single_off = pg.Surface((self.options_width, self.rect_single.height))
        self.surface_single_rect = self.surface_single_off.get_rect(center=self.first_option_position)
        crop_area = self.surface_single_rect.topleft[0], self.surface_single_rect[1], self.surface_single_rect.width, self.surface_single_rect.height
        self.surface_single_rect.topleft = (0,0)
        center_of_surface = self.surface_single_rect.center 
        self.surface_single_off.blit(self.MENU_IMAGE, (0,0), crop_area)
        self.rect_single.center = center_of_surface
        self.surface_single_off.blit(self.single_off, self.rect_single)
        
        self.surface_single_on = pg.Surface((self.options_width, self.rect_single.height))
        self.surface_single_rect.topleft = (0,0)
        center_of_surface = self.surface_single_rect.center 
        self.rect_single.center = center_of_surface
        self.surface_single_on.fill(constants.BLACK)
        self.surface_single_on.blit(self.single_off, self.rect_single)
        
        self.surface_single_rect.center = self.first_option_position

        ###################################################
        ## multiplayer
        self.multi_off = self.font_text.render("MULTIPLAYER", 1, constants.WHITE)
        self.rect_multi = self.multi_off.get_rect()
        
        self.surface_multi_off = pg.Surface((self.options_width, self.rect_multi.height))
        self.surface_multi_rect = self.surface_multi_off.get_rect(center=(self.first_option_position[0], self.first_option_position[1]+self.spacing))
        crop_area = self.surface_multi_rect.topleft[0], self.surface_multi_rect[1], self.surface_multi_rect.width, self.surface_multi_rect.height
        self.surface_multi_rect.topleft = (0,0)
        center_of_surface = self.surface_multi_rect.center 
        self.surface_multi_off.blit(self.MENU_IMAGE, (0,0), crop_area)
        self.rect_multi.center = center_of_surface
        self.surface_multi_off.blit(self.multi_off, self.rect_multi)

        self.surface_multi_on = pg.Surface((self.options_width, self.rect_multi.height))
        self.surface_multi_rect.topleft = (0,0)
        center_of_surface = self.surface_multi_rect.center 
        self.rect_multi.center = center_of_surface
        self.surface_multi_on.fill(constants.BLACK)
        self.surface_multi_on.blit(self.multi_off, self.rect_multi)
        
        self.surface_multi_rect.center = (self.first_option_position[0], self.first_option_position[1]+self.spacing)

        self.mouse_rect = pg.Rect(0,0,3,3)
        ####

    def on_init(self):
        #FlowCrontoller inital value
        self.menu_state= "singleplayer/multiplayer"
        self._in_menu = True

        #Multiplayer Variables
        self.name = None
        self.server_ip = None
        self.have_client = False
        self.is_host = False

        #surface
        self.surface = pg.display.get_surface()
        self.color = (100, 100, 100)
        self.surface.blit(self.MENU_IMAGE, (0, 0))

        #input text configuration
        pg.key.set_repeat(*KEY_REPEAT_SETTING)

        #music configuration
        self.music = pg.mixer.Sound('Assets/Sounds/menu_sound.wav')
        self.music.set_volume(0.5)
        self.music.play(-1)

    def singleplayer_multiplayer_display(self, event):
        self.singleplayer_multiplayer_interactive(event)

    def multiplayer_get_name(self, event):
        self.input.update()
        self.input.draw(self.surface)
        prompt = self.make_prompt('Type your name :')
        self.surface.blit(*prompt)
        self.input.get_event(event)

    def multiplayer_create_connect(self, event):
        self.multiplayer_create_connect_interactive(event)

    def multiplayer_connect_get_ip(self, event):
        self.input.update()
        self.input.draw(self.surface)
        prompt = self.make_prompt('Type server ip :')
        self.surface.blit(*prompt)
        self.input.get_event(event)

    def on_render(self):
        pg.display.update()

    def on_event(self, event):
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            self._in_menu = False
            self._in_menu_multiplayer = False

    def singleplayer_multiplayer_interactive(self, event):
        mouse = pg.mouse.get_pos()
        self.mouse_rect.center = mouse 
        
        single_is_selected = self.mouse_rect.colliderect(self.surface_single_rect)
        multi_is_selected = self.mouse_rect.colliderect(self.surface_multi_rect)
        if single_is_selected or multi_is_selected:
            if not self.is_selected:
                self.is_selected = True
                self.switch_sound.play()
        else:
            self.is_selected = False

        if single_is_selected:
            self.surface.blit(self.surface_single_on, self.surface_single_rect)
            if event.type == pg.MOUSEBUTTONDOWN:
                self._in_menu = False
        else:
            self.surface.blit(self.surface_single_off, self.surface_single_rect)

        if multi_is_selected:
            self.surface.blit(self.surface_multi_on, self.surface_multi_rect)
            if event.type == pg.MOUSEBUTTONDOWN:
                self.input = TextBox((300, 300, 200, 30), command=self.change_name,
                                     clear_on_enter=True, inactive_on_enter=False)
                self.surface.blit(self.MENU_IMAGE, (0, 0))
                self.menu_state = "multiplayer_get_name"
        else:
            self.surface.blit(self.surface_multi_off, self.surface_multi_rect)

    def multiplayer_create_connect_interactive(self, event):
        mouse = pg.mouse.get_pos()

        if 150 + 200 > mouse[0] > 150 and 450 + 50 > mouse[1] > 450:
            self.surface.blit(self.SERVER_ON, (150, 450))
            if event.type == pg.MOUSEBUTTONDOWN:
                self.server_client = pyshooterClient(self.name)
                self.server_client.start()
                self.have_client = True
                self.is_host = True
                self._in_menu = False
        else:
            self.surface.blit(self.SERVER_OFF, (150, 450))

        if 450 + 200 > mouse[0] > 450 and 450 + 50 > mouse[1] > 450:
            self.surface.blit(self.CONNECT_ON, (450, 450))
            if event.type == pg.MOUSEBUTTONDOWN:
                self.input = TextBox((300, 300, 200, 30), command=self.change_ip,
                                     clear_on_enter=True, inactive_on_enter=False)
                self.menu_state = "multiplayer_connect_get_ip"
                self.surface.blit(self.MENU_IMAGE, (0, 0))
        else:
            self.surface.blit(self.CONNECT_OFF, (450, 450))

    def change_name(self, id, name):
        self.name = str(name)
        self.menu_state = "multiplayer_create/connect"
        self.surface.blit(self.MENU_IMAGE, (0, 0))

    def change_ip(self,id,ip):
        self.server_ip = str(ip)
        self.menu_state = "connect"
        self.surface.blit(self.MENU_IMAGE, (0, 0))

    def connect(self):
        self.server_client = pyshooterClient(self.name)
        self.have_client = self.server_client.start_connect(self.server_ip)
        self._in_menu = False


    def make_prompt(self, message):
        # font = pg.font.SysFont("arial", 20)
        font = pg.font.Font("Assets/Fonts/BebasNeue-Regular.otf", 20)
        rend = font.render(message, True, pg.Color("black"))
        return (rend, rend.get_rect(topleft=(270, 270)))


    def intro(self):
        #music and other variables
        self.on_init()

        #while in menu select correct display case
        while(self._in_menu):
            for event in pg.event.get():
                self.on_event(event)
                if self.menu_state == "singleplayer/multiplayer":
                    self.singleplayer_multiplayer_display(event)
                elif self.menu_state == "multiplayer_get_name":
                    self.multiplayer_get_name(event)
                elif self.menu_state == "multiplayer_create/connect":
                    self.multiplayer_create_connect(event)
                elif self.menu_state == "multiplayer_connect_get_ip":
                    self.multiplayer_connect_get_ip(event)
                elif self.menu_state == "connect":
                    self.connect()
            self.on_render()

        self.music.stop()
