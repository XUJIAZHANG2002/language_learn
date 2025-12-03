import threading
import queue
import time
import os
from tempfile import NamedTemporaryFile

from gtts import gTTS
from playsound import playsound


class GTTSSpeaker:
    """
    Threaded German TTS speaker using gTTS + playsound.
    Same interface as GermanSpeaker: call .speak(text).
    """

    def __init__(self, lang="de"):
        self.lang = lang
        self.q = queue.Queue()
        self.running = True

        self.thread = threading.Thread(target=self._worker, daemon=True)
        self.thread.start()

    def speak(self, text: str):
        """Queue a word/sentence to be spoken."""
        if text:
            self.q.put(text)

    def _worker(self):
        while self.running:
            try:
                text = self.q.get(timeout=0.1)

                # 1) synthesize to a temp mp3
                with NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                    tts = gTTS(text=text, lang=self.lang)
                    tts.write_to_fp(f)
                    tmp_path = f.name

                # 2) play it (blocking in this worker thread only)
                try:
                    playsound(tmp_path)
                finally:
                    # 3) clean up
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)

            except queue.Empty:
                pass  # nothing to say right now

    def stop(self):
        self.running = False
        time.sleep(0.05)


