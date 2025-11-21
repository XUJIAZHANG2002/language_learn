import numpy as np

class HeatmapGenerator:
    def __init__(self, height, width, sigma=10, decay=0.9):
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

    def cool_down(self):
        self.map *= self.decay

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

    def step(self, x, y):
        self.cool_down()
        self._add_kernel_patch(int(x), int(y))

    def get(self):
        return self.map.copy()
