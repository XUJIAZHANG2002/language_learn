import numpy as np
import matplotlib.pyplot as plt

class HeatmapApp:
    def __init__(self, image_canvas, tracker, heatmap):
        self.canvas = image_canvas
        self.tracker = tracker
        self.heatmap = heatmap

    def run(self):
        bg = self.canvas.load()
        listener = self.tracker.start()

        plt.ion()
        fig, ax = plt.subplots(figsize=(12, 6))

        heat = self.heatmap.get()
        heat_norm = heat / heat.max() if heat.max() > 0 else heat
        overlay = (bg * 0.7 + plt.cm.jet(heat_norm)[:, :, :3] * 255 * 0.3).astype(np.uint8)

        img_handle = ax.imshow(overlay, origin="upper")
        ax.set_title("Mouse Heatmap (Right-click to quit)")

        try:
            while self.tracker.running:

                x = int(self.tracker.x / self.canvas.W * self.canvas.W)
                y = int(self.tracker.y / self.canvas.H * self.canvas.H)

                x = np.clip(x, 0, self.canvas.W - 1)
                y = np.clip(y, 0, self.canvas.H - 1)

                self.heatmap.step(x, y)

                heat = self.heatmap.get()
                heat_norm = heat / heat.max() if heat.max() > 0 else heat
                overlay = (bg * 0.7 + plt.cm.jet(heat_norm)[:, :, :3] * 255 * 0.3).astype(np.uint8)

                img_handle.set_data(overlay)
                ax.set_xlabel(f"mouse: ({x}, {y})")

                plt.pause(0.005)

        except KeyboardInterrupt:
            pass

        plt.ioff()
        plt.show()
        listener.stop()
