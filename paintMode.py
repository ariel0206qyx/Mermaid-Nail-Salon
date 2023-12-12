from cmu_graphics import *
from PIL import Image
from Nail import Nail
from Customer import Customer
import math

class paintMode:
    def __init__(self):
        paintMode.start(self,app)

    def start(self,app):
        app.thumb = Nail(192.5,580,82,110)
        app.index = Nail(292.5,420,82,110)
        app.middle = Nail(392.5,370,82,110)
        app.ring = Nail(492.5,400,82,110)
        app.pinky = Nail(592.5,530,82,110)
        app.nailList = {'thumb': app.thumb,
                       'index': app.index,
                       'middle': app.middle,
                       'ring': app.ring,
                       'pinky': app.pinky}
        app.colorLabel = True
        app.colorLabelcolor = 'white'
        app.colorLabelword = False
        app.drawn = {}

        app.decoLabel = False
        app.decoLabelcolor = 'lightGray'
        app.decoLabelword = False

        app.colorList = ['red','orange','yellow','green','blue','purple','pink',
                'white','black']
        app.decoList = ['decoPink','decoYellow','decoBlue','decoPurple',None]

        app.cust = app.selectedCustomer

        app.doneWidth = 200
        app.doneHeight = 80
        app.displayScore = False
        app.completion = 0
        app.score = 0
        app.pScore = 0
        app.pSat = None
  
    def draw(self,app):
        drawRect(0,0,app.width,app.height,fill='lavender')
        for finger in app.nailList:
            app.nailList[finger].draw(app)
        drawRect(780,45,80,30,fill=app.colorLabelcolor)
        drawRect(860,45,120,30,fill=app.decoLabelcolor)
        drawRect(780,75,200,600,fill='white')
        drawLabel('Colors',820,60,font='monospace',size=18,bold=app.colorLabelword)
        drawLabel('Decorations',920,60,font='monospace',size=18,bold=app.decoLabelword)

        if app.colorLabel:
            paintMode.drawColorIndex(self,app)
            drawRect(780,45,80,30,fill=None,border='black')
        if app.decoLabel:
            paintMode.drawDecoIndex(self,app)
            drawRect(860,45,120,30,fill=None,border='black')

        paintMode.drawCustOrder(self,app,app.cust)
        
        image = Image.open('images/done.png')
        image = CMUImage(image)
        #https://www.dreamstime.com/done-image149087253
        drawImage(image,650,80,width=app.doneWidth,height=app.doneHeight,align='center')
        
        if app.displayScore:
            drawRect(app.width/2,app.height/2,500,200,align='center',
                     fill = 'gold',border='black')
            drawLabel(f'Order completion: {app.completion}%',500,300,size=18)
            drawLabel(f'{app.pSat}',
                       500,330,size=18)
            drawLabel(f'{app.score} points',500,360,size=18)
            drawLabel('Click anywhere to continue',
                      500,390,size=18,italic=True)

