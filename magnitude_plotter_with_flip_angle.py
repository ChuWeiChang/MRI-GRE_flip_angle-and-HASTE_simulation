import numpy as np
import matplotlib.pyplot as plt
import argparse
from math import cos, sin, radians, degrees

def parse_args():
    parser = argparse.ArgumentParser(
        description="Simulate MRI magnetization evolution."
    )

    parser.add_argument(
        "--duration",
        type=int,
        default=256,
        help="Duration in units of TR (default: 256)",
    )
    parser.add_argument(
        "--t1_1",
        type=float,
        default=1300.0,
        help="T1 in ms (default: 1300)",
    )
    parser.add_argument(
        "--t1_2",
        type=float,
        default=1300.0,
        help="T1 in ms (default: 1300)",
    )
    parser.add_argument(
        "--tr",
        type=int,
        default=90,
        help="TR in ms (default: 90)",
    )
    parser.add_argument(
        "--sample-num",
        type=int,
        default=10,
        help="Number of sample points for plotting (default: 10)",
    )

    return parser.parse_args()

def plot(config, time_all, longitudinal, angle):
    step = 20
    idx_ticks = list(range(0, config["duration"], step))
    fig, ax = plt.subplots()

    ax.plot(time_all, longitudinal, label="M_z (Longitudinal)", color="blue")

    ax.set_xticks([time_all[i * config["sample_num"]] for i in idx_ticks])  # positions in TIME units
    ax.set_xticklabels([str(i) for i in idx_ticks])
    ax.set_xlabel("RF")
    ax.set_ylabel("Magnetization / M0")
    ax.set_title(f"Magnetization with angle {degrees(angle)}")
    ax.grid(True)
    ax.legend()

    return fig

def calc_magnetization(config, t1, angle):
    m0 = 1
    m0_pre = m0
    t1_r = lambda x: m0 - (m0 - m0_pre * cos(angle)) * np.exp(-x / t1)

    # initial time samples for the first [-TR, 0] interval
    time_all = []
    longitudinal = []

    for t in range(0, config["duration"]):
        time = np.linspace(0, config["tr"], config["sample_num"])
        mz = t1_r(time)

        time_all.extend(list(time + (t+1) * config["tr"]))
        longitudinal.extend(mz)
        m0_pre = mz[-1]
    return plot(config, time_all, longitudinal, angle)

def contrast(config, angle) -> float:
    pass
def main():
    args = parse_args()
    config = {
        "duration": args.duration,
        "t1_1": args.t1_1,
        "t1_2": args.t1_2,
        "tr": args.tr,
        "sample_num": args.sample_num,
        "flip_angles": [10, 30, 50, 70, 90],
    }
    mag_plots = {
        "tissue_1": {},
        "tissue_2": {}
    }
    for angle in config["flip_angles"]:
        mag_plots["tissue_1"][angle] = calc_magnetization(config, config["t1_1"],radians(angle))
        # mag_plots["tissue_2"][angle] = calc_magnetization(config, config["t1_2"],radians(angle))


    plt.show()
    # contrasts = {fa: 0.0 for fa in config["flip_angles"]}
    # for angle in config["flip_angles"]:
    #     contrasts[angle] = contrast(config, radians(angle))

if __name__ == '__main__':
    main()