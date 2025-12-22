import numpy as np
import matplotlib.pyplot as plt
import phantominator as ph
import argparse


def main(config):
    img = ph.shepp_logan(config["size"])

    k = np.fft.fftshift(np.fft.fft2(img))

    fig, axs = plt.subplots(1, len(config["t2"] + 1), figsize=(10, 4))

    axs[0].imshow(img, cmap="gray")
    axs[0].set_title("Original")
    axs[0].axis("off")


    k_modified = np.zeros_like(k)
    t2_filter = lambda m, t: m * np.exp(-t / config["t2"])

    time = config["te"]
    esp = config["esp"]
    for phase_encode in range(k.shape[0] / 2):
        for freq_encode in range(k.shape[1]):
            k_modified[phase_encode][freq_encode] = t2_filter(k[phase_encode][freq_encode], time)
            time += esp

    img_mod_cplx = np.fft.ifft2(np.fft.ifftshift(k_modified))
    img_mod_mag = np.abs(img_mod_cplx)



    axs[1].imshow(img_mod_mag, cmap="gray")
    axs[1].set_title("Modified Magnitude")
    axs[1].axis("off")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Modify real/imaginary parts of k-space and compare images."
    )

    parser.add_argument(
        "--size",
        type=int,
        default=192,
        help="Image size for Shepp-Logan phantom (default: 192)",
    )
    parser.add_argument(
        "--esp",
        type=int,
        default=4,
    )

    args = parser.parse_args()
    config = {
        "size": args.size,
        "te": args.te,
        "t2": [60,120,180,240],
        "esp": 4,
    }

    main(config)