import numpy as np
from language_learn.heatmap_app.heatmap_generator import HeatmapGenerator

def test_heatmap_step():
    heatmap = HeatmapGenerator(1000, 1000, sigma=10, decay=0.9)
    heatmap.step(100, 150)
    arr = heatmap.get()

    print("Heatmap shape:", arr.shape)
    assert isinstance(arr, np.ndarray)
    assert arr.max() > 0

if __name__ == "__main__":
    test_heatmap_step()
