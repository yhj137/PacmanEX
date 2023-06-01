
def trans(x):
	n=29
	m=26
	maplist=[]
	res=x
	for i in range(n):
		s=[[1,1,1,1] for j in range(m)]
		maplist.append(s)
	for i in range(n):
		maplist[i][0][2]=0
		maplist[i][m-1][3]=0
	for i in range(m):
		maplist[0][i][0]=0
		maplist[n-1][i][1]=0
	
	for i in range(n):
		for j in range(m):
			if x[i][j]=='1':
				maplist[i][j]=[0,0,0,0]
				if i+1<n:
					maplist[i+1][j][0]=0
				if i-1>=0:
					maplist[i-1][j][1]=0
				if j+1<m:
					maplist[i][j+1][2]=0
				if j-1<m:
					maplist[i][j-1][3]=0
	
	for i in range(n):
		for j in range(m-1):	
			if x[i][j]=='1' and x[i][j+1]=='1':
				maplist[i][j][3]=1
				maplist[i][j+1][2]=1
	
	for j in range(m):
		for i in range(n-1):
			if x[i][j]=='1' and x[i+1][j]=='1':
				maplist[i][j][1]=1
				maplist[i+1][j][0]=1
	
	for i in range(n):
		for j in range(m):
			res[i][j]=maplist[i][j][0]*8+maplist[i][j][1]*4+maplist[i][j][2]*2+maplist[i][j][3]*1
	
	return res
	

x=[]
z=[]
for i in range(29):
	s= list(input().split())
	x.append(s)
	z.append([])
for i in range(29):
	for j in range(26):
		z[i].append(1 if x[i][j]=='0' else 0)

y=trans(x)
for i in range(29):
	print('{},\\'.format(y[i]))

for i in range(29):
	print('{},\\'.format(z[i]))