"""
GTTSSpeaker: asynchronous text-to-speech using gTTS.

Uses a background thread + queue to avoid blocking the main application
(e.g., UI / detection loop) while generating and playing audio.
"""


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
        # continuously process queued speech requests
        while self.running:
            try:
                text = self.q.get(timeout=0.1)
                print("[speaker] got text:", repr(text))

                with NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                    print("[speaker] generating mp3...")
                    tts = gTTS(text=text, lang=self.lang)
                    tts.write_to_fp(f)
                    tmp_path = f.name

                print("[speaker] saved mp3:", tmp_path)

                try:
                     # blocking playback (but safe since it's in worker thread)
                    print("[speaker] start playing...")
                    playsound(tmp_path)
                    print("[speaker] play finished")
                finally:
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)
                        print("[speaker] temp deleted")

            except queue.Empty:
                pass
            except Exception as e:
                print("[speaker] ERROR:", e)

    def stop(self):
        self.running = False
        time.sleep(0.05)


