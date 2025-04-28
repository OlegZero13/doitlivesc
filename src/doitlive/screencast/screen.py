from pathlib import Path
import time
import threading
from typing import Dict

import cv2
from mss import mss
import numpy as np

from .base import BaseRecorder


class ScreenRecorder(BaseRecorder):
    def __init__(
        self,
        filepath: Path,
        monitor: Dict[str, int],
    ) -> None:
        super().__init__(filepath)
        self.monitor = monitor
        
        self._fps = 20
        self._codec = cv2.VideoWriter_fourcc(*"XVID")
        self._is_recording = False
        self._thread = None
        self._buffer = None

    def _record(self) -> None:
        with mss() as sct:
            frame_duration = 1 / self._fps

            while self._is_recording:
                start_time = time.time()

                img = sct.grab(self.monitor)
                frame = np.array(img).astype(np.uint8)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                self._buffer.write(frame)

                elapsed_time = time.time() - start_time
                time_to_wait = frame_duration - elapsed_time
                if time_to_wait > 0:
                    time.sleep(time_to_wait)

    def start(self) -> None:
        self._is_recording = True
        screen_size = self.monitor["width"], self.monitor["height"]
        self._buffer = cv2.VideoWriter(
            str(self.filepath),
            self._codec,
            self._fps,
            screen_size,
        )
        self._thread = threading.Thread(target=self._record)
        self._thread.start()

    def stop(self) -> None:
        self._is_recording = False
        if self._thread.is_alive():
            self._thread.join()
        
        self._buffer.release()
