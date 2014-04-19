# Oscar Rubio Pons, oscar.rubio.pons@gmail.com
# 23 Oct 2013, Hamburg, Germany
# -----------------------------------------------------------------------------


import numpy as np

def RK4(y_0, n, h):
    #4th order Runge-Kutta solver, takes as input
    #initial value y_0, the number of steps n and stepsize h
    #returns solution vector y and time vector t
    #right now function f is defined below

    t = np.linspace(0,n*h,n,endpoint = False)   #create time vector t
    y = np.zeros((n,len(y_0))) #create solution vector y
    y[0] = y_0 #assign initial value to first position in y
    for i in range(0,n-1):
        #compute Runge-Kutta weights k_1 till k_4
        k_1 = f(t[i],y[i])
        k_2 = f(t[i] + 0.5*h, y[i] + 0.5*h*k_1)
        k_3 = f(t[i] + 0.5*h, y[i] + 0.5*h*k_2)
        k_4 = f(t[i] + 0.5*h, y[i] + h*k_3)
        #compute next y        
        y[i+1] = y[i] + h / 6. * (k_1 + 2.*k_2 + 2.*k_3 + k_4)
    return t,y

def f(t,vec):
    theta=vec[0]
    omega = vec[1]
    omegaDot = -np.sin(theta) - omega + np.cos(t)
    result = np.array([omega,omegaDot])    
    return result

test = np.array([0,0.5])
t,y = RK4(test,10,0.1)
print t,y
