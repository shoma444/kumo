# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 13:47:36 2016

@author: shoma
"""

import numpy as np
import scipy.integrate as integrate
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#constants
c1 = 15.6 #capacitance for C1
c2 = 1.0 #capacitance C2
L = 28.0 #inductance for L1
m0 = -1.143
m1 = -0.714

#defining a non-linear function
def f(x):
    f = m1*x+(m0-m1)/2.0*(abs(x+1.0)-abs(x-1.0))
    return f
    
def h(x):
    if (x<=-1):
      f = m1*(x+1)-m0
    elif(-1<x<=1):
      f = m0*x
    elif (x>1):
      f = m1*(x-1)+m0
    return f   

#integrating using ODEint
def dH_dt(H, t=0):
    return np.array([c1*(H[1]-H[0]-h(H[0])),
                  c2*(H[0]-H[1]+H[2]),
                  -L*H[1]])

#time steps
t = np.linspace(0, 20, 2000)

#x, y, and z initial conditions
H0 = [0.7, 0.0, 0.0]

H, infodict = integrate.odeint(dH_dt, H0, t, full_output=True)

print infodict['message']

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(H[:,0], H[:,1], H[:,2])
ax.set_xlabel('Voltage drop on C1')
ax.set_ylabel('Voltage drop on C2')
ax.set_zlabel('Current through L1')
plt.title('Chua Circuit Simulation')
plt.show()

