from cmu_graphics import *
from PIL import Image

class Nail:
    def __init__(self,cx,cy,rx,ry):
        self.cx = cx
        self.cy = cy
        self.rx = rx
        self.ry = ry
        self.reset()

    def reset(self):
        self.color = None
        self.fixedColor = None
        self.deco = None
        self.colorLabel = True
        self.decoLabel = False
        self.decoX = self.decoY = None
        self.fingerColor = rgb(254,200,174)
        self.fingerList = []
        self.nailColor = rgb(255, 180, 160)
        self.fingerPaint = False
        self.fingerDone = False
        self.keyX = 0
        self.keyY = 0
        self.size = 10
        self.colorList = ['red','orange','yellow','green','blue','purple','pink',
                          'white','black']
        self.decoList = ['decoPink','decoYellow','decoBlue','decoPurple',None]
        self.current = {'color': None,
                        'deco': None}
 
    def draw(self,app):
        drawRect(self.cx-42.5,self.cy+50,85,20,fill=self.fingerColor)
        drawRect(self.cx-42.5,self.cy,85,470,fill=self.fingerColor,border='black')
        drawOval(self.cx,self.cy,self.rx,self.ry,fill=self.nailColor,border='black')
        if not self.fingerPaint and self.fixedColor != None:
            for (x,y) in self.fingerList:
                drawCircle(x,y,self.size,fill = self.fixedColor)
        if self.color != None and self.colorLabel and not self.fingerDone:
            drawCircle(self.keyX,self.keyY,10,fill=self.color)
        if self.deco != None and self.decoLabel and not self.fingerDone:
            image = Image.open('images/' + self.deco + '.png')
            image = CMUImage(image)
            drawImage(image,self.keyX,self.keyY,height=40,width=40,align='center')
        if self.fingerPaint and self.decoX != None and self.deco != None:
            deco = self.deco
            image = Image.open('images/' + deco + '.png')
            image = CMUImage(image)
            drawImage(image,self.decoX,self.decoY,height=40,width=40,align='center')

    def mouseDrag(self,app,mouseX,mouseY):
        if not self.fingerPaint:
            distance = ((mouseX - self.cx)**2/((self.rx/2)-10)**2 +
                    (mouseY - self.cy)**2/((self.ry/2)-10)**2)
            if (self.color != None and distance <= 1):
                if (len(self.fingerList) == 0 or
                    self.fixedColor == self.color):
                    self.fingerList.append((mouseX,mouseY)) 
                    self.fixedColor = self.color   
                    self.current['color'] = self.fixedColor 
            if len(self.fingerList) >= 160:
                self.fingerPaint = True
                self.nailColor = self.color
                self.current['color'] = self.fixedColor

    def mouseMove(self,app,mouseX,mouseY):
        self.keyX,self.keyY = mouseX,mouseY

    def mousePress(self,app,mouseX,mouseY):
        if (780 <= mouseX <= 780+80 and
            45 <= mouseY <= 45+30):
            self.colorLabel = True
            self.decoLabel = False
            if not self.fingerDone:
                self.deco = None
        if (860 <= mouseX <= 860+120 and
            45 <= mouseY <= 45+30):
            self.decoLabel = True
            self.colorLabel = False
            self.color = None
        if self.colorLabel:
            self.changeColor(mouseX,mouseY)
        if self.decoLabel and not self.fingerDone:
            self.changeDeco(mouseX,mouseY)
        if self.deco != None and self.fingerPaint and not self.fingerDone:
            self.decoX,self.decoY=self.putDeco(mouseX,mouseY)
            if self.decoX != None:
                self.current['deco'] = self.deco
                self.fingerDone = True

    def changeColor(self,mouseX,mouseY):    
        for i in range(len(self.colorList)):
            if (860 <= mouseX <= 860+30 and
                100+60*i <= mouseY <= 130+60*i):
                self.color = self.colorList[i]

    def changeDeco(self,mouseX,mouseY):
        for i in range(len(self.decoList)-1):
            if (860 <= mouseX <= 900 and
                110+50*i <= mouseY <= 150+50*i):
                self.deco = self.decoList[i]

    def putDeco(self,mouseX,mouseY):
        distance = ((mouseX - self.cx)**2/self.rx**2 +
                    (mouseY - self.cy)**2/self.ry**2)
        if distance <= 1 or self.fingerDone:
            return (mouseX,mouseY)
        if not self.fingerDone:
            return None,None

    def keyPress(self,app,key):
        if key == 'r':
            self.reset()