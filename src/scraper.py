"""
scraper.py
==========
Scrapes PH motorcycle specs from:
  - zigwheels.ph
  - autodeal.com.ph
  - motodeal.com.ph

Requires a local/residential IP — PH moto sites block datacenter IPs.
Falls back gracefully per-source if a site is unreachable.

Output: data/bikes_raw.json

Run:
  python src/scraper.py
"""

import json
import re
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, Page, Browser

from utils import normalise_type, normalise_fuel, normalise_cool, extract_cc, validate_records

# ── Config ───────────────────────────────────────────────────────────────────
OUT_FILE = Path(__file__).parent.parent / "data" / "bikes_raw.json"
BRANDS   = ["Honda", "Yamaha", "Suzuki", "Kawasaki"]
DELAY    = 1.0   # seconds between page loads — be polite


@dataclass
class BikeRecord:
    brand:      str
    model:      str
    type:       str
    year:       int
    engineSize: Optional[int]
    fuelSys:    str
    coolSys:    str
    source:     str = ""  # stripped before DB insert


# ── Browser helpers ───────────────────────────────────────────────────────────

def new_browser(p) -> Browser:
    return p.chromium.launch(headless=True, args=["--no-sandbox"])


def new_page(browser: Browser) -> Page:
    ctx = browser.new_context(
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        locale="en-PH",
        viewport={"width": 1280, "height": 900},
    )
    page = ctx.new_page()
    page.set_extra_http_headers({
        "Accept-Language": "en-PH,en;q=0.9",
        "Referer": "https://www.google.com/",
    })
    return page


def safe_goto(page: Page, url: str, timeout: int = 25_000) -> bool:
    """Navigate to URL; return False if it fails or returns 4xx/5xx."""
    try:
        resp = page.goto(url, wait_until="networkidle", timeout=timeout)
        page.wait_for_timeout(1500)
        if resp and resp.status >= 400:
            print(f"    ✗ HTTP {resp.status}: {url}")
            return False
        return True
    except Exception as e:
        print(f"    ✗ Load error: {e}")
        return False


def parse_spec_table(page: Page) -> dict[str, str]:
    """Generic spec table parser — covers zigwheels/autodeal/motodeal layouts."""
    soup = BeautifulSoup(page.content(), "lxml")
    specs: dict[str, str] = {}
    for row in soup.select("tr, .specRow, .spec-row, .spec-item, .bike-spec"):
        cells = row.select("td, th, .specKey, .specVal, .label, .value")
        if len(cells) >= 2:
            k = cells[0].text.strip().lower()
            v = cells[1].text.strip()
            if k:
                specs[k] = v
    return specs


def specs_to_record(brand: str, model: str, specs: dict[str, str], source_url: str) -> BikeRecord:
    engine_str = specs.get("displacement", specs.get("engine displacement", specs.get("engine", "")))
    fuel_str   = specs.get("fuel system", specs.get("fuel supply", specs.get("fuel delivery", specs.get("fuel", ""))))
    cool_str   = specs.get("cooling system", specs.get("cooling", ""))
    type_str   = specs.get("body type", specs.get("category", specs.get("class", specs.get("type", ""))))
    year_raw   = specs.get("year", "")

    cc    = extract_cc(engine_str)
    yr_m  = re.search(r"\d{4}", year_raw)
    year  = int(yr_m.group()) if yr_m else 2024

    return BikeRecord(
        brand=brand,
        model=model,
        type=normalise_type(type_str),
        year=year,
        engineSize=cc,
        fuelSys=normalise_fuel(fuel_str),
        coolSys=normalise_cool(cool_str),
        source=source_url,
    )


# ── Source scrapers ───────────────────────────────────────────────────────────

def scrape_zigwheels(page: Page, brand: str) -> list[BikeRecord]:
    records: list[BikeRecord] = []
    listing_url = f"https://www.zigwheels.ph/motorcycles/{brand}"
    print(f"  [zigwheels] {listing_url}")

    if not safe_goto(page, listing_url):
        return records

    soup = BeautifulSoup(page.content(), "lxml")
    anchors = soup.select("a.mkModel, li.mkListItem a, .modelLinks a, a[href*='/motorcycles/']")
    anchors = [a for a in anchors if brand.lower() in (a.get("href") or "").lower() and a.text.strip()]
    anchors = list({a["href"]: a for a in anchors if a.get("href")}.values())
    print(f"    → {len(anchors)} models")

    for a in anchors[:60]:
        model_name = a.text.strip()
        href       = a["href"].rstrip("/")
        spec_url   = f"https://www.zigwheels.ph{href}/specifications"

        if not safe_goto(page, spec_url):
            continue

        specs  = parse_spec_table(page)
        record = specs_to_record(brand, model_name, specs, spec_url)
        records.append(record)
        print(f"    ✓ {model_name} ({record.year}) {record.engineSize}cc")
        time.sleep(DELAY)

    return records


