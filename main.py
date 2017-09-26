from pylab import *
import numpy as np
import matplotlib.cbook as cbook
import random
import time
from scipy.misc import imread
from scipy.misc import imresize
import matplotlib.image as mpimg
import os
from scipy.ndimage import filters
import urllib
from scipy.misc import toimage
gray()

# Please change to the directory containing the images being used
os.chdir('###')

def find_alpha_fg(bg1, bg2, cp1, cp2):
    
    cp_bg = zeros([6,1])
    
    matrix = zeros([6, 4])
    matrix[0][0] = 1
    matrix[1][1] = 1
    matrix[2][2] = 1
    matrix[3][0] = 1
    matrix[4][1] = 1
    matrix[5][2] = 1
    
    f_red = zeros([bg1.shape[0],bg1.shape[1]])
    f_blue = zeros([bg1.shape[0],bg1.shape[1]]) 
    f_green = zeros([bg1.shape[0],bg1.shape[1]]) 
    alpha = zeros([bg1.shape[0],bg1.shape[1]])
    
    for i in range(bg1.shape[0]):
        if i%20 == 0:
            print(str(bg1.shape[0] - i) + ' pixels left')
        for j in range(bg1.shape[1]):
            for l in range(3):
                matrix[l][3] = -bg1[i][j][l]
                cp_bg[l] = cp1[i][j][l] - bg1[i][j][l]
            for l in range(3):
                matrix[3+l][3] = -bg2[i][j][l]
                cp_bg[3+l] = cp2[i][j][l] - bg2[i][j][l]
                
            result = dot(linalg.pinv(matrix),cp_bg)
            
            result = np.clip(result, 0, 1)
                
            alpha[i][j] = result[3]

            f_red[i][j] = result[0]
            f_green[i][j] = result[1]
            f_blue[i][j] = result[2]
    
    fg = zeros([bg1.shape[0],bg1.shape[1],3])
    
    fg[:,:,0] = f_red
    fg[:,:,1] = f_green
    fg[:,:,2] = f_blue
    
    return [alpha, fg]
    
def create_composite(alpha, fg, bg):
    """
    Create a composite image given images of a background, a foreground, and                                     an alpha layer corresponding to the transparency of the background (all of the same dimensions).
    """
    dims = (bg.shape[0], bg.shape[1], 3)
    
    clr_alpha = np.dstack((alpha, alpha, alpha))
    print clr_alpha.shape
    
    comp = fg + (1 - clr_alpha) * bg

    return comp
 
c_bg1 = imread('leaves-backA.jpg')/255.0
c_cp1 = imread('leaves-compA.jpg')/255.0
c_bg2 = imread('leaves-backB.jpg')/255.0
c_cp2 = imread('leaves-compB.jpg')/255.0

# Alphas and Foregrounds

print('\nFinding alpha and foreground ...')


        
#LEAVES
print('Leaves:')

alpha_2, fg_2 = find_alpha_fg(c_bg1, c_bg2, c_cp1, c_cp2)

imsave("leaves_alpha.jpg", alpha_2)
imsave("leaves_foreground", fg_2)

    
## Composites
window = imread('window.jpg')/255.0


# LEAVES    
    
composite_2 = create_composite(alpha_2, fg_2, window)
imsave("leaves_window", composite_2)

figure(2); imshow(composite_2)
pause(1)

figure(3); imshow(alpha_2)
pause(1)
figure(4); imshow(fg_2)
pause(1)


