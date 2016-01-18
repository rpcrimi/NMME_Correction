import matplotlib

def xn_vs_n(R, xo, m):
	n = [i for i in range(m)]
	xn = [xo]
	for i in range(m):
		xn.append(R*xn[i-1]*(1-xn[i-1]))

	print n
	print xn

xn_vs_n(0.5, 0.2, 3)