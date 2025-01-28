from pathlib import Path
from time import sleep

from doitlive.screencast import ScreencastContext


PATH = Path("videos")
MUSIC_FILEPATH = "music/jazz.mp3"
VOICE_FILENAME = "microphone_recording.wav"
VIDEO_FILENAME = "screencast.mp4"


def emulate_script(seconds):
    for i in range(seconds):
        print(i)
        sleep(1.0)

    print("Done")


context = ScreencastContext(
    path=PATH,
    voice_filename=VOICE_FILENAME,
    video_filename=VIDEO_FILENAME,
    music_filename=MUSIC_FILEPATH,
    x_position=1394,
    y_position=37,
)
with context as sc:
    emulate_script(5)

