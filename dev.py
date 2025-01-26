from pathlib import Path
from time import sleep

from doitlive.screencast import ScreenCaster


PATH = Path("videos/dev.mp4")
MUSIC_PATH = Path("videos/jazz.mp3")


def emulate_script(seconds):
    for i in range(seconds):
        print(i)
        sleep(1.0)

    print("Done")


context = ScreenCaster(
    filepath=PATH,
    music_filepath=MUSIC_PATH,
    x_position=1394,
    y_position=37,
)
with context as screencaster:
    emulate_script(3)

