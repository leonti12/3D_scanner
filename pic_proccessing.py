# steger.py
import time
import cv2
import numpy as np


class StegerExtractor:
    """Sub-pixel laser line extraction (Steger) on a single frame, one point per row."""

    def __init__(self, threshold=40, blur_ksize=5, sigma=1.0):
        self.threshold = threshold
        self.blur_ksize = blur_ksize
        self.sigma = sigma
        self.last_time_ms = 0.0

    def process(self, frame: np.ndarray) -> np.ndarray:
        """
        frame: array from picam2.capture_array() (gray, or 3/4 channel)
        returns: (N, 2) float32 array of (x, y) sub-pixel points
        Processing time is stored in self.last_time_ms.
        """
        t0 = time.perf_counter()

        # Make sure we have a single-channel uint8 image
        if frame.ndim == 3:
            code = cv2.COLOR_BGRA2GRAY if frame.shape[2] == 4 else cv2.COLOR_BGR2GRAY
            frame = cv2.cvtColor(frame, code)

        # 1. Zero out baseline noise
        _, thresh = cv2.threshold(frame, self.threshold, 255, cv2.THRESH_TOZERO)

        # 2. Smooth
        img = cv2.GaussianBlur(thresh.astype(np.float32),
                               (self.blur_ksize, self.blur_ksize), self.sigma)

        # 3. Derivatives. scale=1/8 makes each Sobel a true per-pixel derivative,
        #    so t comes out in real pixel units.
        s = 1.0 / 8.0
        dx = cv2.Sobel(img, cv2.CV_32F, 1, 0, ksize=3, scale=s)
        dy = cv2.Sobel(img, cv2.CV_32F, 0, 1, ksize=3, scale=s)
        dxx = cv2.Sobel(dx, cv2.CV_32F, 1, 0, ksize=3, scale=s)
        dyy = cv2.Sobel(dy, cv2.CV_32F, 0, 1, ksize=3, scale=s)
        dxy = cv2.Sobel(dx, cv2.CV_32F, 0, 1, ksize=3, scale=s)

        # 4. Integer peak per row (vectorized)
        h, w = thresh.shape
        ys = np.arange(1, h - 1)
        xs = np.argmax(thresh[1:-1, :], axis=1)
        valid = (thresh[ys, xs] > 0) & (xs > 0) & (xs < w - 1)
        ys, xs = ys[valid], xs[valid]

        if ys.size == 0:
            self.last_time_ms = (time.perf_counter() - t0) * 1000
            return np.empty((0, 2), np.float32)

        Hxx, Hyy, Hxy = dxx[ys, xs], dyy[ys, xs], dxy[ys, xs]
        Ix, Iy = dx[ys, xs], dy[ys, xs]

        # 5. Normal direction = eigenvector of the largest-|eigenvalue|
        tmp = np.sqrt((Hxx - Hyy) ** 2 + 4 * Hxy ** 2)
        lam1 = 0.5 * (Hxx + Hyy + tmp)
        lam2 = 0.5 * (Hxx + Hyy - tmp)
        theta = 0.5 * np.arctan2(2 * Hxy, Hxx - Hyy)   # direction of lam1's eigenvector
        use1 = np.abs(lam1) >= np.abs(lam2)
        nx = np.where(use1, np.cos(theta), -np.sin(theta))
        ny = np.where(use1, np.sin(theta), np.cos(theta))

        # 6. Sub-pixel offset along the normal
        denom = Hxx * nx**2 + 2 * Hxy * nx * ny + Hyy * ny**2
        ok = np.abs(denom) > 1e-9
        t = np.zeros_like(denom)
        t[ok] = -(Ix[ok] * nx[ok] + Iy[ok] * ny[ok]) / denom[ok]
        ok &= np.abs(t) <= 1.0

        pts = np.stack([xs[ok] + t[ok] * nx[ok], ys[ok] + t[ok] * ny[ok]], axis=1).astype(np.float32)
        # print(pts)
        
        self.last_time_ms = (time.perf_counter() - t0) * 1000
        return pts