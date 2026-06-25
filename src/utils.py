"""
utils.py — shared helpers for normalising scraped spec strings
into your DB enum values.
"""

import re
from typing import Optional


def normalise_type(raw: str) -> str:
    """Map scraped category string → bikeTypeEnum value."""
    t = raw.lower()
    if any(k in t for k in ["scooter", "automatic", "cvt", "maxi"]):
        return "Auto Scooter"
    if any(k in t for k in ["underbone", "cub", "step-through", "moped"]):
        return "Underbone"
    # default — sport/naked covers standard, dual-sport, big bike
    return "Sport/Naked/Big Bike"


def normalise_fuel(raw: str) -> str:
    """Map scraped fuel string → fuelSystemEnum value."""
    t = raw.lower()
    if any(k in t for k in ["fi", "fuel inject", "efi", "pgm-fi", "injection"]):
        return "fuel_injected"
    return "carbureted"


def normalise_cool(raw: str) -> str:
    """Map scraped cooling string → coolingSystemEnum value."""
    t = raw.lower()
    if any(k in t for k in ["liquid", "water", "oil-cooled"]):
        return "liquid"
    return "air"


def extract_cc(text: str) -> Optional[int]:
    """Pull displacement in cc from a spec string like '155cc' or '155 cc'."""
    m = re.search(r"(\d{2,4})\s*cc", text, re.I)
    return int(m.group(1)) if m else None


def validate_records(bikes: list[dict]) -> tuple[list[dict], list[str]]:
    """
    Validate a list of bike dicts against enum constraints.
    Returns (valid_records, error_messages).
    """
    valid_types    = {"Auto Scooter", "Underbone", "Sport/Naked/Big Bike"}
    valid_fuel_sys = {"carbureted", "fuel_injected"}
    valid_cool_sys = {"air", "liquid"}

    valid:  list[dict] = []
    errors: list[str]  = []

    for b in bikes:
        ref = f"{b.get('brand', '?')} {b.get('model', '?')}"
        errs = []
        if not b.get("brand"):               errs.append("missing brand")
        if not b.get("model"):               errs.append("missing model")
        if b.get("type") not in valid_types: errs.append(f"bad type: {b.get('type')}")
        if b.get("fuelSys") not in valid_fuel_sys: errs.append(f"bad fuelSys: {b.get('fuelSys')}")
        if b.get("coolSys") not in valid_cool_sys: errs.append(f"bad coolSys: {b.get('coolSys')}")
        yr = b.get("year", 0)
        if not (1990 <= yr <= 2026): errs.append(f"bad year: {yr}")

        if errs:
            errors.append(f"  ✗ {ref}: {', '.join(errs)}")
        else:
            valid.append(b)

    return valid, errors
