
import os, pygame, math, time, sys, colorsys, random

from pygame.locals import *
sys.path.append(os.path.split(sys.path[0])[0])
from geometry import *
from loaders import *
from sound import *

def scrpos2(value, coord):
	area = pygame.display.get_surface().get_rect()
	if coord == "x":
		tmpdist = (mpx - gunformotiontracking.xrectfixed)/4
		newpos = focused.fixed.x + tmpdist
		if -(newpos - back.rect.width/2) <= area.width/2:
			centerx = back.rect.width/2 - area.width/2
		elif newpos - (-back.rect.width/2)<= area.width/2:
			centerx = (-back.rect.width/2) + area.width/2
		else:
			centerx = newpos
		returnvalue =  (((value - centerx)*masterscale + centerx) - (centerx)) + area.width / 2
		return returnvalue
	else:
		tmpdist = (mpy - gunformotiontracking.yrectfixed)/4
		newpos = focused.fixed.y + tmpdist	
		if -(newpos - back.rect.height/2) <= area.height/2:
			centery = back.rect.height/2 - area.height/2
		elif newpos - (-back.rect.height/2)<= area.height/2:
			centery = (-back.rect.height/2) + area.height/2
		else:
			centery = newpos	
		return (((value - centery)*masterscale + centery) - centery) + area.height /2

def realpos2(value, coord):
	area = pygame.display.get_surface().get_rect()
	if coord == "x":
		tmpdist = (mpx - gunformotiontracking.xrectfixed)/4
		newpos = focused.fixed.x + tmpdist
		if -(newpos - back.rect.width/2) <= area.width/2:
			centerx = back.rect.width/2 - area.width/2
		elif newpos - (-back.rect.width/2)<= area.width/2:
			centerx = (-back.rect.width/2) + area.width/2
		else:
			centerx = newpos
		return (((value - scrpos2(centerx, "x"))/masterscale + scrpos2(centerx, "x")) + centerx) - area.width / 2
	else:
		tmpdist = (mpy - gunformotiontracking.yrectfixed)/4
		newpos = focused.fixed.y + tmpdist	
		if -(newpos - back.rect.height/2) <= area.height/2:
			centery = back.rect.height/2 - area.height/2
		elif newpos - (-back.rect.height/2)<= area.height/2:
			centery = (-back.rect.height/2) + area.height/2
		else:
			centery = newpos	
		return (((value - scrpos2(centery, "y"))/masterscale + scrpos2(centery, "y")) + centery) - area.height /2		
		
def scrpos(value0, value1):
	return (scrpos2(value0, "x"), scrpos2(value1, "y"))
	
def realpos(value0, value1):
	return (realpos2(value0, "x"), realpos2(value1, "y"))
		
def findempty():
	global hitter
	random.seed()
	count = 0
	foundstart = False
	hitter = 0
	while foundstart == False:
		count +=1
		x = random.randint(int(-front.scale/2), int(front.scale/2))
		y = random.randint(int(-front.height()/2), int(front.scale/front.height()/2))
		foundstart = True
		for i in range(-18, 18):
			for j in range(-18, 18):
				if isblack(*scrpos(x + i, y +j)):
					foundstart = False
					break
	return 	(x, y)	

masterscale = 1	

def get_alphaed( surf, alpha):
	global tmpsurf
	try:
		if front.scale != front.scalelast or 1==1:
			tmpsurf = pygame.transform.scale(tmpsurf, (int(surf.scale), int(surf.height())))
		print("sucessful try")
	except:
		tmpsurf = pygame.Surface(surf.get_size(), SRCALPHA, 32)
	tmpsurf.fill( (255,255,255,alpha) )
	tmpsurf.blit( surf, (0,0), None, BLEND_RGBA_MULT)
	return tmpsurf, tmpsurf.get_rect()			

def collidepoint(self):
	if self.hashitlastt == 1:
		self.lasttest = "t"
		return self.x, self.y - self.scale/2
	if self.hashitlastb == 1:
		self.lasttest = "b"
		return self.x, self.y + self.scale/2
	if self.hashitlastl == 1:
		self.lasttest = "l"
		return self.x - self.height()/2, self.y
	if self.hashitlastr == 1:
		self.lasttest = "r"
		return self.x + self.height()/2, self.y
	if self.lasttest == "t":
		return self.x, self.y - self.scale/2
	if self.lasttest == "b":
		return self.x, self.y + self.scale/2
	if self.lasttest == "l":
		return self.x - self.height()/2, self.y
	if self.lasttest == "r":
		return self.x + self.height()/2, self.y

