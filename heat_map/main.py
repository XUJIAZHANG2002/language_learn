from heatmap_app import HeatmapApp
from heatmap_generator import HeatmapGenerator
from image_canvas import ImageCanvas
from mouse_tracker import MouseTracker

if __name__ == "__main__":
    canvas = ImageCanvas(mode="blue_background", path="../env.jpg")
    tracker = MouseTracker()
    heatmap = HeatmapGenerator(height=canvas.H, width=canvas.W, sigma=80, decay=0.96)

    app = HeatmapApp(canvas, tracker, heatmap)
    app.run()
