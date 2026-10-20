"""Dutch (Belgian) number formatting: 1.234,5 and €865.950."""
from __future__ import annotations


def num(value: float, decimals: int = 0) -> str:
    text = f"{value:,.{decimals}f}"
    return text.replace(",", "§").replace(".", ",").replace("§", ".")


def eur(value: float, decimals: int = 0) -> str:
    sign = "-" if value < 0 else ""
    return f"{sign}€{num(abs(value), decimals)}"


def pct(value: float, decimals: int = 1) -> str:
    return f"{num(value, decimals)}%"
