from .v1 import EvATive7ENCv1, EvATive7ENCv1Chinese, EvATive7ENCv1Short
from types import MappingProxyType as _MappingProxyType

_algs: dict[str, type] = {
    "v1": EvATive7ENCv1,
    "v1short": EvATive7ENCv1Short,
    "v1cn": EvATive7ENCv1Chinese,
}


algs = _MappingProxyType(_algs)
