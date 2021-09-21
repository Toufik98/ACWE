# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 05:40:17 2021

@author: Ferhat Toufik 

@author: Dagmoune Asma 


"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import scipy.ndimage as nd

def acwe(Img, phi0, max_iter, time_step, mu, v, lambda1, lambda2, epsilon):
    """
    Input:
	    Img: array_like, the input gray image[0,255]
	    phi: nparray, the initial curve function(level set function)
	    max_iter: int, the max number of iterations
	    time_step: float, learning rate
	    mu: coefficiency of  length term
	    v: coefficiency of  area term 
	    lambda1, lambda2: coefficiency of "fitting" term(Image energy)	
    """
    print(time_step, mu, v, lambda1, lambda2)
    phi = phi0

    plt.ion()
    fig, axes = plt.subplots(ncols=2)
    show_curve_and_phi(fig, Img, phi0, 'r')
    plt.savefig('levelset_start.png', bbox_inches='tight')

	
    for iter in range(max_iter):
        
        print('iteration: {0}'.format(iter))
        if np.mod(iter, 1) == 0:
            show_curve_and_phi(fig, Img, phi, 'r')

        #Applying boundary conditions
        phi = NeumannBoundCond(phi)

            
        delta = (epsilon/np.pi) / (epsilon**2 + phi ** 2)
            """
            Only update the neighbor of curve
            """
        #Internal force
        length_term = curvature_central(phi)
        print("delta:{}".format(np.max(delta)))
        print ("length term:{}".format(np.max(length_term)))

        #Image force
        inside_idx = np.flatnonzero(phi >= 0)
        outside_idx = np.flatnonzero(phi < 0)		
        
        #mean value inside curve
        c1 = np.sum(Img.flat[inside_idx]) / (len(inside_idx) + 0.00001)  # exterior mean
        #mean value outside curve
        c2 = np.sum(Img.flat[outside_idx]) / (len(outside_idx) + 0.00001)  # interior mean

        print( "c1:{}, c2:{}".format(c1, c2))
            
        image_force =  - lambda1 * (Img.flat[idx] - c1)**2  + lambda2 * (Img.flat[idx] - c2)**2
        print ("image_force", np.max(image_force))
        #PDE resolution
        partial_phi = delta.flat[idx] * (mu * length_term.flat[idx] - v + image_force / np.max(image_force))	
            
        phi.flat[idx]= time_step * partial_phi
        print("phi:{}".format(np.max(phi)))
        print(phi)
    plt.savefig("levelset_end", bbox_inches='tight')


def NeumannBoundCond(f):
    """
    Change function f to satisfy Neumann Boundary Condition
    """
    g = f
    #4 corner
    g[0, 0] = g[2, 2]
    g[0, -1] = g[2, -3]
    g[-1, 0] = g[-3, 2]
    g[-1, -1] = g[-3, -3]
    #first row and last row
    g[0, 1:-1] = g[2, 1:-1]
    g[-1, 1:-1] = g[-3, 1:-1]
    #first column and last column
    g[1:-1, 0] = g[1:-1, 2]
    g[1:-1, -1] = g[1:-1, -3]
    return g

def curvature_central(phi):
    """
    Compute divergence in equation(9) by definition of divergence rather the discretization of divergence mentioned in paper.
    """
    #gradient of phi 
    phi_x, phi_y = gradient(phi)
   
    #Norm of phi
    norm_gradient = np.sqrt(phi_x ** 2 + phi_y ** 2 + 1e-10)

    #return the divergence
    nxx, _ = gradient(phi_x / norm_gradient)
    _, nyy = gradient(phi_y / norm_gradient)
    return (nxx+nyy)

def gradient(f):
    """
    Compute gradient of f.
    Input:
	    f: array_like.
    Output:
	    fx:  fx[i, j] = (f[i, j+1] - f[i, j-1]) / 2, special in boundary
	    fy:  fy[i, j] = (f[i+1, j] - f[i-1, j]) / 2
    """		
    fx = f
    fy = f
    n, m = f.shape
    fx[:, 0] = f[:, 1] - f[:, 0]
    fx[:, -1] = f[:, -1] - f[:, -2]
    fy[0, :] = f[1,:] - f[0,:]
    fy[-1, :] = f[-1,:] - f[-2,:]
    for j in range(1, m-1):
	    fx[:, j] = (f[:, j+1] - f[:, j-1]) / 2.0
    for i in range(1, n-1):
	    fy[i, :] = (f[i+1, :] - f[i-1, :]) / 2.0
    return fx, fy

# Displays the image with curve superimposed
def show_curve_and_phi(fig, Img, phi, color):
    fig.axes[0].cla()
    fig.axes[0].imshow(Img, cmap='gray')
    fig.axes[0].contour(phi, 0, colors=color)
    fig.axes[0].set_axis_off()
    #plt.draw()

    fig.axes[1].cla()
    fig.axes[1].imshow(phi)
    fig.axes[1].set_axis_off()
    #plt.draw()

    plt.pause(0.001)

#We initialize the first curve
def initialize(width, height, x_center, y_center, radius):
    phi = np.zeros((height, width))
    for i in range(height):
	    for j in range(width):
		    phi[i,j] = -np.sqrt((i - y_center)**2 + (j - x_center)**2) +radius
    return phi
	
if __name__ == "__main__":

    img = Image.open("Images_TP/rondeldent.tif").convert("L")
    #initialize phi
    width, height = img.size
    phi0 = initialize(width, height, x_center=100, y_center=50, radius=45)
    print("phi0:", phi0)
    print ("index of 0:", np.flatnonzero(np.array(img)==0))

    #We display the first contour with the image and the level set function

    fig, axes = plt.subplots(ncols=2)
    axes[0].imshow(img, cmap='gray')
    axes[1].imshow(phi0)
    plt.show()
    
    # We call the function tha implements The Vese Chan algorithm
    acwe(np.array(img), phi0, max_iter=100, time_step=0.1, mu=0, v=0, lambda1=1, lambda2=1, epsilon=1)