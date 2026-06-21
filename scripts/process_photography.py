#!/usr/bin/env python3
"""Prepare personal photography assets for the GitHub Pages site.

Usage:
    python3 scripts/process_photography.py --source /path/to/shoot

The script compresses source JPEG files into assets/images/photography/ and
rewrites _data/photography.yml. Known files use the curated names and locations
below. New files are added after the curated set with a cleaned filename-based
title/location so they can be edited in _data/photography.yml if needed.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

try:
    from PIL import Image, ImageOps
except ImportError as exc:
    raise SystemExit("Pillow is required: python3 -m pip install Pillow") from exc


CURATED_PHOTOS = [
    {
        "source": "101 S Huntington Ave, Jamaica Plain, MA, United States.jpeg",
        "output": "01-jamaica-plain-boston-ma.jpg",
        "title": "Jamaica Plain",
        "location": "Boston, Massachusetts, United States",
        "region": "United States",
    },
    {
        "source": "30 Adamson St Allston, MA, United States.jpeg",
        "output": "02-allston-boston-ma.jpg",
        "title": "Allston",
        "location": "Boston, Massachusetts, United States",
        "region": "United States",
    },
    {
        "source": "Bailey's Beach, Newport, Rl United States.JPG",
        "output": "03-baileys-beach-newport-ri.jpg",
        "title": "Bailey's Beach",
        "location": "Newport, Rhode Island, United States",
        "region": "United States",
    },
    {
        "source": "Boston University, MA, United States.jpeg",
        "output": "05-boston-university-ma.jpg",
        "title": "Boston University",
        "location": "Boston, Massachusetts, United States",
        "region": "United States",
    },
    {
        "source": "Bryce Canyon National Park, Navajo Loop Trail, Tropic, UT, United States.jpeg",
        "output": "06-bryce-canyon-ut.jpg",
        "title": "Navajo Loop Trail",
        "location": "Bryce Canyon National Park, Utah, United States",
        "region": "United States",
    },
    {
        "source": "Charles River, Dr Paul Dudley White Path, Boston, MA, United States.jpeg",
        "output": "10-charles-river-boston-ma.jpg",
        "title": "Charles River",
        "location": "Boston, Massachusetts, United States",
        "region": "United States",
    },
    {
        "source": "Ellen Browning Scripps Park, Stairs to la Jolla Cove Beach, La Jolla, CA, United States.jpeg",
        "output": "12-la-jolla-cove-san-diego-ca.jpg",
        "title": "La Jolla Cove",
        "location": "San Diego, California, United States",
        "region": "United States",
    },
    {
        "source": "Northside Dr Yosemite National Park, CA, United States.jpeg",
        "output": "19-yosemite-valley-ca.jpg",
        "title": "Yosemite Valley",
        "location": "Yosemite National Park, California, United States",
        "region": "United States",
    },
    {
        "source": "Page, AZ, United States.jpeg",
        "output": "20-page-arizona.jpg",
        "title": "Page",
        "location": "Arizona, United States",
        "region": "United States",
    },
    {
        "source": "Rockefeller Center, 12 W 50th St, New York, NY, United States.jpeg",
        "output": "22-rockefeller-center-nyc.jpg",
        "title": "Rockefeller Center",
        "location": "New York City, New York, United States",
        "region": "United States",
    },
    {
        "source": "S Harbor Blvd, Anaheim, CA United States.jpeg",
        "output": "24-anaheim-california.jpg",
        "title": "Anaheim",
        "location": "California, United States",
        "region": "United States",
    },
    {
        "source": "Sequoia National Park, Three Rivers, CA, United States.jpeg",
        "output": "26-sequoia-national-park-ca.jpg",
        "title": "Sequoia National Park",
        "location": "California, United States",
        "region": "United States",
    },
    {
        "source": "Summer St, Malden, MA United States.jpeg",
        "output": "27-malden-massachusetts.jpg",
        "title": "Malden",
        "location": "Massachusetts, United States",
        "region": "United States",
    },
    {
        "source": "Trinity Church Boston, 206 Clarendon St, Boston, MA, United States.jpeg",
        "output": "31-trinity-church-boston.jpg",
        "title": "Trinity Church",
        "location": "Boston, Massachusetts, United States",
        "region": "United States",
    },
    {
        "source": "Tuna Harbor Park, San Diego, CA United States.JPG",
        "output": "32-tuna-harbor-san-diego.jpg",
        "title": "Tuna Harbor Park",
        "location": "San Diego, California, United States",
        "region": "United States",
    },
    {
        "source": "Wynn Las Vegas, Las Vegas, NV, United States.jpeg",
        "output": "34-wynn-las-vegas.jpg",
        "title": "Wynn Las Vegas",
        "location": "Las Vegas, Nevada, United States",
        "region": "United States",
    },
    {
        "source": "Yosemite National Park.jpeg",
        "output": "35-yosemite-national-park-ca.jpg",
        "title": "Yosemite National Park",
        "location": "California, United States",
        "region": "United States",
    },
    {
        "source": "Bullock lsland, Victoria, Australia.jpeg",
        "output": "07-bullock-island-victoria.jpg",
        "title": "Bullock Island",
        "location": "Victoria, Australia",
        "region": "Australia",
    },
    {
        "source": "Coastal Ward, Corangamite Shire VIC, Australia.jpeg",
        "output": "11-great-ocean-road-victoria.jpg",
        "title": "Great Ocean Road Coast",
        "location": "Corangamite Shire, Victoria, Australia",
        "region": "Australia",
    },
    {
        "source": "Great Barrier Reef, Australia.jpeg",
        "output": "15-great-barrier-reef-australia.jpg",
        "title": "Great Barrier Reef",
        "location": "Queensland, Australia",
        "region": "Australia",
    },
    {
        "source": "Narooma, NSW, Australia.jpeg",
        "output": "18-narooma-nsw.jpg",
        "title": "Narooma",
        "location": "New South Wales, Australia",
        "region": "Australia",
    },
    {
        "source": "RMIT University, Australia.jpeg",
        "output": "21-rmit-university-melbourne.jpg",
        "title": "RMIT University",
        "location": "Melbourne, Victoria, Australia",
        "region": "Australia",
    },
    {
        "source": "The University of Melbourne, Tin Alley, Parkville VIC 3052, Australia.jpeg",
        "output": "30-university-of-melbourne.jpg",
        "title": "The University of Melbourne",
        "location": "Melbourne, Victoria, Australia",
        "region": "Australia",
    },
    {
        "source": "CUHK seaview, Sha Tin District, Hong Kong.jpeg",
        "output": "08-cuhk-seaview-hong-kong.jpg",
        "title": "CUHK Seaview",
        "location": "Sha Tin, Hong Kong",
        "region": "China & Hong Kong",
    },
    {
        "source": "CUHK, Sha Tin District, Hong Kong.jpeg",
        "output": "09-cuhk-sha-tin-hong-kong.jpg",
        "title": "The Chinese University of Hong Kong",
        "location": "Sha Tin, Hong Kong",
        "region": "China & Hong Kong",
    },
    {
        "source": "Flower Sea, lli, Xinjiang Uygur zizhiqu China.jpeg",
        "output": "13-flower-sea-ili-xinjiang.jpg",
        "title": "Flower Sea",
        "location": "Ili, Xinjiang, China",
        "region": "China & Hong Kong",
    },
    {
        "source": "Ganzhou, Jingxi, China.jpeg",
        "output": "14-ganzhou-jiangxi.jpg",
        "title": "Ganzhou",
        "location": "Jiangxi, China",
        "region": "China & Hong Kong",
    },
    {
        "source": "HKUST(GZ), GuangDong, China.jpeg",
        "output": "16-hkust-gz-guangzhou.jpg",
        "title": "HKUST(GZ)",
        "location": "Guangzhou, Guangdong, China",
        "region": "China & Hong Kong",
    },
    {
        "source": "Nan'an, Chongqing China.jpeg",
        "output": "17-nanan-chongqing.jpg",
        "title": "Nan'an",
        "location": "Chongqing, China",
        "region": "China & Hong Kong",
    },
    {
        "source": "Salimu, lli, Xinjiang Uygur zizhiqu China.JPG",
        "output": "25-sayram-lake-ili-xinjiang.jpg",
        "title": "Sayram Lake",
        "location": "Ili, Xinjiang, China",
        "region": "China & Hong Kong",
    },
    {
        "source": "lli, Xinjiang Uygur zizhiqu China.JPG",
        "output": "36-ili-xinjiang.jpg",
        "title": "Ili",
        "location": "Xinjiang, China",
        "region": "China & Hong Kong",
    },
    {
        "source": "Bay of Bangkok, Thailand.jpeg",
        "output": "04-bay-of-bangkok-thailand.jpg",
        "title": "Bay of Bangkok",
        "location": "Bangkok, Thailand",
        "region": "Japan & Thailand",
    },
    {
        "source": "Rokkosancho Kitarokko, Nada, Kobe, Hyogo, Japan.jpeg",
        "output": "23-mount-rokko-kobe.jpg",
        "title": "Mount Rokko",
        "location": "Kobe, Hyogo, Japan",
        "region": "Japan & Thailand",
    },
    {
        "source": "Tajima, Fuji, Shizuoka, Japan.JPG",
        "output": "28-mount-fuji-shizuoka.jpg",
        "title": "Mount Fuji",
        "location": "Shizuoka, Japan",
        "region": "Japan & Thailand",
    },
    {
        "source": "Tawaen Beach, Thailand.jpeg",
        "output": "29-tawaen-beach-thailand.jpg",
        "title": "Tawaen Beach",
        "location": "Ko Lan, Thailand",
        "region": "Japan & Thailand",
    },
    {
        "source": "Wat Arun Ratchawararam, 158 Wang Doem Road, Wat Arun, Bangkok Yai District, Bangkok 10600, Thailand.jpeg",
        "output": "33-wat-arun-bangkok.jpg",
        "title": "Wat Arun",
        "location": "Bangkok, Thailand",
        "region": "Japan & Thailand",
    },
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path, help="Directory with original photos.")
    parser.add_argument("--output-dir", default=Path("assets/images/photography"), type=Path)
    parser.add_argument("--data-file", default=Path("_data/photography.yml"), type=Path)
    parser.add_argument("--max-size", default=1800, type=int, help="Maximum width or height in pixels.")
    parser.add_argument("--quality", default=84, type=int, help="JPEG quality.")
    parser.add_argument("--dry-run", action="store_true", help="Print planned actions without writing files.")
    return parser.parse_args()


def slugify(value: str) -> str:
    value = value.lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "photo"


def clean_piece(value: str) -> str:
    replacements = {
        " lli": " Ili",
        "lli": "Ili",
        "zizhiqu": "",
        "Uygur": "",
        "GuangDong": "Guangdong",
        " Rl ": " RI ",
    }
    cleaned = value
    for old, new in replacements.items():
        cleaned = cleaned.replace(old, new)
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = cleaned.replace(" ,", ",")
    return cleaned.strip(" ,")


def generated_metadata(path: Path, index: int) -> dict[str, str]:
    stem = clean_piece(path.stem)
    parts = [part.strip() for part in stem.split(",") if part.strip()]
    title = parts[0] if parts else stem
    location = ", ".join(parts[1:]) if len(parts) > 1 else "Location to be edited"
    output = f"{index:02d}-{slugify(stem)}.jpg"
    return {
        "source": path.name,
        "output": output,
        "title": title,
        "location": location,
        "region": "Unsorted",
    }


def discover_photos(source_dir: Path) -> list[dict[str, str]]:
    known_sources = {item["source"] for item in CURATED_PHOTOS}
    found = {
        path.name: path
        for path in source_dir.iterdir()
        if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg"}
    }

    records = [item for item in CURATED_PHOTOS if item["source"] in found]
    next_index = len(CURATED_PHOTOS) + 1
    for path in sorted(found.values(), key=lambda item: item.name.lower()):
        if path.name in known_sources:
            continue
        records.append(generated_metadata(path, next_index))
        next_index += 1
    return records


def compress_photo(source: Path, target: Path, max_size: int, quality: int, dry_run: bool) -> None:
    if dry_run:
        print(f"would write {target} from {source}")
        return

    target.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as image:
        image = ImageOps.exif_transpose(image).convert("RGB")
        image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        image.save(target, "JPEG", quality=quality, optimize=True, progressive=True)
        print(f"wrote {target}: {image.width}x{image.height}")


def yaml_quote(value: str) -> str:
    if re.search(r"[:#\\[\\]{},&*!|>'\"%@`]", value):
        return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return value


def write_yaml(records: list[dict[str, str]], data_file: Path, dry_run: bool) -> None:
    lines: list[str] = []
    previous_region = None
    for item in records:
        if lines and item["region"] != previous_region:
            lines.append("")
        lines.extend(
            [
                f"- title: {yaml_quote(item['title'])}",
                f"  location: {yaml_quote(item['location'])}",
                f"  region: {yaml_quote(item['region'])}",
                f"  image: /assets/images/photography/{item['output']}",
            ]
        )
        previous_region = item["region"]

    content = "\n".join(lines) + "\n"
    if dry_run:
        print(f"would write {data_file} with {len(records)} records")
        return

    data_file.parent.mkdir(parents=True, exist_ok=True)
    data_file.write_text(content, encoding="utf-8")
    print(f"wrote {data_file}: {len(records)} records")


def main() -> None:
    args = parse_args()
    source_dir = args.source.expanduser().resolve()
    if not source_dir.is_dir():
        raise SystemExit(f"Source directory does not exist: {source_dir}")

    records = discover_photos(source_dir)
    if not records:
        raise SystemExit(f"No JPEG photos found in {source_dir}")

    for item in records:
        compress_photo(
            source_dir / item["source"],
            args.output_dir / item["output"],
            args.max_size,
            args.quality,
            args.dry_run,
        )
    write_yaml(records, args.data_file, args.dry_run)


if __name__ == "__main__":
    main()
