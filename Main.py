from cmu_graphics import *
from PIL import Image
import random
from Customer import Customer
from initialMode import initialMode
from storeMode import *
from paintMode import *

def onAppStart(app):
    restart(app)
    app.leaveMessage = False
    app.mode1 = True
    app.initial = initialMode()
    app.initial.start(app)
    app.mode2 = False
    app.store = storeMode()
    app.store.start(app)
    app.mode3 = False
    app.paint = paintMode()
    app.paint.start(app)
    app.paused = True
    app.scoreGoal = 300
    restart(app)

def restart(app):
    app.totalScore = 0
    app.gameOver = False
    app.ticker = 200
    Customer.seatList = [False, False, False, False, False, False]

    
def redrawAll(app):
    if app.mode1:
        app.initial.draw(app)
    if app.mode2:
        app.store.draw(app)
    if app.mode3:
        app.paint.draw(app)
    if not app.mode1:
        drawRect(150,200,180,35,fill ='lavender',align='center')
        drawLabel(f'Total Score:{app.totalScore}',150,200,size=25)
        drawRect(875,25,150,30,fill='lavender',align='center')
        drawLabel(f'Time left: {app.ticker}',875,25,size=20)


    if app.leaveMessage:
        drawRect(app.width//2,app.height//2,260,70,fill='white',align='center',border='black')
        drawLabel('Oh no! One customer left -100 points',app.width//2,app.height//2-10,
                  size = 14,bold = True)
        drawLabel('Click anywhere to continue',app.width//2,app.height//2+10,
                  size = 14,bold = True, italic=True)
        
    if app.gameOver:
        drawRect(app.width//2,app.height//2,220,70,fill='white',align='center',border='black')
        if app.totalScore >= app.scoreGoal:
            drawLabel('Congratualations You win',app.width//2,app.height//2-20,
                  size = 16,bold = True)
        else:
            drawLabel('Game Over!',app.width//2,app.height//2-20,
                  size = 16,bold = True)
        drawLabel(f'Your total score is {app.totalScore}',app.width//2,app.height//2,
                size = 16,bold = True)
        drawLabel('Press enter to restart',app.width//2,app.height//2+20,
                size = 16,bold = True)

def onMouseMove(app,mouseX,mouseY):
    if app.mode1:
        app.initial.mouseMove(app,mouseX,mouseY)
    if not app.paused:
        if app.mode3:
            app.paint.mouseMove(app,mouseX,mouseY)

def onMousePress(app,mouseX,mouseY):
    if app.leaveMessage:
        app.totalScore -= 100
        app.leaveMessage = False
    if app.mode1:
        if app.initial.mousePress(app,mouseX,mouseY):
            app.mode1=False
            app.mode2=True
            app.paused = False
    if not app.paused:
        if app.mode2:
            app.store.mousePress(app,mouseX,mouseY)
        if app.mode3:
            app.paint.mousePress(app,mouseX,mouseY)

def onMouseDrag(app,mouseX,mouseY):
    if not app.paused:
        if app.mode2:
            app.store.mouseDrag(app,mouseX,mouseY)
        if app.mode3:
            app.paint.mouseDrag(app,mouseX,mouseY)

def onMouseRelease(app,mouseX,mouseY):
    if not app.paused:
        if app.mode2:
            app.store.mouseRelease(app,mouseX,mouseY)

def onKeyPress(app,key):
    if not app.paused:
        if app.mode3: 
            app.paint.keyPress(app,key)
    if app.gameOver:
        if key == 'enter':
            Customer.custList = []
            app.store.start(app)
            app.paused = False
            app.mode2 = True
            app.mode3 = False
            restart(app)

def onStep(app):
    app.stepsPerSecond = 1
    if not app.mode1 and not app.paused:
        app.store.step(app)
        app.ticker -= 1
    if app.ticker == 0:
        app.paused = True
        app.gameOver = True

def main():
    runApp(width=1000,height=700)

main()