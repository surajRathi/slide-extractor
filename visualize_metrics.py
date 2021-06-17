#! /usr/bin/env python

from input import CVReadVideo
from slide_check import SimpleSlideChecker

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

FILES = ['./videos/ppt_test.mp4', './videos/wb_test.mp4']

IMAGE_NAME_FORMAT = 'image_%04d.png'


def main():
    FILE = FILES[1]
    VIDEO_NAME = FILE[:FILE.rfind('.')] if (index := FILE.rfind('/')) == -1 else FILE[index + 1:FILE.rfind('.')]
    KEY_FRAMES_FILENAME = f"./videos/{VIDEO_NAME}.txt"
    METRIC_OUTPUT_FILENAME = f"./videos/{VIDEO_NAME}.csv"

    keyframes: list[int] = []
    with open(KEY_FRAMES_FILENAME) as f:
        for line in f:
            if (line := line.strip())[0] == '#':
                continue
            keyframes.append(int(line))

    metrics = None
    with CVReadVideo(FILE) as stream:
        metrics = np.zeros((4, len(stream)))

        sc = SimpleSlideChecker(*stream.get_dims())
        prev = next(stream)
        i = 1
        for i, frame in enumerate(stream, start=1):
            n, n_bg, n_changed, n_overwritten, n_annotated = sc.extract_metrics(frame, prev)
            prev = frame

            p_bg = n_bg / n
            p_ch = n_changed / n * 10
            p_ow = n_overwritten / n * 10
            p_oc = np.nan if n_changed == 0 else n_overwritten / n_changed
            metrics[:, i] = (p_bg, p_ch, p_ow, p_oc)

            if i % 500 == 0:
                print('.', end='')

        print('\n', i)

    sns.set_style("darkgrid")
    fig = plt.figure(figsize=(20, 10))

    sns.scatterplot(data=metrics[0], label='Percent Background')
    sns.scatterplot(data=metrics[1], label='Percent Changed (* 10)')
    sns.scatterplot(data=metrics[2], label='Percent Overwritten (* 10)')
    sns.scatterplot(data=metrics[3], label='Percent Overwritten wrt Changed')

    plt.xlim(0, metrics.shape[1])
    plt.ylim(0, 1)
    for kf in keyframes:
        plt.axvline(x=kf, color='black', linewidth=15, alpha=0.2)

    fig.show()

    print()

    np.savetxt(METRIC_OUTPUT_FILENAME, metrics, delimiter=',')


if __name__ == '__main__':
    main()
