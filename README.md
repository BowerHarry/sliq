# <img src="https://github.com/BowerHarry/sliq/blob/main/README/icon.png" width="200">
<b>! Currently in development !</b></br></br>
SLIQ is a great new puzzle game being developed for iOS, with a view for future multi-platform releases.</br></br>
The plan is for SLIQ to be published to the App Store in 2024. Both the code, and the Xcode project will remain available online. Any questions or collaborations are welcome.</br> 

## Xcode Build
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

## Source Code Prerequisites

## Toolchain Build (Kivy)
SLIQ is developed in Python, mostly using the Kivy library. Kivy has the potential to be great because (with care) the same code can theoretically be deployed to iOS, WatchOS, MacOS, Windows, Linux, Android etc. However, in practice, this can sometimes be very tough and building the code can be particularly temperamental. Below are some steps which have worked for me. Any advice in this particular area is very welcome, I have spent a very long time fighting with Toolchain builds.

```
pip install virtualenv
```
```
mkdir _environments
mkdir _builds
cd _environments
```
```
python3.11 -m venv venv-sliq
```
```
source venv-sliq/bin/activate
```

```
pip install kivy-ios
toolchain build kivy
```
```
toolchain status
```
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
```
cd ..
cd _builds
```

```
toolchain create sliq <sliq_filepath_main.py>
```

This will build an Xcode project. See Xcode build.
## Gameplay

#### The board
<p align="left">
  <img src="https://github.com/BowerHarry/sliq/blob/main/README/board.png" width="400">
</p>


#### Tiles
<p align="left">
  <img src="https://github.com/BowerHarry/sliq/blob/main/README/4-tile.png" width="100">
  <img src="https://github.com/BowerHarry/sliq/blob/main/README/3-tile.png" width="100">
  <img src="https://github.com/BowerHarry/sliq/blob/main/README/2-tile.png" width="100">
  <img src="https://github.com/BowerHarry/sliq/blob/main/README/1-tile.png" width="100">
  <img src="https://github.com/BowerHarry/sliq/blob/main/README/0-tile.png" width="100">
</p>

#### Tiles moving
<p align="left">
  <img src="https://github.com/BowerHarry/sliq/blob/main/README/tile-moving.gif" width="400">
</p>

#### Scoring points
+3 POINTS
<p align="left">
  <img src="https://github.com/BowerHarry/sliq/blob/main/README/scoring-points.gif" width="200">
</p>

+2 POINTS
<p align="left">
  <img src="https://github.com/BowerHarry/sliq/blob/main/README/score-points-edge.gif" width="100">
</p>


#### Board rotating
<p align="left">
  <img src="https://github.com/BowerHarry/sliq/blob/main/README/board-rotate-readme.gif" width="400">
</p>


#### Feed the hungry bear!

<p align="left">
  <img src="https://github.com/BowerHarry/sliq/blob/main/README/feeding-bear.gif" width="400">
</p>

#### Winning a level

<p align="left">
  <img src="https://github.com/BowerHarry/sliq/blob/main/README/filled-head.png" width="50">
  <img src="https://github.com/BowerHarry/sliq/blob/main/README/filled-head.png" width="50">
  <img src="https://github.com/BowerHarry/sliq/blob/main/README/filled-head.png" width="50">
</p>
<p align="left">
  <img src="https://github.com/BowerHarry/sliq/blob/main/README/body.png" width="100">
</p>

<p align="left">
  <img src="https://github.com/BowerHarry/sliq/blob/main/README/filled-head.png" width="50">
  <img src="https://github.com/BowerHarry/sliq/blob/main/README/filled-head.png" width="50">
  <img src="https://github.com/BowerHarry/sliq/blob/main/README/empty-head.png" width="50">
</p>

## Known Bugs

## License


