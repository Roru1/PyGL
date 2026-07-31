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
      while True:
        print("Choose a shader from the selection below:")

        for i in range(1,len(b)+1):
          print(f"{i}: {b[i-1]}")
        c = input("Enter which number shader you want: ")
        try:
            c = int(c)
        except ValueError:
            print("do the number next time")
            continue
        if c > len(b) or c<1:
            print("That's not a shader dummy")
            continue

        if not isinstance(shader_dict[b[c-1]],pygl.Shaderdata):
          pygl.shader = shader_dict[b[c-1]]
          inputs = 3
        else:
          shader_data = shader_dict[b[c-1]]
          print(shader_data.description)
          if input("Do you want this shader?(y/n) ").startswith("y"):
              pygl.shader = shader_data.shader
              inputs = shader_data.inputs
              break


    else:
        if hasattr(shader_module, "shader"):
            pygl.shader = shader_module.shader
            inputs = 3
        else:
            print("""You must define your shaders in shaderpicker, or name your shader "shader" """)



    x = int(input("X Resolution: "))
    y = int(input("Y Resolution: "))

    frames = int(input("Frames (1 for a still image): "))
    data = [input("What is the 1st data (for textures do .ppm)? ")]
    for i in range(inputs-1):
        i +=2
        j = str(i)
        if j.endswith("2"):
            suffix = "nd"
        elif j.endswith("3"):
            suffix = "rd"
        elif j.endswith("1"):
            suffix = "st"
        else:
            suffix = "th"
        data.append(input(f"What is the {i}{suffix} data? "))
    name = input("Enter name for image: ")
    pygl.render(x, y,frames,name,data)


    if frames != 1:
        afbtogif(name)
    else:
        ppmtopng(name)

    if input("e to exit: ") == "e":
        exit()
while True:
        main()
