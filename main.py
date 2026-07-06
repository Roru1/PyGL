import pygl
import importlib
import os
import inspect
from afbconverter import afbtogif
from ppmconverter import ppmtopng

print("\033[34;1mSHADER RUNNER\033[0m")
print("Press\033[35;5m [ENTER]\033[0m to continue")

input()
def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    a = input("Enter python script with your shaders (without extention): ")
    shader_module = importlib.import_module(a)
    if hasattr(shader_module,"shaderpicker"):
      shader_dict = shader_module.shaderpicker()
      b = list(shader_dict)
      print("Choose a shader from the selection below:")
      for i in range(1,len(b)+1):
        print(f"{i}: {b[i-1]}")
      c = int(input("Enter which number shader you want: "))
      pygl.shader = shader_dict[b[c-1]]
    else:
        if hasattr(shader_module, "shader"):
            pygl.shader = shader_module.shader
        else:
            print("""You must define your shaders in shaderpicker, or name your shader "shader" """)



    x = int(input("X Resolution: "))
    y = int(input("Y Resolution: "))

    frames = int(input("Frames (1 for a still image): "))
    pygl.render(x, y,frames)


    if frames != 1:
        name = input("Enter name for image (.gif): ")
        if not name.endswith(".gif"):
            name += ".gif"
        afbtogif(name)
    else:
        name = input("Enter name for image (.png): ")
        if not name.endswith(".png"):
            name += ".png"
        ppmtopng(name)

    if input("e to exit: ") == "e":
        exit()
while True:
    main()
