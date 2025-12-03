from language_learn.event.event_bus import EventBus
from language_learn.event.event_type import EventType
from language_learn.heatmap_app.heatmap_builder import HeatmapAppBuilder


def on_image_loaded(img):
    print("[EVENT] Image loaded:", img.shape)


def on_objects_detected(dets):
    print(f"[EVENT] {len(dets)} objects detected")


def on_heat_enter(box):
    print("[EVENT] Heat entered box:", box)


def on_heat_leave(box):
    print("[EVENT] Heat left box:", box)


DEFAULT_GAUSSIAN_SIGMA = 120
DEFAULT_HEAT_DECAY_RATE = 0.9
DEFUALT_FONT_SIZE = 1.2
DEFUALT_FONT_THICKNESS = 2

if __name__ == "__main__":
    # 1. Event bus
    bus = EventBus()
    bus.subscribe(EventType.IMAGE_LOADED, on_image_loaded)
    bus.subscribe(EventType.OBJECTS_DETECTED, on_objects_detected)
    bus.subscribe(EventType.HEATMAP_ENTER_THRESHOLD, on_heat_enter)
    bus.subscribe(EventType.HEATMAP_LEAVE_THRESHOLD, on_heat_leave)

    # 2. Build the app
    app = (
        HeatmapAppBuilder()
            .with_canvas("language_learn/imgs/classroom.jpg")
            .with_mouse_tracker()
            .with_object_detector("omdet")
            .with_visualizer(font_scale=DEFUALT_FONT_SIZE, thickness=DEFUALT_FONT_THICKNESS)
            .with_heatmap(sigma=DEFAULT_GAUSSIAN_SIGMA, decay=DEFAULT_HEAT_DECAY_RATE)
            .with_text_labels_file("language_learn/text_labels/classroom.txt")
            .with_language("fr")
            .with_event_bus()   
            .build()
    )

    # 3. Inject the bus into the app
    app.event_bus = bus

    # 4. Start the application
    app.run()
