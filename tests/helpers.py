import functools
import json
from pathlib import Path

from erpcase import sap_extract, transform

ROOT = Path(__file__).resolve().parent.parent


@functools.lru_cache(maxsize=None)
def extract(mock: str) -> dict:
    return sap_extract.generate(mock)


@functools.lru_cache(maxsize=None)
def summary(mock: str) -> dict:
    return transform.migration_summary(extract(mock))


@functools.lru_cache(maxsize=None)
def programme() -> dict:
    return json.loads((ROOT / "data/programme.json").read_text(encoding="utf-8"))


def migrations() -> dict:
    return {m: summary(m) for m in sap_extract.MOCKS}
