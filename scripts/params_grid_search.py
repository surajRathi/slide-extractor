#! /usr/bin/env python
import matplotlib.pyplot
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

FILES = ['./videos/ppt_test.mp4', './videos/wb_test.mp4']

def main():
    FILE = FILES[0]
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
    perc_ch = metrics[1] / 10
    perc_ow = metrics[2] / 10

    # def is_valid(a: float, b: float) -> bool:
    #     return np.array_equal(
    #         np.where((perc_ch > a) & (perc_ow > b))[0],
    #         keyframes
    #     )

    def score(a: float, b: float) -> int:
        indices = np.where((perc_ch > a) & (perc_ow > b))[0]
        if np.all(np.in1d(keyframes, indices)):
            return len(indices)
        return np.nan

    # # TODO: Use binary search
    # a = np.linspace(0, 1, 20)
    # b = np.linspace(0, 1, 20)

    a = np.linspace(0, 0.45, 40)
    b = np.linspace(0, 0.020, 40)
    aa, bb = np.meshgrid(a, b)

    # index_passes = np.frompyfunc(is_valid, 2, 1)(aa, bb)
    # print(np.where(index_passes))
    # print(np.where((perc_ch > 0.4) & (perc_ow > 0.1))[0])

    scores = np.frompyfunc(score, 2, 1)(aa, bb).astype(float)
    print(np.nanmin(scores), len(keyframes))
    import seaborn as sns
    import matplotlib.pyplot as plt
    plt.figure(figsize=(20, 10))
    sns.heatmap(np.clip(scores, 0, 80), vmin=len(keyframes), annot=True)
    matplotlib.pyplot.show()
    print(a[36], b[34])


if __name__ == '__main__':
    main()
