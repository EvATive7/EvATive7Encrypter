import io
from pathlib import Path
from typing import Optional

import const
import pytest
from pytest_console_scripts import ScriptRunner

from evative7enc import *


def _testv1(
    script_runner: ScriptRunner,
    algname,
    origin_file: Optional[Path],
    encoded_file: Optional[Path],
    decoded_file: Optional[Path],
    custom_key: bool,
):
    origin = const.LONG_TEXT

    if origin_file:
        origin_file.parent.mkdir(parents=True, exist_ok=True)
        origin_file.touch(exist_ok=True)
        origin_file.write_text(origin, "utf-8")

    if encoded_file:
        encoded_file.parent.mkdir(parents=True, exist_ok=True)
        encoded_file.touch(exist_ok=True)

    if decoded_file:
        decoded_file.parent.mkdir(parents=True, exist_ok=True)
        decoded_file.touch(exist_ok=True)

    alg: type[EvATive7ENCv1] = algs[algname]

    if custom_key:
        key = alg.key()

    enc_cmd = ["evative7enc"]
    if origin_file:
        enc_cmd.append("--input-file")
        enc_cmd.append(str(origin_file.absolute()))
    if encoded_file:
        enc_cmd.append("--output-file")
        enc_cmd.append(str(encoded_file.absolute()))
    enc_cmd.append(algname)
    enc_cmd.append("--mode")
    enc_cmd.append("enc")
    if custom_key:
        enc_cmd.append("--key")
        enc_cmd.append(key)

    if origin_file:
        enc_result = script_runner.run(enc_cmd)
    else:
        enc_result = script_runner.run(enc_cmd, stdin=io.StringIO(origin))

    assert enc_result.success

    if not encoded_file:
        encoded = enc_result.stdout

    dec_cmd = ["evative7enc"]
    if encoded_file:
        dec_cmd.append("--input-file")
        dec_cmd.append(str(encoded_file.absolute()))
    if decoded_file:
        dec_cmd.append("--output-file")
        dec_cmd.append(str(decoded_file.absolute()))
    dec_cmd.append(algname)
    dec_cmd.append("--mode")
    dec_cmd.append("dec")

    if encoded_file:
        dec_result = script_runner.run(dec_cmd)
    else:
        dec_result = script_runner.run(dec_cmd, stdin=io.StringIO(encoded))

    assert dec_result.success

    if decoded_file:
        decoded = decoded_file.read_text("utf-8")
    else:
        decoded = dec_result.stdout

    assert origin.strip() == decoded.strip()

    if origin_file:
        origin_file.unlink(missing_ok=True)
    if encoded_file:
        encoded_file.unlink(missing_ok=True)
    if decoded_file:
        decoded_file.unlink(missing_ok=True)


@pytest.mark.parametrize(
    "custom_key",
    [
        False,
        True,
    ],
    ids=["Random Key", "Custom Key"],
)
@pytest.mark.parametrize(
    "origin_file, encoded_file, decoded_file",
    [
        (None, None, None),
        (
            Path(".cache/test_console/origin.txt"),
            Path(".cache/test_console/encoded.txt"),
            Path(".cache/test_console/decoded.txt"),
        ),
    ],
    ids=["stdio", "file"],
)
@pytest.mark.parametrize(
    "alg",
    ["v1", "v1short", "v1cn"],
)
def test_EvATive7ENCv1(
    script_runner: ScriptRunner,
    alg: str,
    origin_file: Optional[Path],
    encoded_file: Optional[Path],
    decoded_file: Optional[Path],
    custom_key: bool,
):
    _testv1(script_runner, alg, origin_file, encoded_file, decoded_file, custom_key)
