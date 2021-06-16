#! /usr/bin/env python3

import cv2 as cv
import os

from input import CVReadVideo
from slide_check import SimpleSlideChecker
# Assumes videos in ./videos/
FILES = ['./videos/ppt_test.mp4', './videos/wb_test.mp4']

KEY_RIGHT_ARROW = 83
KEY_ENTER = 13


class ScrollableVideo:
    def __init__(self, FILENAME):
        self.stream = CVReadVideo(FILENAME)

    def __enter__(self):
        self.stream = self.stream.__enter()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stream.__exit__(exc_type, exc_val, exc_tb)


def main():
    FILE = FILES[0]
    VIDEO_NAME = FILE[:FILE.rfind('.')] if (index := FILE.rfind('/')) == -1 else FILE[index:FILE.rfind('.')]
    OUTPUT_FILENAME = f"./videos/{VIDEO_NAME}.txt"

    cv.namedWindow('main')

    with CVReadVideo(FILE) as stream, open(OUTPUT_FILENAME, 'w') as out:
        for i, frame in enumerate(stream):
            cv.imshow('main', frame)
            key = cv.waitKey(0)

            if key == ord('q'):
                break
            elif key == KEY_ENTER:
                print(f"Marked frame {i} as new.")
                print(i, file=out)
            elif key == KEY_RIGHT_ARROW:
                continue

    cv.destroyWindow('main')


if __name__ == '__main__':
    main()