# Draws customer order based on the randomly generated 
# nail designs on top left corner     
    def drawCustOrder(self,app,cust):
        drawRect(0,0,300,180,fill='white',border='black')
        fingerIndex = {'thumb':[90,140,25,40],
                       'index': [120,90,25,90],
                       'middle':[150,70,25,110],
                       'ring':[180,80,25,100],
                       'pinky':[210,120,25,60]}
        fingerColor = rgb(254,200,174)
        for finger in cust.order:
            color = cust.order[finger]['color']
            deco = cust.order[finger]['deco']
            x,y,l,w = fingerIndex[finger]
            drawRect(x-12.5,y,l,w,fill=fingerColor,border='black')
            drawOval(x,y,25,35,fill=color,border='black')
            if deco != None:
                image = Image.open('images/' + deco + '.png')
                image = CMUImage(image)
                drawImage(image,x,y+5,height=12,width=12,align='center')
        
    def drawColorIndex(self,app):
        for i in range(len(app.colorList)):
            drawRect(860, 100+60*i,30,30,fill=app.colorList[i],
                    border='black', borderWidth = 2)

    def drawDecoIndex(self,app):
        #https://www.gameszap.com/game/10348/samis-nail-studio.html
        for i in range(len(app.decoList)-1):
            name = 'images/' + app.decoList[i] + '.png'
            image = Image.open(name)
            image = CMUImage(image)
            drawImage(image,880,130+50*i,height=40,width=40,align='center')

    def mouseMove(self,app,mouseX,mouseY):
        #change Label to bold when mouse hovers
        if (780 <= mouseX <= 780+80 and
            45 <= mouseY <= 45+30):
            app.colorLabelword = True
            app.decoLabelword = False
        if (860 <= mouseX <= 860+120 and
            45 <= mouseY <= 45+30):
            app.decoLabelword = True
            app.colorLabelword = False        
            app.keyX,app.keyY = mouseX,mouseY
        for finger in app.nailList:
            app.nailList[finger].mouseMove(app,mouseX,mouseY)
        if (550 <= mouseX <= 750 and
            40 <= mouseY <= 120):
            app.doneWidth = 220
            app.doneHeight = 90
        else:
            app.doneWidth = 200
            app.doneHeight=80

    def mouseDrag(self,app,mouseX,mouseY):
        for finger in app.nailList:
            app.nailList[finger].mouseDrag(app,mouseX,mouseY)

    def mousePress(self,app,mouseX,mouseY):
        #change Labels
        if (780 <= mouseX <= 780+80 and
            45 <= mouseY <= 45+30):
            app.colorLabel = True
            app.decoLabel = False
            app.colorLabelcolor = 'white'
            app.decoLabelcolor = 'lightGray'
            app.deco = None
        if (860 <= mouseX <= 860+120 and
            45 <= mouseY <= 45+30):
            app.decoLabel = True
            app.colorLabel = False
            app.colorLabelcolor = 'lightGray'
            app.decoLabelcolor = 'white'        
        for finger in app.nailList:
            app.nailList[finger].mousePress(app,mouseX,mouseY)
        if (not app.cust.served and
            550 <= mouseX <= 750 and
            40 <= mouseY <= 120):
                app.cust.served = True
                app.drawn = {'thumb': app.thumb.current,
                            'index': app.index.current,
                            'middle':app.middle.current,
                            'ring': app.ring.current,
                            'pinky': app.pinky.current}
                app.completion = paintMode.check(self,app)
                app.pScore,app.pSat = paintMode.patienceCheck(self,app)
                app.score = math.ceil(app.completion - app.pScore)
                app.displayScore = True
                app.totalScore += app.score
        if app.displayScore:
            if not (550 <= mouseX <= 750 and
                40 <= mouseY <= 120):
                app.displayScore = False
                Customer.seatList[app.selectedCustomer.seatIndex] = False
                Customer.custList.remove(app.selectedCustomer)
                app.mode3 = False
                app.paint.start(app)
                app.mode2 = True
    
    def check(self,app):
        score = 0
        for finger in app.cust.order:   
            nail = app.nailList[finger]
            length = len(nail.fingerList)
            # maximum length of this list is 180, because the nail
            # autofills once it reaches this length
            if app.cust.order[finger]['deco'] == None:
                if app.cust.order[finger]['color'] == app.drawn[finger]['color']:
                    if length < 180:
                    # if length is less than 180, this means that 
                    # the nail is partially colored
                    # so the score is calculated according to
                    # how much the nail is painted
                        score += math.ceil(length/180 * 20)
                    else:
                        score += 20               
            else:
                if app.cust.order[finger]['color'] == app.drawn[finger]['color']:
                    if length < 180:
                        score += math.ceil(length/180 * 10)
                    else:
                        score += 10
                if app.cust.order[finger]['deco'] == app.drawn[finger]['deco']:
                    preciseX = abs(nail.decoX - nail.cx)
                    preciseY = abs(nail.decoY - (nail.cy + 20))
                    score += (10 - (preciseX + preciseY)//10)
                    # scores based on how precise the decoration is placed
        return score
    
    def patienceCheck(self,app):
        d = {'green':(0,'She is satisfied with her waiting time!'),
             'gold' : (20, 'She is getting impatient! -20 points'),
             'red': (40, 'She is angry for waiting too long! -40 points')}
        return d[app.cust.patienceColor]
    # customer patience changes according to waiting time
    # (check Customer class)
    # longer the customer waits, more points will be deducted  

    def keyPress(self,app,key):
        for finger in app.nailList:
            app.nailList[finger].keyPress(app,key)
