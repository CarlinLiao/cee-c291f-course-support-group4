# -*- coding: utf-8 -*-
"""
Created on Wed Oct 04 20:28:59 2017

@author: Rob Ruigrok
"""

# This file will model/simulate the random motion

import numpy as np
from random import *
#from matplotlib import mpl,pyplot
import pylab

###############################################################################
########################## START INPUT ########################################
###############################################################################

N = 10
x_grid = N                 #define the size of your grid. There will be walls around the box
y_grid = N
Pos_init = np.array([int(N/3),int(N/3)])  #define starting position
T = int(.1*N*N)                      #this is the total amount of time steps
Plot_interval = 10;          #This determines when you take snapshots of the proces, every "Plot_interval" timesteps
n_particles = 1000         # amount of particles. 10000+ gives a nice distribution
subplot_row = 2             # define the amount of subplots that you like
subplot_column = 2
motion_prob = np.array([0.2,0.2,0.2,0.2,0.2])   #defines the probabilities for drift: ([up,right,down,left,no motion]) 

###############################################################################
########################## END INPUT ##########################################
###############################################################################


n_subplot = subplot_row*subplot_column;
# now define the probabilities of the random walk
# notation of motion ([up,right,down,left,no motion])
motion_prob = motion_prob/np.sum(motion_prob)   #normalize in case probabilities do not add up to 1...
motion_xy = np.array([[0,1],[1,0],[0,-1],[-1,0],[0,0],])
motion_prob_percentile = np.cumsum(motion_prob)
#print motion_prob_percentile

# this is where we should make the a massive loop to simulate 1000000 particles
# make an empty data grid from where you are going to count the amount occurances and hits against the wall
Data = np.zeros((x_grid+2,y_grid+2)) #be careful with x-y being row-column here
Data_resized = np.zeros((Data.shape[0]+1,Data.shape[1]+1))  #only for plotting purposes
Data_TimeVarying = np.zeros((n_subplot,Data_resized.shape[0],Data_resized.shape[1]))    #for subplots
# prepare some arrays for later plotting (not in loop for speed)
xx, yy = pylab.meshgrid(
    pylab.linspace(-1,x_grid+1,x_grid+3),
    pylab.linspace(-1,y_grid+1,y_grid+3))

for i in range(1, n_particles+1):
    # Initialize simulation
    t = 0
    HitWall = False
    Pos = Pos_init
    Subplot = 1
    
    # start simulation
    while t < T and not HitWall:
        
        # Now continue with the motion simulation
        MotionRandom = random()
        IndexMotion = np.argmax(motion_prob_percentile>MotionRandom)
        Pos = Pos + motion_xy[IndexMotion,:] #this works
          
        # Now record the position for time dependent plotting purposes
        if t % Plot_interval == 0 and Subplot <= n_subplot:   #so create a subplot every Plot_interval time steps
            Data_TimeVarying[Subplot-1,Pos[0],Pos[1]] = Data_TimeVarying[Subplot-1,Pos[0],Pos[1]]+1
            Subplot = Subplot+1
        
        # Now check for hitting the wall
        if Pos[0] == 0 or Pos[1] == 0 or Pos[0] == x_grid+1 or Pos[1] == y_grid+1:
            #Data_TimeVarying[Subplot-1,Pos[0],Pos[1]] = Data_TimeVarying[Subplot,Pos[0],Pos[1]]+1
            HitWall = True
        t = t+1
    
    
    #This was basically the whole simulation, now save the results
    Data[Pos[0],Pos[1]] = Data[Pos[0],Pos[1]] + 1
    # I need to give resize Data with an extra row and column, since pcolor doesn't plot the full range of the matrix...
    Data_resized[:-1,:-1] = Data       

# this part was for some debugging, but I can't get the 3d indexing right to get the data for the wall crossings out
'''print 'this are the old values vvv'
print np.round(Data_TimeVarying)
print 'test, what is the Old data [1][1:x_grid][1:y_grid]'
print Data_TimeVarying[0:2][1:x_grid][1:y_grid]
Data_TimeVarying_cumsum = np.cumsum(Data_TimeVarying,axis=0)
print 'this are the cumsum values before replacing center vvv'
print Data_TimeVarying_cumsum
Data_TimeVarying_cumsum[:][1:x_grid][1:y_grid] = Data_TimeVarying[:][1:x_grid][1:y_grid]
print 'this are the cumsum after replacing values vvv'
print Data_TimeVarying_cumsum
print 'this are the final (good) values vvv'
print Data_resized'''

# In these time-dependent plot, I did not manage to include distribution in hitting the walls
for j in range(1, n_subplot+1):
    #Now visualize the outcomes
    pylab.subplot(subplot_row, subplot_column, j)
    pylab.pcolor(xx,yy,np.transpose(Data_TimeVarying[j-1,:,:]))
    TitleString = 'Distribution at t = ' + str((j-1)*Plot_interval)
    pylab.title(TitleString)
    # and a color bar to show the correspondence between function value and color
    pylab.colorbar()
    pylab.hold(True)
    pylab.plot([0, x_grid],[0, 0], 'r',[0, x_grid],[y_grid, y_grid], 'r',[0, 0],[0, y_grid], 'r',[x_grid, x_grid],[0, y_grid], 'r')
    pylab.plot(Pos_init[0]-0.5,Pos_init[1]-0.5,'ro')

pylab.show()

# This plot shows the final distribution, including distribution along the walls
pylab.pcolor(xx,yy,np.transpose(Data_resized))
pylab.title('Final distribution, including hitting walls')
# and a color bar to show the correspondence between function value and color
pylab.colorbar()
pylab.hold(True)
pylab.plot([0, x_grid],[0, 0], 'r',[0, x_grid],[y_grid, y_grid], 'r',[0, 0],[0, y_grid], 'r',[x_grid, x_grid],[0, y_grid], 'r')
pylab.plot(Pos_init[0]-0.5,Pos_init[1]-0.5,'ro')
pylab.show

    
    
    
    
    