from language_learn.speech.speaker import GTTSSpeaker
from language_learn.strategy.speaker_strategy import SpeakerStrategy

class FrenchSpeaker(SpeakerStrategy):

    def __init__(self):
        self.speaker = GTTSSpeaker(lang="fr")

    def speak(self, text: str):
        self.speaker.speak(text)
