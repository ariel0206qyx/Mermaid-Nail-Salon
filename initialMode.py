from cmu_graphics import *
from PIL import Image

class initialMode:
    def start(self,app):
        app.initialView = Image.open('images/initial.png')
        app.initialView = CMUImage(app.initialView)
        #https://www.freepik.com/premium-vector/nail-polish-salon-template-hand-drawn-illustration-receiving-manicure-pedicure-young-girl_32633573.htm
        app.mermaidIcon = Image.open('images/whiteMermaid.png')
        app.mermaidIcon = CMUImage(app.mermaidIcon)
        #https://www.freepik.com/free-photos-vectors/mermaid-icon
        app.startIcon = Image.open('images/startIcon.png')
        app.startIcon = CMUImage(app.startIcon)
        #https://www.pngkit.com/view/u2q8y3o0i1q8q8t4_start-button-start-button-png-pink/
        app.startWidth = 500
        app.startHeight = 140
        

    def draw(self,app):
        drawImage(app.initialView,app.width//2,app.height//2, align='center')
        drawImage(app.mermaidIcon,290,130,width=100,height=100,align='center')
        drawImage(app.startIcon,700,500,width=app.startWidth,
                height=app.startHeight,align='center')
        drawRect(687.5,420,330,50,fill='Magenta',align='center')
        drawLabel(f'Goal: {app.scoreGoal} points in {app.ticker} seconds!',687.5,420,size=20,
                  bold=True,fill='white')

    def mouseMove(self,app,mouseX,mouseY):
        if (687.5-250 <= mouseX <= 687.5+250 and
            420-70 <= mouseY <= 420+70):
            app.startWidth=550
            app.startHeight=175
        else:
            app.startWidth=500
            app.startHeight=140

    def mousePress(self,app,mouseX,mouseY):
        if (700-app.startWidth/2 <= mouseX <= 700+app.startWidth/2 and
            500-app.startHeight/2 <= mouseY <= 500+app.startHeight):
            return True