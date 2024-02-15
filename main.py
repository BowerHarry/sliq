from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.graphics import Rectangle, Color
from kivy.core.window import Window
from operator import itemgetter

Window.size = 640, 1200


class BoardTile(RelativeLayout):
    pass

class Board(Widget):
    pass

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for i in range(0,8):
            for j in range (0,8):
                self.add_widget(BoardTile(x=220+(i*100), y=400+(j*100), ids={'x': i, 'y': j}))

    def remove(self, x, y):
        for child in self.children:
            if (child.ids.x) == x and (child.ids.y) == y:
                self.remove_widget(child)

    def change(self, x, y, value):
        for child in self.children:
            if (child.ids.x) == x and (child.ids.y) == y:
                self.remove_widget(child)


class SliqGame(Widget):
    board = ObjectProperty(None)

    #player.score = 0
    def start(self):
        pass
            

class SliqApp(App):
    def build(self):
        game = SliqGame()
        game.start() # kick off game
        return game


if __name__ == '__main__':
    #Window.clearcolor = (.5, .5, .5, 1)
    SliqApp().run()
