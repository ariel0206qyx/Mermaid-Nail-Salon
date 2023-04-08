#starter test codes
from cmu_graphics import *


def onAppStart(app):
    resetAll(app)

def resetAll(app):
    app.indexList = []
    app.color = None
    app.size = 10
    app.colorList = ['red','orange','yellow','green','blue','purple','pink',
              'white','black']
    app.nailColor = 'beige'
    app.done = False

def redrawAll(app):
    drawLabel('Pick a color to paint your nails! Press r to restart',
              200,15)
    drawLabel(f'The current color is {app.color}',200,30)
    drawFinger(app)
    if not app.done:
        paintNails(app)
    drawRect(160,180,80,260,fill=None,border='black',borderWidth=4)
    drawColorIndex(app)
    if app.done:
        drawLabel('Nails painted! Press r to restart',100,100)

def drawFinger(app):
    drawRect(160,260,80,180,fill='lightPink',border='black')
    drawRect(160,180,80,80,fill=app.nailColor,border='black')

def drawColorIndex(app):
    for i in range(len(app.colorList)):
        drawRect(350, 30+30*i,15,15,fill=app.colorList[i],
                 border='black', borderWidth = 2)

def paintNails(app):
    if app.color != None:
        for (x,y) in app.indexList:
            color = app.color
            drawCircle(x,y,app.size,fill = color)

def onMouseDrag(app,mouseX,mouseY):
    if (app.color != None and not app.done and
        170<=mouseX<=170+60 and 190<=mouseY<=190+60):
            app.indexList.append((mouseX,mouseY))
    if len(app.indexList) >= 200:
        app.done = True
        app.nailColor = app.color
    



def onMousePress(app,mouseX,mouseY):
    if app.color == None:
        changeColor(app,mouseX,mouseY)

def changeColor(app,mouseX,mouseY):
    for i in range(len(app.colorList)):
        if (350 <= mouseX <= 350+15 and
            30+30*i <= mouseY <= 45+30*i):
            app.color = app.colorList[i]
        
def onKeyPress(app,key):
    if key == 'r':
        resetAll(app)
    

def main():
    runApp()

main()