class Ob():
	def __init__(self, x =0, y =0):
		self.x = x
		self.y = y
	def __getitem__(self, number):
		if number == 0:
			return self.x
		if number == 1:
			return self.y  	
		if number == 2:
			try:
				self.z
				return self.z
			except:
				return "garbage"
		if number >2:
			return "garbage"
	def __setitem__(self, number, result):
		if number == 0:
			self.x = result
		if number == 1:
			self.y = result
		if number == 2:
			self.z = result
	def __len__(self):
		count = 0
		a = True
		while a == True:
			if self[count] != "garbage" and self[count] != None:
				count +=1
			else:
				a = False
				return count
		return count				

class A(pygame.sprite.Sprite, Ob):
	"""Base class defining all the objects"""
	def pyname(self):
		result = []
		for item in globals():
			if globals()[item] is self:
				result.append(item)		
		return result
	def width(self):
		return self.scale
	def height(self):
		return self.scale/self.origwidth*self.origheight
	def redraw(self):
		if self.rescale() or self.recolor() or self.reangle():
			result = True
		else:
			result = False
		return result
	def reangle(self):
		try:
			if self.angle != self.anglel:
				result = True
			else:
				result = False
		except:
			result =  True
		self.anglel = self.angle
		return result
	def recolor(self):
		try:
			if self.parent.rcolor != self.rcolorl or self.parent.rcolor != self.parent.rcolorl:
				result = True
			else:
				result = False
		except:
			result = True
			
		self.rcolorl = self.parent.rcolor
		return result			
	def rescale(self):
		try:
			if self.scale != self.scalel:# or self.angle != self.anglel:
				result = True
			else:
				result = False
		except:#for first time
			result = True
		self.scalel = self.scale
		return result			
	def __init__(self, limage = 0, limage2 = 0):
		self.parent = self
		pygame.sprite.Sprite.__init__(self) 
		self.image1, self.rect1 = load_image(limage, None)
		self.image, self.rect = self.image1, self.rect1

		self.original1, self.rect1 = load_image(limage, None)
		self.original, self.rect = self.original1, self.rect1
		if not limage2 == 0:
			self.image2, self.rect2 = load_image(limage2, None)
			self.original2, self.rect2 = load_image(limage2, None)
			
		self.image3, self.rect3 = get_alphaed(self.image1, 100)
		self.original3, self.rect3 = get_alphaed(self.image1, 100)
					
		self.origwidth =self.rect.width
		self.origheight = self.rect.height
		self.scale = self.rect.width
		self.scalelast = 0#so that it will do the first scale		
		
		self.x = 0
		self.y = 0
		self.xvc = 0.0
		self.yvc = 0.0
		self.xv = 0.0 #x velocity supplied
		self.yv = 0.0
		self.xf = 0.0
		self.yf = 0
				
		self.angle = 0
		self.scaleincrement = 0.0
		
		self.t = 0.2 #time step
		self.mu = 1
		self.modifiedx = 0
		self.modifiedy = 0
		
		self.xvlast = 0
		self.yvlast = 0
		self.xflast = 0
		self.yflast = 0
		
		self.name = 0
		self.framecount = 100
		self.weregoing = 0
		self.pressingbutton3 = 0
		self.maxfrac = 10
		self.maxframe = 8
		
		self.fullstate = 1
		self.timesincelasthealth = 9000
		self.title = 0
		self.firingstate = 0		
		self.timesinceupdate = 0
		self.explodecount=1
		
		self.hashitlastt = 0
		self.hashitlastb =0
		self.hashitlastl = 0
		self.hashitlastr = 0
		self.catchcount = 0
		self.modifiedscale = 0
		self.lasthealth = 1
		self.lastscale = 0
		self.score = 0
		
		self.init = Ob(0,0)
		self.fixed = Ob(0,0)
		self.best = Ob(0.0)

		self.random = random.random()
		self.hookhitcount =0
		
		self.rcolor = 0
		self.bcolor = 0
		self.gcolor = 0
		
		self.rcolorl = 0
		self.bcolorl = 0
		self.gcolorl = 0
		
		self.explosive = 0
		
		self.sound = Sound("sample.wav")
		self.sound.array = pygame.sndarray.array(self.sound.sound)
		self.sound.parent = self
		
		self.tfirst = -1
		self.bfirst = -1
		self.lfirst = -1
		self.rfirst = -1
		self.lasttest = 0
		self.lasttest2 = 0
		self.listofblocks = []
		self.dealtwith = 0
		self.stopnow = 0
		self.werepoppin = 0
		self.oldlength = 0
		self.touching = 0
		
		self.best.x = 0
		self.best.y = 0
		self.targetfound = 0
		
		self.capturedlist = []
		self.captured = 0
		self.returned = 0
		
		try:
			self.target = man.init
		except:
			self.target = Ob()
		self.touchingcount = 0
		
		self.scroll = 0
		self.gunlist = []
		self.originallist = []
		self.state = 0
		self.lastscroll = 0
		self.on = 0
		self.onlast = 0
		self.blur = 0
		
	def update(self):

		if self.title == "bullet":
			self.scale = self.parent.scale/290*75
			self.scaledifference = 0
		self.scale *=masterscale
		
		global hitter
		self.lastscale = self.scale#fixme, move to end of update?
		self.scale = self.scale * (100 + self.scaleincrement)/100
		
		self.scaledifference = self.scale - self.lastscale
		
		#calculate new velocity based on acceleration
		self.xvc += 2*self.xf*self.t
		self.yvc += 2*self.yf*self.t		
	
		#apply non physical absolute velocties
		if self.modifiedx == 1:
			self.xvc = self.xv
		if self.modifiedy == 1:
			self.yvc = self.yv
	
		self.maxfrac = int(max(math.fabs(self.xvc), math.fabs(self.yvc))/20) + 1#plus 1 to stop zero division#the faster you go, the more it will stop you going through walls. (can still go through really thin walls though)
				
		hitter = self
		if self is man or (self.title == "bullet"): #correct line

			for frac in  range(0,self.maxfrac+1):
			#is these isblack test come back true, no action taken, ie dont move the man
				if isblack(*scrpos(self.x + self.scale/2 + self.xvc*self.t*(frac/self.maxfrac), self.y)) or isblack(*scrpos(self.x + self.scale/2 + self.xvc*self.t*(frac/self.maxfrac), self.y - self.height()/(4.0))) or isblack(*scrpos(self.x + self.scale/2 + self.xvc*self.t*(frac/self.maxfrac), self.y + self.height()/(4.0))):
					self.hashit = 1
					self.hashitr = 1			
					if self.xvc >= 0:
						self.xvc *= frac/self.maxfrac
					break
			if self.xvc >=0: #so we dont end up moving twice
				self.x += self.xvc*self.t
			########
			for frac in  range(0,self.maxfrac+1):
				if isblack(*scrpos(self.x - self.scale/2 + self.xvc*self.t*(frac/self.maxfrac), self.y)) or isblack(*scrpos(self.x - self.scale/2 + self.xvc*self.t*(frac/self.maxfrac), self.y - self.height()/(4.0))) or isblack(*scrpos(self.x - self.scale/2 + self.xvc*self.t*(frac/self.maxfrac), self.y + self.height()/(4.0))):
					self.hashit = 1
					self.hashitl = 1				
					if self.xvc <= 0:
						self.xvc *= frac/self.maxfrac
					break
			if self.xvc <=0:
				self.x += self.xvc*self.t	
			########
			for frac in  range(0,self.maxfrac+1):
				if isblack(*scrpos(self.x , self.y+ self.height()/2 + self.yvc*(frac/self.maxfrac)*self.t)) or isblack(*scrpos(self.x - self.scale/(4.0), self.y+ self.height()/2 + self.yvc*(frac/self.maxfrac)*self.t)) or isblack(*scrpos(self.x + self.scale/(4.0), self.y+ self.height()/2 + self.yvc*(frac/self.maxfrac)*self.t)):
					self.hashit = 1
					self.hashitb = 1
					self.jumpcount = 0 #say it has 				
					if self.yvc >= 0:
						self.yvc *= frac/self.maxfrac #slow it down
					break
			if self.yvc >= 0:	
					self.y += self.yvc*self.t
			#########
			for frac in  range(0,self.maxfrac +1):
				if isblack(*scrpos(self.x , self.y - self.height()/2 + self.yvc*(frac/self.maxfrac)*self.t)) or isblack(*scrpos(self.x - self.scale/(4.0), self.y - self.height()/2 + self.yvc*(frac/self.maxfrac)*self.t)) or isblack(*scrpos(self.x + self.scale/(4.0), self.y - self.height()/2 + self.yvc*(frac/self.maxfrac)*self.t)):
					self.hashit = 1
					self.hashitt = 1
					#if self is bot:
					#	print "touchin top"
					if self.yvc <= 0:
						self.yvc *=frac/self.maxfrac
			if self.yvc <= 0:	
				self.y += self.yvc*self.t
	
		else:
			self.x += self.xvc*self.t
			self.y += self.yvc*self.t

		#non phyiscal things	
		if self.title == "bullet": #ie if it is a bullet
			self.angle = math.pi + math.atan2(self.xvc, self.yvc)
		
		#this could be the thing blocking shooting when you are stuck between walls
		

		if self.scaledifference > 0: #so when you shrink, just shrinks to the center
			if self.hashitb == 1:
				if isblack(*scrpos(self.x , self.y - (self.scale+self.scaledifference)*self.height()/self.width()/2)):#odd code#shouldnt this just have self.scale, as difference is already added
					None
				else:
					self.y -= (self.scaledifference*self.height()/(self.width()*2))
			if self.hashitt == 1:
				if isblack(*scrpos(self.x , self.y + (self.scale+self.scaledifference)*self.height()/self.width()/2)):
					None
				else:
					self.y += (self.scaledifference*self.height()/(self.width()*2))
			if self.hashitl == 1:
				if isblack(*scrpos(self.x + (self.scale + self.scaledifference), self.y)):
					None
				else:	
					self.x += (self.scaledifference/2)
			if self.hashitr == 1:
				if isblack(*scrpos(self.x - (self.scale + self.scaledifference), self.y)):
					None
				else:	
					self.x -= (self.scaledifference/2)
					
		if self is man:#opponents dont use this routine :(
			self.squishsoundcount = 0
				

		if self.redraw():
			self.image = self.original
		
			if self in home:
				
				pygame.draw.circle(self.image, (self.rcolor, self.gcolor, self.bcolor), (int(self.origwidth/2), int(self.origheight/2)), int(self.origwidth*0.4 + 1), 0)#could draw this circle onto a blank surface and then render that at subpixel places

			self.image = pygame.transform.scale(self.image, (int(self.scale), int(self.height())))#line seems redundant, but somehow isnt
		
			if self.title == "bullet":
				self.image2 = self.original2
				self.image2 = pygame.transform.scale(self.image2, (int(self.scale), int(self.height())))
				self.image2.fill((255-self.parent.rcolor, 255-self.parent.gcolor, 255-self.parent.bcolor), None, BLEND_RGB_SUB)
				self.image.blit(self.image2, (0,0))
			self.image = pygame.transform.scale(self.image, (int(self.scale), int(self.height())))
			self.image = pygame.transform.rotate(self.image, math.degrees(self.angle))

		self.rect = self.image.get_rect()
		self.rect.center = scrpos(self.x, self.y)	
		
		self.xvlast = self.xvc
		self.yvlast = self.yvc
		self.xflast = self.xf
		self.yflast = self.yf			
	
		#reset
		self.xv = 0
		self.yv = 0
		self.xf = 0
		self.yf = 0	
		self.modifiedx = 0
		self.modifiedy = 0
		
		self.hashitt = 0
		self.hashitb = 0
		self.hashitl = 0
		self.hashitr = 0
		self.scale /=masterscale
		
