#! /usr/bin/env python
import os
from typing import Tuple

import cv2 as cv


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

#
# from mss import mss
# class MSSGetStream:
#     def __init__(self, monitor=None):
#         self.mss = mss()
#
#     def __enter__(self):
#         raise RuntimeError("Wayland is not Supported yet")
#         return self
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         pass
#
#     def __iter__(self):
#         return self
#
#     def __next__(self):
#         raise StopIteration()
#
#     def get_dims(self) -> Tuple[int, int]:  # height, width
#         return -1, -1
#
#
# class WaylandGetScreen:
#     def __init__(self, monitor=None):
#         assert os.getenv('$WAYLAND_DISPLAY') is not None
#
#     def __enter__(self):
#         raise RuntimeError("Wayland is not Supported yet")
#         return self
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         pass
#
#     def __iter__(self):
#         return self
#
#     def __next__(self):
#         raise StopIteration()
#
#     def get_dims(self) -> Tuple[int, int]:  # height, width
#         return -1, -1
