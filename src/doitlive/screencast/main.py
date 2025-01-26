import threading
from pathlib import Path
import time
from typing import Self

import cv2
import numpy as np
from moviepy import AudioClip, AudioFileClip, VideoFileClip, CompositeAudioClip
import mss
import pygame


class ScreenCaster:
    def __init__(
        self,
        filepath: Path,
        music_filepath: Path = None,
        width: int = 720,
        height: int = 1280,
        x_position: int = 0,
        y_position: int = 0,
    ) -> None:
        filepath.parent.mkdir(parents=True, exist_ok=True)

        self.filepath = filepath
        self.music_filepath = music_filepath
        self.width = width
        self.height = height
        self.x_position = x_position
        self.y_position = y_position

        self._fps = 20
        self._codec = cv2.VideoWriter_fourcc(*"XVID")
        self._buffer = None
        self._is_recording = False
        self._recoding_thread = None

    def record(self) -> None:
        monitor = {"top": self.y_position, "left": self.x_position, "width": self.width, "height": self.height}
        with mss.mss() as sct:
            frame_duration = 1 / self._fps

            while self._is_recording:
                start_time = time.time()

                img = sct.grab(monitor)
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self._buffer.write(frame)

                elapsed_time = time.time() - start_time
                time_to_wait = frame_duration - elapsed_time
                if time_to_wait > 0:
                    time.sleep(time_to_wait)


    def __enter__(self) -> Self:
        print("Start recording...")
        pygame.mixer.init()
        if self.music_filepath is not None:
            pygame.mixer.music.load(self.music_filepath)
            pygame.mixer.music.play(-1)

        self._buffer = cv2.VideoWriter(str(self.filepath), self._codec, self._fps, (self.width, self.height))
        self._is_recording = True
        self._recoding_thread = threading.Thread(target=self.record)
        self._recoding_thread.start()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        print("Stop recording...")
        self._is_recording = False
        if self._recoding_thread.is_alive():
            self._recoding_thread.join()
        
        self._buffer.release()

        if self.music_filepath is not None:
            pygame.mixer.music.stop()

        self.add_background_music()

    def add_background_music(self) -> None:
        video_clip = VideoFileClip(str(self.filepath))
        audio_clip = AudioFileClip(str(self.music_filepath))
        final_clip = video_clip.with_audio(audio_clip)
        final_clip.audio.duration = video_clip.duration

        final_clip.write_videofile(str(self.filepath), codec="libx264")

        audio_clip.close()
        video_clip.close()
        print("Combined")
