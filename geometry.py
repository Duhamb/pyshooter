import math

def distance(p1, p2):
	total = 0
	for i in range(len(p1)):
		total += (p1[i] - p2[i])**2
	return total **(1/2)
	
def distance2(a, b, c, d):
	return 	math.sqrt (( a - c )*( a - c ) + ( b - d )*( b - d ) )
	
def findangle( q, w, e, r ): #angle a to b
	return math.pi + math.atan2( (q - e), (w - r) )


