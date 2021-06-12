#! /usr/bin/env python
import numpy as np
import sys
import matplotlib
matplotlib.use('agg')

import matplotlib.pyplot as plt

import cv2 as cv
class SimpleSlideChecker:
    def __init__(self, width, height, **kwargs):
        self.params = {
            "cdist_threshold": 100,  # Max color dist for pixel to be in background
            "changed_cdist_threshold": 0,  # Minimum color dist for pixel to be changed

        }
        self.params.update(kwargs)

        self.bg = np.array((255,))
        self.n_pixels = width * height

    def toblackwhite(self, frame):
        gray_image = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        frame_threshed = cv.adaptiveThreshold(gray_image,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C, \
            cv.THRESH_BINARY,11,2)
        return frame_threshed/255

    def toBackgroundScore(self,frame,prev):

        score= (np.sum((frame-prev)[prev==0]))/(frame.shape[0]*frame.shape[1]-np.sum(prev))
     
        if not np.isnan(score):
            return round(score,3)
        else:
            return 0

    def changeratiobackground(self,frame,prev):
        totalchange=np.sum(np.abs(frame-prev))
        temp=(prev-frame)
        changebg=np.sum(temp[prev==0])
        return round(-changebg/totalchange,3)


    def check(self, frame: np.ndarray, prev=None) -> bool:
        if prev is None:
            return True

        frame_threshed = self.toblackwhite(frame)
        prev_threshed = self.toblackwhite(prev)
        
        back_score=self.toBackgroundScore(frame_threshed,prev_threshed)
        changeratio=self.changeratiobackground(frame_threshed,prev_threshed)

        print(back_score)
        print('back_score: {} and change_ratio: = {}'.format(back_score,changeratio))

        if changeratio!=0 and changeratio<0.6 and back_score>0.03:
            return True
        else:
            return False

        sys.exit()
       

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

        
