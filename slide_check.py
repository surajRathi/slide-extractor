#! /usr/bin/env python
import numpy as np


class SimpleSlideChecker:
    def __init__(self, width, height):
        self.bg = np.array((255, 255, 255,)).reshape((1, 1, -1))
        self.n_pixels = width * height

    def check(self, frame: np.ndarray, prev=None) -> bool:
        if prev is None:
            return True
        bg = ((prev - self.bg) ** 2).sum(axis=2) < 100
        print(np.count_nonzero(bg) / self.n_pixels * 100)

        changed = ((frame - prev) ** 2).sum(axis=2) > 0
        # print(((frame - prev) ** 2).sum(axis=2))
        overwritten = changed[bg]
        print(np.count_nonzero(changed) / self.n_pixels * 100)
        print(np.count_nonzero(overwritten) / self.n_pixels * 100)
        print()
        return False
