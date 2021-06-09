#! /usr/bin/env python3
from typing import Generator, Tuple

import cv2 as cv
import numpy as np
import os

FILE = '/home/suraj/test.mp4'
IMAGE_DIRECTORY = 'slides_extraction_out'
IMAGE_NAME_FORMAT = 'image_%04d.png'


class CVReadVideo:
    def __init__(self, filename: str):
        self.filename = filename

    def __enter__(self):
        self.cap = cv.VideoCapture(self.filename)
        if not self.cap.isOpened():
            raise RuntimeError("Video capture not opened")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cap.release()

    def __iter__(self):
        return self

    def __next__(self):
        ret, frame = self.cap.read()
        if ret:
            return frame
        raise StopIteration()

    def get_dims(self) -> Tuple[int, int]:  # height, width
        return int(self.cap.get(4)), int(self.cap.get(3))


class SlideChecker:
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


def main():
    try:
        os.mkdir(IMAGE_DIRECTORY)
    except FileExistsError:
        pass

    cv.namedWindow('main')

    with CVReadVideo(FILE) as stream:
        sc = SlideChecker(*stream.get_dims())
        i = 0
        prev = None
        for frame in stream:
            if sc.check(frame, prev):  # Save the previous frame when the slide changes
                if prev is not None:
                    cv.imwrite(os.path.join(IMAGE_DIRECTORY, IMAGE_NAME_FORMAT % i), frame)
                    i += 1
            prev = frame

            # # Visualize Background
            # bg = np.array((255, 255, 255,)).reshape((1, 1, -1))
            # frame[((np.linalg.norm(frame - bg, ord=2, axis=2)) < 200)] = (0, 255, 255)

            cv.imshow('main', frame)
            if cv.waitKey(1) == ord('q'):
                break

        if prev is not None:
            cv.imwrite(os.path.join(IMAGE_DIRECTORY, IMAGE_NAME_FORMAT % i), frame)
    cv.destroyWindow('main')


if __name__ == '__main__':
    main()