class Man(A):
	def setMultiBullet(self, image):
		for i in range(0,4):
			self.gunlist[0][1].append(Bullet(image))
			self.gunlist[0][1][i].image2, self.gunlist[0][1][i].rect2 = load_image(image[0:-4]+"variable.png", None)
			self.gunlist[0][1][i].original2, self.gunlist[0][1][i].rect2 = load_image(image[0:-4]+"variable.png", None)
			self.gunlist[0][1][i].parent = self
			self.gunlist[0][1][i].explode = pistolhit
			self.gunlist[0][1][i].title = "bullet"
			
	def setBullet(self, image):
		self.b = Bullet(image)
		self.b.image2, self.b.rect2 = load_image(image[0:-4]+"variable.png", None)
		self.b.original2, self.b.rect2 = load_image(image[0:-4]+"variable.png", None)
		self.b.parent = self.parent
		self.b.title = "bullet"
		self.b.explode = explode

	def setGun0(self, image):
		self.gun0= Gun(image)
		self.gun0.image2, self.gun0.rect2 = load_image(image[0:-4]+"variable.png", None)
		self.gun0.original2, self.gun0.rect2 = load_image(image[0:-4]+"variable.png", None)
		self.originallist.append(self.gun0.original2)
		self.gun0.parent = self
		self.gun0.title = "gun"
		self.gunlist.append([self.gun0, []])
		self.setMultiBullet("bullet0.png")
		self.gun0.gunnumber = 0

	def setCross(self):
		self.cross = Cross("cross.png")
		self.cross.parent = self
		self.cross.title = "cross"

	
