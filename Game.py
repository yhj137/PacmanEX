import source
import pygame,sys
from mysprite import *
import map
import gui
import control
import autofind
from copy import deepcopy
import time


class Pacman_Game():
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((600,365))
		pygame.display.set_caption('Pacman EX')

		# set fps

		self.clock = pygame.time.Clock()

		# create sprite

		self.pacman = Pacman(self.screen,source.pacman_img,(25,25),(8,10),3)
		self.ghost1 = ghost(self.screen,source.ghost1_img,(25,25),(4,8),1)
		self.ghost2 = ghost(self.screen,source.ghost2_img,(25,25),(4,9),1)
		#self.ghost1.smart = True
		
		control.loadinf(source.classic_map1, self.screen,self.pacman,ghost = True, ghost1 = self.ghost1,ghost2 = self.ghost2)
		self.screen = pygame.display.set_mode((control.winw,control.winh))

		# create text
		self.ABfont=pygame.font.SysFont('Arial Black',24)
		self.AB18font=pygame.font.SysFont('Arial Black',18)

		self.mouseflag=0
		self.standard_color = {'normal':(100,100,150),'normalx':(150,200,200),'normalt':(150,200,200),\
							'active':(150,150,200),'activex':(200,20,230),'activet':(170,220,220),\
							'pressed':(50,50,100),'pressedx':(100,0,130),'pressedt':(120,170,170),\
							'Disabled':(50,50,100),'Disabledx':(50,50,70),'Disabledt':(100,150,150)}

		self.button1=gui.Button(self.screen,"Random",(160,30,10,20),(-200,105,control.winw),self.standard_color)
		self.button2=gui.Button(self.screen,"Classic 1",(160,30,10,20),(-200,35,control.winw),self.standard_color)
		self.button3=gui.Button(self.screen,"Classic 2",(160,30,10,20),(-200,70,control.winw),self.standard_color)

		self.clear_button = gui.Button(self.screen,"CL",(25,25,5,12),(-200,555,control.winw),self.standard_color)
		self.reduce_button = gui.Button(self.screen,"-",(25,25,5,14),(-175,555,control.winw),self.standard_color)
		self.plus_button = gui.Button(self.screen,"+",(25,25,5,14),(-140,555,control.winw),self.standard_color)
		self.c1_button = gui.Button(self.screen,"C1",(25,25,5,12),(-115,555,control.winw),self.standard_color)
		self.c2_button = gui.Button(self.screen,"C2",(25,25,5,12),(-90,555,control.winw),self.standard_color)
		self.r_button = gui.Button(self.screen,"R",(25,25,5,12),(-65,555,control.winw),self.standard_color)

		self.menu1 = gui.Menu(self.screen,(160,30,15),(-200,135,control.winw),['Play by yourself','DFS Search','BFS Search','DP Search',"A Star Search","Greedy Search 1","Greedy Search 2","AI Agent"],self.standard_color)
		self.menu2 = gui.Menu(self.screen,(160,30,15),(-200,405,control.winw),['No Ghost','Weak Ghost','Strong Ghost'],self.standard_color,1)
		self.print_text = gui.text_box((350,100,14),(180,control.gameh+20),(180,230,230),source.Print_text[0])
		
		# create agent
		self.autoagent = autofind.AutoFind(self.pacman)
		#autoagent.loadmap(temp_test[0],temp_test[2])

		self.Control_Mode = 'Player'
		self.Ghost_Mode = 'Weak'
		self.Select_Points_Function = None
		self.Create_Path_Function = None
		self.start_time = 0
		self.end_time = 0
		self.Change_flag = 0
		self.Pea_num = 100
	
	def button_update(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				self.mouseflag=1
			elif event.type == pygame.MOUSEBUTTONUP:
				self.mouseflag=0
		
		# logical update
		self.Change_flag = 0
		if self.button1.ispress():
			Wall.Group.clear()
			Pea.Group.clear()
			Capsule.Group.clear()
			temp = []
			limit_num = None
			if self.menu1.nowitem == 0:
				self.Control_Mode = 'Player'
				self.Select_Points_Function = None
				self.Create_Path_Function = None
			elif self.menu1.nowitem == 1: #DFS
				self.Control_Mode = 'Computer'
				self.Select_Points_Function = self.autoagent.dfs_search
				self.Create_Path_Function = self.autoagent.return_path
				limit_num = 50
			elif self.menu1.nowitem == 2: #BFS
				self.Control_Mode = 'Computer'
				self.Select_Points_Function = self.autoagent.bfs_search
				self.Create_Path_Function = self.autoagent.return_path
				limit_num = 30
			elif self.menu1.nowitem == 3: #DP
				self.Control_Mode = 'Computer'
				self.Select_Points_Function = self.autoagent.dp_search
				self.Create_Path_Function = self.autoagent.return_path
				limit_num = 15
			elif self.menu1.nowitem == 4: #a*
				self.Control_Mode = 'Computer'
				self.Select_Points_Function = self.autoagent.a_star_search
				self.Create_Path_Function = self.autoagent.return_path
				limit_num = 30
			elif self.menu1.nowitem == 5: #Greedy
				self.Control_Mode = 'Computer'
				self.Select_Points_Function = self.autoagent.greedy_search
				self.Create_Path_Function = None
			elif self.menu1.nowitem == 6: #Greedy
				self.Control_Mode = 'Computer'
				self.Select_Points_Function = self.autoagent.greedy_search2
				self.Create_Path_Function = self.autoagent.return_path
			elif self.menu1.nowitem == 7: #AI
				self.Control_Mode = 'AI'
				self.Select_Points_Function = None
				self.Create_Path_Function = None
			
			gh = False
			if self.menu2.nowitem == 0:
				self.Ghost_Mode = 'No'
			elif self.menu2.nowitem == 1: #DFS
				self.Ghost_Mode = 'Weak'
				self.ghost1.smart = False
				gh = True
			elif self.menu2.nowitem == 2: #BFS
				self.Ghost_Mode = 'Strong'
				self.ghost1.smart = True
				gh = True
			
			control.loadinf("rand",self.screen,self.pacman,temp,self.Pea_num ,ghost = gh,ghost1 = self.ghost1,ghost2 = self.ghost2)
			self.autoagent.loadmap(temp[0][0],temp[0][1], gh)
			self.screen = pygame.display.set_mode((control.winw,control.winh))
			for i in gui.Button.ButtonGroup:
				i.xy=(i.xy[0],i.xy[1],control.winw)
			for i in gui.Menu.MenuGroup:
				i.xy=(i.xy[0],i.xy[1],control.winw)
			self.Change_flag = 1
			
				
		if self.button2.ispress():
			Wall.Group.clear()
			Pea.Group.clear()
			Capsule.Group.clear()
			# map load
			The_map = []
			if self.menu1.nowitem == 0:
				self.Control_Mode = 'Player'
				self.Select_Points_Function = None
				self.Create_Path_Function = None
			elif self.menu1.nowitem == 1: #DFS
				self.Control_Mode = 'Computer'
				self.Select_Points_Function = self.autoagent.dfs_search
				self.Create_Path_Function = self.autoagent.return_path
			elif self.menu1.nowitem == 2: #BFS
				self.Control_Mode = 'Computer'
				self.Select_Points_Function = self.autoagent.bfs_search
				self.Create_Path_Function = self.autoagent.return_path
			elif self.menu1.nowitem == 3: #DP
				self.Control_Mode = 'Computer'
				self.Select_Points_Function = self.autoagent.dp_search
				self.Create_Path_Function = self.autoagent.return_path
			elif self.menu1.nowitem == 4: #a*
				self.Control_Mode = 'Computer'
				self.Select_Points_Function = self.autoagent.a_star_search
				self.Create_Path_Function = self.autoagent.return_path	
			elif self.menu1.nowitem == 5: #Greedy
				self.Control_Mode = 'Computer'
				self.Select_Points_Function = self.autoagent.greedy_search
				self.Create_Path_Function = None
			elif self.menu1.nowitem == 6: #Greedy2
				self.Control_Mode = 'Computer'
				self.Select_Points_Function = self.autoagent.greedy_search2
				self.Create_Path_Function = self.autoagent.return_path
			elif self.menu1.nowitem == 7: #AI
				self.Control_Mode = 'AI'
				self.Select_Points_Function = None
				self.Create_Path_Function = None
			
			gh = False
			if self.menu2.nowitem == 0:
				self.Ghost_Mode = 'No'
			elif self.menu2.nowitem == 1: #DFS
				self.Ghost_Mode = 'Weak'
				self.ghost1.smart = False
				gh = True
			elif self.menu2.nowitem == 2: #BFS
				self.Ghost_Mode = 'Strong'
				self.ghost1.smart = True
				gh = True
			
			The_map = deepcopy(source.classic_map1)
			The_map[2] = map.limit_pea(The_map[2],The_map[3], self.Pea_num)
			
			control.loadinf(The_map, self.screen,self.pacman, ghost = gh, ghost1 = self.ghost1,ghost2 = self.ghost2)
			if self.menu1.nowitem != 0:
				self.autoagent.loadmap(The_map[0],The_map[2], gh)
			# self.screen set
			self.screen = pygame.display.set_mode((control.winw,control.winh))
			for i in gui.Button.ButtonGroup:
				i.xy=(i.xy[0],i.xy[1],control.winw)
			for i in gui.Menu.MenuGroup:
				i.xy=(i.xy[0],i.xy[1],control.winw)
			self.Change_flag = 2
			
		if self.button3.ispress():
			Wall.Group.clear()
			Pea.Group.clear()
			Capsule.Group.clear()
			The_map = []
			if self.menu1.nowitem == 0:
				self.Control_Mode = 'Player'
				self.Select_Points_Function = None
				self.Create_Path_Function = None
			elif self.menu1.nowitem == 1: #DFS
				self.Control_Mode = 'Computer'
				self.Select_Points_Function = self.autoagent.dfs_search
				self.Create_Path_Function = self.autoagent.return_path	
			elif self.menu1.nowitem == 2: #BFS
				self.Control_Mode = 'Computer'
				self.Select_Points_Function = self.autoagent.bfs_search
				self.Create_Path_Function = self.autoagent.return_path	
			elif self.menu1.nowitem == 3: #DP
				self.Control_Mode = 'Computer'
				self.Select_Points_Function = self.autoagent.dp_search
				self.Create_Path_Function = self.autoagent.return_path
			elif self.menu1.nowitem == 4: #a*
				self.Control_Mode = 'Computer'
				self.Select_Points_Function = self.autoagent.a_star_search
				self.Create_Path_Function = self.autoagent.return_path	
			elif self.menu1.nowitem == 5: #Greedy
				self.Control_Mode = 'Computer'
				self.Select_Points_Function = self.autoagent.greedy_search
				self.Create_Path_Function = None
			elif self.menu1.nowitem == 6: #Greedy2
				self.Control_Mode = 'Computer'
				self.Select_Points_Function = self.autoagent.greedy_search2
				self.Create_Path_Function = self.autoagent.return_path	
			elif self.menu1.nowitem == 7: #AI
				self.Control_Mode = 'AI'
				self.Select_Points_Function = None
				self.Create_Path_Function = None
			
			gh = False
			if self.menu2.nowitem == 0:
				self.Ghost_Mode = 'No'
			elif self.menu2.nowitem == 1: #DFS
				self.Ghost_Mode = 'Weak'
				self.ghost1.smart = False
				gh = True
			elif self.menu2.nowitem == 2: #BFS
				self.Ghost_Mode = 'Strong'
				self.ghost1.smart = True
				gh = True
			
			The_map = deepcopy(source.classic_map2)
			The_map[2] = map.limit_pea(The_map[2],The_map[3], self.Pea_num)
			
			control.loadinf(The_map, self.screen,self.pacman, ghost = gh, ghost1 = self.ghost1,ghost2 = self.ghost2)
			if self.menu1.nowitem != 0:
				self.autoagent.loadmap(The_map[0],The_map[2], gh)
			self.screen = pygame.display.set_mode((control.winw,control.winh))
			for i in gui.Button.ButtonGroup:
				i.xy=(i.xy[0],i.xy[1],control.winw)
			for i in gui.Menu.MenuGroup:
				i.xy=(i.xy[0],i.xy[1],control.winw)
			self.Change_flag = 3
			
		if self.clear_button.ispress():
			self.Pea_num = 1
		if self.reduce_button.ispress():
			if self.Pea_num > 1:
				self.Pea_num -= 1
		if self.plus_button.ispress():
			self.Pea_num += 1
		if self.c1_button.ispress():
			self.Pea_num = 100
		if self.c2_button.ispress():
			self.Pea_num = 330
		if self.r_button.ispress():
			self.Pea_num = 144
			
		if self.menu1.is_item_change() != -1:
			if self.menu1.nowitem == 1:
				if self.Pea_num > 5:
					self.Pea_num = 5
			elif self.menu1.nowitem == 2:
				if self.Pea_num > 10:
					self.Pea_num = 10
			elif self.menu1.nowitem == 3:
				if self.Pea_num > 15:
					self.Pea_num = 15
			elif self.menu1.nowitem == 4:
				if self.Pea_num > 12:
					self.Pea_num = 12
			
		if self.menu1.nowitem == 0 or self.menu1.nowitem == 5 or self.menu1.nowitem == 6:
			self.button1.isable = True
			self.button2.isable = True
			self.button3.isable = True
		if self.menu1.nowitem == 1:
			if self.Pea_num > 50:
				self.button2.isable = False
			else:
				self.button2.isable = True
			if self.Pea_num > 5:
				self.button3.isable = False
			else:
				self.button3.isable = True
			if self.Pea_num > 50:
				self.button1.isable = False
			else:
				self.button1.isable = True
		if self.menu1.nowitem == 2:
			if self.Pea_num > 12:
				self.button2.isable = False
			else:
				self.button2.isable = True
			if self.Pea_num > 10:
				self.button3.isable = False
			else:
				self.button3.isable = True
			if self.Pea_num > 32:
				self.button1.isable = False
			else:
				self.button1.isable = True
		if self.menu1.nowitem == 3:
			if self.Pea_num > 15:
				self.button2.isable = False
			else:
				self.button2.isable = True
			if self.Pea_num > 15:
				self.button3.isable = False
			else:
				self.button3.isable = True
			if self.Pea_num > 15:
				self.button1.isable = False
			else:
				self.button1.isable = True
		if self.menu1.nowitem == 4:
			if self.Pea_num > 17:
				self.button2.isable = False
			else:
				self.button2.isable = True
			if self.Pea_num > 12:
				self.button3.isable = False
			else:
				self.button3.isable = True
			if self.Pea_num > 34:
				self.button1.isable = False
			else:
				self.button1.isable = True
	
				
	def update(self):
		self.tick = pygame.time.get_ticks()
		self.clock.tick(60)
		self.screen.fill((30,30,50))
		self.button_update()
		for pea in Pea.Group:
			if -15<self.pacman.rect.x-pea.rect.x<0 and -15<self.pacman.rect.y-pea.rect.y<0:
				Pea.Group.remove(pea)
				if self.Control_Mode == 'Computer':
					self.autoagent.pea.remove((self.pacman.unitz[0],self.pacman.unitz[1]))
				map.points+=1
				map.now_pea+=1
				if map.now_pea==map.target_points:
					map.winflag = 1
		
		if control.is_ghost == True:
			for capsule in Capsule.Group:
				if -15<self.pacman.rect.x-capsule.rect.x<0 and -15<self.pacman.rect.y-capsule.rect.y<0:
					Capsule.Group.remove(capsule)
					self.ghost1.fear = 30
					self.ghost2.fear = 30
			
			if -10 < self.pacman.rect.x - self.ghost1.rect.x < 10 and -10 < self.pacman.rect.y - self.ghost1.rect.y < 10:
				if self.ghost1.fear > 0:
					self.ghost1.reset()
					map.points+=10
				else:
					map.loseflag = 1
			if -12 < self.pacman.rect.x - self.ghost2.rect.x < 12 and -12 < self.pacman.rect.y - self.ghost2.rect.y < 12:
				if self.ghost2.fear > 0:
					self.ghost2.reset()
					map.points+=10
				else:
					map.loseflag = 1
		
		if self.Control_Mode == 'Computer':
			self.start_time = time.time()
			self.autoagent.findway(self.Select_Points_Function,self.Create_Path_Function)
			self.end_time = time.time()
		
		if map.loseflag == 0 and map.winflag == 0:
			self.pacman.update(map.winflag)
			if control.is_ghost == True:
				self.ghost1.update(self.pacman.unitz)
				self.ghost2.update(self.pacman.unitz)
		for i in Wall.Group:
			i.update()
		for i in Pea.Group:
			i.update()
		for i in Capsule.Group:
			i.update()
		for i in gui.Button.ButtonGroup:
			i.update(self.mouseflag)	
		for i in gui.Menu.MenuGroup:
			i.update(self.mouseflag)	
	
	def draw(self):
		pygame.draw.rect(self.screen, (10,10,20),(0,0,control.gamew+5,control.gameh+5))
		pygame.draw.rect(self.screen, (50,40,100),(0,control.gameh+5,control.gamew+5,control.winh-control.gameh))
		pygame.draw.rect(self.screen, (5,5,10),(10,control.gameh+15,150,control.winh-control.gameh-25), border_radius=5)
		pygame.draw.rect(self.screen, (5,5,10),(170,control.gameh+15,control.gamew-175,control.winh-control.gameh-25), border_radius=5)
		
		if self.Change_flag != 0:
			temp = source.Print_text[self.menu1.nowitem]
			if self.menu1.nowitem != 0 and self.menu1.nowitem != 5 and self.menu1.nowitem != 7:
				temp = temp[:-1]+ " " + "%.3f" % (self.end_time-self.start_time)+"s" 
			if self.Change_flag == 1:
				self.print_text = gui.text_box((170,100,11),(180,control.gameh+20),(180,230,230),temp)
			elif self.Change_flag == 2:
				self.print_text = gui.text_box((350,100,14),(180,control.gameh+20),(180,230,230),temp)
			elif self.Change_flag == 3:
				self.print_text = gui.text_box((590,100,14),(180,control.gameh+20),(180,230,230),temp)
				
			
		self.print_text.draw(self.screen)
		
		for i in Pea.Group:
			i.draw(self.screen)
		for i in Capsule.Group:
			i.draw(self.screen)
		for i in gui.Button.ButtonGroup:
			i.draw()
		for i in gui.Menu.MenuGroup:
			i.draw()
		for i in Wall.Group:
			i.draw(self.screen)
		if control.is_ghost == True:
			self.ghost1.draw(self.screen)
			self.ghost2.draw(self.screen)
		self.screen.blit(self.pacman.image,self.pacman.rect)
		
		maptext = self.AB18font.render("Choose a Map",1,(180,230,230))
		modetext = self.AB18font.render("Choose a Mode",1,(180,230,230))
		numtext = self.AB18font.render("Pea Num: "+str(self.Pea_num),1,(180,230,230))
		ghosttext = self.AB18font.render("Ghost Mode",1,(180,230,230))
		self.screen.blit(maptext,(control.winw-190,10))
		self.screen.blit(modetext,(control.winw-195,140))
		self.screen.blit(ghosttext,(control.winw-180,410))
		self.screen.blit(numtext,(control.winw-190,530))
		
		if map.winflag == 0 and map.loseflag == 0:
			ptext = self.AB18font.render("Points: "+str(map.points),1,(180,230,230))
			stext = self.AB18font.render("Steps: "+str(self.pacman.step),1,(180,230,230))
			self.screen.blit(ptext,(20,control.gameh+20))
			self.screen.blit(stext,(20,control.gameh+45))
		elif map.winflag == 1:
			ptext=self.AB18font.render("Points: "+str(map.points),1,(255,255,0))
			stext = self.AB18font.render("Steps: "+str(self.pacman.step),1,(255,255,0))
			wintext=self.AB18font.render("You win!!",1,(255,255,0))
			self.screen.blit(ptext,(20,control.gameh+20))
			self.screen.blit(stext,(20,control.gameh+45))
			self.screen.blit(wintext,(20,control.gameh+70))
		elif map.loseflag == 1:
			ptext=self.AB18font.render("Points: "+str(map.points),1,(255,0,0))
			stext = self.AB18font.render("Steps: "+str(self.pacman.step),1,(255,0,0))
			wintext=self.AB18font.render("You Lose!!",1,(255,0,0))
			self.screen.blit(ptext,(20,control.gameh+20))
			self.screen.blit(stext,(20,control.gameh+45))
			self.screen.blit(wintext,(20,control.gameh+70))
		pygame.display.flip()
	
	
		
	def get_now_state(self):
		pea_list = []
		for i in Pea.Group:
			pea_list.append(i.ij)
		return (tuple(self.pacman.unitz), tuple(self.ghost1.unitz), tuple(self.ghost2.unitz), pea_list, map.points, self.pacman.step, self.ghost1.fear, self.ghost2.fear)
		
	def get_next_state(self, state, who, action):
		if who == 'Pacman':
			temp = deepcopy(state[3])
			points = state[4]
			if action == 'U':
				pac_u = (state[0][0], state[0][1] - 1)
			elif action == 'D':
				pac_u = (state[0][0], state[0][1] + 1)
			elif action == 'L':
				pac_u = (state[0][0] - 1, state[0][1])
			elif action == 'R':
				pac_u = (state[0][0] + 1, state[0][1])
			
			if (pac_u[1], pac_u[0]) in temp:
				temp.remove((pac_u[1], pac_u[0]))
				points += 1
			if state[0] == state[1]:
				if state[6] > 0:
					points += 10
			if state[0] == state[2]:
				if state[7] > 0:
					points += 10
			
			return (pac_u, state[1], state[2], temp, points, state[5]+1, state[6], state[7])
		else:
			if action[0] == 'U':
				g1_u = (state[1][0], state[1][1] - 1)
			elif action[0] == 'D':
				g1_u = (state[1][0], state[1][1] + 1)
			elif action[0] == 'L':
				g1_u = (state[1][0] - 1, state[1][1])
			elif action[0] == 'R':
				g1_u = (state[1][0] + 1, state[1][1])
			
			if action[1] == 'U':
				g2_u = (state[2][0], state[2][1] - 1)
			elif action[1] == 'D':
				g2_u = (state[2][0], state[2][1] + 1)
			elif action[1] == 'L':
				g2_u = (state[2][0] - 1, state[2][1])
			elif action[1] == 'R':
				g2_u = (state[2][0] + 1, state[2][1])
			
			return (state[0],g1_u,g2_u,state[3],state[4],state[5],max(0,state[6]-1),max(0,state[7]-1))
			
	def get_value(self, state):
		add = 0
		if state[0] == state[1] and control.is_ghost == True:
			if state[6] == 0:
				return -10000000
			else:
				add = 10
		if state[0] == state[2] and control.is_ghost == True:
			if state[7] == 0:
				return -10000000
			else:
				add = 10
		if len(state[3]) == 0:
			return 9999999999
		
		pg_dis = 100
		if control.is_ghost == True:
			pg_dis = min(control.dis[(state[0][1],state[0][0]),(state[1][1],state[1][0])] ,\
						control.dis[(state[0][1],state[0][0]),(state[2][1],state[2][0])])
		
		pp_dis = 99999999 if len(state[3])!=0 else 0
		for i in state[3]:
			pp_dis = min(pp_dis, control.dis[(state[0][1],state[0][0]),(i[0],i[1])])
		
		return min((pg_dis * pg_dis - 25),0) - pp_dis*pp_dis*2 + (state[4]+add)*10000
	
	def get_legal_action(self, unitz):
		x = public.build(self.pacman.map[unitz[1]][unitz[0]])
		action_list = []
		if x[0] == 1:
			action_list.append('U')
		if x[1] == 1:
			action_list.append('D')
		if x[2] == 1:
			action_list.append('L')
		if x[3] == 1:
			action_list.append('R')
		return action_list
		
	def if_game_over(self, state):
		if len(state[3]) == 0:
			return 'Win'
		if ((state[0] == state[1] and state[6] == 0) or (state[0] == state[2] and state[7] == 0)) and control.is_ghost == True:
			return 'Lose'
		return 'No'
	
	def reset(self):
		Wall.Group.clear()
		Pea.Group.clear()
		Capsule.Group.clear()
		# map load
		The_map = deepcopy(source.classic_map2)
		
		control.loadinf(The_map, self.screen,self.pacman, ghost = True, ghost1 = self.ghost1,ghost2 = self.ghost2)
		
		self.screen = pygame.display.set_mode((control.winw,control.winh))
		for i in gui.Button.ButtonGroup:
			i.xy=(i.xy[0],i.xy[1],control.winw)
		for i in gui.Menu.MenuGroup:
			i.xy=(i.xy[0],i.xy[1],control.winw)
		