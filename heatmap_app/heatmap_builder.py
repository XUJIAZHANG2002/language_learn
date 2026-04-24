"""
HeatmapAppBuilder: constructs HeatmapApp using Builder pattern.

Provides a flexible way to configure components (detector, heatmap,
translator, speaker, etc.) and inject them into the main application.
"""


from language_learn.event.event_bus import EventBus
from language_learn.heatmap_app.heatmap_generator import HeatmapGenerator
from language_learn.heatmap_app.mouse_tracker import MouseTracker
from language_learn.heatmap_app.image_canvas import ImageCanvas
from language_learn.vision_models.object_detector import OmDetObjectDetector
from language_learn.vision_models.box_visualizer import BoxVisualizer
from language_learn.speech.speaker import GTTSSpeaker
from language_learn.translator.translator import Translator
from language_learn.translator.german_translator import GermanTranslator
from language_learn.translator.french_translator import FrenchTranslator
from language_learn.speech.german_speaker import GermanSpeaker
from language_learn.speech.french_speaker import FrenchSpeaker
from language_learn.heatmap_app.heatmap_app import HeatmapApp


class HeatmapAppBuilder:

    def __init__(self):
        self.canvas = None
        self.tracker = None
        self.heatmap = None
        self.detector = None
        self.visualizer = None
        self.translator = None
        self.speaker = None
        self.text_labels = None
        self.bus = None

    def with_canvas(self, path, mode="image"):
        self.canvas = ImageCanvas(mode=mode, path=path)
        return self

    def with_mouse_tracker(self):
        self.tracker = MouseTracker()
        return self

    def with_object_detector(self, kind="omdet"):
         # simple factory behavior for detector selection
        if kind == "omdet":
            self.detector = OmDetObjectDetector()
        else:
            raise ValueError(f"Unknown detector: {kind}")
        return self

    def with_visualizer(self, font_scale=0.6, thickness=2):
        self.visualizer = BoxVisualizer(font_scale=font_scale, thickness=thickness)
        return self

    def with_translator(self, source="en", target="de"):
        self.translator = Translator(source_lang=source, target_lang=target)
        return self

    def with_speaker(self, lang="de"):
        self.speaker = GTTSSpeaker(lang=lang)
        return self

    def with_heatmap(self, sigma=10, decay=0.97, width=None, height=None):
        if width is None or height is None:
            if self.canvas is None:
                raise ValueError("Canvas required before heatmap if no size given")
            width = self.canvas.W
            height = self.canvas.H

        self.heatmap = HeatmapGenerator(height=height, width=width, sigma=sigma, decay=decay)
        return self
    
    def with_text_lables(self, text_labels):
        self.text_labels = text_labels
        return self

    def with_language(self, lang="de"):
        if lang == "de":
            self.translator = GermanTranslator()
            self.speaker = GermanSpeaker()
        elif lang == "fr":
            self.translator = FrenchTranslator()
            self.speaker = FrenchSpeaker()
        else:
            raise ValueError("Unsupported language")
        return self


    def with_text_labels_file(self, filepath):
        import os
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Label file not found: {filepath}")

        with open(filepath, "r", encoding="utf-8") as f:
            labels = [line.strip() for line in f.readlines() if line.strip()]

        self.text_labels = labels
        return self
    def with_event_bus(self, bus):
        self.bus = bus
        return self

    def build(self):
        if not all([self.canvas, self.tracker, self.heatmap, self.detector,
                    self.visualizer, self.translator,self.text_labels, self.speaker, self.bus]):
            raise ValueError("Builder missing components")
# dependenty injection
        return HeatmapApp(
            self.canvas,
            self.tracker,
            self.heatmap,
            self.detector,
            self.visualizer,
            self.translator,
            self.speaker,
            self.text_labels,
            self.bus
        )