def scrape_autodeal(page: Page, brand: str) -> list[BikeRecord]:
    records: list[BikeRecord] = []
    listing_url = f"https://www.autodeal.com.ph/motorcycles/{brand.lower()}"
    print(f"  [autodeal] {listing_url}")

    if not safe_goto(page, listing_url):
        return records

    soup = BeautifulSoup(page.content(), "lxml")
    anchors = soup.select(
        f"a.car-info-link, .model-title a, a[href*='/motorcycles/{brand.lower()}/']"
    )
    anchors = list({a["href"]: a for a in anchors if a.get("href") and a.text.strip()}.values())
    print(f"    → {len(anchors)} models")

    for a in anchors[:60]:
        model_name = a.text.strip()
        href       = a["href"].rstrip("/")
        spec_url   = f"https://www.autodeal.com.ph{href}/specifications"

        if not safe_goto(page, spec_url):
            continue

        specs  = parse_spec_table(page)
        record = specs_to_record(brand, model_name, specs, spec_url)
        records.append(record)
        print(f"    ✓ {model_name} ({record.year}) {record.engineSize}cc")
        time.sleep(DELAY)

    return records


def scrape_motodeal(page: Page, brand: str) -> list[BikeRecord]:
    records: list[BikeRecord] = []
    listing_url = f"https://www.motodeal.com.ph/{brand.lower()}"
    print(f"  [motodeal] {listing_url}")

    if not safe_goto(page, listing_url):
        return records

    soup = BeautifulSoup(page.content(), "lxml")
    anchors = soup.select(f"a[href*='/{brand.lower()}/']")
    anchors = [a for a in anchors if a.text.strip()]
    anchors = list({a["href"]: a for a in anchors if a.get("href")}.values())
    print(f"    → {len(anchors)} models")

    for a in anchors[:60]:
        href = a["href"]
        if not href.startswith("http"):
            href = "https://www.motodeal.com.ph" + href
        model_name = a.text.strip()

        if not safe_goto(page, href):
            continue

        specs  = parse_spec_table(page)
        record = specs_to_record(brand, model_name, specs, href)
        records.append(record)
        print(f"    ✓ {model_name} ({record.year}) {record.engineSize}cc")
        time.sleep(DELAY)

    return records


# ── De-dupe ───────────────────────────────────────────────────────────────────

def dedup(records: list[BikeRecord]) -> list[BikeRecord]:
    seen: set[tuple] = set()
    out:  list[BikeRecord] = []
    for r in records:
        key = (r.brand.lower(), r.model.lower(), r.year)
        if key not in seen:
            seen.add(key)
            out.append(r)
    return out


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    all_records: list[BikeRecord] = []

    sources = [
        ("zigwheels", scrape_zigwheels),
        ("autodeal",  scrape_autodeal),
        ("motodeal",  scrape_motodeal),
    ]

    with sync_playwright() as p:
        browser = new_browser(p)

        for brand in BRANDS:
            print(f"\n{'='*55}\n  {brand}\n{'='*55}")
            for name, fn in sources:
                pg = new_page(browser)
                try:
                    results = fn(pg, brand)
                    print(f"    [{name}] {len(results)} records collected")
                    all_records.extend(results)
                except Exception as e:
                    print(f"    [{name}] ERROR: {e}")
                finally:
                    pg.context.close()
                time.sleep(1.5)

        browser.close()

    deduped = dedup(all_records)
    payload = [asdict(r) for r in deduped]

    # Validate before writing
    valid, errors = validate_records(payload)
    if errors:
        print("\n⚠  Validation issues:")
        for e in errors:
            print(e)

    OUT_FILE.write_text(json.dumps(valid, indent=2, ensure_ascii=False))
    print(f"\n✅  {len(valid)} records → {OUT_FILE}")


if __name__ == "__main__":
    main()
