#bmp_processor
#Por Luis Diego Fernandez
#V_A
import sys
import math
import struct
import random
import numpy as np

class bmpImage:

    # Define init(). Attributes Initializer
    def __init__(self, new_width, new_height):

        # image attributes
        self.width = new_width
        self.height = new_height
        self.bits_per_pixel = 32
        self.row_bytes = new_width * 4
        self.row_padding = int(math.ceil(int(self.row_bytes / 4.0))) * 4 - self.row_bytes

        # clear colors
        self.clearRgbRed = 0
        self.clearRgbGreen = 0
        self.clearRgbBlue = 0

        # object
        self.object_skeleton = []

        # texture image
        self.textureImg = []
        self.texture_width = 0
        self.texture_height = 0
        self.texture_width_ratio = 0
        self.texture_height_ratio = 0

        # z_buffer
        self.pixels = []

        for i in range(self.height):
            x_coordinates = []
            for j in range(self.width):
                x_coordinates.append([0,0,0])
            self.pixels.append(x_coordinates)

        self.shaderColors = []

        for i in range(self.height):
            x_coordinates = []
            for j in range(self.width):
                x_coordinates.append([0,0,0])
            self.shaderColors.append(x_coordinates)

        # z_buffer
        self.z_buffer = [
          [-float('inf') for y in range(self.height)]
          for x in range(self.width)
        ]


    ############################################################################
    ##################### IMAGE PROCESING FUNCTIONS ############################
    ############################################################################

    # Define glAbsolutePointPaint(int, int). Paints an individual pixel
    # returns: 0 on success
    def absolutePoint(self,x,y,z_avg,color):

        if y >= self.height or x >= self.width:
            return -1

        if y < 0 or x < 0:
            return -1

        if z_avg  < self.z_buffer[y][x]:
            return -1

        self.pixels[y][x] = color
        self.z_buffer[y][x] = z_avg

        return 0

    # Define glAbsolutePointPaint(int, int). Paints an individual pixel
    # returns: 0 on success
    def absolutePointTS(self,x,y,z_avg, color):

        if y >= self.height or x >= self.width:
            return -1

        if y < 0 or x < 0:
            return -1

        if z_avg  < self.z_buffer[y][x]:
            return -1

        r = int((self.shaderColors[y][x][0] + color[0])/2)
        g = int((self.shaderColors[y][x][1] + color[1])/2)
        b = int((self.shaderColors[y][x][2] + color[2])/2)

        self.pixels[y][x] = (r,g,b)

        self.z_buffer[y][x] = z_avg

        return 0

    def absoluteLine(self,start,end,z_avg,color = [], onlyShader = False):
        x1, y1 = start
        x2, y2 = end

        dy = abs(y2 - y1)
        dx = abs(x2 - x1)
        steep = dy > dx

        if steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2

        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        dy = abs(y2 - y1)
        dx = abs(x2 - x1)

        offset = 0
        threshold = dx

        paintedPoints = []

        y = y1
        for x in range(x1, x2 + 1):

            if onlyShader:
                if steep:
                    self.absolutePointTS(y,x,z_avg,color)
                    paintedPoints.append((y,x))
                else:
                    self.absolutePointTS(x,y,z_avg,color)
                    paintedPoints.append((x,y))

            else:
                if steep:
                    self.absolutePoint(y,x,z_avg,color)
                    paintedPoints.append((y,x))
                else:
                    self.absolutePoint(x,y,z_avg,color)
                    paintedPoints.append((x,y))

            offset += dy * 2
            if offset >= threshold:
                y += 1 if y1 < y2 else -1
                threshold += dx * 2

        return paintedPoints

    # Define clear(). It paints the whole image in a specific rgb color.
    # returns: 0 on success
    def clear(self,r = 0,g = 0,b =0):

        for y in range(self.height):
            for x in range(self.width):
                self.pixels[y][x] = [r,g,b]

        return 0

    # Define clearZBuffer(). Clears z_buffer
    # returns: 0 on success
    def clear_zbuffer(self):
        # z_buffer
        self.z_buffer = [
          [-float('inf') for y in range(self.height)]
          for x in range(self.width)
        ]
        return 0

    # Define clearShader(). It paints the whole image in a specific rgb color.
    # returns: 0 on success
    def clearShader(self):

        for y in range(self.height):
            for x in range(self.width):
                self.pixels[y][x] = self.pixelColors[y][x]

        return 0

    # Define rgbToByte(int, int, int). Converts RGB to bytes
	# returns: 4 bytes indicating the RGB of a pixel
    def rgbToByte(self,r,g,b):
        pixel = struct.pack('B', b)
        pixel += struct.pack('B', g)
        pixel += struct.pack('B', r)
        pixel += struct.pack('B', 0)

        return pixel

    # Define finish(). Takes the image_data and makes a file out of it with
    # a specif name
    # returns: 0 on success
    def writeImage(self, fileName):

        counter = 0

        # image data
        self.image_data =  bytes('BM', 'utf-8')
        self.image_data += struct.pack('i', 26 + 4 * self.width * self.height)
        self.image_data += struct.pack('h', 0)
        self.image_data += struct.pack('h', 0)
        self.image_data += struct.pack('i', 26)
        self.image_data += struct.pack('i', 12)
        self.image_data += struct.pack('h', self.width)
        self.image_data += struct.pack('h', self.height)
        self.image_data += struct.pack('h', 1)
        self.image_data += struct.pack('h', 32)

        for y in range(self.height):

            sys.stdout.write('\r' + "Processing Scene: " + str(y/self.height*100)[0:4] + "% complete")

            pixel_x = self.pixels[y]

            for x in range(self.width):
                r = int(pixel_x[x][0])
                g = int(pixel_x[x][1])
                b = int(pixel_x[x][2])

                if r > 255:
                    r = 255
                if g > 255:
                    g = 255
                if b > 255:
                    b = 255

                if r < 0:
                    r = 0
                if g < 0:
                    g = 0
                if b < 0:
                    b = 0

                self.image_data += self.rgbToByte(r,g,b)


        sys.stdout.write('\r' + "Processing Scene: 100% complete   \n")

        # Makes the image file
        img = open(fileName + ".bmp", 'wb')
        img.write(self.image_data)

        return 0

    ############################################################################
    ##################### OBJECT PROCESING FUNCTIONS ###########################
    ############################################################################

    def objMaker(self, objectName, scale, translate_x, translate_y, textures = False, greyScale = True, onlyShader = False):

        self.objReader(objectName)
        self.polygons(scale, translate_x ,translate_y,textures,greyScale,onlyShader)

        return 0

    def objReader(self, objectName):

        # opens obj file
        file = open(objectName + '.obj')
        lines = file.read().splitlines()

        # vertices and faces
        vertices = []
        textures = []
        faces = []
        normals = []

        # reads each line and stores each vertice and face
        for line in lines:

        	# gets the prefix and the values of either a vertice or a face
        	try:
        		prefix, value = line.split(' ',1)
        	except ValueError:
        		continue

        	# reads and store vertices
        	if prefix == 'v':
        		try:
        			vertices.append(list(map(float, value.split(' '))))
        		except ValueError:
        			continue

        	# reads and store vertices
        	elif prefix == 'vt':
        		try:
        			textures.append(list(map(float, value.split(' '))))
        		except ValueError:
        			continue

        	# reads and store normals
        	elif prefix == 'vn':
        		try:
        			normals.append(list(map(float, value.split(' '))))
        		except ValueError:
        			continue

        	# reads and store faces
        	elif prefix == 'f':
        		section = []
        		for face in value.split(' '):
        			try:
        				section.append(list(map(int, face.split('/'))))
        			except ValueError:
        				try:
        					section.append(list(map(int, face.split('//'))))
        				except ValueError:
        					break
        		faces.append(section)

        # 2D list to return with the vertices, faces, textures and normals
        self.object_skeleton = [vertices,faces,textures,normals]

        return 0

    def loadTextureImage(self, texture, scale_X, scale_Y):
        image = open(texture + '.bmp', "rb")

        image.seek(10)
        header_size = struct.unpack("=l", image.read(4))[0]
        image.seek(18)

        self.texture_width = struct.unpack("=l", image.read(4))[0]
        self.texture_height = struct.unpack("=l", image.read(4))[0]
        self.texture_width_ratio = self.texture_width/self.width
        self.texture_height_ratio = self.texture_height/self.height
        self.textureImg = []
        image.seek(header_size)
        for y in range(self.texture_height):
            self.textureImg.append([])
            for x in range(self.texture_width):
            	b = ord(image.read(1))
            	g = ord(image.read(1))
            	r = ord(image.read(1))

            	#32 bits
            	self.textureImg[y].append((r,g,b))

        image.close()

        return 0

    def polygons(self,scale,translate_x,translate_y,textureScale,greyScale,onlyShader):

        vertices = self.object_skeleton[0]
        faces = self.object_skeleton[1]
        textures = self.object_skeleton[2]

        for face in faces:

            facePremiter = []
            texturePerimeter = []
            x_avg = 0
            y_avg = 0
            z_avg = 0

            # paint perimeter
            for i in range(len(face)):

                vertice_i = vertices[face[i][0]-1]

                xi = int((vertice_i[0]/scale)*self.width) + translate_x
                yi = int((vertice_i[1]/scale)*self.height) + translate_y
                zi = int(vertice_i[2])


                if i == len(face) - 1:
                    vertice_f = vertices[face[0][0]-1]
                else:
                    vertice_f = vertices[face[i+1][0]-1]

                xf = int((vertice_f[0]/scale)*self.width) + translate_x
                yf = int((vertice_f[1]/scale)*self.height) + translate_y

                x_avg += xi
                y_avg += yi
                z_avg += zi

                if textureScale:

                    texture_i = textures[face[i][1]-1]
                    xti = int((texture_i[0])*self.texture_width)
                    yti = int((texture_i[1])*self.texture_height)

                    if i == len(face) - 1:
                        texture_f = textures[face[0][1]-1]
                    else:
                        texture_f = textures[face[i+1][1]-1]

                    xtf = int((texture_f[0])*self.texture_width)
                    ytf = int((texture_f[1])*self.texture_height)

                    texturePerimeter += self.getPerimeter((xti,yti),(xtf,ytf))

                facePremiter += self.getPerimeter((xi,yi),(xf,yf))

            x_avg /= len(face)
            y_avg /= len(face)
            z_avg /= len(face)

            facePremiter.sort(key=lambda elem: (elem[1], elem[0]))
            texturePerimeter.sort(key=lambda elem:  (elem[1], elem[0]))

            # paint area
            if greyScale:

                light_y = 200
                light_x = 400

                y_factor = abs((light_y - abs(light_y - y_avg)))/light_y
                x_factor = abs((light_x - abs(light_x - x_avg)))/light_x

                grey = 25 * y_factor + 125 * (1 - z_avg/100)

                if grey > 255:
                    grey = 255

                if grey < 0:
                    grey = 0

                color = [grey, grey, grey]

                for i in range(len(facePremiter)):

                    pointsToPaint = []
                    firstPoint = facePremiter[i]

                    for j in range(i+1, len(facePremiter)):

                        secondPoint = facePremiter[j]

                        if (firstPoint[1] == secondPoint[1]):
                            pointsToPaint.append(secondPoint)
                            i += 1
                        else:
                            break

                    len_line = len(pointsToPaint)

                    # with grey
                    if len_line == 0 and greyScale:
                        if not onlyShader:
                            self.absolutePoint(firstPoint[0],firstPoint[1],z_avg,color)
                        else:
                            self.absolutePointTS(firstPoint[0],firstPoint[1],z_avg,color)
                    elif greyScale:
                        self.absoluteLine(firstPoint,pointsToPaint[len(pointsToPaint)-1]\
                        ,z_avg,color,onlyShader)

            elif textureScale:

                facePoints = []
                texPoints = []
                lastFP = -1
                lastTP = -1

                # get each line to paint
                for i in range(len(facePremiter)):

                    firstPoint = facePremiter[i]
                    secondPoint = []

                    if firstPoint[1] == lastFP:
                        continue

                    for j in range(i+1, len(facePremiter)):

                        if (firstPoint[1] == facePremiter[j][1]):
                            secondPoint = facePremiter[j]
                        else:
                            break

                    if secondPoint == []:
                        secondPoint = firstPoint

                    facePoints.append([firstPoint,secondPoint])
                    lastFP = firstPoint[1]

                # get each line texture
                for i in range(len(texturePerimeter)):

                    firstPoint = texturePerimeter[i]
                    secondPoint = []

                    if firstPoint[1] == lastTP:
                        continue

                    for j in range(i+1, len(texturePerimeter)):

                        if (firstPoint[1] == texturePerimeter[j][1]):
                            secondPoint = texturePerimeter[j]
                        else:
                            break

                    if secondPoint == []:
                        secondPoint = firstPoint

                    texPoints.append([firstPoint,secondPoint])
                    lastTP = firstPoint[1]

                # counter and ratio between textures and image
                counter_y = 0
                skip_y = len(texPoints)/len(facePoints)

                # paint each line of the face
                for line in facePoints:

                    x1 = line[0][0]
                    x2 = line[1][0]
                    y  = line[0][1]

                    indicador_y = round(skip_y*counter_y)

                    try:
                        tex_y = texPoints[indicador_y][0][1]
                    except IndexError:
                        indicador_y = indicador_y - 1
                        tex_y = texPoints[indicador_y][0][1]


                    try:
                        skip_x = (texPoints[indicador_y][1][0] - texPoints[indicador_y][0][0])/\
                        (x2 - x1)
                    except ZeroDivisionError:
                        skip_x = (texPoints[indicador_y][1][0] - texPoints[indicador_y][0][0])/\
                        (x2 - x1 + 1)

                    i = x1
                    counter_x = 0

                    while i < x2:

                        tex_x = round(texPoints[indicador_y][0][0] + skip_x*counter_x)

                        if tex_x >= texPoints[indicador_y][1][0]:
                            tex_x = texPoints[indicador_y][1][0]
                        if tex_y >= self.texture_height:
                            tex_y = self.texture_height - 1
                        if tex_x < 0:
                            tex_x = 0
                        if tex_y < 0:
                            tex_y = 0

                        color = self.textureImg[tex_y][tex_x]
                        # color = self.rgbToByte(255,0,0)

                        if onlyShader:
                            r = color[0] + self.shaderColors[y][i][0]
                            g = color[1] + self.shaderColors[y][i][1]
                            b = color[2] + self.shaderColors[y][i][2]

                            color = (r,g,b)

                        self.absolutePoint(i,y,z_avg,color)

                        i += 1
                        counter_x += 1

                    counter_y += 1

        return 0

    def setBackground(self):

        for y in range(self.height):
            for x in range(self.width):

                if y > self.height/2:
                    self.absolutePoint(x,y,-500,(150,0,0))
                else:
                    if y%int((self.height)/(self.height/16)) == 0:
                        self.absolutePoint(x,y,-500,(0,0,0))
                    else:
                        self.absolutePoint(x,y,-500,(130,90,60))

    def setLight(self,light_x,light_y):
        for y in range(self.height):

            y_factor = abs((light_y - abs(light_y - y)))/light_y

            for x in range(self.width):

                x_factor = abs((light_x - abs(light_x - x)))/light_x

                color = self.pixels[y][x]
                r = color[0]*0.60 + color[0]*0.40 * x_factor * y_factor
                g = color[1]*0.60 + color[1]*0.40 * x_factor * y_factor
                b = color[2]*0.60 + color[2]*0.40 * x_factor * y_factor

                self.pixels[y][x] = (r,g,b)

        return 0

    def getPerimeter(self,start,end):
        x1, y1 = start
        x2, y2 = end

        dy = abs(y2 - y1)
        dx = abs(x2 - x1)
        steep = dy > dx

        if steep:
          x1, y1 = y1, x1
          x2, y2 = y2, x2

        if x1 > x2:
          x1, x2 = x2, x1
          y1, y2 = y2, y1

        dy = abs(y2 - y1)
        dx = abs(x2 - x1)

        offset = 0
        threshold = dx

        paintedPoints = []

        y = y1
        for x in range(x1, x2 + 1):
          if steep:
              paintedPoints.append((y,x))
          else:
              paintedPoints.append((x,y))

          offset += dy * 2
          if offset >= threshold:
              y += 1 if y1 < y2 else -1
              threshold += dx * 2

        return paintedPoints


    ############################################################################
    ############################## Shaders #####################################
    ############################################################################

    def setShaderSofa(self):

        mul = 0
        limit = 25

        for y in range(self.height):

            mul += 1

            if mul == limit:
                mul = 1

            if y > 0.192 * self.height:
                limit = 11

            for x in range(self.width):

                r = 200 * math.sin(x * mul)
                g = 10 * math.sin(x * mul)
                b = 10 * math.sin(x * mul)

                if y > 0.192 * self.height:
                    g = g + 10
                    b = b + 10

                self.shaderColors[y][x] = (r,g,b)

        return 0

    def setShaderSword(self):
        for y in range(self.height):

            for x in range(self.width):

                r = 600 - int(y/2) + int(x/4)
                g = - 100 - int(y/2) + int(x/4)
                b = - 100 - int(y/2) + int(x/4)
                self.shaderColors[y][x] = (r,g,b)

        return 0

    def setShaderTable(self):
        for y in range(self.height):

            mul = 1

            for x in range(self.width):

                r = 75 + 50 * math.sin(x/(0.125*self.width))
                g = 10 + 50 * math.sin(x/(0.125*self.width))
                b = 10 + 50 * math.sin(x/(0.125*self.width))

                self.shaderColors[y][x] = (r,g,b)

        return 0


    def absolutePointShaders(self,x,y,color):

        if y >= self.height or x >= self.width:
            return -1

        if y < 0 or x < 0:
            return -1

        self.shaderColors[y][x] = color

        return 0
