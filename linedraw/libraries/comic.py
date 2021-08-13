
# system libraries
import json
import sys

# external libraries
import cairo
from PyQt5.QtGui import QFont, QFontMetrics
from PyQt5.QtWidgets import QApplication
from svgpath2mpl import parse_path
from xml.dom import minidom

class comic:
    def __init__(self):
        self.name = "comic"
    
    def computeWidthText(self, text):
        app = QApplication(sys.argv)
        font = QFont("CNC Vector",self.textSize)
        fm = QFontMetrics(font)
        width = fm.width(text)
        #height=fm.height()
        arr=[width,self.textSize]
        return arr

    def generateComicTextBox(self, widthText, numberlines):
        output = []
        return output

    def textToSVG(self, text):
        #global lines
        textAr = []
        # Calculate number lines
        arr = computeWidthText(text)
        if widthText<arr[0]:
            #print("not dividing!")
            textAr.append(text)
        else:
            print("divide text")
            words =  text.split(" ")
            newLine = words[0]
            #for word in words:
            #    if computeWidthText(newLine)<width

        linesComicBox = generateComicTextBox(arr[0],len(textAr)) 

        with cairo.SVGSurface(folderPath+"outputTextPath.svg", 700, 700) as surface:
            # creating a cairo context object for SVG surface
            # useing Context method
            Context = cairo.Context(surface)
            
            # setting color of the context
            Context.set_source_rgb(1, 0, 0)
            
            # approximate text height
            Context.set_font_size(textSize)
            
            # Font Style
            Context.select_font_face(
                "CNC Vector", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            
            for textLine in textAr:
                print("texline:"+textLine)
                # position for the text
                print("Size: "+str(textSize))
                #Context.move_to(5, 45 * (textSize+5))
                Context.move_to(35, 45)
                
                # displays the text
                Context.text_path(textLine)
                #Context.rectangle(20, 20, 120, 80)

                # Width of outline
                Context.set_line_width(2)
                
                # stroke out the color and width property
                Context.stroke()
                #value=surface.get_document_unit()
                
                path=Context.copy_path()

        # printing message when file is saved
        print("File Saved")

        doc = minidom.parse(folderPath+"svgNew.svg")  # parseString also exists
        path_strings = [path.getAttribute('d') for path
                        in doc.getElementsByTagName('path')]
        #print(path_strings)
        doc.unlink()
        #print(path_strings[0])

        #print(path_strings[0])

        lines = []
        pathAr =  str(path_strings[0]).split("M")[1:]
        #print(len(pathAr))
        #print(parse_path("M"+pathAr[0] ).vertices)
        for path in pathAr:
            pathVertices = parse_path("M"+path).vertices
            lines.append(pathVertices)
        
        rotateAndScaleLinesAr = [] 
        xTranslate = 90000
        yTranslate = -150000
        scaleFont = (1000 * 0.25) #0.35
        for l in lines:
            rotateAndScaleLine = []
            for point in l:
                rotateAndScaleLine.append([(point[1]*scaleFont)+xTranslate,(point[0]*scaleFont)+yTranslate])
            rotateAndScaleLinesAr.append(rotateAndScaleLine)
        # copy transformed lines    
        lines = rotateAndScaleLinesAr 
        return lines

    def prepareDrawingText(lines):
        homePositionAr = (185000,0,125000,1800000,0,0,0)
        w = lines[0]
        h = lines[1]
        print("width: "+str(w))
        print("height: "+str(h))
        usefulDrawingSizeX = 160.0   #160 MAX x on paper
        usefulDrawingSizeY = 160.0 #160 MAX y on paper
        #outputAr = deepcopy(lines[2])
    
        brushLift = 20000
        #CALIBRATION FOR TOOL Z AXIS
        #z=41000 #marker
        #z=62000 #pencil
        #z = 77502
        #z=toolType
        z=64664
        z=65000
        print("z: ",z)
        
        indexi = 0
        outputAr = []
        
        for i in lines[2]: 
            indexj = 0
            
            for j in i:
                x = j[0]
                y = j[1]
                
                #TOP border X LIMIT 345000(185000+usefulDrawingX)
                if(x <185000+usefulDrawingSizeX*1000.0):
                    if indexj==0:
                        outputAr.append((round(x),round(y),z+brushLift,1800000,0,0,0))
                    
                    outputAr.append((round(x),round(y),z,1800000,0,0,0))
                    # find begining line and lift pen
                    if(indexj==len(i)) :
                        outputAr.append((round(x),round(y),z+brushLift,1800000,0,0,0))
                    print(str(j)+"->"+str(round(x))+","+str(round(y)))
                
                indexj += 1
            indexi += 1

        print("number of lines: "+str(indexi))
        # add Home
        outputAr.append(homePositionAr)
        return outputAr
    
    def prepareDrawing(self,lines,toolType):

        w = lines[0]
        h = lines[1]

        usefulDrawingSizeX = 160.0  #MAX x on paper
        usefulDrawingSizeY = 160.0 #MAX y on paper
        #outputAr = deepcopy(lines[2])
        if w!=h:  
            print("horizontal")
            usefulDrawingSizeY = 270.0  #270

        brushLift = 20000
        #CALIBRATION FOR TOOL Z AXIS
        #z=41000 #marker
        #z=62000 #pencil
        #z = 77502
        z=toolType
        print("z: ",z)
        z=65000
        indexi = 0
        outputAr = []
        for i in lines[2]: 
            indexj = 0
            for j in i:
                #185000+160000
                x = (((((j[0]* 0.5)/w)*usefulDrawingSizeX) )*1000.0) - ((usefulDrawingSizeX*0.5)*1000.0) + 185000
                y = (((((j[1]* 0.5)/h)*usefulDrawingSizeY) )*1000.0) - ((usefulDrawingSizeY*0.5)*1000.0)
                #TOP border X LIMIT 345000(185000+usefulDrawingX)
                if(x <185000+usefulDrawingSizeX*1000.0):
                    if indexj==0:
                        outputAr.append((round(x),round(y),z+brushLift,1800000,0,0,0))
                    #if indexi==0 and indexj==0:
                    #    print(j[0],x)
                    #outputAr[indexi][indexj] = (round(x),round(y),z,1800000,0,0,0)
                    #outputAr[indexi][indexj] = (round(x),round(y),z,1800000,0,0,0)
                    
                    outputAr.append((round(x),round(y),z,1800000,0,0,0))
                    if(indexj==len(i)) :
                        outputAr.append((round(x),round(y),z+brushLift,1800000,0,0,0))
                        # if we want to change color 

                indexj += 1
            indexi += 1
        # add Home
        outputAr.append(homePositionAr)
        return outputAr


if __name__ == '__main__':
     test = comic ()
     test.textToSVG("text")