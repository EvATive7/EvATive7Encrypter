import argparse
import logging
import sys
import time

from evative7enc import *

logging.basicConfig(level=logging.ERROR, format="%(levelname)s - %(message)s")

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


def _mainv1(model: EvATive7ENCv1 | EvATive7ENCv1Short, input_, mode, key=None):
    if mode == "enc":
        if not key:
            key = model.key()
        result = model.encode_to_evative7encformatv1(key, input_)
    elif mode == "dec":
        if not key:
            result = model.decode_from_evative7encformatv1(input_)
        else:
            result = model.decode(key, input_)
    else:
        raise Exception("Invalid mode. Use 'enc' or 'dec'")

    return result


def main():
    global input_file, output_file
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
        dest="version",
        required=True,
        help="Version of EvATive7ENC.",
    )

    parser_v1 = subparsers.add_parser("v1", help="EvATive7ENCv1")
    parser_v1.add_argument(
        "--mode",
        choices=["enc", "dec"],
        default="enc",
        help="Mode of operation: 'enc' for encryption or 'dec' for decryption.",
    )
    parser_v1.add_argument(
        "--key",
        nargs="?",
        help="Key for encoding or decoding. If not specified, a random key will be generated for encryption.",
    )
    parser_v1short = subparsers.add_parser("v1short", help="EvATive7ENCv1Short")
    parser_v1short.add_argument(
        "--mode",
        choices=["enc", "dec"],
        default="enc",
        help="Mode of operation: 'enc' for encryption or 'dec' for decryption.",
    )
    parser_v1short.add_argument(
        "--key",
        nargs="?",
        help="Key for encoding or decoding. If not specified, a random key will be generated for encryption.",
    )

    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file

    if args.version == "v1":
        _output(_mainv1(EvATive7ENCv1, _input(), args.mode, args.key))
    elif args.version == "v1short":
        _output(_mainv1(EvATive7ENCv1Short, _input(), args.mode, args.key))
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
