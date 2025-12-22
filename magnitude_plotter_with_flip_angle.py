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

def plot(config, tissue):
    angles = config["flip_angles"]
    step = 20
    fig, axes = plt.subplots(1, len(angles), figsize=(4 * len(angles),3), sharey=True)

    idx_ticks = list(range(0, config["duration"], step))
    for i, angle in enumerate(angles):
        ax = axes[i]
        time_all = tissue[angle]["time"]
        longitudinal = tissue[angle]["mz"]

        ax.plot(time_all, longitudinal, label="M_z (Longitudinal)", color="blue") # tick positions in TIME units (pick the time at those TR indices)
        ax.set_xticks([time_all[k * config["sample_num"]] for k in idx_ticks])
        ax.set_xticklabels([str(k) for k in idx_ticks], fontsize=6)
        ax.set_xlabel("RF")

        ax.tick_params(axis="y", labelleft=True)
        if i == 0:
            ax.set_ylabel("Magnetization / M0")

        ax.set_title(f"Angle {angle}°")
        ax.grid(True)
        ax.legend()

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
    return time_all, longitudinal

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
    tissue_t1 = {
        "tissue_1": config["t1_1"],
        "tissue_2": config["t1_2"],
    }

    mags = {tissue: {} for tissue in tissue_t1}

    # compute and store data
    for tissue, t1 in tissue_t1.items():
        for angle in config["flip_angles"]:
            time_all, mz = calc_magnetization(config, t1, radians(angle))
            mags[tissue][angle] = {"time": time_all, "mz": mz}

    # plot each tissue (1×5 each)
    for tissue in tissue_t1:
        plot(config, mags[tissue])
    plt.show()
    # contrasts = {fa: 0.0 for fa in config["flip_angles"]}
    # for angle in config["flip_angles"]:
    #     contrasts[angle] = contrast(config, radians(angle))

if __name__ == '__main__':
    main()