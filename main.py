from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.core.window import Window
from kivy.clock import Clock
from border import Border
from board import Board


Window.size = Window.size
screenX, screenY = Window.size


class Score(Label):
    points = NumericProperty(0)


class SliqGame(Widget):
    board = ObjectProperty(None)
    score = ObjectProperty(None)
    timer = None

    def start(self):
        self.timer = Clock.schedule_interval(self.rotateBorder, 10)

        pass

    def rotateBorder(self, dt=None):
        Clock.unschedule(self.timer)
        self.board.rotateBorder()
        self.timer = Clock.schedule_interval(self.rotateBorder, 10)


class SliqApp(App):

    def build(self):
        game = SliqGame()
        game.start() # kick off game
        return game
    

if __name__ == '__main__':
    Window.clearcolor = (.9, .9, .9, 1)
    SliqApp().run()