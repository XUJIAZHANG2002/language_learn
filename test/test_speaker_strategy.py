from language_learn.strategy.speaker_strategy import SpeakerStrategy
from language_learn.speech.french_speaker import FrenchSpeaker
from language_learn.speech.german_speaker import GermanSpeaker

def test_german_speaker():
    speaker = GermanSpeaker()
    print("German Speaker OK")

def test_french_speaker():
    speaker = FrenchSpeaker()
    print("French Speaker OK")

if __name__ == "__main__":
    test_german_speaker()
    test_french_speaker()
