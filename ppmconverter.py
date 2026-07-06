from PIL import Image
from pygl import imagegrabber2
from pygl import make_image

def ppmtopng(name):
    pixels, width, height = imagegrabber2("output.ppm")
    pixels.pop()

    pixel_bytes = bytes(int(float(x)) for x in pixels)

    img = Image.frombytes("RGB", (width, height), pixel_bytes)

    img.save("output.png")


if __name__ == "__main__":
    img = Image.open("input.png")

    width, height = img.size

    if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
        # Create a solid white background matching the image size
        background = Image.new("RGB", img.size, (255, 255, 255))

        # Paste the image onto the background using itself as the mask
        background.paste(img, mask=img.split()[-1])
        rgb_img = background
    else:
        # If no alpha channel exists, just convert it directly
        rgb_img = img.convert("RGB")

    pixel_bytes = rgb_img.tobytes()

    pixels = [int(x) for x in pixel_bytes]
    with open("imported.ppm", "w", encoding="ascii") as file:
        file.write(make_image(width, height, pixels))
