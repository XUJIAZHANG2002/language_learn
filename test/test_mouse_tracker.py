from language_learn.heatmap_app.mouse_tracker import MouseTracker

def test_mouse_tracker():
    tracker = MouseTracker()
    print("Tracker initialized:", tracker.running is False)
    assert hasattr(tracker, "x")
    assert hasattr(tracker, "y")

if __name__ == "__main__":
    test_mouse_tracker()
