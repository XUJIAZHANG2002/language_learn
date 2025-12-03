from language_learn.translator.translator import Translator
from language_learn.strategy.translator_strategy import TranslationStrategy

class FrenchTranslator(TranslationStrategy):

    def __init__(self):
        self.translator = Translator("en", "fr")

    def translate(self, text: str) -> str:
        return self.translator.translate_one(text)
