from functools import cache
from math import sqrt
import shutil

class vec2:
    def __init__(self, x, y=None):
        if y is None:
            self.x = x
            self.y = x
        if y is not None:
            self.x = x
            self.y = y

    def __add__(self, other):
        return vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return vec2(self.x * other.x, self.y * other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __round__(self):
        return vec2(round(self.x), round(self.y))

    def __truediv__(self, other):
        return vec2(self.x / other.x, self.y / other.y)
    def cross(self, other):
        return self.x*other.y-self.y*other.x
    def __neg__(self):
        return vec2(-self.x,-self.y)
    def sqrt(self):
        return vec2(sqrt(self.x),sqrt(self.y))
    def float(self):
        return vec2(float(self.x),float(self.y))
    def sqr(self):
        return vec2(self.x*self.x,self.y*self.y)
    def __mod__(self,other):
        return vec2(self.x%other.x,self.y%other.y)


class vec3:
    def __init__(self, r, g=None, b=None):
        if g is None and b is None:
            self.r = r
            self.g = r
            self.b = r
        else:
            self.r = r
            self.g = g
            self.b = b

    def __add__(self, other):
        return vec3(self.r + other.r, self.g + other.g, self.b + other.b)

    def __sub__(self, other):
        return vec3(self.r - other.r, self.g - other.g, self.b - other.b)

    def __mul__(self, other):
        return vec3(self.r * other.r, self.g * other.g, self.b * other.b)

    def __eq__(self, other):
        return self.r == other.r and self.g == other.g and self.b == other.b

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        return f'({self.r}, {self.g}, {self.b})'

    def __truediv__(self, other):
        return vec3(self.r / other.r, self.g / other.g, self.b / other.b)
    def __round__(self):
        return vec3(round(self.r),round(self.g),round(self.b))
    def dot(self, other):
        return (self.r*other.r)+(self.g*other.g)+(self.b*other.b)
    def greyscale(self):
        return self.dot(vec3(0.2126,0.7152,0.0722))
    def sqrt(self):
        return vec3(sqrt(self.r),sqrt(self.g),sqrt(self.b))
    def sqr(self):
        return vec3(self.r*self.r,self.g*self.g,self.b*self.b)

class Context:
    def __init__(self, time=0, width=0, height=0, data=None):
        if data is None:
            data = []
        self.time = time
        self.size = vec2(width,height)
        self.data = data
        self.textures = self.data

class Shaderdata:
    def __init__(self,shader,description="This shader shows off my awesome shader abilities okay bye",inputs=0):
        self.shader = shader
        self.description = description
        self.inputs = inputs


# Renderer stuff

@cache
def mciparser(mci):
    with open(mci, "rb") as file:
        bytesarray = list(file.read(-1))
    print(bytesarray)

    width, height = bytesarray[0], bytesarray[1]

    print(width)
    print(height)
    imagebytes = []
    bytesarray.pop(0)
    bytesarray.pop(0)

    for x in bytesarray:
        binary = format(int(bin(x)[2:]), "08")
        h = "0b"
        j = ""

        r = int(h + binary[:2], 2) * 85
        g = int(h + binary[2:4], 2) * 85
        b = int(h + binary[4:6], 2) * 85

        imagebytes.extend([r, g, b])
    return [imagebytes, width, height]


@cache
def imagegrabber(image):
    with open(image, "r") as file:
        lines = file.readlines()
        width = int(lines[1].split(" ")[0])
        height = int(lines[1].split(" ")[1])

        content = lines[3].replace("\n", "")
        return [content.split(" "), width, height]


def imagegrabber2(image):
    with open(image, "r") as file:
        lines = file.readlines()
        width = int(lines[1].split(" ")[0])
        height = int(lines[1].split(" ")[1])

        content = lines[3].replace("\n", "")
        return [content.split(" "), width, height]

# Sampling function, basically texture2d()
def sample(image, x, y, imagetype=0, mode=0, border=vec3(255, 0, 255)):
    if imagetype == 0:
        colors, width, height = imagegrabber(image)

    else:
        colors, width, height = mciparser(image)
    x = round(x*(width-1))
    y = round(y*(height-1))
    if (x) > width - 1 or x < 0 or y < 0 or y > height - 1:
        match mode:
            case 0:
                x = x % width
                y = y % height
            case 1:
                if (x < 0):
                    x = 0
                if (y < 0):
                    y = 0
                if (x > width - 1):
                    x = width - 1
                if (y > height - 1):
                    y = height - 1
            case 2:
                return border
    index = int((x + y * width) * 3)
    return vec3(float(colors[index]), float(colors[index + 1]), float(colors[index + 2]))

# Makes a PPM P3
def make_image(width, height, pixels):
    header = "P3\n" + str(width) + " " + str(height) + "\n255\n"
    pix_text = ""
    for i in range(len(pixels)):
        pix_text += str(pixels[i]) + " "
    header += pix_text
    return header
# Makes an AFB file from the TFB file and TAB file
def make_afb(width,height,frames):
    x = width.to_bytes(2, "big")
    y = height.to_bytes(2, "big")
    frames = frames.to_bytes(2,"big")
    image = b""
    audio = b""
    with open("temp.tfb", "rb") as file:
        image = file.read()
    with open("temp.tab", "rb") as file:
        audio = file.read()
        if audio == b"":
            with open("wiiumiimaker.tab", "rb") as music:
                audio = music.read()
    return x+y+frames+image+audio


# Main render function
def render(x=255, y=255,frames=1,name="output",data=[]):
    total = x * y
    with open("temp.tfb", "wb") as file:
        file.write(b"")
    with open("temp.tab", "wb") as file:
        file.write(b"")

    pixel_buffer = []
    for t in range(frames):
        count = 0
        ctx = Context(t, x, y, data)
        for i in range(0, y):
            for j in range(0, x):
                count += 1

                v = vec2(j, i)

                pixel = round(shader(v, ctx))

                pixel_buffer += [pixel.r, pixel.g, pixel.b]
                print(f"\r{count}/{total}, frame {t+1}/{frames}", end="")

        if frames != 1:
            with open("temp.tfb", "ab") as file:
                file.write(bytes(pixel_buffer))
            pixel_buffer = []
    if frames == 1:
        with open(f"{name}.ppm", "w", encoding="ascii") as file:
            file.write(make_image(x, y, pixel_buffer))
    else:
        with open(f"{name}.afb", "wb") as file:
            file.write(make_afb(x,y,frames))
        with open("temp.tfb", "wb") as file:
            file.write(b"")

# Cool Stuff

def invBilinear(p, a, b, c, d):
    e = b-a
    f = d-a
    g = a-b+c-d
    h = p-a

    k2 = g.cross(f)
    k1 = e.cross(f) + h.cross(g)
    k0 = h.cross(e)

    if abs(k2) < 0.001:
        denom = e.x*k1 - g.x*k0
        if abs(denom) < 0.000001:
            return vec2(-1)
        return vec2((h.x*k1 + f.x*k0)/denom, -k0/k1)

    w = k1*k1 - 4*k0*k2
    if w < 0:
        return vec2(-1)
    w = sqrt(w)
    ik2 = 0.5/k2

    v = (-k1 - w)*ik2
    denom = e.x + g.x*v
    valid1 = abs(denom) >= 0.000001
    u = (h.x - f.x*v)/denom if valid1 else None

    if not valid1 or u < 0 or u > 1 or v < 0 or v > 1:
        v = (-k1 + w)*ik2
        denom = e.x + g.x*v
        if abs(denom) < 0.000001:
            return vec2(-1)
        u = (h.x - f.x*v)/denom

    return vec2(u, v)

def distance(v21,v22):
    difference = v21-v22
    return sqrt(difference.x*difference.x+difference.y*difference.y)