scene = "3"

class Bullet(A):
	pass
		
class Gun(Man):	
	def update(self):
		self.original2 = ultimateman.originallist[self.gunnumber % len(ultimateman.gunlist)]#hack

		self.scale = self.parent.scale*1.5
		self.scale *=masterscale
		
		self.x = self.parent.x
		self.y = self.parent.y
		
		if self.parent == man and focused == man:
			self.angle = math.pi + math.atan2(mpx - scrpos2(self.x, "x"), mpy - scrpos2(self.y, "y"))
		
		if self.rescale():# or True:	
			self.image = self.original
		
			self.image = pygame.transform.scale(self.image, (int(self.scale), int(self.height())))
		
			self.image = pygame.transform.scale(self.image, (int(self.scale), int(self.height())))
			self.imagestraight = self.image
		#else:
		if math.pi < self.angle < 2*math.pi:
			self.image = self.imagestraight
		else:
			self.image = self.imagestraight	
			self.image = pygame.transform.flip(self.image, 1, 0)		
		self.image = pygame.transform.rotate(self.image, math.degrees(self.angle))		
		
		self.rect = self.image.get_rect()
		self.rect.center = scrpos(self.x,self.y)
		self.scale /=masterscale
		print(scale)
	
class Ground(A):
	def update(self):
		#blurring stuff	
		if self is front:
				if blur == 2:
					if needsmask == 0:
						self.image = self.image3
				if blur == 0:
					if needsmask == 0:
						self.image = self.image1				
		
		self.scale *=masterscale
		if self.redraw():#we dont want to have to redo scaling images for these big images everytime
			self.image1 = pygame.transform.scale(self.original1, (int(self.scale), int(self.height())))
			self.image3 = pygame.transform.scale(self.original3, (int(self.scale), int(self.height())))
			self.image = self.image1#just the first time setup#should be done elsewhere fixme
		
			self.rect = self.image.get_rect()#can be tabbed, as this only changes if the image changes, ie needs a redraw (FIXME, ie put me everywhere)
		self.rect.center = scrpos(self.x,self.y)#	
		self.scale /=masterscale
		
