# -*- coding: utf-8 -*-
"""
Created on Thu Nov 27 15:47:36 2016

@author: shoma
"""

import numpy as np
import math
import scipy.integrate as integrate
from multiprocessing import Pool
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.pyplot import quiver, subplot, show, figure, axis, title, xlabel, ylabel, plot, xlim, ylim

#constants
c1 = 15.6 #capacitance for C1
c2 = 1.0 #capacitance C2
L = 28.0 #inductance for L1
m0 = -1.143
m1 = -0.714

#x, y, and z initial conditions (actual)
H0 = [0.7, 0.0, 0.0] #Do NOT change this, it could affect the chaotic nature of the system

#Perturbed initial state (change as necessary)
Pert = [0.61, 0.089, 0.078] #[0.603,0.09,-0.09]

#frequency of observation
tfreq = 25

#end time & time step resolution
Tend = 8.0
Tres = 800

#resolution of J
res = 40

#parameters of data assimilation
Q = 0 #no model error
sigma0 = 0.1
sigmaR = 0.1
P0 = np.linalg.inv(np.eye(3)*sigma0**2)
R = np.linalg.inv(np.eye(3)*sigmaR**2)

#defining a non-linear function
def f(x): #This is not the function we want, but we could graph it for fun 
    f = np.sin(x/np.pi)+0.05*x**3
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
t = np.linspace(0, Tend, Tres)

#Noise
NOISE = np.random.uniform(0,sigmaR,Tres)


print('True initial state is:')
print(H0)
print('Frequency of observation is:')
print(tfreq)

H, infodict = integrate.odeint(dH_dt, H0, t, full_output=True)

print infodict['message']

Pertcopy = np.copy(Pert)

#data assimilation
def TL(inputPert, t=0):
    return np.array([c1*(inputPert[1]-inputPert[0]-h(inputPert[0])),
                  c2*(inputPert[0]-inputPert[1]+inputPert[2]),
                  -L*inputPert[1]])    
                                    

#Cost Function
def J(x0input):
    i = tfreq
    t = np.linspace(0, Tend, Tres)
    x0copy = np.copy(x0input)
    x0k, infodict = integrate.odeint(TL, x0input, t, full_output=True)
    SUM = 0.0000
    while (i < Tres):
        SUM = SUM + np.dot(np.transpose(x0k[i,:]-H[i]),np.matmul(R,x0k[i,:]-H[i]+NOISE[i]))
        i = i + tfreq
    return 0.5*np.dot(np.transpose(x0copy-Pertcopy),np.matmul(P0,x0copy-Pertcopy))+0.5*SUM
    #np.dot(np.transpose(Pert[i]-H[i]),np.dot(R,Pert[i]-H[i]))



#some initial conditions
print('Here are some values of the cost function (J) with different initial conditions.')
print('Cost function (J) value with initial conditions [0.7,0,0] (truth) is:')
print(J([0.7,0,0]))
print('Cost function (J) value with initial conditions [0.75,0.1,0] is:')
print(J([0.75,0.1,0]))
print('Cost function (J) value with initial conditions [0.79,0.1,0] is:')
print(J([0.79,0.1,0]))
print('Cost function (J) value with initial conditions [0.9,0.2,0.1] is:')
print(J([0.9,0.2,0.1]))


#Creat an array of possible initial conditions
i = 0
j = 0
k = 0
l = 0
allstates = np.zeros([(res + 1)**3,3])
while (j<res + 1):
    while (k < res + 1):
        while (l < res + 1):
            allstates[i,:] = [Pertcopy[0]-2*sigma0+((4*sigma0)/res)*j,Pertcopy[1]-2*sigma0+((4*sigma0)/res)*k,Pertcopy[2]-2*sigma0+((4*sigma0)/res)*l]
            l = l + 1
            i = i + 1
        
        k = k + 1
        l = 0
    j = j + 1
    k = 0

#Parallel processing to save time    
p = Pool(8)
Jmin = p.map(J, allstates)

minvalue = np.min(Jmin)
minloc = np.argmin(Jmin)

#Some modular math to get back the vector coordinate
x01 = math.floor(minloc/((res+1)**2))
x02 = math.floor((minloc-x01*((res+1)**2))/(res+1))
x03 = math.floor(minloc-((res+1)**2)*(x01)-(res+1)*(x02))
x0 = [Pertcopy[0]-2*sigma0+((4*sigma0)/res)*x01,Pertcopy[1]-2*sigma0+((4*sigma0)/res)*x02,Pertcopy[2]-2*sigma0+((4*sigma0)/res)*x03]
print('The optimized initial condition is:')
print(x0)
print('The cost function at optimized initial condition is:')
print(J(x0))
def optimized(x0, t=0):
    return np.array([c1*(x0[1]-x0[0]-h(x0[0])),
                  c2*(x0[0]-x0[1]+x0[2]),
                  -L*x0[1]])
x0, infodict = integrate.odeint(optimized, x0, t, full_output=True)

delta = np.abs(x0-H)

#3D plot of Chua's Circuit
fig = plt.figure(1,figsize=(16,16))
ax = fig.add_subplot(111, projection='3d')
ax.plot(H[:,0], H[:,1], H[:,2],label='Truth')
ax.plot(x0[:,0], x0[:,1], x0[:,2],label='Estimate')
ax.set_xlabel('Voltage drop on C1')
ax.set_ylabel('Voltage drop on C2')
ax.set_zlabel('Current through L')
plt.title('Chua Circuit Simulation')
plt.legend()


#Plot of V1
fig = plt.figure(2,figsize=(16,16))
plot(t,H[:,0], label="Truth")
plot(t,x0[:,0], label="Estimate")
plot(t,delta[:,0], label="Error")
plt.xlabel('Time')
plt.ylabel('Voltage drop on C1')
plt.title('Voltage drop on C1 vs. Time (Estimate and Truth)')
plt.legend()


#Plot of V2
fig = plt.figure(3,figsize=(16,16))
plot(t,H[:,1], label="Truth")
plot(t,x0[:,1], label="Estimate")
plot(t,delta[:,1], label="Error")
plt.xlabel('Time')
plt.ylabel('Voltage drop on C2')
plt.title('Voltage drop on C2 vs. Time (Estimate and Truth)')
plt.legend()


#Plot of L
fig = plt.figure(4,figsize=(16,16))
plot(t,H[:,2], label="Truth")
plot(t,x0[:,2], label="Estimate")
plot(t,delta[:,2], label="Error")
plt.xlabel('Time')
plt.ylabel('Current through L')
plt.title('Current through L vs. Time (Estimate and Truth)')
plt.legend()








plt.show()

