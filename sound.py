import math
from loaders import *

class Sound():
	def __init__(self, name):
		self.sound = load_sound(name)
		self.on = 0
		self.onlast = 0
		self.stop()
	def play(self, dist):
		self.sound.set_volume(math.exp(-dist/400))
		self.sound.play() #comment this line out to turn off sounds
	def stop(self):
		self.sound.stop()
	def update(self):
		if self.on == 1 and self.onlast == 0:
			self.play()
		if self.on == 0 and self.onlast == 1:
			self.stop()
		self.onlast = self.on
	def setArray(self):
		self.sound = pygame.sndarray.make_sound(self.array)