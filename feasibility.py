import numpy as np
from scipy import optimize
import itertools


o_12 = -1
o_13 = 1
o_23 = 1


A = np.eye(10)
b = np.ones(10)
c = np.ones(10)
bounds = []
for i in range(10):
	bounds.append((None, None))

opt = optimize.linprog(c, A_ub=A, b_ub=b, bounds = bounds ) 



#Inequalities
#	0   1    2    3    4      5    6      7
#[a_1, a_2, a_3, a_4, w_14, w_24, w_34, bias]

# First group
v_000 = np.zeros((2, 8))
v_000[1,3] = 1
v_000[1,4] = 1
v_000[1,5] = 1
v_000[1,6] = 1

u_000 = np.zeros(8)
u_000[7] = 1

b_000 = 0 


#Second group
v_001 = np.zeros((2, 8))
v_001[0,6] = 1


v_001[1,3] = 1
v_001[1,4] = 1
v_001[1,5] = 1


u_001 = np.zeros(8)
u_001[2] = 1
u_001[7] = 1

b_001 = o_13+o_23


#Third Group
v_010 = np.zeros((2,8))
v_010[0,5]  = 1

v_010[1,4] = 1
v_010[1,6] = 1
v_010[1,3] = 1

u_010 = np.zeros(8)
u_010[1] = 1
u_010[7] = 1

b_010 = o_12+o_23



#Fourth Group
v_011 = np.zeros((2,8))
v_011[0,5] = 1
v_011[0,6] = 1

v_011[1,4] = 1
v_011[1,3] = 1

u_011 = np.zeros(8)
u_011[1] = 1
u_011[2] = 1
u_011[7] = 1

b_011 = o_12+o_13



#Fifth Group
v_100 = np.zeros((2,8))
v_100[0,4] = 1

v_100[1,3] = 1
v_100[1,5] = 1
v_100[1,6] = 1

u_100 = np.zeros(8)
u_100[0] = 1
u_100[7] = 1

b_100 = o_12 + o_13



#Sixth group
v_101 = np.zeros((2,8))
v_101[0,4] = 1
v_101[0,6] = 1
v_101[1,5] = 1
v_101[1,3] = 1

u_101 = np.zeros(8)
u_101[0] = 1
u_101[2] = 1
u_101[7] = 1

b_101 = o_12+ o_23


#Seventh group
v_110 = np.zeros((2,8))
v_110[0,4] = 1
v_110[0,5] = 1

v_110[1,6] = 1
v_110[1,3] = 1

u_110 = np.zeros(8)
u_110[0] = 1
u_110[1] = 1
u_110[7] = 1

b_110 = o_13 + o_23

#Inequalities
#	0   1    2    3    4      5    6
#[a_1, a_2, a_3, a_4, w_14, w_24, w_34]

#Eigth group
v_111 = np.zeros((2,8))
v_111[0,4] = 1
v_111[0,5] = 1
v_111[0,6] = 1

v_111[1,3] = 1

u_111 = np.zeros(8)
u_111[0] = 1
u_111[1] = 1
u_111[2] = 1
u_111[7] = 1

b_111 = 0 





signs = [-1,1]
for x in itertools.product(signs, signs, signs, signs, signs, signs, signs, signs):
	A = np.zeros((8, 8))
	b = np.zeros(8)

	bounds = []
	for i in range(8):
		bounds.append((None, None))

	curr_sign = x[0]
	A[0,:] = curr_sign*v_000[0,:] + (-curr_sign)*v_000[1,:]
	

	curr_sign = x[1]
	A[1,:] = curr_sign*v_001[0,:] + (-curr_sign)*v_001[1,:]
	
	curr_sign = x[2]
	A[2,:] = curr_sign*v_010[0,:] + (-curr_sign)*v_010[1,:]
	
	curr_sign = x[3]
	A[3,:] = curr_sign*v_011[0,:] + (-curr_sign)*v_011[1,:]
	
	curr_sign = x[4]
	A[4,:] = curr_sign*v_100[0,:] + (-curr_sign)*v_100[1,:]
	
	curr_sign = x[5]
	A[5,:] = curr_sign*v_101[0,:] + (-curr_sign)*v_101[1,:]
	
	curr_sign = x[6]
	A[6,:] = curr_sign*v_110[0,:] + (-curr_sign)*v_110[1,:]
	
	curr_sign = x[7]
	A[7,:] = curr_sign*v_111[0,:] + (-curr_sign)*v_111[1,:]
	


	### The row with the negative sign is the one achieving a larger objective value
	A_eq = np.zeros((8,8))
	b_eq = np.zeros(8)

	curr_sign = x[0]
	A_eq[0,:] = (curr_sign == -1)*v_000[0,:]   + (-curr_sign == -1 ) *v_000[1,:] -u_000  
	b_eq[0] = b_000

	curr_sign = x[1]
	A_eq[1,:] = (curr_sign == -1)*v_001[0,:]   + (-curr_sign == -1 ) *v_001[1,:] -u_001  
	b_eq[1] = b_001

	curr_sign = x[2]
	A_eq[2,:] = (curr_sign == -1)*v_010[0,:]   + (-curr_sign == -1 ) *v_010[1,:] -u_010  
	b_eq[2] = b_010

	curr_sign = x[3]
	A_eq[3,:] = (curr_sign == -1)*v_011[0,:]   + (-curr_sign == -1 ) *v_011[1,:] -u_011  
	b_eq[3] = b_011

	curr_sign = x[4]
	A_eq[4,:] = (curr_sign == -1)*v_100[0,:]   + (-curr_sign == -1 ) *v_100[1,:] -u_100  
	b_eq[4] = b_100

	curr_sign = x[5]
	A_eq[5,:] = (curr_sign == -1)*v_101[0,:]   + (-curr_sign == -1 ) *v_101[1,:] -u_101  
	b_eq[5] = b_101

	curr_sign = x[6]
	A_eq[6,:] = (curr_sign == -1)*v_110[0,:]   + (-curr_sign == -1 ) *v_110[1,:] -u_110  
	b_eq[6] = b_110

	curr_sign = x[7]
	A_eq[7,:] = (curr_sign == -1)*v_111[0,:]   + (-curr_sign == -1 ) *v_111[1,:] -u_111  
	b_eq[7] = b_111


	#UUU = np.dot(A_eq, A_eq.transpose())
	## build A
	#print(np.linalg.eig(UUU)[0])

	c = np.ones(8)
	opt = optimize.linprog(c, A_ub=A, b_ub=b, A_eq = A_eq, b_eq = b_eq, bounds = bounds ) 
	
	if opt.status != 2:
		
		print(opt)
	#print(opt.status)


