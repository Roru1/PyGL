from pygl import *
import pygl

def translation(uv,time):
    x=uv.x
    y=uv.y
    x += time*(10.625/2)

    return sample("cobblestone.ppm",x,y)

def shaderpicker():
    return {"Translation (animated)": translation}