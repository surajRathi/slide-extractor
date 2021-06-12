#! /usr/bin/env python3

import cv2 as cv
import os
import pathlib

from input import CVReadVideo
from slide_check import SimpleSlideChecker

FILE = ['./videos/ppt_test.mp4', './videos/wb_test.mp4'][0]

IMAGE_DIRECTORY = f'slide_extraction_out' + (
    FILE[:FILE.rfind('.')] if (index := FILE.rfind('/')) == -1 else FILE[index:FILE.rfind('.')]
)
IMAGE_NAME_FORMAT = 'image_%04d.png'

 
def main():
    try:
        os.makedirs(IMAGE_DIRECTORY)
    except FileExistsError:
        pass

    cv.namedWindow('main')

    with CVReadVideo(FILE) as stream:
        sc = SimpleSlideChecker(*stream.get_dims())
        i = 0
        prev = None
        for frame in stream:
            debug_new = False
            if sc.check(frame, prev):  # Save the previous frame when the slide changes
                debug_new = True
                print("NEW!!!")
                if prev is not None:
                    cv.imwrite(os.path.join(IMAGE_DIRECTORY, IMAGE_NAME_FORMAT % i), frame)
                    i += 1
            prev = frame

            # # Visualize Background
            # bg = np.array((255, 255, 255,)).reshape((1, 1, -1))
            # frame[((np.linalg.norm(frame - bg, ord=2, axis=2)) < 200)] = (0, 255, 255)

            if debug_new:
                frame[:, :, :] = (0, 0, 255)  # BGR

            cv.imshow('main', frame)
            if cv.waitKey(1) == ord('q'):
                break

        if prev is not None:
            cv.imwrite(os.path.join(IMAGE_DIRECTORY, IMAGE_NAME_FORMAT % i), frame)
    cv.destroyWindow('main')


if __name__ == '__main__':
    main()
