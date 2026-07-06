from pygl import *
import pygl
import numpy as np
from math import sin,cos

def translation(uv,ctx):
    x=uv.x
    y=uv.y
    x += ctx.time*(ctx.size.x/48)

    return sample("cobblestone.ppm",x,y)

def rotation(uv,ctx):
    xy = uv/ctx.size
    x = xy.x-0.5
    y = xy.y-0.5
    angle = ctx.time * 2*3.14159/48
    c = cos(angle)
    s = sin(angle)
    
    xy = vec2(float(s*x-c*x)+0.5,float(s*y+c*y)+0.5)*ctx.size
    color = sample("cobblestone.ppm",xy.x,xy.y)
    return color

def shaderpicker():
    return {"Translation (animated)": translation,"Rotation (animated)":rotation}
