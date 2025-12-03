from abc import ABC, abstractmethod

class SpeakerStrategy(ABC):

    @abstractmethod
    def speak(self, text: str):
        pass
