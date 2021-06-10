#! /usr/bin/env python3

import cv2 as cv
import os

from input import CVReadVideo
from slide_check import SlideChecker

FILE = '/home/suraj/test.mp4'
IMAGE_DIRECTORY = 'slides_extraction_out'
IMAGE_NAME_FORMAT = 'image_%04d.png'


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
