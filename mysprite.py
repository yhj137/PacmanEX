import pygame
import public
from copy import deepcopy
import random
import source
from queue import Queue

class mysprite(pygame.sprite.Sprite):
	
	def __init__(self,target,imgname,wh,xy,n):
		pygame.sprite.Sprite.__init__(self)
		self.target_surface=target
		self.image = pygame.Surface((wh[0],wh[1]),flags=pygame.HWSURFACE)
		if imgname!='rec':
			x=deepcopy(imgname)
			self.real_image = pygame.image.load(x,'flie').convert_alpha()
		else:
			self.real_image = pygame.Surface((wh[0],wh[1]),flags=pygame.HWSURFACE)
		self.rect = self.real_image.subsurface((0,0,wh[0],wh[1])).get_rect()
		self.rect.x=xy[0]
		self.rect.y=xy[1]
		
		self.frame_num=n
		self.frame=1
		self.fpst=0
	
	
	def update(self):
		self.fpst+=1
		if self.fpst==6:
			self.frame+=1
			self.fpst=0
		# self.rect = (self.rect[0]+1,self.rect[1]+1,self.rect[2],self.rect[3])
		if self.frame>self.frame_num:
			self.frame=1
		rect=(self.rect.w*(self.frame-1),0,self.rect.w,self.rect.h)
		self.image = self.real_image.subsurface(rect)
	
	def draw(self,surf):
		surf.blit(self.image,self.rect)
	
	
			
class Pacman(mysprite):
	def __init__(self,target,imgname,wh,xy,n):
		mysprite.__init__(self,target,imgname,wh,(xy[1]*30+5,xy[0]*30+5),n)
		self.lastx=xy[1]*30+5
		self.lasty=xy[0]*30+5
		self.speed=3
		self.direct='R'
		self.keyflag=1
		self.dictx=xy[1]*30+5
		self.dicty=xy[0]*30+5
		self.unitz=[xy[1],xy[0]]
		self.map=[]
		self.next_step_flag = 1
		self.step = 0
	
	def update(self, winflag):
		#print(self.unitz[0],self.unitz[1])
		#self.lastx=self.rect.x
		#self.lasty=self.rect.y
		Pacman.move(self)
		mysprite.update(self)
		
		self.next_step_flag = 0
		if self.rect.x>self.dictx:
			self.rect.x-=self.speed
			if self.rect.x == self.dictx and self.rect.y == self.dicty:
				self.next_step_flag = 1
		elif self.rect.x<self.dictx:
			self.rect.x+=self.speed
			if self.rect.x == self.dictx and self.rect.y == self.dicty:
				self.next_step_flag = 1
		elif self.rect.y>self.dicty:
			self.rect.y-=self.speed
			if self.rect.x == self.dictx and self.rect.y == self.dicty:
				self.next_step_flag = 1
		elif self.rect.y<self.dicty:
			self.rect.y+=self.speed
			if self.rect.x == self.dictx and self.rect.y == self.dicty:
				self.next_step_flag = 1
		else:
			#self.next_step_flag = 1
			#print("asd")
			x=public.build(self.map[self.unitz[1]][self.unitz[0]])
			if self.direct=='L' and x[2]==1:
				self.dictx-=self.speed*10
				self.unitz[0]-=1
			elif self.direct=='R' and x[3]==1:
				self.dictx+=self.speed*10
				self.unitz[0]+=1
			elif self.direct=='U' and x[0]==1:
				self.dicty-=self.speed*10
				self.unitz[1]-=1
			elif self.direct=='D' and x[1]==1:
				self.dicty+=self.speed*10
				self.unitz[1]+=1
			if winflag == 0 and (self.unitz[0]!=self.lastx or self.unitz[1]!=self.lasty):
				self.step += 1
			self.lastx = self.unitz[0]
			self.lasty = self.unitz[1]
			
		if self.direct=='L':
			self.image=pygame.transform.flip(self.image,True,False)
		elif self.direct=='R':
			self.image=pygame.transform.flip(self.image,False,False)
		elif self.direct=='U':
			self.image=pygame.transform.rotate(self.image,90)
		elif self.direct=='D':
			self.image=pygame.transform.rotate(self.image,-90)
	
	def move(self):
		thekey = pygame.key.get_pressed()
		if not (thekey[pygame.K_UP] or thekey[pygame.K_DOWN] or \
			thekey[pygame.K_LEFT] or thekey[pygame.K_RIGHT]):
			self.keyflag=1
		
		x=public.build(self.map[self.unitz[1]][self.unitz[0]])
		if thekey[pygame.K_UP] and x[0]==1 and self.direct!='U':
			if self.direct!='D' or self.keyflag==1:
				self.direct='U'
			self.keyflag=0
		elif thekey[pygame.K_DOWN] and x[1]==1 and self.direct!='D':
			if self.direct!='U' or self.keyflag==1:
				self.direct='D'
			self.keyflag=0
		elif thekey[pygame.K_LEFT] and x[2]==1 and self.direct!='L':
			if self.direct!='R' or self.keyflag==1:
				self.direct='L'
			self.keyflag=0
		elif thekey[pygame.K_RIGHT] and x[3]==1 and self.direct!='R':
			if self.direct!='L' or self.keyflag==1:
				self.direct='R'
			self.keyflag=0

	def gotolast(self):
		self.rect.x=self.lastx
		self.rect.y=self.lasty
		
	def if_can_control(self):
		if self.next_step_flag == 1:
			return True
		return False
	
	def move_to(self, direct):
		self.direct = direct
		
		
			
