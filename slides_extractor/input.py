#! /usr/bin/env python
from __future__ import annotations
from typing import Tuple

import cv2 as cv
import numpy as np


class CVReadVideo:
    frame_t = np.ndarray

    def __init__(self, filename: str):
        self.filename = filename

    def __enter__(self):
        self.cap = cv.VideoCapture(self.filename)
        if not self.cap.isOpened():
            raise RuntimeError("Video capture not opened")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cap.release()

    def __iter__(self) -> CVReadVideo:
        return self

    def __next__(self) -> frame_t:
        ret, frame = self.cap.read()
        if ret:
            return frame
        raise StopIteration()

    def __len__(self) -> int:
        return int(self.cap.get(cv.CAP_PROP_FRAME_COUNT))

    def get_dims(self) -> Tuple[int, int]:
        return int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT)), \
               int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH))

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
