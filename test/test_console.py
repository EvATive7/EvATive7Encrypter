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
    encrypted_file: Optional[Path],
    decrypted_file: Optional[Path],
    custom_key: bool,
):
    origin = const.LONG_TEXT

    if origin_file:
        origin_file.parent.mkdir(parents=True, exist_ok=True)
        origin_file.touch(exist_ok=True)
        origin_file.write_text(origin, "utf-8")

    if encrypted_file:
        encrypted_file.parent.mkdir(parents=True, exist_ok=True)
        encrypted_file.touch(exist_ok=True)

    if decrypted_file:
        decrypted_file.parent.mkdir(parents=True, exist_ok=True)
        decrypted_file.touch(exist_ok=True)

    alg: type[EvATive7ENCv1] = algs[algname]

    if custom_key:
        key = alg.key()

    enc_cmd = ["evative7enc"]
    if origin_file:
        enc_cmd.append("--input-file")
        enc_cmd.append(str(origin_file.absolute()))
    if encrypted_file:
        enc_cmd.append("--output-file")
        enc_cmd.append(str(encrypted_file.absolute()))
    enc_cmd.append(algname)
    enc_cmd.append("enc")
    if custom_key:
        enc_cmd.append("--key")
        enc_cmd.append(key)

    if origin_file:
        enc_result = script_runner.run(enc_cmd)
    else:
        enc_result = script_runner.run(enc_cmd, stdin=io.StringIO(origin))

    assert enc_result.success, enc_result.stderr

    if not encrypted_file:
        encrypted = enc_result.stdout

    dec_cmd = ["evative7enc"]
    if encrypted_file:
        dec_cmd.append("--input-file")
        dec_cmd.append(str(encrypted_file.absolute()))
    if decrypted_file:
        dec_cmd.append("--output-file")
        dec_cmd.append(str(decrypted_file.absolute()))
    dec_cmd.append(algname)
    dec_cmd.append("dec")

    if encrypted_file:
        dec_result = script_runner.run(dec_cmd)
    else:
        dec_result = script_runner.run(dec_cmd, stdin=io.StringIO(encrypted))

    assert dec_result.success, dec_result.stderr

    if decrypted_file:
        decrypted = decrypted_file.read_text("utf-8")
    else:
        decrypted = dec_result.stdout

    assert origin.strip() == decrypted.strip()

    if origin_file:
        origin_file.unlink(missing_ok=True)
    if encrypted_file:
        encrypted_file.unlink(missing_ok=True)
    if decrypted_file:
        decrypted_file.unlink(missing_ok=True)


@pytest.mark.parametrize(
    "custom_key",
    [
        False,
        True,
    ],
    ids=["Random Key", "Custom Key"],
)
@pytest.mark.parametrize(
    "origin_file, encrypted_file, decrypted_file",
    [
        (None, None, None),
        (
            Path(".cache/test_console/origin.txt"),
            Path(".cache/test_console/encrypted.txt"),
            Path(".cache/test_console/decrypted.txt"),
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
    encrypted_file: Optional[Path],
    decrypted_file: Optional[Path],
    custom_key: bool,
):
    _testv1(script_runner, alg, origin_file, encrypted_file, decrypted_file, custom_key)
