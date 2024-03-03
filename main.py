from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.core.window import Window
from kivy.clock import Clock
import functools
from border import Border
from board import Board


Window.size = Window.size
screenX, screenY = Window.size


class Score(Label):
    points = NumericProperty(0)


class SliqGame(Widget):
    board = ObjectProperty(None)
    score = ObjectProperty(None)
    rotateButton = ObjectProperty(None)
    timer = None

    def start(self):
        self.timer = Clock.schedule_interval(self.rotateBorder, 10)

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
    def rotateBorder(self, dt=None):
        self.rotateButton.disabled = True
        Clock.unschedule(self.timer)
        self.board.rotateBorder()
        self.timer = Clock.schedule_interval(self.rotateBorder, 10)
        yield(1.5)
        self.rotateButton.disabled = False


class SliqApp(App):

    def build(self):
        game = SliqGame()
        game.start() # kick off game
        return game
    

if __name__ == '__main__':
    Window.clearcolor = (.9, .9, .9, 1)
    SliqApp().run()