class Cross(A):
	def update(self):

		if self.title == "cursor":
			(self.x, self.y) = realpos(mpx, mpy)
			self.scale = focused.scale/2#could cause problems with the two threads, due to setting scale somewhere in the middle....(mastersclae type problem)
		self.scale *=masterscale
		
		if self.redraw():
			self.image = self.original
			self.image = pygame.transform.scale(self.image, (int(self.scale), int(self.height())))		
			if self.title == "cursor":
				self.image.fill((255-focused.rcolor, 255-focused.gcolor, 255-focused.bcolor), None, BLEND_RGB_SUB)#awesome, just changes the non transparent colors#
				
		
		
		self.rect = self.image.get_rect()
		self.rect.center = scrpos(self.x,self.y)#	
		self.scale /=masterscale			
	
framecount = 1


pressinga=0
pressingd=0
pressingw=0
pressings=0
pressingbutton3=0
tmpcount=0
goingdownforquit=0
fullscreen = 0	

def readinput(events):
	global screen
	global fullscreen
	global focused
	man = focused
	global mpx, mpy
	global pressinga
	global pressingd
	global pressingw
	global pressings
	global pressingbutton3
	global tmpcount
	global goingdownforquit
	global hitter
	hitter = man

	(mpx, mpy) = pygame.mouse.get_pos()

	for event in events:
		# controle da janela
		if event.type == pygame.VIDEORESIZE:
			global smallresolution
			smallresolution = event.size
			screen = pygame.display.set_mode(smallresolution, pygame.RESIZABLE)#event.size gives the size of the resized window as a rect
		if event.type == QUIT or (event.type == KEYDOWN and event.key == K_q) or (event.type == KEYDOWN and event.key == K_ESCAPE):
			goingdownforquit=1 
			time.sleep(1) #wait for the other thread to send the quit message to the server
			sys.exit() #then really close
		if event.type == KEYDOWN:
			if event.key == K_f:
				if fullscreen == 0:
					fullscreen = 1
					screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
				else:
					fullscreen = 0
					screen = pygame.display.set_mode(smallresolution, pygame.RESIZABLE)
		
		if event.type == KEYDOWN:			
			if event.key == K_a:
				pressinga=1
			elif event.key == K_d:
				pressingd=1
			elif event.key == K_w:
				pressingw=1
			elif event.key == K_s:
				pressings=1
		
		if event.type == MOUSEBUTTONDOWN:

			for item in man.gunlist[0][1]:
				man.b = item
				
					
		if event.type == KEYUP:
			if event.key == K_w:
				pressingw=0
			elif event.key == K_s:
				pressings=0
			elif event.key == K_a:
				pressinga=0
			elif event.key == K_d:
				None
				pressingd=0
		if event.type == MOUSEBUTTONUP:
			if event.button == 3:
				pressingbutton3=0
			
	(mpx, mpy) = pygame.mouse.get_pos()
	dis = distance2(man.xf, man.yf, mpx, mpy)

	dx = mpx - man.x
	dy = mpy - man.y

	if pressinga == 1:
		man.xf =  400*realpos2(-dy, "x")/dis*(man.scale/100)*masterscale
		man.yf =  400*realpos2(dx, "y")/dis*(man.scale/100)*masterscale
	if pressingd == 1:
		man.xf =  -400*realpos2(dy, "y")/dis*(man.scale/100)*masterscale
		man.yf =  -400*realpos2(-dx, "x")/dis*(man.scale/100)*masterscale
	if pressingw == 1:
		man.xf =  400*realpos2(dx, "x")/dis*(man.scale/100)*masterscale
		man.yf =  400*realpos2(dy, "y")/dis*(man.scale/100)*masterscale
	if pressings == 1:
		man.xf =  -400*realpos2(dx, "x")/dis*(man.scale/100)*masterscale
		man.yf =  -400*realpos2(dy, "y")/dis*(man.scale/100)*masterscale

	if pressingw == 0 or pressings == 0 or pressingd == 0 or pressinga == 0:
		man.xvc = 0
		man.yvc = 0

