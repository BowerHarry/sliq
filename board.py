from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
import random
import math
from kivy.uix.behaviors import ButtonBehavior
import functools
from functools import partial
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

    def __init__(self, x, y, v, b, newTile, **kwargs):
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
        self.newTile = newTile
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
    
class Timer():
    time_elapsed = 0

    def increment_time(self, interval):
        self.time_elapsed += .1

class TriggerReturn():
    addedByTrigger = False

class Board(RelativeLayout):
    length = 8+2
    game_instance = ObjectProperty(None)
    score = NumericProperty(0)
    turn = NumericProperty(1)
    border = ObjectProperty()
    events = {}
    events_timeElapsed = {}
    tiles_dropping = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for i in range(1,self.length-1):
            for j in range (1,self.length-1):
                newTile = BoardTile(i, j, -1, self, False)
                self.add_widget(newTile)
        self.fillWithStartingGrid()
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
                        print("\n" + str(value) + " points gained. (R)(" + str(x) + ","+ str(y) +")")
                        self.gravity(x)
                        self.update()
                    # print("BORDER TILE!")
                elif self.isEmpty(x+1, y):
                    end_x, end_y = self.calcGravity(x+1, y)
                    y_duration = 0.2 * abs(y-end_y)
                    anim = Animation(x=end_x*100, y=y*100, duration=0.2) + Animation(x=end_x*100, y=end_y*100, duration = y_duration)
                    anim.start(tile)
                    yield y_duration + 0.1
                    # print("SOUNDS GOOD")
                    self.remove(x, y)
                    self.add(end_x, end_y, value-1)
                    self.update()
                else:
                    pass
                    # print("CAN'T MOVE THERE")
            elif direction == "LEFT":
                if self.isBorder(x-1, y) != None:
                    if self.isBorder(x-1, y) == value:
                        self.score += value
                        self.remove(x, y)
                        print("\n" + str(value) + " points gained. (L)(" + str(x) + ","+ str(y) +")")
                        self.gravity(x)
                        self.update()
                    # print("BORDER TILE!")
                elif self.isEmpty(x-1, y):
                    end_x, end_y = self.calcGravity(x-1, y)
                    y_duration = 0.2 * abs(y-end_y)
                    anim = Animation(x=end_x*100, y=y*100, duration=0.2) + Animation(x=end_x*100, y=end_y*100, duration = y_duration)
                    anim.start(tile)
                    yield y_duration + 0.1
                    # print("SOUNDS GOOD")
                    self.remove(x, y)
                    self.add(end_x, end_y, value-1)
                    self.update()
                else:
                    pass
                    # print("CAN'T MOVE THERE")
        self.gravity(x)
        self.update()
    
    
    def gravity(self, x):
        yOrder = 1
        while yOrder < self.length-1:
            for child in self.children:
                if (not isinstance(child, Border)):
                    if (child.ids.x) == x and (child.ids.y) == yOrder and (child.ids.value) != -1 and (child.newTile) == False:
                        self.remove(x, child.ids.y)
                        end_x, end_y = self.calcGravity(x, child.ids.y)
                        self.add(end_x, end_y, child.ids.value)
            yOrder+=1

    @yield_to_sleep
    def rotateBorder(self):
        self.border.rotate()
        yield(1)
        self.update()
        Clock.schedule_once(self.newTile, 0.3)
        yield(0.3)
        Clock.schedule_once(self.newTile, 0.3)
        yield(0.3)
        # self.newTile()
        # self.newTile()
        for i in range(math.ceil(self.turn/2)):
            if i < 7:
                Clock.schedule_once(self.newTile, 0.3)
            yield(0.3)
        self.update()
        self.turn += 1
        self.tiles_dropping.clear()

    def gameLoseConditionCheck(self):
        for i in range (1, self.length-1):
            if not self.isEmptyLose(i, self.length-2):
                return True
        return False


    @yield_to_sleep
    def fillWithStartingGrid(self):
        self.add(1, 1, 4)
        self.add(2, 1, 1)
        self.add(2, 2, 2)
        #board.add(Tile(3, 7, 0))
        self.add(6, 1, 3)
        self.add(6, 2, 4)
        self.add(7, 1, 4)
        Clock.schedule_once(self.newTile, 0.3)
        yield(0.3)
        Clock.schedule_once(self.newTile, 0.3)
        yield(0.3)
        Clock.schedule_once(self.newTile, 0.3)
        yield(0.3)
        Clock.schedule_once(self.newTile, 0.3)
        yield(0.3)
        
        self.tiles_dropping.clear()
        
        
    
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
    def newTile(self, widget):
        x = self.randomX()
        y = self.length-2
        v = self.randomValue()
        end_x, end_y = self.calcGravity(x, y-1)
        if end_y > 8:
            return
        tile = self.add(x, y, v, True)
        
        if (end_x, end_y) in self.tiles_dropping:
            end_y +=1
        self.tiles_dropping.append((end_x, end_y))
        y_duration = 0.2 * abs(y-end_y)
        anim = Animation(x=end_x*100, y=end_y*100, duration = y_duration)
        anim.start(tile)
        timer = Timer()
        Clock.schedule_interval(timer.increment_time, .1)
        self.events_timeElapsed[tile] = timer
        tr = TriggerReturn()
        def callback(value):
            tr.addedByTrigger  = value

        self.events[tile] = (Clock.schedule_interval(partial(self.checkAnimY, x, y-1, end_y, anim, tile, v, callback), 0.05), 0)
        
        
        yield y_duration
        try:
            clock, n = self.events[tile]
            t = self.events_timeElapsed[tile]
            Clock.unschedule(clock)
            Clock.unschedule(t)
            self.events.pop(tile)
            self.events_timeElapsed.pop(t)
        except:
            pass
        

        self.remove_widget(tile)
        if tr.addedByTrigger == False:
            self.add(end_x, end_y, v)
        else:
            pass
        self.gravity(x)
        self.update()
        
        print("\nNew tile at (" + str(end_x) + "," + str(end_y) + ")")

    @yield_to_sleep
    def checkAnimY(self, x, y, currentEnd_Y, anim, tile, v, callback, dt):
        end_x, end_y = self.calcGravity(x, y)
        if end_y > 8:
            callback(True)
            return
        if (x, end_y) in self.tiles_dropping and end_y != currentEnd_Y:
            end_y += 1
            if end_y > 8:
                callback(True)
                return
            self.tiles_dropping.append((end_x, end_y))
        if end_y > currentEnd_Y:
            t = 0.2
            try:
                clock, n = self.events[tile]
                t = self.events_timeElapsed[tile]
                Clock.unschedule(clock)
                Clock.unschedule(t)
                self.events.pop(tile)
                self.events_timeElapsed.pop(t)
            except:
                pass

            anim.cancel(tile)
            y_duration = abs(anim.duration - t.time_elapsed - (0.2*(end_y-currentEnd_Y)))
            anim2 = Animation(x=end_x*100, y=end_y*100, duration=y_duration)
            anim2.start(tile)
            yield(y_duration)
            self.add(end_x, end_y, v)
            callback(True)
        
    
    def isBorder(self, x, y):
        return self.border.grid[x][y]


    def isEmpty(self, x, y):
        for child in self.children:
            if (not isinstance(child, Border)):
                if (child.ids.x) == x and (child.ids.y) == y and (child.ids.value) != -1:
                    return False
        return True
    
    def isEmptyLose(self, x, y):
        for child in self.children:
            if (not isinstance(child, Border)):
                if (child.ids.x) == x and (child.ids.y) == y and (child.ids.value) != -1 and (child.newTile) == False:
                    return False
        return True
    
    

    def remove(self, x, y):
        for child in self.children:
            if (not isinstance(child, Border)):
                if (child.ids.x) == x and (child.ids.y) == y and (child.ids.value) != -1:
                    self.remove_widget(child)

    def add(self, x, y, v, newTile=False):
        # for child in self.children:
        #     if (not isinstance(child, Border)):
        #         if (child.ids.x) == x and (child.ids.y) == y and (child.ids.value) != -1 and (child.ids.value) >= 1:
                    # self.remove_widget(child)
                    # newTile = BoardTile(x, y, v, self, newTile)
                    # self.add_widget(newTile)
                    # return newTile
                
        newTile = BoardTile(x, y, v, self, newTile)
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