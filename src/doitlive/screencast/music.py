from pathlib import Path

import pygame

from .base import BaseRecorder


class MusicPlayer(BaseRecorder):
    def __init__(self, filepath: Path) -> None:
        super().__init__(filepath)

    def start(self) -> None:
        pygame.mixer.init()
        pygame.mixer.music.load(self.filepath)
        pygame.mixer.music.play(-1)
    
    def stop(self) -> None:
        pygame.mixer.music.stop()
