import map
import source
from copy import deepcopy
from queue import Queue
import public
from mysprite import *

winw=12*30+240
winh=365
gamew=12*30+240
gameh=365
is_ghost = False
dis = {}

def loadinf(inf,surf,pac,tempm = None,limit_pea_num = None, ghost = False, ghost1 = None, ghost2 = None):
	def _bfs(x, map):
		global dis
		s = Queue(maxsize = 0)
		s.put(x)
		vis = {}
		vis[x] = 1
		dis[(x,x)] = 0
		while s.empty() == False:
			now = s.get()
			
			if public.build(map[now[0]][now[1]])[0] != 0 and (now[0]-1,now[1]) not in vis.keys():
				s.put((now[0]-1,now[1]))
				dis[(x,(now[0]-1,now[1]))] = dis[(x,now)] + 1
				vis[(now[0]-1,now[1])] = 1
			if public.build(map[now[0]][now[1]])[1] != 0 and (now[0]+1,now[1]) not in vis.keys():
				s.put((now[0]+1,now[1]))
				dis[(x,(now[0]+1,now[1]))] = dis[(x,now)] + 1
				vis[(now[0]+1,now[1])] = 1
			if public.build(map[now[0]][now[1]])[2] != 0 and (now[0],now[1]-1) not in vis.keys():
				s.put((now[0],now[1]-1))
				dis[(x,(now[0],now[1]-1))] = dis[(x,now)] + 1
				vis[(now[0],now[1]-1)] = 1
			if public.build(map[now[0]][now[1]])[3] != 0 and (now[0],now[1]+1) not in vis.keys():
				s.put((now[0],now[1]+1))
				dis[(x,(now[0],now[1]+1))] = dis[(x,now)] + 1
				vis[(now[0],now[1]+1)] = 1
	
	global winw,winh,gamew,gameh,is_ghost,dis
	is_ghost = ghost
	if inf=='rand':
		tempmap=map.creatm(12,12)
		tempmap[1][0][11] = 2
		tempmap[1][11][0] = 2
		for i in range(12):
			for j in range(12):
				_bfs((i,j),tempmap[0])
		
		if limit_pea_num != None:
			tempmap = (tempmap[0],map.limit_pea(tempmap[1],source.random_random,limit_pea_num))
		if tempm != None:
			tempm.append(tempmap)
		winw=12*30+240
		winh=600
		gamew=12*30
		gameh=360
		pac.map=tempmap[0]
		map.transm(surf,pac.map)
		map.addpea(surf,tempmap[1],is_ghost)
		
		map.target_points=len(Pea.Group)
		map.points=0
		map.winflag=0
		map.loseflag=0
		map.now_pea=0
		pac.rect.x=5
		pac.rect.y=5
		pac.dictx=5
		pac.dicty=5
		pac.unitz=[0,0]
		if public.build(tempmap[0][0][0])[1] == 1:
			pac.direct='D'
		else:
			pac.direct='R'
		pac.keyflag=1
		pac.next_step_flag = 1
		temp_u = [[10,11],[11,11]]
		ghost1.unitz = temp_u[0]
		ghost2.unitz = temp_u[1]
		ghost1.init_unitz = tuple(temp_u[0])
		ghost2.init_unitz = tuple(temp_u[1])
		
		ghost1.rect.x = temp_u[0][0]*30+5
		ghost1.rect.y = temp_u[0][1]*30+5
		ghost2.rect.x = temp_u[1][0]*30+5
		ghost2.rect.y = temp_u[1][1]*30+5
		
		ghost1.dictx = temp_u[0][0]*30+5
		ghost1.dicty = temp_u[0][1]*30+5
		ghost2.dictx = temp_u[1][0]*30+5
		ghost2.dicty = temp_u[1][1]*30+5
		
		ghost1.direct = 'L'
		ghost2.direct = 'L'
		ghost1.map = tempmap[0]
		ghost2.map = tempmap[0]
		
		ghost1.fear = 0
		ghost2.fear = 0
	else:
		pac.map=inf[0]
		for i in range(inf[1][0]):
			for j in range(inf[1][1]):
				if inf[5][i][j] == 1:
					_bfs((i,j),inf[0])
		map.transm(surf,pac.map)
		map.addpea(surf,inf[2],is_ghost)
		map.target_points=len(Pea.Group)
		map.winflag=0
		map.loseflag=0
		map.points=0
		map.now_pea=0
		pac.rect.x=inf[6][1]*30+5
		pac.rect.y=inf[6][0]*30+5
		pac.dictx=inf[6][1]*30+5
		pac.dicty=inf[6][0]*30+5
		pac.unitz=[inf[6][1],inf[6][0]]
		pac.direct='R'
		pac.keyflag=1
		pac.next_step_flag = 1
		
		
		temp_u = deepcopy(inf[4])
		ghost1.unitz = temp_u[0]
		ghost2.unitz = temp_u[1]
		ghost1.init_unitz = tuple(temp_u[0])
		ghost2.init_unitz = tuple(temp_u[1])
		
		ghost1.rect.x = temp_u[0][0]*30+5
		ghost1.rect.y = temp_u[0][1]*30+5
		ghost2.rect.x = temp_u[1][0]*30+5
		ghost2.rect.y = temp_u[1][1]*30+5
		
		ghost1.dictx = temp_u[0][0]*30+5
		ghost1.dicty = temp_u[0][1]*30+5
		ghost2.dictx = temp_u[1][0]*30+5
		ghost2.dicty = temp_u[1][1]*30+5
		
		ghost1.direct = 'L'
		ghost2.direct = 'L'
		ghost1.map = inf[0]
		ghost2.map = inf[0]
		
		ghost1.fear = 0
		ghost2.fear = 0
		
		winw=inf[1][1]*30+240
		winh=max(inf[1][0]*30+5+115,600)
		gamew=inf[1][1]*30
		gameh=inf[1][0]*30
		
	pac.step = 0