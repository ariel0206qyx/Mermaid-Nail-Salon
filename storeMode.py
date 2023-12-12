from cmu_graphics import *
from PIL import Image
import random
from Customer import Customer

class storeMode:
    def start(self,app):
        app.tutorial = True
        app.nailShopView = Image.open('images/nailShop.png')
        app.nailShopView = CMUImage(app.nailShopView)
        #https://www.gameszap.com/game/10348/samis-nail-studio.html
        app.speechBubble = Image.open('images/speechBubble.png')
        app.speechBubble = CMUImage(app.speechBubble)
        #https://stock.adobe.com/search?k=text+bubble+png&asset_id=540071975        
        app.stepsPerSecond = 1
        app.leaveMessage = False
        app.selectedCustomer = None
        app.time = 0
        app.waitDict = {560: False,460:False,
                        360: False,260:False}
        storeMode.addCustomer(self)

    def draw(self,app):
        drawImage(app.nailShopView,app.width//2,app.height//2, align='center')
        for cust in Customer.custList:
            if not cust.seatStatus and app.tutorial:
                drawImage(app.speechBubble,710,70,width=200,height=100,align='center')
                drawLabel('Seat customers by',715,40,size=14,bold=True)
                drawLabel('dragging them',715,55,size=14,bold=True)
                drawLabel('to an empty seat!',715,70,size=14,bold=True)
            if cust.seatStatus and app.tutorial:
                drawImage(app.speechBubble,710,70,width=200,height=100,align='center')
                drawLabel('Serve customers by',715,50,size=14,bold=True)
                drawLabel('clicking them',715,65,size=14,bold=True)
            if cust.seatStatus and app.tutorial and cust.selected:
                drawImage(app.speechBubble,710,70,width=200,height=100,align='center')
                drawLabel('Move to mode:',715,50,size=14,bold=True)
                drawLabel('Run Nail.py for now',715,65,size=14,bold=True)
            drawImage(cust.image,cust.x,cust.y,width=150,height=150,align='center')
            drawRect(cust.x+50,cust.y,15,50,fill='white',align='bottom')
            drawRect(cust.x+50,cust.y,11,48*cust.patience/150,
                    align='bottom',fill=cust.patienceColor)
        
        if app.leaveMessage:
            drawRect(app.width//2,app.height//2,220,70,fill='white',align='center',border='black')
            drawLabel('Oh no! One customer left',app.width//2,app.height//2-10,
                    size = 16,bold = True)
            drawLabel('Click anywhere to continue',app.width//2,app.height//2+10,
                    size = 16,bold = True, italic=True)
        
    def mousePress(self,app,mouseX,mouseY):
        for cust in Customer.custList:
            if not cust.seatStatus:
                cust.selectCust(mouseX,mouseY)
            if cust.seatStatus:
                cust.selectCust(mouseX,mouseY)
                if cust.selected:
                    app.selectedCustomer = cust
                    app.mode2 = False
                    app.mode3 = True
                    app.paint.start(app)

    def mouseDrag(self,app,mouseX,mouseY):
        for cust in Customer.custList:
            if cust.selected and not cust.seatStatus:
                cust.x = mouseX
                cust.y = mouseY

    def mouseRelease(self,app,mouseX,mouseY):
        for cust in Customer.custList:
            if cust.selected and not cust.seatStatus:
                if cust.placeToSeat(mouseX,mouseY) != None:
                    x,y = cust.placeToSeat(mouseX,mouseY)
                    index = Customer.seatIndexList.index((x,y))
                    if not Customer.seatList[index]:
                        app.waitDict[cust.x0] = False
                        cust.x,cust.y = x,y
                        cust.seatStatus = True
                        cust.patience = min(cust.patience+20,150)
                        Customer.seatList[index] = True
                        cust.selected = False
                        cust.seatIndex = index
                    else:
                        cust.x,cust.y = cust.x0,cust.y0
                else:
                    cust.x,cust.y = cust.x0,cust.y0

    def step(self,app):
        app.time += 1
        for cust in Customer.custList:
            cust.patience -= 1
            cust.patience = max(cust.patience,0) 
            cust.patienceColorChange() 
            if cust.patience == 0:
                Customer.custList.remove(cust)
                app.leaveMessage = True 
        if app.time % 20 == 0:
            storeMode.addCustomer(self)  

    def addCustomer(self):
        positionX = None
        index = random.randint(0,6)
        for position in app.waitDict:
                if not app.waitDict[position]:
                    positionX = position
                    app.waitDict[position] = True         
                    Customer.custList.append(Customer(index,positionX,80))
                    break