# PyGL
PyGL is a rendering api which has vectors, sampleing, and a plug &amp; play style main.py
## How to use
To use this first write a shaderpack, a shaderpack is a python file that contains shader functions and a shaderpicker function

a shader function is a function like this
```
def shader(uv,ctx):
	xy = uv/ctx.size
	x = xy.x
	y = xy.y
	color = sample("cobblestone.ppm",x,y)
	return color
```
it takes uv, which is is a vec2 which stores the pixel coordenates, and ctx, ctx contains time which is the frame index from 0, and size, which is a vec2 with the size of the image, it must return a vec3 containing the resulting color

if you want to have more than one shader or have the shader named something other than shader, use a function named shaderpicker, it should return a dictionary like this
```
{"name of shader":shader_function,"name of other shader":other_shader_function}
```
make sure the shaderpack python file has this on top
```
from pygl import *
```
and that it is in the same folder as the rest of the files, then just run main.py and follow what it says
## How to get images
to get images just name your image "input.png", and run ppmconverter.py then a file named imported.ppm should show up, just rename it and now you have an image you can sample
## Things inside pygl.py
### **sample()**
sample requires first, a filename, then the x coordinate, then y coordinate in 0-1 coordinates, then you can optionally do mode=int
1. mode 0 is the default, it wraps out of bounds
2. mode 1 clamps to the edge color out of bounds
3. mode 2 sets to a vec3 color you set with border=vec3(r,g,b)
### **vectors**
vec2 has two components, x and y, it supports arithmatic with other vec2s, rounding and if you only do vec2(number) instead of vec2(number,number2) it sets both to that number

vec3 has three components, r, g, and b, it supports the same things vec2 does exept with other vec3s
