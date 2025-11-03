import argparse
from pathlib import Path

from libvhls.dist import VitisHLSDist


def main(args: argparse.Namespace) -> None:
    if args.dist_dir is None:
        print(
            "No Vitis HLS distribution directory given, trying to find one"
            " automatically..."
        )
        try:
            dist = VitisHLSDist.auto_find()
        except RuntimeError:
            print(
                "Could not find Vitis HLS distribution automatically, please specify"
                " the path manually."
            )
            return
    else:
        print("Looking for the specified Vitis HLS distribution...")
        dist = VitisHLSDist(args.dist_dir)

    print(f"Vitis HLS distribution loaded from: {dist.dist_dir}")
    print()
    print("=" * 80)
    print("Vitis HLS distribution information:")
    print(f"  vitis_hls_bin: {dist.vitis_hls_bin}")
    print(f"  bin_dir: {dist.bin_dir}")
    print(f"  include_dir: {dist.include_dir}")
    print("=" * 80)
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "A CLI program that uses libvhls to find and print information about a"
            " Vitis HLS distribution"
        )
    )

    parser.add_argument(
        "dist_dir",
        nargs="?",
        type=Path,
        help="The path to the Vitis HLS distribution",
    )

    args = parser.parse_args()
    main(args)
