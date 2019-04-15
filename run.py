#SR5
#Luis Diego Fernandez
import sys
import BMP

WIDTH = 800
HEIGHT = 800

def makeTable():
    print("Painting Table...")
    image.clear_zbuffer()
    image.setShaderTable()
    x = int(0.500*WIDTH)
    y = int(0.350*HEIGHT)
    image.objMaker("Table/Table",435,x,y,False,True,True)

def makeSword():
    print("Painting Sword...")
    image.clear_zbuffer()
    image.setShaderSword()
    x = int(0.160*WIDTH)
    y = int(0.582*HEIGHT)
    image.objMaker("Sword/Sword",30,x,y,False,True,True)

def makeSofa():
    print("Painting Sofa...")
    image.clear_zbuffer()
    image.setShaderSofa()
    x = int(0.525*WIDTH)
    y = int(0.063*HEIGHT)
    image.objMaker("Sofa/Sofa",205,x,y,False,True,True)

def makeCat():
    print("Painting Cat...")
    image.clear_zbuffer()
    image.loadTextureImage("Cat/Col",0,0)
    x = int(0.763*WIDTH)
    y = int(0.504*HEIGHT)
    image.objMaker("Cat/Cat",200,x,y,True,False)

def makeTV():
    print("Painting TV...")
    image.clear_zbuffer()
    image.loadTextureImage("Sam/Col",0,0)
    x = int(0.500*WIDTH)
    y = int(0.588*HEIGHT)
    image.objMaker("Sam/Sam",20,x,y,True,False)

def makeTeddy():
    print("Painting Teddy...")
    image.clear_zbuffer()
    image.loadTextureImage("Teddy/Col",0,0)
    x = int(0.220*WIDTH)
    y = int(0.440*HEIGHT)
    image.objMaker("Teddy/Teddy",10,x,y,True,False)

def makeIvysaur():
    print("Painting Ivysaur...")
    image.clear_zbuffer()
    image.loadTextureImage("Ivysaur/Col",0,0)
    x = int(0.200*WIDTH)
    y = int(0.460*HEIGHT)
    image.objMaker("Ivysaur/Ivy",13,x,y,True,False)

# image
image = BMP.bmpImage(WIDTH,HEIGHT)
image.setBackground()
makeSword()
makeIvysaur()
makeTV()
makeCat()
makeTeddy()
makeTable()
makeSofa()
image.setLight(WIDTH/2,HEIGHT)
image.writeImage("out")
