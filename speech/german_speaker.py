from language_learn.speech.speaker import GTTSSpeaker
from language_learn.strategy.speaker_strategy import SpeakerStrategy

class GermanSpeaker(SpeakerStrategy):

    def __init__(self):
        self.speaker = GTTSSpeaker(lang="de")

    def speak(self, text: str):
        self.speaker.speak(text)
