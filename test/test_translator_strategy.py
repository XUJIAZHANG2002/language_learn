from language_learn.strategy.translator_strategy import TranslationStrategy
from language_learn.translator.german_translator import GermanTranslator
from language_learn.translator.french_translator import FrenchTranslator

def test_german_translator():
    translator = GermanTranslator()
    result = translator.translate("chair")
    print("German:", result)
    assert isinstance(result, str)

def test_french_translator():
    translator = FrenchTranslator()
    result = translator.translate("chair")
    print("French:", result)
    assert isinstance(result, str)

if __name__ == "__main__":
    test_german_translator()
    test_french_translator()
