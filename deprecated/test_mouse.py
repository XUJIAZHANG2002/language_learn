import numpy as np
import matplotlib.pyplot as plt
from pynput import mouse
from PIL import Image
import ctypes

# ==============================
# Heatmap generator (your code)
# ==============================

class HeatmapGenerator:
    def __init__(self, height, width, sigma=10, decay=0.95):
        self.height = height
        self.width = width
        self.sigma = sigma
        self.decay = decay
        self.map = np.zeros((height, width), dtype=np.float32)
        self.kernel = self._make_kernel(sigma)

    def _make_kernel(self, sigma):
        size = int(3 * sigma)
        ax = np.arange(-size, size + 1)
        xx, yy = np.meshgrid(ax, ax)
        kernel = np.exp(-(xx**2 + yy**2) / (2 * sigma**2))
        return kernel.astype(np.float32)

    def _add_kernel_patch(self, x, y):
        k = self.kernel
        ks = k.shape[0] // 2

        x0 = max(0, x - ks)
        x1 = min(self.width, x + ks + 1)
        y0 = max(0, y - ks)
        y1 = min(self.height, y + ks + 1)

        kx0 = ks - (x - x0)
        ky0 = ks - (y - y0)

        kx1 = kx0 + (x1 - x0)
        ky1 = ky0 + (y1 - y0)

        self.map[y0:y1, x0:x1] += k[ky0:ky1, kx0:kx1]

    def cool_down(self):
        self.map *= self.decay

    def step(self, x, y):
        self.cool_down()
        self._add_kernel_patch(int(x), int(y))

    def get_heatmap(self):
        return self.map.copy()


# ==============================
# Mouse listener
# ==============================

mouse_pos = [0, 0]
running = True

def on_move(x, y):
    mouse_pos[0] = x
    mouse_pos[1] = y

def on_click(x, y, button, pressed):
    global running
    if not pressed and button == mouse.Button.right:
        running = False
        return False


# ==============================
# MAIN FUNCTION
# ==============================

def main():

    # -----------------------------
    # Select Background Mode
    # -----------------------------
    mode = "blue"      # "blue" OR "image"
    background_path = "../env.jpg"  # used only if mode="image"

    # -----------------------------
    # Detect real screen size
    # -----------------------------
    user32 = ctypes.windll.user32
    SCREEN_W = user32.GetSystemMetrics(0)
    SCREEN_H = user32.GetSystemMetrics(1)

    H, W = SCREEN_H, SCREEN_W   # match screen size
    generator = HeatmapGenerator(H, W, sigma=80, decay=0.96)

    # -----------------------------
    # Load background based on mode
    # -----------------------------
    if mode == "blue":
        # classic pure blue background
        bg_img = np.zeros((H, W, 3), dtype=np.uint8)
        bg_img[:, :, 2] = 150   # blue tint

    elif mode == "image":
        # load and resize image
        bg_img = np.array(Image.open(background_path).resize((W, H)).convert("RGB"))

    else:
        raise ValueError("mode must be 'blue' or 'image'")

    # -----------------------------
    # Start mouse tracker
    # -----------------------------
    listener = mouse.Listener(on_move=on_move, on_click=on_click)
    listener.start()

    # -----------------------------
    # Matplotlib real-time plot
    # -----------------------------
    plt.ion()
    fig, ax = plt.subplots(figsize=(12, 6))

    # Initial overlay
    heatmap = generator.get_heatmap()
    heatmap_norm = heatmap / heatmap.max() if heatmap.max() > 0 else heatmap
    overlay = (bg_img * 0.7 + plt.cm.jet(heatmap_norm)[:, :, :3] * 255 * 0.3).astype(np.uint8)

    img = ax.imshow(overlay, origin="upper")
    ax.set_title("Mouse Heatmap (right-click to quit)")

    try:
        while running:

            # scale mouse coords → heatmap coords
            x = int(mouse_pos[0] / SCREEN_W * W)
            y = int(mouse_pos[1] / SCREEN_H * H)

            x = max(0, min(W - 1, x))
            y = max(0, min(H - 1, y))

            generator.step(x, y)

            heatmap = generator.get_heatmap()
            if heatmap.max() > 0:
                heatmap_norm = heatmap / heatmap.max()
            else:
                heatmap_norm = heatmap

            overlay = (bg_img * 0.7 + plt.cm.jet(heatmap_norm)[:, :, :3] * 255 * 0.3).astype(np.uint8)

            img.set_data(overlay)
            ax.set_xlabel(f"mouse: ({x}, {y})")

            plt.pause(0.005)

    except KeyboardInterrupt:
        pass

    plt.ioff()
    plt.show()
    listener.stop()


# ==============================
# Run main
# ==============================

if __name__ == "__main__":
    main()