def related(a,b):
	try:
		if a is b or a is b.parent or b is a.parent:
			return True
	except:
		None
		
	return False


hitter = 0
isblackobject = 0


def isblack(x, y):
	try:
		if hitter.title == "bullet" and hitter.parent in home:#local players bullets
			firing = 1
		else:
			firing = 0
	except:
		firing = 0

	by = hitter
			
	x = int(x)
	y = int(y)
	global isblackobject
	(rx, ry) = realpos(x,y) 
	for item in grounds:
		if not related(item, by):	
			if item.rect.collidepoint(x,y): #makes sure that the later pixel test is really on the image
				(imagex,imagey)=(int((item.origwidth/item.width())*(rx - realpos2(item.rect.left, "x"))), int((item.origheight/item.height())*(ry - realpos2(item.rect.top, "y")))) #gets coords on image, relative to image
				try: 
					if item.array[int(imagex)][int(imagey)] != 16777215: #isnt white			
						if firing == 1:
							if item in opponents or item is man: #stuff abut the shooting switch
								if not [item, hitter.parent] in listofdeaths: #only add new deaths.
									listofdeaths.append([item, hitter.parent]) #not really appropriate place in a test for an action to take place#needs parent as it is a bullet 								
						isblackobject = item
						return True #first true deserves a return
				except:
					return False
	return False

numberofplayers = 1
scoreaverage = 0
scores = [0]

captured = 0
returned = 0

