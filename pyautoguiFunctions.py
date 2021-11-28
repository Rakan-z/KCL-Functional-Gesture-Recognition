import pyautogui as pg

previousXY = (229,333)
nextXY = (91,363)
inXY = (99,332)
outXY = (162,331)
brightenXY = (141,361)
darkenXY = (201,360)


def previousImg():
    pg.click(previousXY)


def nextImg():
    pg.click(nextXY)


def zoomIn():
    pg.click(inXY)


def zoomOut():
    pg.click(outXY)


def Brighten():
    pg.click(brightenXY)


def Darken():
    pg.click(darkenXY)
    
    
def scrollUp():
    pg.scroll(20, x=571, y=429)  
    
    
def scrollDown():
    pg.scroll(-20, x=571, y=429) 
    
    
def scrollRight():
    pg.hscroll(-20, x=571, y=429) 
    
    
def scrollLeft():
    pg.hscroll(20, x=571, y=429) 