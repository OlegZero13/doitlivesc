from abc import ABC, abstractmethod
from pathlib import Path


class BaseRecorder(ABC):
    def __init__(self, filepath: Path) -> None:
        self.filepath = filepath
    
    @abstractmethod
    def start(self) -> None:
        ...

    @abstractmethod
    def stop(self) -> None:
        ...
