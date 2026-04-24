"""
HeatmapApp: main controller of the system.

Coordinates:
- mouse heatmap tracking
- periodic object detection
- event triggering (via EventBus)
- visualization and UI update
"""

import numpy as np
import time
import matplotlib.pyplot as plt

from language_learn.event.event_bus import EventBus
from language_learn.event.event_type import EventType


class HeatmapApp:
    """
    Interactive heatmap + periodic object detection + event-based architecture.
    Object detection runs every 2 seconds.
    """
# dependenty injection
    def __init__(self, image_canvas, tracker, heatmap, object_detector, box_visualizer,translator, speaker, text_lables, event_bus):
        self.canvas = image_canvas
        self.tracker = tracker
        self.heatmap = heatmap
        self.translator = translator
        self.speaker = speaker
        self.detector = object_detector
        self.visualizer = box_visualizer

    
        self.detections = []
        self.last_detection_time = 0
        self.detect_interval = 2.0  

        self.text_lables = text_lables
        self.prev_active_boxes = set()

     
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
        for det in self.detections:
            en = det["label"]
            det["label_en"] = en
            det["label_de"] = self.label_map.get(en, "")
        # Publish event
        self.event_bus.publish(EventType.OBJECTS_DETECTED, self.detections)

        self.last_detection_time = now


    # ---------------------------------------------------------
    # Check heat entering / exiting bounding boxes
    # ---------------------------------------------------------
    def check_heat_events(self, heatmap):
        threshold = 0.3  
        active_boxes = set()

        for i, det in enumerate(self.detections):
            x1, y1, x2, y2 = map(int, det["box"])
            region = heatmap[y1:y2, x1:x2]

            if region.size == 0:
                continue

            avg_heat = region.mean() / (heatmap.max() + 1e-6)

            # ---- HEAT ABOVE THRESHOLD ----
            if avg_heat > threshold:
                active_boxes.add(i)

             
                if i not in self.prev_active_boxes:
                    german = det.get("label_de", "")
                    print("shall speak " , german, )
                    
                    self.speaker.speak(german)

                    self.event_bus.publish(EventType.HEATMAP_ENTER_THRESHOLD, det)

            # ---- HEAT BELOW THRESHOLD ----
            else:
                if i in self.prev_active_boxes:
                    self.event_bus.publish(EventType.HEATMAP_LEAVE_THRESHOLD, det)

        # Update active set AFTER loop
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


    def _update_cursor_and_heatmap(self):
        screen_w = 2560
        screen_h = 1600

        x = int(self.tracker.x * self.canvas.W / screen_w)
        y = int(self.tracker.y * self.canvas.H / screen_h)

        x = np.clip(x, 0, self.canvas.W - 1)
        y = np.clip(y, 0, self.canvas.H - 1)

        self.heatmap.step(x, y)
        return x, y, self.heatmap.get()



    def _update_heat_overlay(self, bg, heatmap):
        heat_norm = heatmap / (heatmap.max() + 1e-6)
        overlay = (
            bg * 0.7 + plt.cm.jet(heat_norm)[:, :, :3] * 255 * 0.3
        ).astype(np.uint8)
        return overlay


    def _run_object_pipeline(self, bg, heatmap, text_labels):

        self.run_detection(bg, text_labels)


        self.check_heat_events(heatmap)

  
        hot_boxes = self.filter_boxes_by_heat(heatmap, self.detections)

   
        for det in hot_boxes:
            det["label"] = f"{det['label_en']} / {det['label_de']}"

        return hot_boxes

    def _draw_and_refresh(self, ax, img_handle, overlay, hot_boxes, x, y):
        overlay = self.visualizer.draw(overlay, hot_boxes)

        img_handle.set_data(overlay)
        ax.set_xlabel(f"mouse: ({x}, {y})")
        plt.pause(0.01)

    def initialize(self):
        """Facade: prepare everything before the loop runs."""
        # Load background image
        self.bg = self.canvas.load()
        self.event_bus.publish(EventType.IMAGE_LOADED, self.bg)

        # Start mouse tracker
        self.listener = self.tracker.start()

        # Translate English → German
        text_labels_en = self.text_lables
        text_labels_de = self.translator.translate_many(text_labels_en)
        self.label_map = {en: de for en, de in zip(text_labels_en, text_labels_de)}
        self.text_labels_en = text_labels_en  # store for pipeline

        # Create plot window
        plt.ion()
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.img_handle = self.ax.imshow(self.bg, origin="upper")
        self.ax.set_title("Interactive Heatmap + OmDet-Turbo Detection")

        print("[INIT] Finished initialization.")

    def main_loop(self):
        """Facade: run the main loop using façade sub-steps."""
        try:
            while self.tracker.running:

                # update heatmap 
                x, y, heatmap = self._update_cursor_and_heatmap()

                # update heat overlay on the background image
                overlay = self._update_heat_overlay(self.bg, heatmap)

                # run detection + heat events + label fusion
                hot_boxes = self._run_object_pipeline(self.bg, heatmap, self.text_labels_en)

                #  draw boxes + refresh UI
                self._draw_and_refresh(self.ax, self.img_handle, overlay, hot_boxes, x, y)

        except KeyboardInterrupt:
            pass

        plt.ioff()
        plt.show()
        self.listener.stop()

    def run(self):
        self.initialize()
        self.main_loop()

