from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty
from kivy.clock import Clock
from kivy.app import App
import functools
from kivy.storage.jsonstore import JsonStore
from border import Border
from board import Board
from kivy.utils import platform
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
import random
import math
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
import functools
from functools import partial
from kivy.properties import BooleanProperty
from kivy.clock import Clock
from kivy.animation import Animation
from border import Border

Window.size = Window.size
screenX, screenY = Window.size

class Tile(RelativeLayout):
    s=StringProperty()
    v=NumericProperty()

    def __init__(self, v, **kwargs):
        self.s='src/' + str(v) + '-tile.png'
        img = Image(source = self.s)
        # img.size_hint_x = None
        # img.size_hint_y = None
        # img.size = (50,50)
        img.size_hint_x = .18
        img.size_hint_y = .18
        # img.size = 50, 50
        self.x = 1915
        self.size_hint_x = .1
        self.size_hint_y = .1
        # self.size = (50, 50)
        self.y = 168
        self.v = v
        super(Tile, self).__init__(**kwargs)
        self.add_widget(img)
        self.img = img

class SliqGame(RelativeLayout):
    controller = ObjectProperty(None)
    board = ObjectProperty(None)
    score = ObjectProperty(None)
    highscore = ObjectProperty(None)
    endGameMessage = ObjectProperty(None)
    rotateButton = ObjectProperty(None)
    endGameVisible = BooleanProperty(False)
    gameLost = BooleanProperty(False)
    gameWon = BooleanProperty(False)
    teddy = ObjectProperty(None)
    timer = None
    tiles_removed = []
    score_target = 100
    stars = 0

    def __init__(self, controller, leaderboard, score_target, **kwargs):
        self.controller = controller
        self.leaderboard = leaderboard
        self.score_target = score_target
        super(SliqGame, self).__init__(**kwargs)
        self.newConveyorTile()
        self.timer = Clock.schedule_interval(self.rotateBorder, 20)
        self.conveyorTimer = Clock.schedule_interval(self.newConveyorTile, 1.5)
        self.growTeddyTimer = Clock.schedule_interval(self.growTeddy, 1.1)
        
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
    
    def growTeddy(self, dt):
        if self.board.score < self.score_target:
            s = (self.board.score / self.score_target) * 100
            anim = Animation(size = (200+s, 200+s), duration = 1)
            anim.start(self.teddy)

    @yield_to_sleep
    def newConveyorTile(self, dt=None):
        if len(self.tiles_removed) > 0:
            v = self.tiles_removed[0]
            self.tiles_removed.pop(0)
            tile = Tile(v)
            self.add_widget(tile)
            anim = Animation(x=1320, y=168, duration=5) + Animation(size_hint =(0, 0), duration=1.5)
            anim &= Animation(size_hint = (.1, .1), duration=.3) + Animation(size_hint = (.19, .19), duration=.3)
            anim.start(tile)
            animTimer = Clock.schedule_interval(partial(self.checkGameEnd, anim, tile), 0.1)
            yield(7)
            self.remove_widget(tile)
            Clock.unschedule(animTimer)

    def checkGameEnd(self, anim, tile, dt):
        if self.endGameVisible:
            self.remove_widget(tile)
            anim.cancel(tile)
            Clock.unschedule(self)
    

    def start(self):
        pass

    def stop(self):
        Clock.unschedule(self.timer)
        Clock.unschedule(self.conveyorTimer)
        c = self.board.score / self.score_target
        if c >= 1:
            self.stars = 3
        elif c >= 0.65:
            self.stars = 2
        elif c >= 0.33:
            self.stars = 1
        else:
            self.stars = 0
        self.endGameVisible = True
        self.updateHighscore()
        self.controller.gameEnd = True

    

    def updateHighscore(self):
        if self.score.points > self.highscore.score:
            self.highscore.score = self.score.points
            self.leaderboard.put('highscore', points=self.highscore.score)
    
    @yield_to_sleep
    def rotateBorder(self, dt=None):
        if self.board.gameLoseConditionCheck():
            self.stop()
            self.gameLost = True
            return
        if self.board.score >= self.score_target:
            self.stop()
            self.gameWon = True
            return
        self.rotateButton.disabled = True
        Clock.unschedule(self.timer)
        self.board.rotateBorder()
        self.timer = Clock.schedule_interval(self.rotateBorder, 20)
        yield(1.5)
        self.rotateButton.disabled = False
