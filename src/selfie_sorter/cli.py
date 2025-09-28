"""
This module provides a command-line interface for sorting selfies using NudeNet and
OpenNSFW2 classification algorithms. It includes functions to set up an argument parser
and defines the main entry point for the script execution.
"""
from __future__ import annotations
import argparse
from pathlib import Path

from .config import SortConfig
from .sorter import SelfieSorter


def build_parser() -> argparse.ArgumentParser:
    """
    Constructs and configures an argument parser for the selfie sorter application.

    This function sets up an argument parser for a command-line interface to sort
    selfies using NudeNet and OpenNSFW2 classifiers. It includes options for input
    and output directories, enables or disables features like NSFW classification,
    and configures various operational thresholds and flags.

    Returns:
        argparse.ArgumentParser:
            Configured argument parser instance.

    Parameters:
        None

    Raises:
        None
    """
    p = argparse.ArgumentParser(
        prog='selfie-sort',
        description='Local selfie sorter using NudeNet + OpenNSFW2'
    )
    p.add_argument('--in', dest='root_in', required=True, type=Path, help='Input directory')
    p.add_argument('--out', dest='root_out', required=True, type=Path, help='Output directory')
    p.add_argument(
        '--files',
        dest='input_files',
        type=Path,
        nargs='+',
        help='Optional explicit list of image files to process instead of scanning the input directory',
    )
    p.add_argument('--no-coarse', action='store_true', help='Disable OpenNSFW2 gate')
    p.add_argument('--nsfw-threshold', type=float, default=0.80)
    p.add_argument('--keep-safe', action='store_true', help='Keep safe images in place (do not move)')
    p.add_argument('--no-exif-strip', action='store_true', help='Do not remove metadata')
    p.add_argument('--dup-hamming', type=int, default=5)
    p.add_argument('--censor-copies', action='store_true', help='Write a censored copy beside each moved file')
    p.add_argument(
        '--censor-style',
        choices=['pixelated', 'blurred', 'black-box'],
        default='pixelated',
        help='Censoring style to apply to generated copies',
    )
    p.add_argument(
        '--censor-strength',
        type=int,
        default=12,
        help='Intensity of the censoring effect (block size, blur radius, or box height)',
    )
    p.add_argument(
        '--censor-label',
        default='CENSORED',
        help='Text drawn inside black-box censor copies (ignored for other styles)',
    )
    return p


def main() -> None:
    """
    Main entry point for the script.

    This function;
        - Initializes the argument parser;
        - Parses the command-line arguments;
        - Constructs a `SortConfig` object with the provided arguments;
        - Executes the `SelfieSorter` process via the `run` method.

    Parameters:
        None

    Returns:
        None
    """
    p = build_parser()
    a = p.parse_args()
    cfg = SortConfig(
        root_in=a.root_in,
        root_out=a.root_out,
        use_coarse_gate=not a.no_coarse,
        nsfw_threshold=a.nsfw_threshold,
        move_safe=not a.keep_safe,
        strip_metadata=not a.no_exif_strip,
        dup_hamming=a.dup_hamming,
        input_files=tuple(a.input_files) if a.input_files else None,
        write_censored=a.censor_copies,
        censor_style=a.censor_style.replace('-', '_'),
        censor_strength=a.censor_strength,
        censor_label=a.censor_label,
    )
    SelfieSorter(cfg).run()

if __name__ == '__main__':
    main()
