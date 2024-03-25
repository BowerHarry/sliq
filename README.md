# <img src="https://github.com/BowerHarry/sliq/blob/main/README/icon.png" width="200">
<b>! Currently in development !</b></br></br>
SLIQ is a great new puzzle game being developed for iOS, with a view for future multi-platform releases.</br></br>
The plan is for SLIQ to be published to the App Store in 2024. Both the code, and the Xcode project will remain available online. Any questions or collaborations are welcome.</br> 

## Table of Contents
- [Toolcahin Build (Kivy)](README.md#toolchain-build-kivy)
- [Xcode Build/Deployment](README.md#xcode-build-deployment)
- [Gameplay](README.md#gameplay)
     - [The Board](README.md#the-board)
     - [Scoring Points](README.md#scoring-points)
     - [Rotating the Board](README.md#rotating-the-board)
     - [Winning a Level](README.md#winning-a-level)
- [Known Bugs](README.md#known-bugs)
- [License](README.md#license)

## Toolchain Build (Kivy)
This section contains instructions to build the Python project into an Xcode project (presumably after making some changes). If you wish to deploy the latest Xcode build to your device - skip to the [Xcode Build/Deployment section](README.md#xcode-build-deployment).</br></br>
SLIQ is developed in Python, mostly using the Kivy library. Kivy has the potential to be great because (with care) the same code can theoretically be deployed to iOS, WatchOS, MacOS, Windows, Linux, Android etc. However, in practice, this can sometimes be very tough and building the code can be particularly temperamental. Below are some steps which have worked for me. Any advice in this particular area is very welcome, I have spent a very long time fighting with Toolchain builds.

Clone the repository:
```
git clone https://github.com/BowerHarry/sliq.git
```
Prerequisites:
```
brew install autoconf automake libtool pkg-config
brew link libtool
```
Using a Python virtual environment minimises conflicts with preinstalled libraries.
```
pip install virtualenv
```
Setup file structure in preferred location:
```
mkdir _environments
mkdir _builds
cd _environments
```
Create a Python virtual environment:
```
python3.11 -m venv venv-sliq
```
Activate virtual environment:
```
source venv-sliq/bin/activate
```
Install dependencies (whilst venv is active):
```
pip install Cython==3.0.0
pip install kivy-ios
toolchain build kivy
```
Check the status of the required files:
```
toolchain status
```
The output should be the same as the output below. If anything is not built, you can manually build it using "toolchain build <library-name>":
```
audiostream  - Not built
click        - Not built
curly        - Not built
cymunk       - Not built
ffmpeg       - Not built
ffpyplayer   - Not built
flask        - Not built
freetype     - Build OK (built at 2024-02-22 16:48:48.310601)
hostopenssl  - Build OK (built at 2024-02-22 16:40:48.460346)
hostpython3  - Build OK (built at 2024-02-22 16:43:38.379137)
ios          - Build OK (built at 2024-02-22 16:46:11.515884)
itsdangerous - Not built
jinja2       - Not built
kivent_core  - Not built
kivy         - Build OK (built at 2024-02-22 16:48:08.447449)
kiwisolver   - Not built
libcurl      - Not built
libffi       - Build OK (built at 2024-02-22 16:41:33.733359)
libjpeg      - Build OK (built at 2024-02-22 16:48:59.890444)
libpng       - Build OK (built at 2024-02-22 16:41:45.708015)
libzbar      - Not built
markupsafe   - Not built
matplotlib   - Not built
netifaces    - Not built
numpy        - Not built
openssl      - Build OK (built at 2024-02-22 16:42:18.091667)
photolibrary - Not built
pillow       - Build OK (built at 2024-02-22 16:49:42.167376)
plyer        - Not built
py3dns       - Not built
pycrypto     - Not built
pykka        - Not built
pyobjus      - Build OK (built at 2024-02-22 16:46:30.057945)
python3      - Build OK (built at 2024-02-22 16:57:14.309049)
pyyaml       - Not built
sdl2         - Build OK (built at 2024-02-22 16:42:36.785922)
sdl2_image   - Build OK (built at 2024-02-22 16:43:47.061092)
sdl2_mixer   - Build OK (built at 2024-02-22 16:43:55.553344)
sdl2_ttf     - Build OK (built at 2024-02-22 16:44:11.741270)
werkzeug     - Not built
zbarlight    - Not built
```
Navigate to build folder:
```
cd ..
cd _builds
```
Create the Xcode project:
```
toolchain create sliq <sliq_filepath_main.py>
```

This will build an iOS Xcode project. See [Xcode Build/Deployment section](README.md#xcode-build-deployment).

## Xcode Build/ Deployment
This section contains instructions on how to build the Xcode project and deploy it to your device. Apple Developer Program membership not required.</br></br>
Clone the repository:
```
git clone https://github.com/BowerHarry/sliq.git
```
Change to the build directory:
```
cd sliq/sliq01-ios
```
Open the Xcode build
```
xed .
```
#### Install on iOS device
1. Rename Xcode to Xcode15
2. Plug in iOS device
3. Choose device from the dropdown menu
4. Click Build (you might be asked for your devices password)

#### Run with an iOS simulator
1. Choose a simulator from the dropdown menu
2. Click Build
   
## Gameplay
This section will provide instructions on how to play SLIQ. SLIQ is still being developed so this is subject to change.</br></br>
Every SLIQ level has a target score - level difficulty is established by the target score and game-speed. Perfecting a level with earn 3 severed bear-heads. Perform well in these levels to earn more severed heads to unlock more levels!</br></br>
Freeplay offers the player the chance to play an endless, casual level and aim for a highscore! 
### The Board
This is the game board. There are two key components: Tiles, and the Border.
<p align="left">
  <img src="https://github.com/BowerHarry/sliq/blob/main/README/board.png" width="400">
</p>

#### Tiles
Tiles are the building blocks of SLIQ. The number on the tile corresponds to the <b>number of moves</b> that tile can make AND its <b>value</b>.
<p align="left">
  <img src="https://github.com/BowerHarry/sliq/blob/main/README/4-tile.png" width="100">
  <img src="https://github.com/BowerHarry/sliq/blob/main/README/3-tile.png" width="100">
  <img src="https://github.com/BowerHarry/sliq/blob/main/README/2-tile.png" width="100">
  <img src="https://github.com/BowerHarry/sliq/blob/main/README/1-tile.png" width="100">
  <img src="https://github.com/BowerHarry/sliq/blob/main/README/0-tile.png" width="100">
</p>

#### The border
The border refers to the colours at the edge of the game board. These colours match the colours on the tiles. If a tile matches the colour of the border beneath it it will fall through and you score points equal to the tiles value. This will become much clearer in the next section.


### Scoring Points
Points are scored by moving tiles so that their colour matches the border colour. When this happens the tile will fall through and you score points! Lets look at how to move tiles:
#### Moving a tile
You can move a tile by swiping on it, left or right. When you move a tile the number on it will decrease by 1. If a tile reaches a value of 0 it cannot be moved and will remain there for the rest of the level (you will want to avoid this where possible).
<p align="left">
  <img src="https://github.com/BowerHarry/sliq/blob/main/README/tile-moving.gif" width="400">
</p>

#### Gaining points
In this example we have a 4-tile. No points are being scored because the colour of the tile does not match the border beneath it. When we move the tile to the right, it changes to a 3-tile as we have used one of its movement points. This now matches the colour of the border beneath and it falls through, scoring 3 POINTS!
<p align="left">
  <img src="https://github.com/BowerHarry/sliq/blob/main/README/scoring-points.gif" width="200">
</p>
In this example we have a 2-tile. No points are being scored because the colour of the tile does not match the border beneath it. However, the border edge on the right of the tile is the same colour. We can move the tile right into the border and score 2 POINTS!
<p align="left">
  <img src="https://github.com/BowerHarry/sliq/blob/main/README/score-points-edge.gif" width="100">
</p>

### Rotating the Board
When we press the lever attached to the border, the whole border rotates clockwise and new tiles drop down from the ceiling!</br></br> You'll soon learn that looking 1 or 2 board rotations into the future is necessary to survive harder levels. </br></br>Also, the board will rotate automatically if no move has been played for a given period of time. The frequency of this auto-rotation is level dependant and massively impacts difficulty.
<p align="left">
  <img src="https://github.com/BowerHarry/sliq/blob/main/README/board-rotate-readme.gif" width="400">
</p>
Watch the board rotate one more time. When tiles pass through the top-left-most corner they are regenerated to a new colour.

### Winning a Level
Whilst playing SLIQ the aim of the game is to feed the bear tiles. He's oh so hungry and boy does he not know when he is full. Make sure to feed the bear enough tiles before the clock hits 0. The level ends when the timer hits 0 or your board gets so full that tiles are touching the ceiling when the borde rotates. If you've done well you will be in for a treat, and more severed bear heads for you.
#### Feeding the bear
When tiles drop through the game border they end up on the happy bear's plate. Make sure to feed him more, he's hungry.
<p align="left">
  <img src="https://github.com/BowerHarry/sliq/blob/main/README/feeding-bear.gif" width="400">
</p>

#### End of the level
Each level will have a target score. If you reach this score when the level ends you will earn 3 bear heads!
<p align="left">
  <img src="https://github.com/BowerHarry/sliq/blob/main/README/filled-head.png" width="50">
  <img src="https://github.com/BowerHarry/sliq/blob/main/README/filled-head.png" width="50">
  <img src="https://github.com/BowerHarry/sliq/blob/main/README/filled-head.png" width="50">
</p>

If the bear is left hungry you will earn fewer heads.
<p align="left">
  <img src="https://github.com/BowerHarry/sliq/blob/main/README/filled-head.png" width="50">
  <img src="https://github.com/BowerHarry/sliq/blob/main/README/filled-head.png" width="50">
  <img src="https://github.com/BowerHarry/sliq/blob/main/README/empty-head.png" width="50">
</p>

## Known Bugs
- [ ] New tiles overloading the board when full (resolution identified) https://github.com/BowerHarry/sliq/issues/1
- [ ] Moving a tile into another tile <0.2s before it's animation was due to finish causes weird behaviour (potential resolution identified) https://github.com/BowerHarry/sliq/issues/2
## License
This project is provided under the MIT License. See LICENSE.txt.

