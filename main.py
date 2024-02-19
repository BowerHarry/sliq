from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label

from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import (
    NumericProperty, ObjectProperty
)
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
import random
import math
import numpy
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import BooleanProperty

Window.size = 640, 1200

class BoardTile(ButtonBehavior, RelativeLayout):
    s=StringProperty()
    x=NumericProperty()
    y=NumericProperty()
    gridX=NumericProperty()
    gridY=NumericProperty()
    v=NumericProperty()
    clicked_inside = BooleanProperty(False)
    board_instance = ObjectProperty(None) 

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.clicked_inside = True
            return True
        return super(BoardTile, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.clicked_inside and not self.collide_point(*touch.pos) and not self.v==-1:
            releaseX, releaseY = touch.pos
            self.clicked_inside = False
            # print("Mouse click at ({}, {})".format(self.x, self.y))
            # print("Mouse click released at ({}, {})".format(releaseX, releaseY))
            if self.board_instance:
                if (self.x + 10 < releaseX):
                    self.board_instance.moveTile(self.gridX, self.gridY, self.v, "RIGHT")
                elif (self.x - 10 > releaseX):
                    self.board_instance.moveTile(self.gridX, self.gridY, self.v, "LEFT")
            
        return super(BoardTile, self).on_touch_up(touch)

class Score(Label):
    points = NumericProperty(0)

class TileVerticalEdge(RelativeLayout):
    s=StringProperty()
    x=NumericProperty()
    y=NumericProperty()

class TileHorizontalEdge(RelativeLayout):
    s=StringProperty()
    x=NumericProperty()
    y=NumericProperty()

class Border:
    def __init__(self, length):
        self.length = length
        self.grid = [[None for x in range(length)] for y in range(length)]
        grid = self.grid
        for i in range(len(grid[0])):
            grid[0][i] = self.randomValue()
            grid[length-1][i] = self.randomValue()
            grid[i][0] = self.randomValue()
            grid[i][length-1] = self.randomValue()

    def randomValue(self):
        return random.randint(1,4)
    
    def print(self):
        g = self.grid
        grid = [[None for x in range(self.length)] for y in range(self.length)]
        for i in range(self.length):
            for j in range(self.length):
                if g[i][j] == None:
                    grid[i][j] = 0
                else:
                    grid[i][j] = g[i][j]
        
        for i in grid:
            print(i)

    def rotate(self):
        self.grid = numpy.rot90(self.grid, -1)

class Board(Widget):
    length = 8+2
    border = Border(length)
    game_instance = ObjectProperty(None)
    score = NumericProperty(0)
    turn = NumericProperty(1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for i in range(1,self.length-1):
            for j in range (1,self.length-1):
                self.add_widget(BoardTile(x=120+(i*100), y=300+(j*100), ids={'x': i, 'y': j, 'value':-1, 'object':'tile'}, s='src/tile.png', v=-1, gridX= i, gridY=j, board_instance=self))
        self.fillWithStartingGrid()
        print(self.newTile())
        print(self.newTile())
        print(self.newTile())
        print(self.newTile())
        self.drawBorder()
        self.update()

    def moveTile(self, x, y, value, direction):
        if value != 0:
            if direction == "RIGHT":
                if self.isBorder(x+1, y) != -1 and self.isBorder(x+1, y) == value:
                    self.score += value
                    self.add(x, y, -1)
                    self.gravity(x)
                    self.update()
                    print("BORDER TILE!")
                elif self.isEmpty(x+1, y):
                    print("SOUNDS GOOD")
                    self.add(x, y, -1)
                    self.addWithGravity(x+1, y, value-1)
                    self.update()
                else:
                    print("CAN'T MOVE THERE")
            elif direction == "LEFT":
                if self.isBorder(x-1, y) != -1 and self.isBorder(x-1, y) == value:
                    self.score += value
                    self.add(x, y, -1)
                    self.gravity(x)
                    self.update()
                    print("BORDER TILE!")
                elif self.isEmpty(x-1, y):
                    print("SOUNDS GOOD")
                    self.add(x, y, -1)
                    self.addWithGravity(x-1, y, value-1)
                    self.update()
                else:
                    print("CAN'T MOVE THERE")
        self.gravity(x)
        self.update()
    
    def gravity(self, x):
        yOrder = 1
        while yOrder < self.length-1:
            for child in self.children:
                if (child.ids.x) == x and (child.ids.y) == yOrder and (child.ids.value) != -1:
                    self.add(x, child.ids.y, -1)
                    self.addWithGravity(child.ids.x, child.ids.y, child.ids.value)
            yOrder+=1

    def rotateBorder(self):
        self.border.rotate()
        self.removeBorder()
        self.drawBorder()
        print(self.newTile())
        print(self.newTile())
        print(self.newTile())
        for i in range(math.ceil(self.turn/2)):
            print(self.newTile())
        self.update()
        self.turn += 1

    def fillWithStartingGrid(self):
        self.add(1, 1, 4)
        self.add(2, 1, 1)
        self.add(2, 2, 2)
        #board.add(Tile(3, 7, 0))
        self.add(6, 1, 3)
        self.add(6, 2, 4)
        self.add(7, 1, 4)

    def removeBorder(self):
        for child in self.children:
            if (child.ids.x) == 0 or (child.ids.y) == self.length-1 or (child.ids.y) == 0 or (child.ids.x) == self.length-1:
                self.remove_widget(child)
    
    def drawBorder(self):
        for i in range(self.length):
            for j in range(self.length):
                if (i == 0 and j==0) or (i == self.length-1 and j == 0) or (i == 0 and j == self.length-1) or (i == self.length-1 and j == self.length-1):
                    # ignore corners
                    pass
                else:
                    if i == 0 or i == self.length-1:
                        s='src/' + str(self.border.grid[i][j]) + '-vertical-edge.png'
                        if i == self.length-1:
                            x = i-1
                        else:
                            x = i
                        self.add_widget(TileVerticalEdge(x=170+(x*100), y=300+(j*100), ids={'x': i, 'y': j, 'value':self.border.grid[i][j], 'object':'border'}, s=s))
                    if j == 0 or j == self.length-1:
                        if j == self.length-1:
                            y = j-1
                        else:
                            y = j
                        s='src/' + str(self.border.grid[i][j]) + '-horizontal-edge.png'
                        self.add_widget(TileHorizontalEdge(x=120+(i*100), y=350+(y*100), ids={'x': i, 'y': j, 'value':self.border.grid[i][j], 'object':'border'}, s=s))

    
    def randomValue(self):
        return random.randint(1,4)

    def randomX(self):
        return random.randint(1,self.length-2)
    
    def addWithGravity(self, x, y, v):
        for i in range(y, 0, -1):
            if self.isEmpty(x, i) == False:
                y = i+1
                self.add(x, y, v)
                return("\nNew tile at (" + str(x) + "," + str(y) + ")")
                
            elif i == 1:
                y = i
                self.add(x, y, v)
                return("\nNew tile at (" + str(x) + "," + str(y) + ")")

    def newTile(self):
        x = self.randomX()
        y = self.length-2
        v = self.randomValue()
        for i in range(self.length-2, 0, -1):
            if self.isEmpty(x, i) == False:
                y = i+1
                self.add(x, y, v)
                return("\nNew tile at (" + str(x) + "," + str(y) + ")")
                
            elif i == 1:
                y = i
                self.add(x, y, v)
                return("\nNew tile at (" + str(x) + "," + str(y) + ")")
        return ("failed")
    
    def isBorder(self, x, y):
        for child in self.children:
            if (child.ids.x) == x and (child.ids.y) == y and (child.ids.object) == "border":
                return child.ids.value
        return -1


    def isEmpty(self, x, y):
        for child in self.children:
            if (child.ids.x) == x and (child.ids.y) == y and (child.ids.value) == -1:
                return True
        return False
    


    def remove(self, x, y):
        for child in self.children:
            if (child.ids.x) == x and (child.ids.y) == y:
                self.remove_widget(child)

    def add(self, x, y, value):
        s='src/tile.png'
        if value in range (0,5):
            s='src/' + str(value) + '-tile.png'
        for child in self.children:
            if (child.ids.x) == x and (child.ids.y) == y:
                self.remove_widget(child)
                self.add_widget(BoardTile(x=120+(x*100), y=300+(y*100), ids={'x': x, 'y': y, 'value': value, 'object':'tile'}, s=s, v=value, gridX= x, gridY=y, board_instance=self))

    def update(self):
        # floor case
        for child in self.children:
            if (child.ids.y) == 1 and self.border.grid[child.ids.x][0] == child.ids.value and child.ids.object=='tile':
                points = self.border.grid[child.ids.x][0]
                print("\n" + str(points) + " points gained. (F)(" + str(child.ids.x) + ",0)")
                self.score += points
                self.add(child.ids.x, child.ids.y, -1)
                self.gravity(child.ids.x)
                self.update()
                # print(self.border.grid[child.ids.x][0])


class SliqGame(Widget):
    board = ObjectProperty(None)
    score = ObjectProperty(None)

    def start(self):
        pass

    def rotateBorder(self):
        self.board.rotateBorder()

            

class SliqApp(App):

    def build(self):
        game = SliqGame()
        game.start() # kick off game
        # Clock.schedule_interval(game.update, 5)
        return game
    

if __name__ == '__main__':
    #Window.clearcolor = (.5, .5, .5, 1)
    SliqApp().run()
    
