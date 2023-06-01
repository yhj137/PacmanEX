def build(x):
	a=[0,0,0,0]
	i=3
	while x>0:
		a[i]=x%2
		i-=1
		x=x//2
	return tuple(a)
	
def trans(matrix):
	matrix=list(zip(*matrix))
	for i in range(len(matrix)):
		matrix[i]=list(matrix[i])
	return matrix