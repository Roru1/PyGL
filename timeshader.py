from pygl import *
import pygl
import numpy as np
from math import sin,cos

def translation(uv,ctx):
    x=uv.x
    y=uv.y
    x += ctx.time*(10.625/2)

    return sample("cobblestone.ppm",x,y)

def rotation(uv,ctx):
    xy = uv/ctx.size
    x = xy.x-0.5
    y = xy.y-0.5
    angle = ctx.time * 2*3.14159/48
    A = np.array([[cos(angle), -sin(angle)],
                  [sin(angle), cos(angle)]])

    B = np.array([[x],
                  [y]])

    # Perform matrix multiplication
    result = A @ B
    xy = vec2(float(result[0][0])+0.5,float(result[1][0])+0.5)*ctx.size
    color = sample("cobblestone.ppm",xy.x,xy.y)
    return color

def shaderpicker():
    return {"Translation (animated)": translation,"Rotation (animated)":rotation}