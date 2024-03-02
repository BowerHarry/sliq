from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
import random
import math
from kivy.uix.behaviors import ButtonBehavior
import functools
from kivy.properties import BooleanProperty
from kivy.clock import Clock
from kivy.animation import Animation
from border import Border

class BoardTile(ButtonBehavior, RelativeLayout):
    s=StringProperty()
    x=NumericProperty()
    y=NumericProperty()
    gridX=NumericProperty()
    gridY=NumericProperty()
    v=NumericProperty()
    clicked_inside = BooleanProperty(False)
    board_instance = ObjectProperty(None)

    def __init__(self, x, y, v, b, **kwargs):
        self.s='src/tile.png'
        if v in range (0,5): self.s='src/' + str(v) + '-tile.png'
        img = Image(source = self.s)
        img.size_hint_x = None
        img.size_hint_y = None
        img.size_x = 100
        img.size_y = 100
        self.x = x*100
        self.y = y*100
        self.gridX = x
        self.gridY = y
        self.v = v
        self.board_instance = b
        self.ids = {'x': x, 'y': y, 'value': v, 'object':'tile'}
        super(BoardTile, self).__init__(**kwargs)
        self.add_widget(img)


    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.clicked_inside = True
            return True
        return super(BoardTile, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.clicked_inside and not self.v==-1:
            releaseX, releaseY = touch.pos
            abs_x = self.x + 50
            self.clicked_inside = False
            if self.board_instance:
                if (abs_x + 50 < releaseX):
                    self.board_instance.moveTile(self.gridX, self.gridY, self.v, "RIGHT", self)
                elif (abs_x - 50 > releaseX):
                    self.board_instance.moveTile(self.gridX, self.gridY, self.v, "LEFT", self)
            
        return super(BoardTile, self).on_touch_up(touch)

class Board(RelativeLayout):
    length = 8+2
    game_instance = ObjectProperty(None)
    score = NumericProperty(0)
    turn = NumericProperty(1)
    border = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for i in range(1,self.length-1):
            for j in range (1,self.length-1):
                newTile = BoardTile(i, j, -1, self)
                self.add_widget(newTile)
        self.fillWithStartingGrid()
        self.newTile()
        self.newTile()
        self.newTile()
        self.newTile()
        Clock.schedule_once(lambda dt: self.update())
        

    def yield_to_sleep(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            gen = func(*args)
            def next_step(*_):
                try:
                    t = next(gen)  # this executes 'func' before next yield and returns control to you
                except StopIteration:
                    pass
                else:
                    Clock.schedule_once(next_step, t)  # having control you can resume func execution after some time
            next_step()
        return wrapper
    
    @yield_to_sleep
    def moveTile(self, x, y, value, direction, tile):
        if value != 0:
            if direction == "RIGHT":
                if self.isBorder(x+1, y) != None:
                    if self.isBorder(x+1, y) == value:
                        self.score += value
                        self.remove(x, y)
                        self.gravity(x)
                        self.update()
                    print("BORDER TILE!")
                elif self.isEmpty(x+1, y):
                    end_x, end_y = self.calcGravity(x+1, y)
                    y_duration = 0.2 * abs(y-end_y)
                    anim = Animation(x=end_x*100, y=y*100, duration=0.2) + Animation(x=end_x*100, y=end_y*100, duration = y_duration)
                    anim.start(tile)
                    yield y_duration + 0.1
                    print("SOUNDS GOOD")
                    self.remove(x, y)
                    self.add(end_x, end_y, value-1)
                    self.update()
                else:
                    print("CAN'T MOVE THERE")
            elif direction == "LEFT":
                if self.isBorder(x-1, y) != None:
                    if self.isBorder(x-1, y) == value:
                        self.score += value
                        self.remove(x, y)
                        self.gravity(x)
                        self.update()
                    print("BORDER TILE!")
                elif self.isEmpty(x-1, y):
                    end_x, end_y = self.calcGravity(x-1, y)
                    y_duration = 0.2 * abs(y-end_y)
                    anim = Animation(x=end_x*100, y=y*100, duration=0.2) + Animation(x=end_x*100, y=end_y*100, duration = y_duration)
                    anim.start(tile)
                    yield y_duration + 0.1
                    print("SOUNDS GOOD")
                    self.remove(x, y)
                    self.add(end_x, end_y, value-1)
                    self.update()
                else:
                    print("CAN'T MOVE THERE")
        self.gravity(x)
        self.update()
    
    
    def gravity(self, x):
        yOrder = 1
        while yOrder < self.length-1:
            for child in self.children:
                if (not isinstance(child, Border)):
                    if (child.ids.x) == x and (child.ids.y) == yOrder and (child.ids.value) != -1:
                        self.remove(x, child.ids.y)
                        end_x, end_y = self.calcGravity(x, child.ids.y)
                        self.add(end_x, end_y, child.ids.value)
            yOrder+=1

    @yield_to_sleep
    def rotateBorder(self):
        self.border.rotate()
        yield(1)
        self.update()
        self.newTile()
        self.newTile()
        self.newTile()
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
    
    def randomValue(self):
        return random.randint(1,4)

    def randomX(self):
        return random.randint(1,self.length-2)
    
    def calcGravity(self, x, y):
        for i in range(y, 0, -1):
            if self.isEmpty(x, i) == False:
                y = i+1
                return x,y
            elif i == 1:
                y = i
                return x, y
            

    @yield_to_sleep
    def newTile(self):
        x = self.randomX()
        y = self.length-2
        v = self.randomValue()
        tile = self.add(x, y, v)
        end_x, end_y = self.calcGravity(x, y-1)
        y_duration = 0.2 * abs(y-end_y)
        anim = Animation(x=end_x*100, y=y*100, duration=0.2) + Animation(x=end_x*100, y=end_y*100, duration = y_duration)
        anim.start(tile)
        yield y_duration + 0.1
        self.remove(x, y)
        self.add(end_x, end_y, v)
        self.update()
        print("\nNew tile at (" + str(end_x) + "," + str(end_y) + ")")
    
    def isBorder(self, x, y):
        return self.border.grid[x][y]


    def isEmpty(self, x, y):
        for child in self.children:
            if (not isinstance(child, Border)):
                if (child.ids.x) == x and (child.ids.y) == y and (child.ids.value) != -1:
                    return False
        return True
    
    

    def remove(self, x, y):
        for child in self.children:
            if (not isinstance(child, Border)):
                if (child.ids.x) == x and (child.ids.y) == y and (child.ids.value) != -1:
                    self.remove_widget(child)

    def add(self, x, y, v):
        s='src/tile.png'
        if v in range (0,5): s='src/' + str(v) + '-tile.png'
        for child in self.children:
            if (not isinstance(child, Border)):
                if (child.ids.x) == x and (child.ids.y) == y and (child.ids.value) != -1:
                    self.remove_widget(child)
                    newTile = BoardTile(x, y, v, self)
                    self.add_widget(newTile)
                    return newTile
        newTile = BoardTile(x, y, v, self)
        self.add_widget(newTile)
        return newTile


    def update(self):
        # floor case
        for child in self.children:
            if (not isinstance(child, Border)):
                if (child.ids.y) == 1 and self.border.grid[child.ids.x][0] == child.ids.value and child.ids.object=='tile':
                    points = self.border.grid[child.ids.x][0]
                    print("\n" + str(points) + " points gained. (F)(" + str(child.ids.x) + ",0)")
                    self.score += points
                    self.remove(child.ids.x, child.ids.y)
                    self.gravity(child.ids.x)
                    self.update()