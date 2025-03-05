import const
import pytest

from evative7enc import *


def _testv1(alg: type[EvATive7ENCv1]):
    key = alg.key()
    origin = const.LONG_TEXT

    encrypted = alg.encrypt_to_evative7encformatv1(key, origin)
    assert encrypted is not None

    decrypted = alg.decrypt_from_evative7encformatv1(encrypted)
    assert decrypted == origin


@pytest.mark.parametrize(
    "alg",
    [EvATive7ENCv1, EvATive7ENCv1Short, EvATive7ENCv1Chinese],
)
def test_EvATive7ENCv1(alg: type[EvATive7ENCv1]):
    _testv1(alg)
