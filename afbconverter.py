from PIL import Image
def afbtogif(name):
    with open("output.afb", "rb") as file:
        bytesarray = file.read()
    bytesarray = list(bytesarray)
    width = bytesarray[0]*256 + bytesarray[1]
    height = bytesarray[2]*256 + bytesarray[3]
    bytesarray.pop(0)
    bytesarray.pop(0)
    bytesarray.pop(0)
    bytesarray.pop(0)
    framelen = width*height*3
    framesnum = round(len(bytesarray)/framelen)
    frames = []
    for i in range(framesnum):
        frame = Image.frombytes("RGB",(width,height),bytes(bytesarray[i*framelen:(i*framelen)+framelen]))
        frames.append(frame)
    frames[0].save(
        name,
        save_all=True,
        append_images=frames[1:],
        duration=1000 // 24,
        loop=0
    )
