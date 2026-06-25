"""
fallback.py
===========
Hardcoded PH market motorcycle data — no internet required.
Use this when scraper.py can't reach the target sites.

Output: data/bikes_raw.json

Run:
  python src/fallback.py
"""

import json
from pathlib import Path
from utils import validate_records

OUT_FILE = Path(__file__).parent.parent / "data" / "bikes_raw.json"

# fmt: off
BIKES = [
    # ── HONDA ─────────────────────────────────────────────────────────────────

    # Auto Scooter
    {"brand": "Honda", "model": "Click 125i",         "type": "Auto Scooter",         "year": 2023, "engineSize": 125, "fuelSys": "fuel_injected", "coolSys": "air"},
    {"brand": "Honda", "model": "Click 160",           "type": "Auto Scooter",         "year": 2023, "engineSize": 160, "fuelSys": "fuel_injected", "coolSys": "liquid"},
    {"brand": "Honda", "model": "PCX 160",             "type": "Auto Scooter",         "year": 2023, "engineSize": 160, "fuelSys": "fuel_injected", "coolSys": "liquid"},
    {"brand": "Honda", "model": "ADV 160",             "type": "Auto Scooter",         "year": 2023, "engineSize": 160, "fuelSys": "fuel_injected", "coolSys": "liquid"},
    {"brand": "Honda", "model": "Stylo 160",           "type": "Auto Scooter",         "year": 2024, "engineSize": 160, "fuelSys": "fuel_injected", "coolSys": "liquid"},
    {"brand": "Honda", "model": "Giorno 125",          "type": "Auto Scooter",         "year": 2022, "engineSize": 125, "fuelSys": "fuel_injected", "coolSys": "air"},

    # Underbone
    {"brand": "Honda", "model": "Wave 110",            "type": "Underbone",            "year": 2023, "engineSize": 110, "fuelSys": "carbureted",    "coolSys": "air"},
    {"brand": "Honda", "model": "Wave 125",            "type": "Underbone",            "year": 2023, "engineSize": 125, "fuelSys": "fuel_injected", "coolSys": "air"},
    {"brand": "Honda", "model": "Wave 125i Alpha",     "type": "Underbone",            "year": 2023, "engineSize": 125, "fuelSys": "fuel_injected", "coolSys": "air"},
    {"brand": "Honda", "model": "EX5 Dream Fi",        "type": "Underbone",            "year": 2022, "engineSize": 110, "fuelSys": "fuel_injected", "coolSys": "air"},

    # Sport / Naked / Big Bike
    {"brand": "Honda", "model": "TMX 125 Alpha",       "type": "Sport/Naked/Big Bike", "year": 2023, "engineSize": 125, "fuelSys": "carbureted",    "coolSys": "air"},
    {"brand": "Honda", "model": "XRM 125",             "type": "Sport/Naked/Big Bike", "year": 2023, "engineSize": 125, "fuelSys": "carbureted",    "coolSys": "air"},
    {"brand": "Honda", "model": "RS-X 150",            "type": "Sport/Naked/Big Bike", "year": 2023, "engineSize": 150, "fuelSys": "fuel_injected", "coolSys": "air"},
    {"brand": "Honda", "model": "CB150R StreetSter",   "type": "Sport/Naked/Big Bike", "year": 2023, "engineSize": 150, "fuelSys": "fuel_injected", "coolSys": "liquid"},
    {"brand": "Honda", "model": "CB300R",              "type": "Sport/Naked/Big Bike", "year": 2023, "engineSize": 286, "fuelSys": "fuel_injected", "coolSys": "liquid"},
    {"brand": "Honda", "model": "CBR150R",             "type": "Sport/Naked/Big Bike", "year": 2023, "engineSize": 150, "fuelSys": "fuel_injected", "coolSys": "liquid"},
    {"brand": "Honda", "model": "CBR650R",             "type": "Sport/Naked/Big Bike", "year": 2023, "engineSize": 649, "fuelSys": "fuel_injected", "coolSys": "liquid"},

    # ── YAMAHA ────────────────────────────────────────────────────────────────

    # Auto Scooter
    {"brand": "Yamaha", "model": "Mio i 125",           "type": "Auto Scooter",         "year": 2023, "engineSize": 125, "fuelSys": "fuel_injected", "coolSys": "air"},
    {"brand": "Yamaha", "model": "Mio Gear 125",        "type": "Auto Scooter",         "year": 2023, "engineSize": 125, "fuelSys": "fuel_injected", "coolSys": "air"},
    {"brand": "Yamaha", "model": "Mio Aerox 155",       "type": "Auto Scooter",         "year": 2023, "engineSize": 155, "fuelSys": "fuel_injected", "coolSys": "liquid"},
    {"brand": "Yamaha", "model": "NMAX 155",            "type": "Auto Scooter",         "year": 2023, "engineSize": 155, "fuelSys": "fuel_injected", "coolSys": "liquid"},
    {"brand": "Yamaha", "model": "NMAX 155 Connected",  "type": "Auto Scooter",         "year": 2024, "engineSize": 155, "fuelSys": "fuel_injected", "coolSys": "liquid"},
    {"brand": "Yamaha", "model": "XMAX 250",            "type": "Auto Scooter",         "year": 2023, "engineSize": 250, "fuelSys": "fuel_injected", "coolSys": "liquid"},

    # Underbone
    {"brand": "Yamaha", "model": "Sniper 150",          "type": "Underbone",            "year": 2023, "engineSize": 150, "fuelSys": "fuel_injected", "coolSys": "air"},
    {"brand": "Yamaha", "model": "Sniper 155R",         "type": "Underbone",            "year": 2023, "engineSize": 155, "fuelSys": "fuel_injected", "coolSys": "liquid"},
    {"brand": "Yamaha", "model": "Jupiter MX King 150", "type": "Underbone",            "year": 2023, "engineSize": 150, "fuelSys": "fuel_injected", "coolSys": "liquid"},
    {"brand": "Yamaha", "model": "Jupiter Z1",          "type": "Underbone",            "year": 2023, "engineSize": 115, "fuelSys": "carbureted",    "coolSys": "air"},

    # Sport / Naked / Big Bike
    {"brand": "Yamaha", "model": "MT-15",               "type": "Sport/Naked/Big Bike", "year": 2023, "engineSize": 155, "fuelSys": "fuel_injected", "coolSys": "liquid"},
    {"brand": "Yamaha", "model": "MT-03",               "type": "Sport/Naked/Big Bike", "year": 2023, "engineSize": 321, "fuelSys": "fuel_injected", "coolSys": "liquid"},
    {"brand": "Yamaha", "model": "R15M",                "type": "Sport/Naked/Big Bike", "year": 2023, "engineSize": 155, "fuelSys": "fuel_injected", "coolSys": "liquid"},
    {"brand": "Yamaha", "model": "R15 V4",              "type": "Sport/Naked/Big Bike", "year": 2023, "engineSize": 155, "fuelSys": "fuel_injected", "coolSys": "liquid"},
    {"brand": "Yamaha", "model": "Vixion R",            "type": "Sport/Naked/Big Bike", "year": 2023, "engineSize": 155, "fuelSys": "fuel_injected", "coolSys": "liquid"},
    {"brand": "Yamaha", "model": "FZ15",                "type": "Sport/Naked/Big Bike", "year": 2022, "engineSize": 150, "fuelSys": "fuel_injected", "coolSys": "air"},

    # ── SUZUKI ────────────────────────────────────────────────────────────────

    # Auto Scooter
    {"brand": "Suzuki", "model": "Skydrive 125",        "type": "Auto Scooter",         "year": 2022, "engineSize": 125, "fuelSys": "carbureted",    "coolSys": "air"},
    {"brand": "Suzuki", "model": "Address 110",         "type": "Auto Scooter",         "year": 2022, "engineSize": 110, "fuelSys": "fuel_injected", "coolSys": "air"},
    {"brand": "Suzuki", "model": "Burgman Street 125",  "type": "Auto Scooter",         "year": 2023, "engineSize": 125, "fuelSys": "fuel_injected", "coolSys": "air"},
    {"brand": "Suzuki", "model": "Avenis 125",          "type": "Auto Scooter",         "year": 2023, "engineSize": 125, "fuelSys": "fuel_injected", "coolSys": "air"},

    # Underbone
    {"brand": "Suzuki", "model": "Smash 115 Fi",        "type": "Underbone",            "year": 2023, "engineSize": 115, "fuelSys": "fuel_injected", "coolSys": "air"},
    {"brand": "Suzuki", "model": "Skydrive Crossover",  "type": "Underbone",            "year": 2022, "engineSize": 125, "fuelSys": "carbureted",    "coolSys": "air"},

    # Sport / Naked / Big Bike
    {"brand": "Suzuki", "model": "Raider R150 Fi",      "type": "Sport/Naked/Big Bike", "year": 2023, "engineSize": 150, "fuelSys": "fuel_injected", "coolSys": "liquid"},
    {"brand": "Suzuki", "model": "Raider J Crossover",  "type": "Sport/Naked/Big Bike", "year": 2023, "engineSize": 115, "fuelSys": "fuel_injected", "coolSys": "air"},
    {"brand": "Suzuki", "model": "GSX-R150",            "type": "Sport/Naked/Big Bike", "year": 2023, "engineSize": 150, "fuelSys": "fuel_injected", "coolSys": "liquid"},
    {"brand": "Suzuki", "model": "GSX-S150",            "type": "Sport/Naked/Big Bike", "year": 2023, "engineSize": 150, "fuelSys": "fuel_injected", "coolSys": "liquid"},
    {"brand": "Suzuki", "model": "GSX-S750",            "type": "Sport/Naked/Big Bike", "year": 2022, "engineSize": 749, "fuelSys": "fuel_injected", "coolSys": "liquid"},
    {"brand": "Suzuki", "model": "V-Strom SX 250",      "type": "Sport/Naked/Big Bike", "year": 2023, "engineSize": 249, "fuelSys": "fuel_injected", "coolSys": "air"},

    # ── KAWASAKI ──────────────────────────────────────────────────────────────

    # Auto Scooter
    {"brand": "Kawasaki", "model": "J300",              "type": "Auto Scooter",         "year": 2021, "engineSize": 299, "fuelSys": "fuel_injected", "coolSys": "liquid"},

    # Underbone
    {"brand": "Kawasaki", "model": "CT100B",            "type": "Underbone",            "year": 2023, "engineSize": 100, "fuelSys": "carbureted",    "coolSys": "air"},
    {"brand": "Kawasaki", "model": "Fury 125R",         "type": "Underbone",            "year": 2023, "engineSize": 125, "fuelSys": "carbureted",    "coolSys": "air"},

    # Sport / Naked / Big Bike
    {"brand": "Kawasaki", "model": "Barako II 175",     "type": "Sport/Naked/Big Bike", "year": 2020, "engineSize": 175, "fuelSys": "carbureted",    "coolSys": "air"},
    {"brand": "Kawasaki", "model": "Rouser NS160",      "type": "Sport/Naked/Big Bike", "year": 2023, "engineSize": 160, "fuelSys": "fuel_injected", "coolSys": "air"},
    {"brand": "Kawasaki", "model": "Rouser NS200",      "type": "Sport/Naked/Big Bike", "year": 2023, "engineSize": 199, "fuelSys": "fuel_injected", "coolSys": "air"},
    {"brand": "Kawasaki", "model": "Z125 Pro",          "type": "Sport/Naked/Big Bike", "year": 2023, "engineSize": 125, "fuelSys": "fuel_injected", "coolSys": "air"},
    {"brand": "Kawasaki", "model": "Z400",              "type": "Sport/Naked/Big Bike", "year": 2023, "engineSize": 399, "fuelSys": "fuel_injected", "coolSys": "liquid"},
    {"brand": "Kawasaki", "model": "Z650",              "type": "Sport/Naked/Big Bike", "year": 2023, "engineSize": 649, "fuelSys": "fuel_injected", "coolSys": "liquid"},
    {"brand": "Kawasaki", "model": "Ninja 400",         "type": "Sport/Naked/Big Bike", "year": 2023, "engineSize": 399, "fuelSys": "fuel_injected", "coolSys": "liquid"},
    {"brand": "Kawasaki", "model": "Ninja ZX-25R",      "type": "Sport/Naked/Big Bike", "year": 2023, "engineSize": 249, "fuelSys": "fuel_injected", "coolSys": "liquid"},
    {"brand": "Kawasaki", "model": "Dominar 250",       "type": "Sport/Naked/Big Bike", "year": 2023, "engineSize": 248, "fuelSys": "fuel_injected", "coolSys": "liquid"},
    {"brand": "Kawasaki", "model": "KLX 150",           "type": "Sport/Naked/Big Bike", "year": 2023, "engineSize": 150, "fuelSys": "carbureted",    "coolSys": "air"},
    {"brand": "Kawasaki", "model": "KLX 230",           "type": "Sport/Naked/Big Bike", "year": 2023, "engineSize": 233, "fuelSys": "fuel_injected", "coolSys": "air"},
]
# fmt: on


def main():
    valid, errors = validate_records(BIKES)

    if errors:
        print("⚠  Validation errors:")
        for e in errors:
            print(e)
    else:
        print("✅  All records valid")

    from collections import Counter
    print(f"\n📊  {len(valid)} records")
    print("  Brands:", dict(Counter(b["brand"] for b in valid)))
    print("  Types: ", dict(Counter(b["type"]  for b in valid)))

    OUT_FILE.write_text(json.dumps(valid, indent=2, ensure_ascii=False))
    print(f"\n💾  Written → {OUT_FILE}")


if __name__ == "__main__":
    main()
