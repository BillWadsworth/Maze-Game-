class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
#        master.bind('<Escape>',self.toggle_geom)            
#    def toggle_geom(self,event):
#        geom=self.master.winfo_geometry()
#        self.master.geometry(self._geom)
#        self._geom=geom


from tkinter import *
import random
finished = False 
gridSizeX = 40
gridSizeY = 35
amountOfSpaces = int((gridSizeX*gridSizeY)*0.625)
spaces = []
numOfCoins = 5
coins = []
light = []
coinsCollected = 0
valid = False


top = Tk()

app=FullScreenApp(top)

createGrid = StringVar()
cave = Label(top, textvariable = createGrid, font = "courier 10")


def lemmeMove():
 global newPlayerYPos
 global newPlayerXPos
 global playerXPos
 global playerYPos
 global newPlayerXPos
 global newPlayerYPos
 global gridsize
 global walls
 global alive
 global finish
 global finished
 global coinsCollected
#checks if new player position is valid, if not then sets the new player
#position to the current position (basically cancels it)
 if (newPlayerXPos, newPlayerYPos) not in spaces:
     newPlayerXPos = playerXPos
     newPlayerYPos = playerYPos
 #if newPlayerXPos == doorX and doorOpened == False:
     #newPlayerXPos = playerXPos
     #newPlayerYPos = playerYPos
 if (newPlayerXPos, newPlayerYPos) == finish and coinsCollected == numOfCoins:
     createGrid.set("Congratulations you won!")
     finished = True
 #if (newPlayerXPos, newPlayerYPos) in keys:
     #doorOpened = True
     #keys.remove((newPlayerXPos, newPlayerYPos))
 if newPlayerYPos < 1 or newPlayerYPos > gridSizeY or\
    newPlayerXPos < 1 or newPlayerXPos > gridSizeX:
     newPlayerXPos = playerXPos
     newPlayerYPos = playerYPos
 if (newPlayerXPos, newPlayerYPos) in coins:
     coinsCollected += 1
     coins.remove((newPlayerXPos, newPlayerYPos))

 playerXPos = newPlayerXPos
 playerYPos = newPlayerYPos
 if finished != True:
      Play()



def createMaze():
    global startPoint
    global playerXPos
    global playerYPos
    global oldPoint
    global spaces
    global amountOfSpaces
    global finish
    def createCandidates(oldPoint, a):
        if a == 0:
            candidate = (oldPoint[0]+1, oldPoint[1])
        elif a == 1:
            candidate = (oldPoint[0]-1, oldPoint[1])
        elif a == 2:
            candidate = (oldPoint[0], oldPoint[1]+1)
        elif a == 3:
            candidate = (oldPoint[0], oldPoint[1]-1)
        elif a == 4:
            candidate = (oldPoint[0], oldPoint[1])
        return candidate
    
    spaces = []
    startPoint = (random.randint(1, gridSizeX),random.randint(1, gridSizeY))
    oldPoint = startPoint
    spaces.append(startPoint)
    for i in range(0, amountOfSpaces):
        spots = []
        for a in range(0,4):
            spots.append(createCandidates(oldPoint, a))

        validSpots = []
        for b in range(0,4):    
            checkCandidate = spots.pop(random.randint(0, len(spots)-1))
            spacesIn = 0
            for a in range(0,5):
                if createCandidates(checkCandidate, a) in spaces:
                    spacesIn += 1
            if spacesIn == 1 and not(checkCandidate[0] < 1 or checkCandidate[1] < 1 or checkCandidate[0] > gridSizeX or checkCandidate[1] > gridSizeY):
                #print(checkCandidate,"is valid")
                validSpots.append(checkCandidate)
            #else:
                #print(checkCandidate,"not valid")

                
        if validSpots == []:
            oldPoint = spaces[random.randint(0, len(spaces)-1)]
        else:
            newSpot = validSpots[random.randint(0, len(validSpots)-1)]
            spaces.append(newSpot)
            oldPoint = newSpot
            
    finish = newSpot
    for i in range(0, numOfCoins):
        coins.append(spaces[random.randint(0, len(spaces)-1)])
    playerXPos = startPoint[0]
    playerYPos = startPoint[1]
    
    Play()


def Play():
  global startPoint
  global playerXPos
  global playerYPos
  global finish
  global newPlayerYPos
  global newPlayerXPos
  global coinsCollected
  global move
  global light
  grid = ""
  for y in range(0, gridSizeY + 2):
   for x in range(0, gridSizeX + 2):   
     if (x, y) == startPoint:
       grid += "S "
     elif (x == 0 or x == gridSizeX + 1) and (y == 0 or y == gridSizeY + 1):
         grid += "+ "
     elif x == 0 or x == gridSizeX + 1:
         grid += "| "
     elif y == 0 or y == gridSizeY + 1:
         grid += "- "
     elif x == playerXPos and y == playerYPos:
        grid += "O "
     elif (x, y) == finish and coinsCollected == numOfCoins:
       grid += "F "
     elif (x, y)  in coins:
         grid += "C "
     elif (x, y) in spaces:
       grid += "  "
     else:
       grid += "# "
   grid += "\n"
  createGrid.set(grid)
  cave.pack()
        

  def keydown(e):
    global startPoint
    global playerXPos
    global playerYPos
    global finish
    global newPlayerYPos
    global newPlayerXPos
    global coinsCollected
    global move
    global light
    if e.keysym == "Up":
        newPlayerYPos = playerYPos - 1
        newPlayerXPos = playerXPos
        lemmeMove()
    if e.keysym == "Down":
        newPlayerYPos = playerYPos + 1
        newPlayerXPos = playerXPos
        lemmeMove()
    if e.keysym == "Left":
        newPlayerXPos = playerXPos - 1
        newPlayerYPos = playerYPos
        lemmeMove()
    if e.keysym == "Right":
        newPlayerXPos = playerXPos + 1
        newPlayerYPos = playerYPos
        lemmeMove()

  frame = Frame(top, width=100, height=100)
  frame.bind("<KeyPress>", keydown)
  frame.pack()
  frame.focus_set()



cave.after(1000,createMaze)


top.mainloop()
