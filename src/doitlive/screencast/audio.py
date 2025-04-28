from pathlib import Path

import numpy as np
from pvrecorder import PvRecorder
import wave
import threading

from .base import BaseRecorder


class AudioRecorder(BaseRecorder):
    def __init__(self, filepath: Path) -> None:
        super().__init__(filepath)

        self._frames = []
        self._is_recording = False
        self._thread = None
        self._recorder = None

    def start(self) -> None:
        self._is_recording = True
        self._frames = []
        self._recorder = PvRecorder(device_index=-1, frame_length=512)  # Use -1 for default microphone
        self._recorder.start()
        
        self._thread = threading.Thread(target=self._record)
        self._thread.start()

    def _record(self) -> None:
        while self._is_recording:
            frame = self._recorder.read()
            self._frames.append(frame)

    def stop(self) -> None:
        self._is_recording = False
        if self._thread is not None:
            self._thread.join()  # Wait for the recording thread to finish
        self._recorder.stop()

        self._save()

    def _save(self) -> None:
        audio_data = np.concatenate(self._frames).astype(np.int16)
        audio_bytes = audio_data.tobytes()

        with wave.open(str(self.filepath), 'wb') as wf:
            wf.setnchannels(1)  # Mono audio
            wf.setsampwidth(2)  # 16 bits per sample
            wf.setframerate(16000)  # Sample rate
            wf.writeframes(audio_bytes)
