from mysprite import *
import random
import public
import source

unitw=30
unith=30
wallw=5
points=0
now_pea=0
winflag=0
loseflag=0
target_points=0

def loadmap(surf,filename):
	with open(filename,'r') as f:
		lines=f.readlines()
		for data in lines:
			s=[eval(i) for i in list(data.split())]
			for i in s:
				wall=Wall(surf,'rec',(s[2],s[3]),(s[0],s[1]),(100,100,200))


def creatm(n,m):	
	maplist=[]
	pealist=[]
	for i in range(n):
		maplist.append([0 for j in range(m)])
		pealist.append([1 for j in range(m)])
	stacku=[]
	vis={}
	for i in range(n):
		for j in range(m):
			vis[(i,j)]=0
	count=n*m
	direct=[(1,0),(-1,0),(0,1),(0,-1)]
	def removewall(x,y): # 0000 udlr
		nonlocal maplist
		if x[0]>y[0]:
			maplist[x[0]][x[1]]|=(1<<1)
			maplist[y[0]][y[1]]|=(1<<0)
		elif x[0]<y[0]:
			maplist[x[0]][x[1]]|=(1<<0)
			maplist[y[0]][y[1]]|=(1<<1)
		elif x[1]>y[1]:
			maplist[x[0]][x[1]]|=(1<<3)
			maplist[y[0]][y[1]]|=(1<<2)
		elif x[1]<y[1]:
			maplist[x[0]][x[1]]|=(1<<2)
			maplist[y[0]][y[1]]|=(1<<3)

	vis[(0,0)]=1
	count-=1
	now=(0,0)
	while count>0:
		choicelist=[]
		for i in range(4):
			if 0<=now[0]+direct[i][0]<n and 0<=now[1]+direct[i][1]<m:
				if vis[(now[0]+direct[i][0],now[1]+direct[i][1])]==0:
					choicelist.append((now[0]+direct[i][0],now[1]+direct[i][1]))
		if len(choicelist)!=0:
			choice=choicelist[random.randint(0,len(choicelist)-1)]
			stacku.append(now)
			removewall(now,choice)
			vis[choice]=1
			now=choice
			count-=1
		else:
			now=stacku.pop()
	return public.trans(maplist),pealist


def transm(surf,maplist):
	
	def fxy(i,j,direct):
		if direct=='U':
			return (j*unitw,i*unith)
		elif direct=='D':
			return (j*unitw,(i+1)*unith)
		elif direct=='L':
			return (j*unitw,i*unith)
		elif direct=='R':
			return ((j+1)*unitw,i*unith)
		
	for i in range(len(maplist)):
		for j in range(len(maplist[i])):
			x=public.build(maplist[i][j])
			if x[0]==0:
				wall=Wall(surf,'rec',(unitw+wallw,wallw),fxy(i,j,'U'),(100,100,200))
			if x[1]==0:
				wall=Wall(surf,'rec',(unitw+wallw,wallw),fxy(i,j,'D'),(100,100,200))
			if x[2]==0:
				wall=Wall(surf,'rec',(wallw,unith),fxy(i,j,'L'),(100,100,200))
			if x[3]==0:
				wall=Wall(surf,'rec',(wallw,unith),fxy(i,j,'R'),(100,100,200))
				

def addpea(surf,pealist,is_ghost):
	for i in range(len(pealist)):
		for j in range(len(pealist[i])):
			if pealist[i][j]==1 or (is_ghost == False and pealist[i][j]==2):
				pea=Pea(surf,source.pea_img,(10,10),(j*unitw+12,i*unith+12),4,(i,j))
			elif is_ghost == True and pealist[i][j]==2:
				capsule = Capsule(surf,source.capsule_img,(15,15),(j*unitw+9,i*unith+9),4,(i,j))
				

def limit_pea(peamap, random_list,num):
	temp = []
	for i in range(len(peamap)):
		for j in range(len(peamap[0])):
			if peamap[i][j] == 1 or peamap[i][j] == 2:
				temp.append((i,j))
	#random.shuffle(temp)
	res = [[0 for i in range(len(peamap[0]))] for j in range(len(peamap))]
	
	for i in range(min(len(temp),num)):
		res[temp[random_list[i]][0]][temp[random_list[i]][1]] = 1
	
	for i in range(len(peamap)):
		for j in range(len(peamap[0])):
			if peamap[i][j] == 2:
				res[i][j] = 2
	
	return res
# creatm(15,15)
