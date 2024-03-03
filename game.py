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

# if platform == 'ios':
#     leaderboard = JsonStore(App.get_running_app().user_data_dir + 'leaderboard.json')
# else: 
#     leaderboard = JsonStore('leaderboard.json')

class SliqGame(Widget):
    controller = ObjectProperty(None)
    board = ObjectProperty(None)
    score = ObjectProperty(None)
    highscore = ObjectProperty(None)
    endGameMessage = ObjectProperty(None)
    rotateButton = ObjectProperty(None)
    endGameVisible = BooleanProperty(False)
    timer = None

    def __init__(self, controller, leaderboard, **kwargs):
        self.controller = controller
        self.leaderboard = leaderboard
        super(SliqGame, self).__init__(**kwargs)
    

    def start(self):
        self.timer = Clock.schedule_interval(self.rotateBorder, 20)

    def stop(self):
        Clock.unschedule(self.timer)
        self.endGameVisible = True
        self.updateHighscore()
        self.controller.gameEnd = True

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

    def updateHighscore(self):
        if self.score.points > self.highscore.score:
            self.highscore.score = self.score.points
            self.leaderboard.put('highscore', points=self.highscore.score)
    
    @yield_to_sleep
    def rotateBorder(self, dt=None):
        if self.board.gameLoseConditionCheck():
            self.stop()
            return
        self.rotateButton.disabled = True
        Clock.unschedule(self.timer)
        self.board.rotateBorder()
        self.timer = Clock.schedule_interval(self.rotateBorder, 20)
        yield(1.5)
        self.rotateButton.disabled = False
