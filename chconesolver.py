""" Solves 1D CH equation using cone construction

    :param eps: Sinkhorn regularisation paramter
    :param K: Number of time steps
    :param N: Number of cells in domain
    :param L: Length of domain
"""
import sys
import multimarg_fluids as mm
import numpy as np
import time as time
import matplotlib.pyplot as plt


load_flag = True 
inputpath = 'Figs/Testpeakoncont'

if load_flag:
    sys.path.append(inputpath)
    from logfile import *
else:    
    Nx = 40 #28#35 
    Nr = 41
    K = 16
    eps = 0.005
    rmin =0.05
    rmax= 2.05


# Parameters for cone metric
a = 1.0
b= 0.5
L = 1.0
h = L/Nx

X0 = np.linspace(0.0,L,Nx)
#X1 = np.asarray([1.0]) 

X1 =np.linspace(rmin,rmax,Nr)
X0m,X1m = np.meshgrid(X0,X1)
X =[X0m,X1m]

# Marginal using x1 = arctan(r) change of variable
nu = h*np.ones(Nx) 


log_flag = False 

Xi0init = mm.generateinitcostcone(X0,X,a,b,eps, log_flag=log_flag)
Xi0 = mm.generatecostcone(X,X,a,b,eps, log_flag=log_flag)
Xi1 = mm.generatecouplingcone(X,X0,mm.peakon, mm.peakondet,a,b,eps)
#Xi1 = mm.generatecouplingcone(X,X0,mm.S,1.0,a,b,eps,log_flag=log_flag)


# Alternate coupling assignment via permuation (odd N)
#sigma = np.concatenate((np.arange(0,N,2),np.arange(N-2,0,-2)),axis=0)
#Xi1 = mm.generatecost(X,X[sigma],eps*0.1)

# Lagrange multiplier matrix 
if load_flag:
    PMAT = np.load('%s/%s' %(inputpath,"PMAT.npy"))
    errv = np.load('%s/%s' %(inputpath,"errv.npy"))
    errv = errv.tolist()
    
else: 
    PMAT = np.zeros([K,Nx])
    errv = []
    


G = [Xi0init,Xi0,Xi1]

# STANDARD ITERATION METHOD
for ii in range(5000):
    t = time.time()
    PMAT, err = mm.fixedpointconeroll(PMAT,G,X1,nu,verbose= False)
    #PMAT, err, S = mm.fixedpointconerollback(PMAT,S,G,X1,nu)
    errv.append(err)
    elaps= time.time()-t
    print("ITERATION %d" % ii)
    print("Elapsed time: %f" % elaps)
    print("Marginal error: %f" % err)


# ANDERSON ITERATION METHOD
#params = [G,X1,nu]
#iterations_simple = 50
#iterations_anderson = 350 #43#400#60 
#number_of_steps = 1 
#memory_number = 10 #40 
#
#PMAT, errv1 = mm.OptimizationAndersonMixed(mm.fixedpointconeroll,PMAT, iterations_simple,iterations_anderson,number_of_steps,memory_number,params)
#errv += errv1 

path = "Figs/Testpeakoncont1"
mm.savefigscone(errv,PMAT, X1, eps ,G, path , ext='eps')
mm.savedatacone(errv,PMAT,X1,eps, path)

#fig = plt.semilogy(errv)
#plt.savefig(('Figs/Convergence.eps' %k_map),format = "eps")
# 
#
#for k_map in range(K):
#    Tmap = mm.computetransportcone(PMAT,k_map,X1,G,conedensity_flag = False, log_flag=log_flag)
#    fig = plt.imshow(-30*Tmap,origin='lower',cmap = 'gray')
#    fig.axes.get_xaxis().set_visible(False)
#    fig.axes.get_yaxis().set_visible(False)
#    plt.savefig(('Figs/transport0_%d.eps' %k_map),format = "eps")
#    Tconemap = mm.computetransportcone(PMAT,k_map,X1,G,conedensity_flag=True, log_flag=log_flag)
#    fig = plt.imshow(-30*Tconemap,origin='lower',cmap = 'gray')
#    fig.axes.get_xaxis().set_visible(False)
#    fig.axes.get_yaxis().set_visible(False)
#    plt.savefig(('Figs/radialmarg0_%d.eps' %k_map),format = "eps")
#
#
