import numpy as np
import time
import matplotlib.pyplot as plt




class HeatmapApp:
    """
    Interactive heatmap + periodic object detection.
    Object detection runs every 2 seconds.
    """

    def __init__(self, image_canvas, tracker, heatmap, object_detector, box_visualizer):
        self.canvas = image_canvas
        self.tracker = tracker
        self.heatmap = heatmap

        # New components
        self.detector = object_detector
        self.visualizer = box_visualizer

        # Store latest detections
        self.detections = []
        self.last_detection_time = 0
        self.detect_interval = 2.0  # seconds

    def _maybe_run_detection(self, bg_img):
        """
        Runs object detection every detect_interval seconds.
        """
        now = time.time()
        if now - self.last_detection_time < self.detect_interval:
            return  # too soon

        # Run detector
        self.detections = self.detector.detect(
            bg_img, 
            text_labels=["car", "person", "flower", "grass", "tree"],
            threshold=0.3
        )

        print("Detections updated:", self.detections)

        self.last_detection_time = now

    def run(self):
        bg = self.canvas.load()
        listener = self.tracker.start()

        plt.ion()
        fig, ax = plt.subplots(figsize=(12, 6))

        img_handle = ax.imshow(bg, origin="upper")
        ax.set_title("Interactive Heatmap + OmDet-Turbo Detection")
        overlay = bg.copy()

        try:
            while self.tracker.running:

                # -------- Mouse & heatmap update --------
                x = int(self.tracker.x / self.canvas.W * self.canvas.W)
                y = int(self.tracker.y / self.canvas.H * self.canvas.H)
                x = np.clip(x, 0, self.canvas.W - 1)
                y = np.clip(y, 0, self.canvas.H - 1)

                self.heatmap.step(x, y)
                heat = self.heatmap.get()
                heat_norm = heat / heat.max() if heat.max() > 0 else heat

                # Blend heatmap on top of background
                overlay = (
                    bg * 0.7 + plt.cm.jet(heat_norm)[:, :, :3] * 255 * 0.3
                ).astype(np.uint8)

                # -------- Object detection every 2 seconds --------
                self._maybe_run_detection(bg)

                # -------- Draw object boxes on overlay --------
                overlay = self.visualizer.draw(overlay, self.detections)

                # -------- Display --------
                img_handle.set_data(overlay)
                ax.set_xlabel(f"mouse: ({x}, {y})")

                plt.pause(0.01)

        except KeyboardInterrupt:
            pass

        plt.ioff()
        plt.show()
        listener.stop()
