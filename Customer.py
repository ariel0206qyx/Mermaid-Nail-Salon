from cmu_graphics import *
from PIL import Image
import random

class Customer:
    custList = []
    seatList = [False, False, False, False, False, False]
    typeList = ['images/pink.png','images/lightBlue.png',
                'images/green.png','images/purple.png',
                'images/blue.png','images/yellow.png',
                'images/orange.png']
    #https://www.pinterest.com/pin/villanas--10907224088755557/
    seatIndexList = [(370,200),(557,200),(745,200),
                     (370,475),(557,475),(745,475)]
    colorList = ['red','orange','yellow','green','blue','purple','pink',
              'white','black']
    decoList = ['decoPink',None,'decoYellow','decoBlue','decoPurple']
 
    def __init__(self, type, x, y):
        self.seatStatus = False
        self.selected = False
        self.type = type
        self.image = Image.open(Customer.typeList[self.type])
        self.image = CMUImage(self.image)
        self.x = x
        self.y = y
        self.x0 = x
        self.y0 = y
        self.seatIndex = None
        self.patience = 150
        self.patienceColor = 'green'
        self.served = False

        self.nailColor1 = random.choice(Customer.colorList)
        self.nailColor2 = random.choice(Customer.colorList)
        self.deco = random.choice(Customer.decoList)
# randomly generates nail designs, limited to a maximum 
# of two colors and one decoration because it gets ugly 
# if there are too many colors or decorations
        self.order = {'thumb': {'color': random.choice([self.nailColor1,self.nailColor2]),
                                'deco':self.deco},
                      'index': {'color': random.choice([self.nailColor1,self.nailColor2]),
                                'deco':self.deco},
                      'middle': {'color': random.choice([self.nailColor1,self.nailColor2]),
                                'deco':self.deco},
                      'ring': {'color': random.choice([self.nailColor1,self.nailColor2]),
                                'deco':self.deco},
                      'pinky': {'color': random.choice([self.nailColor1,self.nailColor2]),
                                'deco':self.deco}}
    
    def selectCust(self, mouseX, mouseY):
        if (self.x-75 <= mouseX <= self.x+75 and
            self.y-75 <= mouseY <= self.y+75):
            self.selected = True
        else:
            self.selected = False

# places a customer in a seat only if mouse is
# released in a certain range
#otherwise, customer returns to original position
    def placeToSeat(self,mouseX,mouseY):
        for (x,y) in Customer.seatIndexList:
            if (x-35 <= mouseX <= x+35 and
                y-35 <= mouseY <= y+35):
                return (x,y)
        return None

# refers to the patience bars that is
# displayed with each customer
    def patienceColorChange(self):
        if self.patience <=50:
            self.patienceColor = 'red'
        elif 50 < self.patience <= 80:
            self.patienceColor = 'gold'
        else:
            self.patienceColor = 'green'