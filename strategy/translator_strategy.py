from abc import ABC, abstractmethod

class TranslationStrategy(ABC):

    @abstractmethod
    def translate(self, text: str) -> str:
        pass

    def translate_many(self, texts):
        return [self.translate(t) for t in texts]
