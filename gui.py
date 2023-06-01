import pygame

class Button():
	ButtonGroup = []
	def __init__(self,target,txt,whr,xy,colorlist,in_group = True):
		self.target_surface=target
		self.txt=txt
		self.whr=whr
		self.xy=xy
		self.colorlist=colorlist
		self.state='normal'
		self.isable = True
		self.ABfont=pygame.font.SysFont('Arial Black',whr[3])
		self.press=0
		if in_group:
			Button.ButtonGroup.append(self)
		
	
	def update(self, mouseflag):
		self.lasts=self.state
		x,y=pygame.mouse.get_pos()
		if self.xy[2]+self.xy[0]<x<self.xy[2]+self.xy[0]+self.whr[0] and self.xy[1]<y<self.xy[1]+self.whr[1]:
			if self.isable == True:
				if mouseflag==1:
					self.state='pressed'
					self.press=1
				else:
					self.state='active'
		else:
			if self.isable == True:
				self.state='normal'
	
	def ispress(self):
		if (self.state=='normal' or self.state=='active') and self.press==1:
			self.press=0
			return True
		return False
	
	def draw(self):
		temp_color = self.state if self.isable else 'Disabled'
		
		pygame.draw.rect(self.target_surface, self.colorlist[temp_color], \
			(self.xy[2]+self.xy[0],self.xy[1],self.whr[0],self.whr[1]), min(self.whr[1],self.whr[0])//2, border_radius=self.whr[2])
		
		pygame.draw.rect(self.target_surface, self.colorlist[temp_color +'x'], \
			(self.xy[2]+self.xy[0],self.xy[1],self.whr[0],self.whr[1]), 2, border_radius=self.whr[2])
		
		ptext=self.ABfont.render(self.txt,1,self.colorlist[temp_color +'t'])
		rect=ptext.get_rect()
		self.target_surface.blit(ptext,(self.xy[2]+self.xy[0]+(self.whr[0]-rect.w)//2,self.xy[1]+(self.whr[1]-rect.h)//2-1))
		
class Menu():
	class locked_button(Button):
		def __init__(self, target, txt, whr, xy, colorlist, in_group=True):
			self.lastmouseflag = 0
			super().__init__(target, txt, whr, xy, colorlist, in_group)
			
		def update(self, mouseflag):
			self.lasts=self.state
			x,y=pygame.mouse.get_pos()
			if self.xy[2]+self.xy[0]<x<self.xy[2]+self.xy[0]+self.whr[0] and self.xy[1]<y<self.xy[1]+self.whr[1]:
				if self.state != 'pressed':
					self.state='active'
				
				if mouseflag == 1 and mouseflag != self.lastmouseflag:
					if self.state == 'active':
						self.state='pressed'
						self.press=1
			else:
				if self.state=='active':
					self.state='normal'
			self.lastmouseflag = mouseflag
				
	MenuGroup = []
	def __init__(self, target, whs, xy,itemlist, colorlist, init_item = 0):
		self.target_surface=target
		self.itemlist = []
		self.colorlist = colorlist
		self.nowitem = init_item
		self.last_item = init_item
		self.last_state = []
		self.xy = xy
		self.whs =whs
		for i in range(len(itemlist)):
			temp = Menu.locked_button(target,itemlist[i],(whs[0],whs[1],0,whs[2]),(xy[0],xy[1]+whs[1]*(i+1),xy[2]),\
						{'normal':(100,100,150),'normalx':(150,200,200),'normalt':(150,200,200),\
						'active':(150,150,200),'activex':(200,20,230),'activet':(170,220,220),\
						'pressed':(50,50,100),'pressedx':(100,0,130),'pressedt':(120,170,170)}, False)
			self.itemlist.append(temp)
			self.last_state.append(temp.state)
		self.itemlist[init_item].state = 'pressed'
		self.itemlist[init_item].press = 1
		Menu.MenuGroup.append(self)
	
	def update(self, mouseflag):
		self.last_item = self.nowitem
		for i in range(len(self.itemlist)):
			self.itemlist[i].update(mouseflag)
			if self.itemlist[i].state == 'pressed' and self.itemlist[i].state != self.last_state[i]:
				self.nowitem = i
		
		for i in range(len(self.itemlist)):
			if i != self.nowitem and self.itemlist[i].state == 'pressed':
				self.itemlist[i].state = 'normal'
				self.press = 0
			self.last_state[i] = self.itemlist[i].state
	
				
	def draw(self):
		cnt = 0 
		for i in self.itemlist:
			cnt +=1
			i.xy = (self.xy[0],self.xy[1]+self.whs[1]*cnt,self.xy[2])
			i.draw()
	
	def is_item_change(self):
		if self.last_item != self.nowitem:
			return self.nowitem
		return -1
			
class text_box():
	def __init__(self, whs, xy, color,txt):
		def cut_text(t):
			temp = self.Font.render(t,1,color)
			res = []
			if temp.get_rect().w > whs[0]:
				for i in range(len(t)-1,0,-1):
					test = self.Font.render(t[:i],1,color)
					if test.get_rect().w <= whs[0]:
						res.append(test)
						get_res = cut_text(t[i:])
						for j in get_res:
							res.append(j)
						return res
			return [temp]
			
		self.whs = whs
		self.xy = xy
		self.txt = txt
		self.Font = pygame.font.SysFont('Arial Black',whs[2])
		self.txt_table = []
		for i in txt.split('\n'):
			#print(i)
			temp = cut_text(i)
			for j in temp:
				self.txt_table.append(j)
	
	def draw(self, target):
		cnt = 0
		for i in self.txt_table:
			#print(i)
			target.blit(i,(self.xy[0],self.xy[1] + cnt*(self.whs[2]+5)))
			cnt += 1
			