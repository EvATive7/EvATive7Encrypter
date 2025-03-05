<div align="center">

# EvATive7Encrypter

Definition, specification, implementation and toolkit of EvATive7ENC

[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/EvATive7/EvATive7Encrypter/package.yml)](https://github.com/EvATive7/EvATive7Encrypter/actions)
[![Python](https://img.shields.io/pypi/pyversions/EvATive7Encrypter)](https://pypi.org/project/EvATive7Encrypter)
[![PyPI version](https://badge.fury.io/py/EvATive7Encrypter.svg)](https://pypi.org/project/EvATive7Encrypter)

</div>

## Install

1. `pip install EvATive7Encrypter`

## Usage

### CLI

- using `evative7enc --help` to see help
- `Write-Output "thisIsATest" | evative7enc v1` (in PowerShell), `echo thisIsATest | evative7enc v1` (in bash or cmd)
- ...

### As a library

```python
import logging
from pathlib import Path

from evative7enc import *

logging.basicConfig(level=logging.DEBUG)

alg = EvATive7ENCv1

input_text = Path(".cache/txt/text.txt").read_text("utf-8")
key = alg.key()
encrypted = alg.encrypt_to_evative7encformatv1(key, input_text)
decrypted = alg.decrypt_from_evative7encformatv1(encrypted)

Path(".cache/txt/encrypted.txt").write_text(encrypted, "utf-8")
Path(".cache/txt/decrypted.txt").write_text(decrypted, "utf-8")

```
