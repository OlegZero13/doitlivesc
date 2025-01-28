from pathlib import Path
from typing import Self

from moviepy import AudioClip, AudioFileClip, VideoFileClip, CompositeAudioClip

from .audio import AudioRecorder
from .screen import ScreenRecorder
from .music import MusicPlayer


class ScreencastContext:
    def __init__(
        self,
        path: Path,
        voice_filename: str,
        video_filename: str,
        music_filename: str = None,
        width: int = 720,
        height: int = 1280,
        x_position: int = 0,
        y_position: int = 0,
    ) -> None:
        self.path = path
        self.path.mkdir(parents=True, exist_ok=True)

        voice_filepath = path / voice_filename
        video_filepath = path / video_filename
        music_filepath = path / music_filename if music_filename is not None else None
        monitor = dict(
            top=y_position,
            left=x_position,
            width=width,
            height=height,
        )
        self.voice_recorder = AudioRecorder(voice_filepath)
        self.screen_recorder = ScreenRecorder(video_filepath, monitor)
        self.music_recorder = MusicPlayer(music_filepath) if music_filename is not None else None

    def __enter__(self) -> Self:
        self.voice_recorder.start()
        self.screen_recorder.start()
        if self.music_recorder is not None:
            self.music_recorder.start()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.voice_recorder.stop()
        self.screen_recorder.stop()
        if self.music_recorder is not None:
            self.music_recorder.stop()



    def add_background_music(self) -> None:
        video_clip = VideoFileClip(str(self.filepath))
        audio_clip = AudioFileClip(str(self.music_filepath))
        final_clip = video_clip.with_audio(audio_clip)
        final_clip.audio.duration = video_clip.duration

        final_clip.write_videofile(str(self.filepath), codec="libx264")

        audio_clip.close()
        video_clip.close()
        print("Combined")
