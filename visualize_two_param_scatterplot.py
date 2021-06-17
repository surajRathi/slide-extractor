#! /usr/bin/env python
import itertools

import matplotlib.pyplot
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

FILES = ['./videos/ppt_test.mp4', './videos/wb_test.mp4']


def main():
    FILE = FILES[1]
    VIDEO_NAME = FILE[:FILE.rfind('.')] if (index := FILE.rfind('/')) == -1 else FILE[index + 1:FILE.rfind('.')]
    KEY_FRAMES_FILENAME = f"./videos/{VIDEO_NAME}.txt"
    METRICS_DATA_FILENAME = f"./videos/{VIDEO_NAME}.csv"

    metrics = pd.read_csv(METRICS_DATA_FILENAME, header=None).to_numpy()

    keyframes = []
    with open(KEY_FRAMES_FILENAME) as f:
        for line in f:
            if (line := line.strip())[0] == '#':
                continue
            keyframes.append(int(line))
    keyframes = np.array(keyframes)
    # Using percent changed and percent overwritten as my metrics
    # doing grid/binary search on kf == (%_ch > p1 and %ow > p2)
    perc_bg = metrics[0]
    perc_ch = metrics[1] / 10
    perc_ow = metrics[2] / 10
    perc_oc = metrics[3]

    import seaborn as sns
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 3, figsize=(30, 20))
    axes = axes.reshape(-1)
    for ax in axes:
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('equal')

    for (a, b), (aa, bb), ax in zip(itertools.combinations((perc_bg, perc_ch, perc_ow, perc_oc), 2),
                                    itertools.combinations(('perc_bg', 'perc_ch', 'perc_ow', 'perc_oc'), 2),
                                    axes):
        sns.scatterplot(ax=ax, x=a, y=b, hue=np.in1d(np.arange(metrics.shape[1]), keyframes))
        ax.legend([], [], frameon=False)
        ax.set_xlabel(aa)
        ax.set_ylabel(bb)

    matplotlib.pyplot.show()


if __name__ == '__main__':
    main()
