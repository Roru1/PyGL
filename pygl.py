from functools import cache
import inspect

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


def sample(image, x, y, imagetype=0, mode=0, border=vec3(255, 0, 255)):
    if imagetype == 0:
        colors, width, height = imagegrabber(image)

    else:
        colors, width, height = mciparser(image)
    x = round(x)
    y = round(y)
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


def make_image(width, height, pixels):
    header = "P3\n" + str(width) + " " + str(height) + "\n255\n"
    pix_text = ""
    for i in range(len(pixels)):
        pix_text += str(pixels[i]) + " "
    header += pix_text
    return header

def make_afb(width,height):
    x = width.to_bytes(2, "big")
    y = height.to_bytes(2, "big")
    image = b""
    with open("temp.tfb", "rb") as file:
        image = file.read()
    return x+y+image



def render(x=255, y=255,frames=1):
    total = x * y

    pixel_buffer = []
    sig = inspect.signature(shader)
    has_time = "time" in sig.parameters
    for t in range(frames):
        count = 0
        for i in range(0, y):
            for j in range(0, x):
                count += 1

                v = vec2(j, i)
                if has_time:
                    pixel = round(shader(v,t))
                else:
                    pixel = round(shader(v))
                pixel_buffer += [pixel.r, pixel.g, pixel.b]
                print(f"\r{count}/{total}, frame {t+1}/{frames}", end="")
        with open("temp.tfb", "ab") as file:
            file.write(bytes(pixel_buffer))
        if frames != 1:
            pixel_buffer = []
    if frames == 1:
        with open("output.ppm", "w", encoding="ascii") as file:
            file.write(make_image(x, y, pixel_buffer))
    else:
        with open("output.afb", "wb") as file:
            file.write(make_afb(x,y))
        with open("temp.tfb", "wb") as file:
            file.write(b"")
