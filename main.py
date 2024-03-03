from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.properties import BooleanProperty
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
from kivy.storage.jsonstore import JsonStore
from game import SliqGame
from kivy.utils import platform
from os.path import join

Window.size = Window.size
screenX, screenY = Window.size

# if platform == 'ios':
#     leaderboard = JsonStore(App.get_running_app().leaderboard_storage)
# else: 
#     leaderboard = JsonStore('leaderboard.json')

class SliqGameController(RelativeLayout):
    gameEnd = BooleanProperty(False)
    playagainButton = ObjectProperty(None)

    def start(self):
        self.getLeaderboard()
        self.startGame()

    def getLeaderboard(self):
        if platform == 'ios':
            self.leaderboard = JsonStore(App.get_running_app().leaderboard_storage)
        else: 
            self.leaderboard = JsonStore('leaderboard.json')

    def startGame(self):
        print("/*-------------------------------------------------*/\n                     New Game                     \n/*-------------------------------------------------*/")
        if not self.leaderboard.exists('highscore'):
            self.leaderboard.put('highscore', points=0)
        game = SliqGame(self, self.leaderboard)
        self.add_widget(game)
        game.highscore.score = self.leaderboard.get('highscore')['points']
        self.game = game

    def playAgain(self):
        self.gameEnd = False
        self.remove_widget(self.game)
        self.startGame()


class SliqApp(App):
    @property
    def leaderboard_storage(self):
        return join(self.user_data_dir, 'leaderboard.json')

    def build(self):
        controller = SliqGameController()
        controller.start()
        self.root = controller
    

if __name__ == '__main__':
    Window.clearcolor = (.9, .9, .9, 1)
    SliqApp().run()