def setup_pygame():
	None
	global whilecount, smallresolution, resolution, screen, fullscreen
	
	pygame.mixer.pre_init(44100,-16,2, 1024)
	random.seed()
	pygame.init()
	whilecount = 0
	pygame.event.set_grab(1)
	try:
		smallresolution = (int(pygame.display.Info().current_w*2/3), int(pygame.display.Info().current_h*2/3))
	except:
		print("requires pygame 1.8.1")
		sys.exit()
	resolution = (int(pygame.display.Info().current_w), int(pygame.display.Info().current_h))#current screen resolution
	try:
		screen = pygame.display.set_mode(smallresolution)#a hack so that when you leave fullscreeen you dont have a window over the whole screeen, but the iamge in jsut the top left, but rather revert back to this screen size
		screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)##change back to 0,0 fror publishing fixme
		fullscreen = 1
	except:
		print("get a newer version of pygame")
		screen = pygame.display.set_mode((640, 480))
		fullscreen = 0

	pygame.display.set_caption(game)

	pygame.mouse.set_pos(pygame.display.get_surface().get_rect().width/2, pygame.display.get_surface().get_rect().height/2)
	pygame.mouse.set_visible(1)

if __name__ == "__main__":

	game = "coffeeworldsssssss"
	name = "Claudio"

	setup_pygame()
	
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((250, 250, 250))

	explode = Sound("explode.wav")
	jump = Sound("jump.wav")
	fire = Sound("fire.wav")
	hookhit = Sound("hookhit.wav")
	hookfire = Sound("hookfire.wav")
	hitwall = Sound("hitwall.wav")
	gotlife = Sound("gotlife.wav")
	injure = Sound("injure.wav")
	changegun = Sound("changegun.wav")
	saber = Sound("saber.wav")
	pistolfire = Sound("pistolfire.wav")
	saberhit = Sound("saberhit.wav")
	pistolhit = Sound("pistolhit.wav")
	clone = Sound("clone.wav")

	blurring = True
	blur = 0

	scene = "1"
	needsmask = 0

	front = Ground("map"+scene+"front.png")
	back = Ground("map"+scene+"back.png")

	front.back = back
	back.front = front

	back.scale=4800 
	front.scale=back.scale

	man = Man("man.png")
	focused = man
	ultimateman = man
	man.scale = 30
	man.name = name
	man.title = man

	home = [man]

	players = []
	for homer in home:
		players.append(homer)

	for player in players:
		player.setGun0("gun0.png")
		player.setCross()
		player.gun = player.gunlist[0][0]
		player.b = player.gunlist[0][1][0]
	
	grounds = [back, man]

	for ground in grounds:
		ground.array = pygame.surfarray.array2d(ground.image)

	gunformotiontracking= Gun("blank.png") 
	gunformotiontracking.parent = man
	gunformotiontracking.gunnumber = 0
	
	cursor = Cross("cross.png")
	cursor.title = "cursor"
	cursor.parent = man

	dspritelist = [front]
	
	for i in range(len(man.gunlist)):
		if i != 4:
			for item in man.gunlist[i][1]:
				dspritelist.append(item) 
	dspritelist += [man.gunlist[0][0]]
	dspritelist += [man]
	
	dspritelist.append(cursor)	

	spritelist = [back]
	spritelist.append(gunformotiontracking)

	spritelist += [man] 
	spritelist += [man.cross]

	for item in man.gunlist:
		spritelist.append(item[0])

	for i in range(len(man.gunlist)):
		for item in man.gunlist[i][1]:
			spritelist.append(item) 

	spritelist.append(front)
	
	spritelist.append(cursor)	

	man.fixed.x = man.x; man.fixed.y = man.y
	gunformotiontracking.xrectfixed, gunformotiontracking.yrectfixed = gunformotiontracking.rect.center

	mpx, mpy = pygame.mouse.get_pos()
	man.init.x, man.init.y = findempty()
	man.x = man.init.x; man.y = man.init.y

	man.fixed.x = man.x; man.fixed.y = man.y
	gunformotiontracking.xrectfixed, gunformotiontracking.yrectfixed = gunformotiontracking.rect.center

	for sprite in spritelist:
		sprite.update()
	for sprite in spritelist:
		sprite.update()	

	lag = 0
	whilecount = 0
	while 1:
	
		whilecount +=1

		readinput(pygame.event.get())

		man.fixed.x = man.x
		man.fixed.y = man.y
	
		gunformotiontracking.xrectfixed, gunformotiontracking.yrectfixed = gunformotiontracking.rect.center	

		for sprite in spritelist:
			sprite.update()
	
		swidth = pygame.display.get_surface().get_rect().width
		sheight = pygame.display.get_surface().get_rect().height	
		for sprite in dspritelist:
			screen.blit(sprite.image, sprite.rect)
	
		pygame.display.flip()