class Wall(mysprite):
	Group = []
	def __init__(self,target,imgname,wh,xy,col):
		mysprite.__init__(self,target,imgname,wh,xy,1)
		self.color=col
		Wall.Group.append(self)
	
	def update(self):
		Wall.updatecol(self)
		mysprite.update(self)
	
	def updatecol(self):
		self.real_image.fill(self.color)
	
		
	
class Pea(mysprite):
	Group = []
	def __init__(self, target, imgname, wh, xy, n, ij):
		mysprite.__init__(self,target,imgname,wh,xy,n)
		self.ij = ij
		Pea.Group.append(self)
		
class Capsule(mysprite):
	Group = []
	def __init__(self, target, imgname, wh, xy, n, ij):
		mysprite.__init__(self,target,imgname,wh,xy,n)
		self.ij = ij
		Capsule.Group.append(self)

class ghost(mysprite):
	def _bfs(self, x, y, map):
		s = Queue(maxsize = 0)
		s.put(x)
		vis = {}
		vis[x] = (-1,-1)
		while s.empty() == False:
			now = s.get()
			if now == y:
				break
			if public.build(map[now[0]][now[1]])[0] != 0 and (now[0]-1,now[1]) not in vis.keys():
				s.put((now[0]-1,now[1]))
				vis[(now[0]-1,now[1])] = now
			if public.build(map[now[0]][now[1]])[1] != 0 and (now[0]+1,now[1]) not in vis.keys():
				s.put((now[0]+1,now[1]))
				vis[(now[0]+1,now[1])] = now
			if public.build(map[now[0]][now[1]])[2] != 0 and (now[0],now[1]-1) not in vis.keys():
				s.put((now[0],now[1]-1))
				vis[(now[0],now[1]-1)] = now
			if public.build(map[now[0]][now[1]])[3] != 0 and (now[0],now[1]+1) not in vis.keys():
				s.put((now[0],now[1]+1))
				vis[(now[0],now[1]+1)] = now
		t = y
		res = []
		while t!=(-1,-1):
			res.insert(0,t)
			t = vis[t]
		return res[1:]
	
	def __init__(self, target, imgname, wh, xy, n):
		super().__init__(target, imgname[0], wh, (xy[1]*30+5,xy[0]*30+5), n)
		self.image_file = [pygame.image.load(imgname[0],'flie').convert_alpha(),\
							pygame.image.load(imgname[1],'flie').convert_alpha(),\
							pygame.image.load(imgname[2],'flie').convert_alpha(),\
							pygame.image.load(imgname[3],'flie').convert_alpha(),\
							pygame.image.load(imgname[4],'flie').convert_alpha()]
		
		self.direct = 'L'
		self.dictx = xy[1]*30+5
		self.dicty = xy[0]*30+5
		self.speed = 2
		self.unitz = list((xy[1],xy[0]))
		self.init_unitz = (xy[1],xy[0])
		self.map=[]
		self.fear = 0
		self.smart = False
		self.path = []
	
	def update(self,pac_unitz):
		super().update()
		#print(self.path)
		if self.rect.x>self.dictx:
			self.rect.x-=self.speed
		elif self.rect.x<self.dictx:
			self.rect.x+=self.speed
		elif self.rect.y>self.dicty:
			self.rect.y-=self.speed
		elif self.rect.y<self.dicty:
			self.rect.y+=self.speed
		else:
			if self.fear > 0:
				self.fear -= 1
			choose = 0
			
			self.path = self._bfs((self.unitz[1],self.unitz[0]),(pac_unitz[1] ,pac_unitz[0]),self.map)
			if self.smart == True:
				if len(self.path) > 0:
					if self.path[0][0] < self.unitz[1]:
						choose = 'U'
					elif self.path[0][0] > self.unitz[1]:
						choose = 'D'
					elif self.path[0][1] < self.unitz[0]:
						choose = 'L'
					elif self.path[0][1] > self.unitz[0]:
						choose = 'R'
			else:
				x=public.build(self.map[self.unitz[1]][self.unitz[0]])
				choose_list = []
				if x[0] == 1:
					choose_list.append('U')
				if x[1] == 1:
					choose_list.append('D')
				if x[2] == 1:
					choose_list.append('L')
				if x[3] == 1:
					choose_list.append('R')
				if len(self.path) > 0:
					if self.path[0][0] < self.unitz[1]:
						choose_list.append('U')
						choose_list.append('U')
					elif self.path[0][0] > self.unitz[1]:
						choose_list.append('D')
						choose_list.append('D')
					elif self.path[0][1] < self.unitz[0]:
						choose_list.append('L')
						choose_list.append('L')
					elif self.path[0][1] > self.unitz[0]:
						choose_list.append('R')
						choose_list.append('R')
				
				choose = choose_list[random.randint(0,len(choose_list)-1)]
				
			self.direct = choose
			if choose == 'U':
				self.dicty -= 30
				self.unitz[1] -= 1
			elif choose == 'D':
				self.dicty += 30
				self.unitz[1] += 1
			elif choose == 'L':
				self.dictx -= 30
				self.unitz[0] -= 1
			elif choose == 'R':
				self.dictx += 30
				self.unitz[0] += 1
		
		if self.fear == 0:
			if self.direct == 'U':
				self.image = self.image_file[0]
			elif self.direct == 'D':
				self.image = self.image_file[1]
			elif self.direct == 'L':
				self.image = self.image_file[2]
			elif self.direct == 'R':
				self.image = self.image_file[3]
		else:
			self.image = self.image_file[4]
			
	def reset(self):
		self.unitz = list(self.init_unitz)
		self.rect.x = self.init_unitz[0]*30+5
		self.rect.y = self.init_unitz[1]*30+5
		self.dictx = self.init_unitz[0]*30+5
		self.dicty = self.init_unitz[1]*30+5
		self.direct = 'L'
		self.fear = 0