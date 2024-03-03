from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
import random
import functools
from kivy.clock import Clock
from kivy.animation import Animation

class BorderVerticalCover(Widget):
    pass

class BorderHorizontalCover(Widget):
    pass

class TileEdge(RelativeLayout):
    s=StringProperty()
    x=NumericProperty()
    y=NumericProperty()
    img = Image()

    def __init__(self, x, y, i, j, v, o, **kwargs):
        self.s='src/' + str(v) + '-'+ o +'-edge.png'
        img = Image(source = self.s)
        img.size_hint_x = None
        img.size_hint_y = None
        if o == "horizontal":
            self.size_x = 100
            self.size_y = 20
            img.size_x = 100
            img.size_y = 20
        elif o == "vertical":
            self.size_x = 20
            self.size_y = 100
            img.size_x = 20
            img.size_y = 100
        img.keep_ratio = False
        self.x = x
        self.y = y
        self.o = o
        self.ids = {'x': i, 'y': j, 'value': v, 'object':'border'}
        super(TileEdge, self).__init__(**kwargs)
        self.img = img
        self.add_widget(img)

class Border(RelativeLayout):
    rotationCount = 1
    a = ObjectProperty()
    a0 = ObjectProperty()
    b = ObjectProperty()
    b0 = ObjectProperty()
    c = ObjectProperty()
    c0 = ObjectProperty()
    d = ObjectProperty()
    d0 = ObjectProperty()


    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.length = 8+2
        self.grid = [[None for x in range(self.length)] for y in range(self.length)]
        self.generateRandomBorder()
        Clock.schedule_once(lambda dt: self.addBorderTiles())
        Clock.schedule_once(lambda dt: self.a0.rotate())
        Clock.schedule_once(lambda dt: self.b0.rotate())
        Clock.schedule_once(lambda dt: self.c0.rotate())
        Clock.schedule_once(lambda dt: self.d0.rotate())

    def generateRandomBorder(self):
        grid = self.grid
        for i in range(len(grid[0])):
            grid[0][i] = self.randomValue()
            grid[self.length-1][i] = self.randomValue()
            grid[i][0] = self.randomValue()
            grid[i][self.length-1] = self.randomValue()
    
    def generateNewEdge(self):
        if self.rotationCount % 4 == 1:
            self.generateNewEdgeValue(self.a, self.a0, "vertical")
        elif self.rotationCount % 4 == 2:
            self.generateNewEdgeValue(self.d, self.d0, "horizontal")
        elif self.rotationCount % 4 == 3:
            self.generateNewEdgeValue(self.c, self.c0, "vertical")
        elif self.rotationCount % 4 == 0:
            self.generateNewEdgeValue(self.b, self.b0, "horizontal")
        
    def generateNewEdgeValue(self, edge, edge0, orientation):
        flip = False
        if self.rotationCount % 4 == 2 or self.rotationCount % 4 == 3:
            flip = True
        grid = list(map(list, self.grid))
        for i in range(len(grid[0])):
            newValue = self.randomValue()
            grid[i][self.length-1] = newValue
            for child in edge.children:
                index = i
                if flip == True:
                    index = self.length - 1 - i
                if ((child.ids.x) == index and child.o == "horizontal") or ((child.ids.y) == index and child.o == "vertical"):
                    child.ids.value = newValue
                    child.img.source='src/' + str(newValue) + '-' + orientation + '-edge.png'
            for child in edge0.children:
                if ((child.ids.x) == index and child.o == "horizontal") or ((child.ids.y) == index and child.o == "vertical"):
                    child.ids.value = newValue
                    child.img.source='src/' + str(newValue) + '-' + orientation + '-edge.png'
        self.grid = grid


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
        
    def rotateAll(self, edge, edge0, plus):
        if ((self.rotationCount + plus) % 4) == 1:
            edge.animateUpWR()
            edge0.animateRight()
        elif ((self.rotationCount + plus) % 4) == 2:
            edge.animateDown()
            edge0.animateRightWR()
        elif ((self.rotationCount + plus) % 4) == 3:
            edge.animateDownWR()
            edge0.animateLeft()
        elif ((self.rotationCount + plus) % 4) == 0:
            edge.animateUp()
            edge0.animateLeftWR()

    def rotate(self):
        self.rotateAll(self.a, self.a0, 0)
        self.rotateAll(self.b0, self.b, 1)
        self.rotateAll(self.c, self.c0, 2)
        self.rotateAll(self.d0, self.d, 3)

        self.rotateBorderGrid()
        self.generateNewEdge()
        self.rotationCount+=1
        


    def randomValue(self):
        return random.randint(1,4)
    
    def rotateBorderGrid(self):
        self.grid = list(zip(*self.grid[::-1]))

    def addBorderTiles(self):
        for i in range(self.length):
            for j in range(self.length):
                if (i == 0 and j==0) or (i == self.length-1 and j == 0) or (i == 0 and j == self.length-1) or (i == self.length-1 and j == self.length-1):
                    # ignore corners
                    pass
                else:
                    if i == 0:
                        s='src/' + str(self.grid[i][j]) + '-vertical-edge.png'
                        if i == self.length-1:
                            x = i-1
                        else:
                            x = i
                        newTileEdge = TileEdge(50+(x*100), (j*100), i, j, self.grid[i][j], "vertical")
                        newTileEdge0 = TileEdge(50+(x*100), (j*100), i, j, self.grid[i][j], "vertical")
                        self.a.add_widget(newTileEdge)
                        self.a0.add_widget(newTileEdge0)

                    if i == self.length-1:
                        s='src/' + str(self.grid[i][j]) + '-vertical-edge.png'
                        if i == self.length-1:
                            x = i-1
                        else:
                            x = i
                        newTileEdge = TileEdge(50+(x*100), (j*100), i, j, self.grid[i][j], "vertical")
                        newTileEdge0 = TileEdge(50+(x*100), (j*100), i, j, self.grid[i][j], "vertical")
                        self.c.add_widget(newTileEdge)
                        self.c0.add_widget(newTileEdge0)

                    if j == 0:
                        if j == self.length-1:
                            y = j-1
                        else:
                            y = j
                        newTileEdge = TileEdge((i*100), 50+(y*100), i, j, self.grid[i][j], "horizontal")
                        newTileEdge0 = TileEdge((i*100), 50+(y*100), i, j, self.grid[i][j], "horizontal")
                        self.d.add_widget(newTileEdge)
                        self.d0.add_widget(newTileEdge0)

                    if j == self.length-1:
                        if j == self.length-1:
                            y = j-1
                        else:
                            y = j

                        newTileEdge = TileEdge((i*100), 50+(y*100), i, j, self.grid[i][j], "horizontal")
                        newTileEdge0 = TileEdge((i*100), 50+(y*100), i, j, self.grid[i][j], "horizontal")
                        self.b.add_widget(newTileEdge)
                        self.b0.add_widget(newTileEdge0)

