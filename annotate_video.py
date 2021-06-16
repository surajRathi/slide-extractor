#! /usr/bin/env python3

import cv2 as cv
from collections import deque

from input import CVReadVideo

# Assumes videos in ./videos/
FILES = ['./videos/ppt_test.mp4', './videos/wb_test.mp4']

KEY_ENTER = 13


class ScrollableVideo:
    def __init__(self, FILENAME, max_buffer_len=100):
        self.max_buffer_len = max_buffer_len
        self.stream = CVReadVideo(FILENAME)
        self.buffer = deque()

        self.i = 0
        self.index = 0

    def __enter__(self):
        self.stream = self.stream.__enter__()
        self.buffer.append(next(self.stream))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stream.__exit__(exc_type, exc_val, exc_tb)

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        if self.index == len(self.buffer) - 1:
            self.buffer.append(next(self.stream))
            if len(self.buffer) > self.max_buffer_len:
                self.index -= 1
                self.buffer.popleft()

        self.index += 1
        self.i += 1

        return self.i, self.buffer[self.index]

    def prev(self):
        if self.index > 0:
            self.index -= 1
            self.i -= 1
        return self.i, self.buffer[self.index]


def main():
    FILE = FILES[None]  # *** Set this file to be able to use this program ***

    VIDEO_NAME = FILE[:FILE.rfind('.')] if (index := FILE.rfind('/')) == -1 else FILE[index + 1:FILE.rfind('.')]
    OUTPUT_FILENAME = f"./videos/{VIDEO_NAME}.txt"

    cv.namedWindow('main')

    with ScrollableVideo(FILE) as stream, open(OUTPUT_FILENAME, 'w') as out:
        # Note: Despite video being scrollable, output file is not scrollable.
        try:
            i, frame = next(stream)

            while True:
                cv.imshow('main', frame)
                key = cv.waitKey(0)

                if key == ord('q'):
                    break
                elif key == KEY_ENTER:
                    print(f"Marked frame {i} as new.")
                    print(i, file=out)
                elif key == ord('l'):
                    i, frame = stream.next()
                elif key == ord('h'):
                    i, frame = stream.prev()
                else:
                    print(key)

        except StopIteration:
            pass

    cv.destroyWindow('main')


if __name__ == '__main__':
    main()
