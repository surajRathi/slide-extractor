#! /usr/bin/env python3
from typing import Generator

import cv2 as cv
import numpy as np

FILE = '/home/suraj/test.mp4'


def cv_read_video(file: str) -> Generator[None, np.ndarray, None]:
    cap = cv.VideoCapture(file)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        yield frame


def main():
    cv.namedWindow('main')
    for frame in cv_read_video(FILE):
        cv.imshow('main', frame)
        if cv.waitKey(1) == ord('q'):
            break
    cv.destroyWindow('main')


if __name__ == '__main__':
    main()