class BorderEdge(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pass

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
    
    def rotate(self, *kwargs):
        self.angle = self.angle-90

    def animateUp(self, *kwargs):
        anim = Animation(x = self.x, y=self.y+800, duration=1)
        anim.start(self)

    @yield_to_sleep
    def animateUpWR(self, *kwargs):
        anim = Animation(x = self.x, y=self.y+800, duration=1)
        anim.start(self)
        yield(1)
        self.rotate()
        self.rotate()
    

    def animateDown(self, *kwargs):
        anim = Animation(x = self.x, y=self.y-800, duration=1)
        anim.start(self)

    @yield_to_sleep
    def animateDownWR(self, *kwargs):
        anim = Animation(x = self.x, y=self.y-800, duration=1)
        anim.start(self)
        yield(1)
        self.rotate()
        self.rotate()

    
    def animateRight(self, *kwargs):
        anim = Animation(x = self.x + 800, y=self.y, duration=1)
        anim.start(self)
    
    def animateLeft(self, *kwargs):
        anim = Animation(x = self.x - 800, y=self.y, duration=1)
        anim.start(self)

    @yield_to_sleep
    def animateLeftWR(self, *kwargs):
        anim = Animation(x = self.x - 800, y=self.y, duration=1)
        anim.start(self)
        yield(1)
        self.rotate()
        self.rotate()
        
    @yield_to_sleep
    def animateRightWR(self, *kwargs):
        anim = Animation(x = self.x + 800, y=self.y, duration=1)
        anim.start(self)
        yield(1)
        self.rotate()
        self.rotate()
    
    def moveRight (self, *kwargs):
        self.center_x = self.center_x + 800