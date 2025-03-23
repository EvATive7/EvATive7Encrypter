import argparse
import io
import logging
import sys
import time

from evative7enc import *

logging.basicConfig(level=logging.ERROR, format="%(levelname)s - %(message)s")
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")

input_file = None
output_file = None


def _input():
    if input_file:
        with open(input_file, "r", encoding="utf-8") as f:
            origin = f.read()
    else:
        origin = sys.stdin.read()
    return origin


def _output(content):
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)
    else:
        print(content)


def _mainv1(alg: type[EvATive7ENCv1], input_, mode, key=None):
    if mode == "enc":
        if not key:
            key = alg.key()
        result = alg.encrypt_to_evative7encformatv1(key, input_)
    elif mode == "dec":
        result = alg.decrypt_from_evative7encformatv1(input_)
    else:
        raise Exception("Invalid mode. Use 'enc' or 'dec'")

    return result


def _add_v1_sub_parser(subparsers, name, description):
    parser = subparsers.add_parser(name, help=description)
    parser.add_argument(
        "--mode",
        choices=["enc", "dec"],
        default="enc",
        help="Mode of operation: 'enc' for encryption or 'dec' for decryption.",
    )
    parser.add_argument(
        "--key",
        nargs="?",
        help="Key for encryption. If not specified, a random key will be generated for encryption.",
    )
    return parser


def _get_parser():
    parser = argparse.ArgumentParser(description="Encrypter/Decrypter via EvATive7ENC")
    parser.add_argument(
        "--input-file",
        help="Input file to be processed. If not specified, read from standard input.",
    )
    parser.add_argument(
        "--output-file",
        help="Output file for the processed content. If not specified, write to standard output.",
    )

    subparsers = parser.add_subparsers(
        dest="id",
        required=True,
        help="ID of EvATive7ENC.",
    )

    _add_v1_sub_parser(subparsers, "v1", "EvATive7ENCv1")
    _add_v1_sub_parser(subparsers, "v1short", "EvATive7ENCv1Short")
    _add_v1_sub_parser(subparsers, "v1cn", "EvATive7ENCv1Chinese")

    return parser


def main():
    global input_file, output_file

    parser = _get_parser()
    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file

    alg = algs[args.id]
    _output(_mainv1(alg, _input(), args.mode, args.key))


if __name__ == "__main__":
    main()
