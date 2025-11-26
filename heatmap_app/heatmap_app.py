
import numpy as np
import time
import matplotlib.pyplot as plt

from event.event_bus import EventBus
from event.event_type import EventType


class HeatmapApp:
    """
    Interactive heatmap + periodic object detection + event-based architecture.
    Object detection runs every 2 seconds.
    """

    def __init__(self, image_canvas, tracker, heatmap, object_detector, box_visualizer, event_bus):
        self.canvas = image_canvas
        self.tracker = tracker
        self.heatmap = heatmap

        self.detector = object_detector
        self.visualizer = box_visualizer

        # Detection state
        self.detections = []
        self.last_detection_time = 0
        self.detect_interval = 2.0  # seconds

        # Heat threshold state
        self.prev_active_boxes = set()

        # Shared event bus
        self.event_bus = event_bus

    # ---------------------------------------------------------
    # Object Detection (2-second interval)
    # ---------------------------------------------------------
    def run_detection(self, bg_img, text_labels):
        now = time.time()
        if now - self.last_detection_time < self.detect_interval:
            return

        self.detections = self.detector.detect(
            bg_img,
            text_labels=text_labels,
            threshold=0.3
        )

        # Publish event
        self.event_bus.publish(EventType.OBJECTS_DETECTED, self.detections)

        self.last_detection_time = now

    # ---------------------------------------------------------
    # Check heat entering / exiting bounding boxes
    # ---------------------------------------------------------
    def check_heat_events(self, heatmap):
        threshold = 0.3  # average heat threshold

        active_boxes = set()

        for i, det in enumerate(self.detections):
            x1, y1, x2, y2 = map(int, det["box"])
            region = heatmap[y1:y2, x1:x2]

            if region.size == 0:
                continue

            avg_heat = region.mean() / (heatmap.max() + 1e-6)

            if avg_heat > threshold:
                active_boxes.add(i)
                if i not in self.prev_active_boxes:
                    self.event_bus.publish(EventType.HEATMAP_ENTER_THRESHOLD, det)

            else:
                if i in self.prev_active_boxes:
                    self.event_bus.publish(EventType.HEATMAP_LEAVE_THRESHOLD, det)

        self.prev_active_boxes = active_boxes
    def filter_boxes_by_heat(self, heatmap, detections, threshold=0.3):
        """
        Return only detections whose average heat exceeds the threshold.
        """
        filtered = []

        for det in detections:
            x1, y1, x2, y2 = map(int, det["box"])
            region = heatmap[y1:y2, x1:x2]

            if region.size == 0:
                continue

            avg_heat = float(region.mean()) / (heatmap.max() + 1e-6)

            if avg_heat > threshold:
                filtered.append(det)

        return filtered

    # ---------------------------------------------------------
    # Main Application Loop
    # ---------------------------------------------------------
    def run(self):
        # Load background image
        bg = self.canvas.load()

        # Publish IMAGE_LOADED event
        self.event_bus.publish(EventType.IMAGE_LOADED, bg)

        listener = self.tracker.start()

        plt.ion()
        fig, ax = plt.subplots(figsize=(12, 6))
        text_labels = ["desk", "chair", "floor", "board", "black board"]

        img_handle = ax.imshow(bg, origin="upper")
        ax.set_title("Interactive Heatmap + OmDet-Turbo Detection")

        try:
            while self.tracker.running:

                # Mouse → heatmap update
                x = int(self.tracker.x / self.canvas.W * self.canvas.W)
                y = int(self.tracker.y / self.canvas.H * self.canvas.H)
                x = np.clip(x, 0, self.canvas.W - 1)
                y = np.clip(y, 0, self.canvas.H - 1)

                self.heatmap.step(x, y)
                heatmap = self.heatmap.get()

                # Heatmap overlay
                heat_norm = heatmap / (heatmap.max() + 1e-6)
                overlay = (
                    bg * 0.7 + plt.cm.jet(heat_norm)[:, :, :3] * 255 * 0.3
                ).astype(np.uint8)

                # Run object detection
                self.run_detection(bg, text_labels)

                # Fire heatmap events (observer pattern)
                self.check_heat_events(heatmap)

                # Draw object boxes
                hot_boxes = self.filter_boxes_by_heat(heatmap, self.detections)
                overlay = self.visualizer.draw(overlay, hot_boxes)


                # Display
                img_handle.set_data(overlay)
                ax.set_xlabel(f"mouse: ({x}, {y})")
                plt.pause(0.01)

        except KeyboardInterrupt:
            pass

        plt.ioff()
        plt.show()
        listener.stop()
