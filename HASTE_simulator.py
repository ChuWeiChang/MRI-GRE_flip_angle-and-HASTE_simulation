import numpy as np
import matplotlib.pyplot as plt
import phantominator as ph
import argparse


def main(config):
    img = ph.shepp_logan(config["size"])

    k = np.fft.fftshift(np.fft.fft2(img))

    fig, axs = plt.subplots(1, len(config["t2"]) + 1, figsize=(10, 4))

    axs[0].imshow(img, cmap="gray")
    axs[0].set_title("Original")
    axs[0].axis("off")
    for i, t2 in enumerate(config["t2"]):
        k_modified = np.zeros_like(k, dtype=complex)
        t2_filter = lambda m, t: m * np.exp(-t / t2)

        time = config["te"]
        esp = config["esp"]
        offset = int(k.shape[0] / 2)
        for phase_encode in range(offset):
                k_modified[phase_encode + offset]= t2_filter(k[phase_encode + offset], time)
                time += esp

        bottom_half_data = k_modified[offset + 1:]
        flipped_data = np.flip(bottom_half_data, axis=(0, 1))
        aligned_data = np.roll(flipped_data, 1, axis=1)
        k_modified[1: offset] = np.conj(aligned_data)

        img_mod_cplx = np.fft.ifft2(np.fft.ifftshift(k_modified))
        img_mod_mag = np.abs(img_mod_cplx)

        axs[i+1].imshow(img_mod_mag, cmap="gray")
        axs[i+1].set_title(f"t2 = {t2}ms")
        axs[i+1].axis("off")

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
    parser.add_argument(
        "--te",
        type=int,
        default=20,
    )

    args = parser.parse_args()
    configs = {
        "size": args.size,
        "te": args.te,
        "t2": [60,120,180,240],
        "esp": 4,
    }

    main(configs)