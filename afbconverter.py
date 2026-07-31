from PIL import Image
import subprocess
import os
import shutil
"""
afbconverter.py

This script uses PIL to convert to gif and FFmpeg to convert to and from mp4

It is simple, and easy to implement a player
"""
def afbtogif(name):
    with open(f"{name}.afb", "rb") as file:
        bytesarray = file.read()
    bytesarray = list(bytesarray)
    width = bytesarray[0]*256 + bytesarray[1]
    height = bytesarray[2]*256 + bytesarray[3]
    framesnum = bytesarray[4]*256 + bytesarray[5]
    bytesarray.pop(0)
    bytesarray.pop(0)
    bytesarray.pop(0)
    bytesarray.pop(0)
    bytesarray.pop(0)
    bytesarray.pop(0)
    framelen = width * height * 3


    frames = []
    for i in range(framesnum):
        frame = Image.frombytes("RGB",(width,height),bytes(bytesarray[i*framelen:(i*framelen)+framelen]))
        frames.append(frame)
    if not name.endswith(".gif"):
        name += ".gif"
    frames[0].save(
        name,
        save_all=True,
        append_images=frames[1:],
        duration=1000 // 24,
        loop=0
    )

def mp4toafb(name):
    try:
        os.remove("temp.tfb")
    except:
        pass
    try:
        os.remove("temp.tab")
    except:
        pass
    subprocess.run(f"ffmpeg -i {name}.mp4 -f rawvideo -pix_fmt rgb24 -vcodec rawvideo temp.tfb",shell=True)
    subprocess.run(f"ffmpeg -i {name}.mp4 -vn -c:a pcm_u8 -ar 16000 -ac 1 -f u8 temp.tab",shell=True)
    out = subprocess.run(f"ffprobe -v error -select_streams v:0 -count_frames -show_entries stream=width,height,nb_read_frames -of default=noprint_wrappers=1 {name}.mp4",shell=True,capture_output=True,text=True).stdout
    print(out)

    d = {}
    exec(out, d)
    width = d["width"]
    height = d["height"]
    frames = d["nb_read_frames"]
    x = width.to_bytes(2, "big")
    y = height.to_bytes(2, "big")
    frames = frames.to_bytes(2, "big")
    with open(f"{name}.afb", "wb") as file:
        file.write(x)
        file.write(y)
        file.write(frames)
        with open("temp.tfb", "rb") as f:
            shutil.copyfileobj(f, file)

        with open("temp.tab", "rb") as f:
            shutil.copyfileobj(f, file)

def afbtomp4(name):
    try:
        os.remove(f"{name}.mp4")
    except:
        pass
    with open(f"{name}.afb", "rb") as file:
        header = file.read(6)
    header = list(header)
    width = header[0]*256 + header[1]
    height = header[2]*256 + header[3]
    framesnum = header[4]*256 + header[5]
    framestop = width * height * 3 * framesnum
    with open(f"{name}.afb", "rb") as file:
        image = file.read()
        with open(f"{name}.tfb", "wb") as tfb:
            tfb.write(image[6:framestop+6])
        with open(f"{name}.tab", "wb") as tab:
            tab.write(image[framestop+6:])
        with open(f"{name}.tfb", "rb") as tfb:
            size = len(tfb.read())
            if size>framestop:
                print(size-framestop)



    subprocess.run(f"ffmpeg -f rawvideo -pixel_format rgb24   -video_size {width}x{height} -framerate 24 -i {name}.tfb  -f u8 -ar 16000 -ac 1 -i {name}.tab -c:v libx264 -pix_fmt yuv420p -c:a aac {name}.mp4", shell = True)

if __name__ == "__main__":
    mp4toafb("input")
