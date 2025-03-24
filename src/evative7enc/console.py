import argparse
import io
import logging
import sys
from pathlib import Path

from evative7enc import *

DEFAULT_ENCODING = "utf-8"
logging.basicConfig(level=logging.ERROR, format="%(levelname)s - %(message)s")

if sys.stdin.encoding is None and hasattr(sys.stdin, "buffer"):
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding=DEFAULT_ENCODING)
if sys.stdout.encoding is None and hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=DEFAULT_ENCODING)


def _input(input_file: str):
    if input_file:
        input_file = Path(input_file)
        if not input_file.exists():
            logging.error(f"Input file '{input_file}' not found.")
            exit(1)
        else:
            return input_file.read_text(encoding=DEFAULT_ENCODING)
    else:
        return sys.stdin.read().strip()


def _output(content, output_file: str):
    if output_file:
        output_file = Path(output_file)
        output_file.touch(exist_ok=True)
        output_file.write_text(content, encoding=DEFAULT_ENCODING)
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
        "mode",
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

    if args.input_file:
        input_file = Path(args.input_file)
    if args.output_file:
        output_file = Path(args.output_file)

    alg = algs[args.id]

    input_ = _input(args.input_file)
    result = _mainv1(alg, input_, args.mode, args.key)
    _output(result, args.output_file)


if __name__ == "__main__":
    main()
