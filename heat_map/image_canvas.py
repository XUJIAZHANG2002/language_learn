import numpy as np
from PIL import Image
import ctypes

class ImageCanvas:
    def __init__(self, mode="blue_background", path=None):
        self.mode = mode
        self.path = path

        # detect screen size
        user32 = ctypes.windll.user32
        self.W = user32.GetSystemMetrics(0)
        self.H = user32.GetSystemMetrics(1)

    def load(self):
        if self.mode == "blue_background":
            img = np.zeros((self.H, self.W, 3), dtype=np.uint8)
            img[:, :, 2] = 150  # blue tint
            return img

        elif self.mode == "image":
            pil = Image.open(self.path).resize((self.W, self.H))
            return np.array(pil.convert("RGB"))

        else:
            raise ValueError("mode must be 'blue_background' or 'image'")
