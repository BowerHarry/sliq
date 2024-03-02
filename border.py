from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
import random
import functools
from kivy.clock import Clock
from kivy.animation import Animation

class TileVerticalEdge(RelativeLayout):
    s=StringProperty()
    x=NumericProperty()
    y=NumericProperty()

class TileHorizontalEdge(RelativeLayout):
    s=StringProperty()
    x=NumericProperty()
    y=NumericProperty()

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
        grid = self.grid
        for i in range(len(grid[0])):
            grid[0][i] = self.randomValue()
            grid[self.length-1][i] = self.randomValue()
            grid[i][0] = self.randomValue()
            grid[i][self.length-1] = self.randomValue()
        Clock.schedule_once(lambda dt: self.addBorderTiles())
        Clock.schedule_once(lambda dt: self.a0.rotate())
        Clock.schedule_once(lambda dt: self.b0.rotate())
        Clock.schedule_once(lambda dt: self.c0.rotate())
        Clock.schedule_once(lambda dt: self.d0.rotate())

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
                        self.a.add_widget(TileVerticalEdge(x=90+(x*100), y=(j*100), ids={'x': i, 'y': j, 'value':self.grid[i][j], 'object':'border'}, s=s))
                        self.a0.add_widget(TileVerticalEdge(x=90+(x*100), y=(j*100), ids={'x': i, 'y': j, 'value':self.grid[i][j], 'object':'border'}, s=s))

                    if i == self.length-1:
                        s='src/' + str(self.grid[i][j]) + '-vertical-edge.png'
                        if i == self.length-1:
                            x = i-1
                        else:
                            x = i
                        self.c.add_widget(TileVerticalEdge(x=90+(x*100), y=(j*100), ids={'x': i, 'y': j, 'value':self.grid[i][j], 'object':'border'}, s=s))
                        self.c0.add_widget(TileVerticalEdge(x=90+(x*100), y=(j*100), ids={'x': i, 'y': j, 'value':self.grid[i][j], 'object':'border'}, s=s))

                    if j == 0:
                        if j == self.length-1:
                            y = j-1
                        else:
                            y = j
                        s='src/' + str(self.grid[i][j]) + '-horizontal-edge.png'
                        self.d.add_widget(TileHorizontalEdge(x=(i*100), y=90+(y*100), ids={'x': i, 'y': j, 'value':self.grid[i][j], 'object':'border'}, s=s))
                        self.d0.add_widget(TileHorizontalEdge(x=(i*100), y=90+(y*100), ids={'x': i, 'y': j, 'value':self.grid[i][j], 'object':'border'}, s=s))


                    if j == self.length-1:
                        if j == self.length-1:
                            y = j-1
                        else:
                            y = j
                        s='src/' + str(self.grid[i][j]) + '-horizontal-edge.png'
                        self.b.add_widget(TileHorizontalEdge(x=(i*100), y=90+(y*100), ids={'x': i, 'y': j, 'value':self.grid[i][j], 'object':'border'}, s=s))
                        self.b0.add_widget(TileHorizontalEdge(x=(i*100), y=90+(y*100), ids={'x': i, 'y': j, 'value':self.grid[i][j], 'object':'border'}, s=s))

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
        print("rotating")
        anim = Animation(x = self.x, y=self.y+800, duration=1)
        anim.start(self)

    @yield_to_sleep
    def animateUpWR(self, *kwargs):
        print("rotating")
        anim = Animation(x = self.x, y=self.y+800, duration=1)
        anim.start(self)
        yield(1)
        self.rotate()
        self.rotate()
    

    def animateDown(self, *kwargs):
        print("rotating")
        anim = Animation(x = self.x, y=self.y-800, duration=1)
        anim.start(self)

    @yield_to_sleep
    def animateDownWR(self, *kwargs):
        print("rotating")
        anim = Animation(x = self.x, y=self.y-800, duration=1)
        anim.start(self)
        yield(1)
        self.rotate()
        self.rotate()

    
    def animateRight(self, *kwargs):
        print("rotating")
        anim = Animation(x = self.x + 800, y=self.y, duration=1)
        anim.start(self)
    
    def animateLeft(self, *kwargs):
        print("rotating")
        anim = Animation(x = self.x - 800, y=self.y, duration=1)
        anim.start(self)

    @yield_to_sleep
    def animateLeftWR(self, *kwargs):
        print("rotating")
        anim = Animation(x = self.x - 800, y=self.y, duration=1)
        anim.start(self)
        yield(1)
        self.rotate()
        self.rotate()
        
    @yield_to_sleep
    def animateRightWR(self, *kwargs):
        print("rotating")
        anim = Animation(x = self.x + 800, y=self.y, duration=1)
        anim.start(self)
        yield(1)
        self.rotate()
        self.rotate()
    
    def moveRight (self, *kwargs):
        self.center_x = self.center_x + 800