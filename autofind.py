import public
import source
from queue import Queue,PriorityQueue

class AutoFind():
	def __init__(self, pacman):
		self.pacman = pacman
		self.map = {}
		self.pea = []
		self.target_point = (0,0)
		self.temp_path = []
		self.dis = {}
    
	def loadmap(self, map, pea, gh = True):
		def bfs(x):
			s = Queue(maxsize = 0)
			s.put((x,0))
			vis = {}
			vis[x] = 1
			while s.empty() == False:
				now = s.get()
				self.dis[(x,now[0])] = now[1]
				for i in range(4):
					if self.map[now[0]][i] != 0 and self.map[now[0]][i] not in vis.keys():
						s.put((self.map[now[0]][i],now[1]+1))
						vis[self.map[now[0]][i]] = 1			
		self.pea = []
		self.map = {}
		self.target_point = (0,0)
		self.temp_path = []
		for i in range(len(map)):
			for j in range(len(map[0])):
				temp = [0,0,0,0]
				x = public.build(map[i][j])
				if x[0] == 1 and i>0:
					temp[0] = (j,i-1)
				if x[1] == 1 and i<len(map)-1:
					temp[1] = (j,i+1)
				if x[2] == 1 and j>0:
					temp[2] = (j-1,i)
				if x[3] == 1 and j<len(map[0])-1:
					temp[3] = (j+1,i)
				self.map[(j,i)] = tuple(temp)
		
		for i in range(len(pea)):
			for j in range(len(pea[0])):
				if pea[i][j] == 1 or (pea[i][j] == 2 and gh == False):
					self.pea.append((j,i))
		for i in range(len(map)):
			for j in range(len(map[0])):		
				bfs((j,i))
	
	def _bfs(self, x, y):
		s = Queue(maxsize = 0)
		s.put(x)
		vis = {}
		vis[x] = (-1,-1)
		while s.empty() == False:
			now = s.get()
			if now == y:
				break
			for i in range(4):
				if self.map[now][i] != 0 and self.map[now][i] not in vis.keys():
					s.put(self.map[now][i])
					vis[self.map[now][i]]=now
		t = y
		res = []
		while t!=(-1,-1):
			res.insert(0,t)
			t = vis[t]
		return res[1:]
	
	def greedy_search(self):
		def bfs(x):
			s = Queue(maxsize = 0)
			s.put(x)
			vis = {}
			vis[x] = 1
			fx = [(0,1),(1,0),(-1,0),(0,-1)]
			cnt = 0
			while s.empty() == False:
				now = s.get()
				cnt += 1
				for i in range(4):
					if (now[0]+fx[i][0],now[1]+fx[i][1]) in self.pea and (now[0]+fx[i][0],now[1]+fx[i][1]) not in vis.keys():
						s.put((now[0]+fx[i][0],now[1]+fx[i][1]))
						vis[(now[0]+fx[i][0],now[1]+fx[i][1])] = 1
			return cnt
			
		if len(self.pea) == 0:
			return (0,0)
		x = self.pacman.unitz[0]
		y = self.pacman.unitz[1]
		minn = (self.pea[0],self.dis[((x,y),self.pea[0])])
		for i in self.pea:
			if self.dis[((x,y),i)] < minn[1]:
				minn = (i,self.dis[((x,y),i)])
		minnn = (minn[0],bfs(minn[0]))
		for i in self.pea:
			if self.dis[((x,y),i)] == minn[1]:
				temp = bfs(i)
				if temp < minnn[1]:
					minnn = (i,temp)
		#return minn[0]
		return minnn[0]
	
	def dfs_search(self):
		cnt = len(self.pea)
		path = []
		flag = 0
		vis = {i:0 for i in self.pea}
		v = []
		def dfs(x):
			nonlocal cnt,path,flag
			if cnt == 0:
				flag = 1
				return
			for i in range(4):
				if self.map[x][i]!=0 and (self.map[x][i], cnt) not in v:
					v.append((self.map[x][i], cnt))
					path.append(self.map[x][i])
					tempflag = 0
					if self.map[x][i] in self.pea and vis[self.map[x][i]] == 0:
						cnt -=1
						vis[self.map[x][i]] = 1
						tempflag = 1
					dfs(self.map[x][i])
					if flag == 1:
						return
					if tempflag == 1:
						cnt +=1
						vis[self.map[x][i]] = 0
					del path[-1]
		dfs(tuple(self.pacman.unitz))
		#print(path)
		return path
	
	def bfs_search(self):
		s = Queue(maxsize = 0)
		s.put((tuple(self.pacman.unitz),tuple(False for i in range(len(self.pea)))))
		vis = {}
		vis[(tuple(self.pacman.unitz),tuple(False for i in range(len(self.pea))))] = ((-1,-1), 0)
		y = ((-1,-1),0)
		pea_bh = {}
		cnt = 0
		for i in self.pea:
			pea_bh[i] = cnt
			cnt += 1
		test  = 0
		while s.empty() == False:
			now = s.get()
			test += 1
			#print(now)
			if all(now[1]) == True:
				y = now
				break
			for i in range(4):
				if self.map[now[0]][i] != 0:
					temp = list(now[1])
					if self.map[now[0]][i] in self.pea:
						temp[pea_bh[self.map[now[0]][i]]] = True
					if (self.map[now[0]][i], tuple(temp)) not in vis.keys():
						s.put((self.map[now[0]][i], tuple(temp)))
						vis[(self.map[now[0]][i], tuple(temp))] = now
		t = y
		res = []
		while t != ((-1,-1), 0):
			res.insert(0,t[0])
			t = vis[t]
		#print(test,len(res))
		return res[1:]
	
	def dp_search(self):
		n = len(self.pea)
		if n == 0:
			return []
		dp = {}
		dis = {}
		path_table = {}
		for i in range(n):
			path_table[(-1,i)] = self._bfs(tuple(self.pacman.unitz),self.pea[i])
		for i in range(n):
			for j in range(n):
				path_table[(i,j)] = self._bfs(self.pea[i],self.pea[j])
				dis[(i,j)] = len(path_table[(i,j)])
		for i in range(2**n):
			for j in range(n):
				dp[(j,i)] = (((-1,-1),0),99999999)
		for j in range(n):
			dp[(j,1<<j)] = (((-1,-1),-1),len(path_table[(-1,j)]))
		for i in range(2**n):
			for j in range(n):
				
				if i&(1<<j) != 1<<j:
					continue
				
				for k in range(n):
					if j == k:
						continue
					if dp[(j,i)][1] > dp[(k,i^(1<<j))][1] + dis[(k,j)]:
						dp[(j,i)]=((k,i^(1<<j)),dp[(k,i^(1<<j))][1] + dis[(k,j)])
		
		minn = (((-1,-1),-1),-1)
		e = (-1,-1)
		for j in range(n):
			if minn[1] == -1 or minn[1] > dp[(j,2**n-1)][1]:
				minn = dp[(j,2**n-1)]
				e = j
		point = [e]
		while minn[0]!=((-1,-1),-1):
			#print(minn)
			point.insert(0, minn[0][0])
			minn = dp[minn[0]]
		res = []
		
		for i in path_table[(-1,point[0])]:
			res.append(i)
		for j in range(len(point)-1):
			for i in path_table[(point[j],point[j+1])]:
				res.append(i)
		#print(res)
		return res
	
	def a_star_search(self):
		
		dis = {}
				
		def h(now, x):
			nonlocal dis
			cnt = []
			minn = 9999999
			minnn = 9999999
			for i in range(len(x)):
				if x[i] == False:
					cnt.append(i)
		
			for i in cnt:
				minn = min(minn,self.dis[(now,self.pea[i])])
			
			if x in dis:
				return min(dis[x], minn) * len(cnt)
			for i in cnt:
				for j in cnt:
					if i != j:
						minnn = min(minnn, self.dis[(self.pea[i],self.pea[j])])
			dis[x] = minnn
			return len(cnt) * min(minn,minnn)
		
		s = PriorityQueue(maxsize = 0)
		s.put((0,(tuple(self.pacman.unitz),tuple(False for i in range(len(self.pea))))))
		dis = {}
		dis[(tuple(self.pacman.unitz),tuple(False for i in range(len(self.pea))))] = 0
		pre = {}
		pre[(tuple(self.pacman.unitz),tuple(False for i in range(len(self.pea))))] = None
		pea_bh = {}
		cnt = 0
		y = None
		for i in self.pea:
			pea_bh[i] = cnt
			cnt += 1
		test = 0
		while s.empty() == False:
			now = s.get()
			test += 1
			if all(now[1][1]) == True:
				y = now[1]
				break
			for i in range(4):
				if self.map[now[1][0]][i] != 0:
					temp = list(now[1][1])
					if self.map[now[1][0]][i] in self.pea:
						temp[pea_bh[self.map[now[1][0]][i]]] = True
					nex = (self.map[now[1][0]][i],tuple(temp))
					new_cost = dis[now[1]] + 1
					if nex not in dis.keys() or new_cost < dis[nex]:
						dis[nex] = new_cost
						s.put((dis[nex]+h(nex[0],nex[1]),nex))
						pre[nex] = now[1]
		res = []
		while y != None:
			res.insert(0,y[0])
			y = pre[y]
		#print(test,len(res))
		return res[1:]
						
	def greedy_search2(self):
		def h(x):
			cnt = 0
			for i in x:
				if i == False:
					cnt +=1000
			return cnt
			
		s = PriorityQueue(maxsize = 0)
		s.put((0,(tuple(self.pacman.unitz),tuple(False for i in range(len(self.pea))))))
		dis = {}
		dis[(tuple(self.pacman.unitz),tuple(False for i in range(len(self.pea))))] = 0
		pre = {}
		pre[(tuple(self.pacman.unitz),tuple(False for i in range(len(self.pea))))] = None
		pea_bh = {}
		cnt = 0
		y = None
		for i in self.pea:
			pea_bh[i] = cnt
			cnt += 1
		test = 0
		while s.empty() == False:
			now = s.get()
			test += 1
			if all(now[1][1]) == True:
				y = now[1]
				break
			for i in range(4):
				if self.map[now[1][0]][i] != 0:
					temp = list(now[1][1])
					if self.map[now[1][0]][i] in self.pea:
						temp[pea_bh[self.map[now[1][0]][i]]] = True
					nex = (self.map[now[1][0]][i],tuple(temp))
					new_cost = dis[now[1]] + 1
					if nex not in dis.keys() or new_cost < dis[nex]:
						dis[nex] = new_cost
						s.put((dis[nex]+h(nex[1]),nex))
						pre[nex] = now[1]
		res = []
		while y != None:
			res.insert(0,y[0])
			y = pre[y]
		#print(test,len(res))
		#print(res[1:])
		return res[1:]	
	
	def return_path(self,x,y):
		return y
	
	def findway(self, select_point, create_path = None):
		if create_path == None:
			create_path = self._bfs
		if self.pacman.next_step_flag == 1 and len(self.temp_path) == 0:
			self.target_point = select_point()
			self.temp_path = create_path(tuple(self.pacman.unitz),self.target_point)
			# print(len(self.temp_path))
		
		if self.pacman.next_step_flag == 1 and len(self.temp_path) > 0:
			#print(self.temp_path[0],self.pacman.unitz)
			if self.pacman.unitz[0] < self.temp_path[0][0]:
				self.pacman.direct = "R"
			elif self.pacman.unitz[0] > self.temp_path[0][0]:
				self.pacman.direct = "L"
			elif self.pacman.unitz[1] < self.temp_path[0][1]:
				self.pacman.direct = "D"
			elif self.pacman.unitz[1] > self.temp_path[0][1]:
				self.pacman.direct = "U"
			self.temp_path = self.temp_path[1:]
			self.pacman.next_step_flag = 0
			
#a = AutoFind(None)
#a.loadmap(source.classic_map1[0],source.classic_map1[2])
#print(a._bfs((0,0),(2,2)))
# print(a.map)
# print(a.pea)