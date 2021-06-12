#! /usr/bin/env python
import numpy as np


class SimpleSlideChecker:
    def __init__(self, width, height, **kwargs):
        self.params = {
            "cdist_threshold": 100,  # Max color dist for pixel to be in background
            "changed_cdist_threshold": 0,  # Minimum color dist for pixel to be changed

        }
        self.params.update(kwargs)

        self.bg = np.array((255, 255, 255,)).reshape((1, 1, -1))
        self.n_pixels = width * height

    def check(self, frame: np.ndarray, prev=None) -> bool:
        if prev is None:
            return True

        bg = ((prev - self.bg) ** 2).sum(axis=2) < self.params['cdist_threshold']
        changed = ((frame - prev) ** 2).sum(axis=2) > self.params['changed_cdist_threshold']
        overwritten = changed[bg]

        n = self.n_pixels
        n_bg = np.count_nonzero(bg)
        n_changed = np.count_nonzero(changed)
        n_overwritten = np.count_nonzero(overwritten)
        n_annotated = n_changed - n_overwritten

        print(f"n: {n:n}\t%bg: {n_bg * 100 / n:.2f}\t"
              f"%ch: {n_changed * 100 / n:.2f}\t"
              f"%an: {n_annotated * 100 / (1 + n_changed):.2f}")

        return not ((n_changed <= 0.005 * n) or (n_annotated >= 0.3 * n_changed))

        
