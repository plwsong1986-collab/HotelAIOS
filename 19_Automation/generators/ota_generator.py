#!/usr/bin/env python3
"""
HotelAIOS OTA Data Generator v1.0.0
Generates OTA JSON from merged property configuration.
"""

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("property_id")
    args = parser.parse_args()

    src = (
        ROOT
        / "19_Automation"
        / "output"
        / "property"
        / "sanlitian-property-config.json"
    )
    if not src.exists():
        print("Property configuration not found:", src)
        return

    with open(src, encoding="utf-8") as f:
        data = json.load(f)

    outdir = ROOT / "19_Automation" / "output" / "ota" / args.property_id
    outdir.mkdir(parents=True, exist_ok=True)

    ota = {
        "property_id": args.property_id,
        "name": data.get("property", {}).get("property_name_en", ""),
        "type": data.get("property", {}).get("property_type", ""),
        "location": data.get("location", {}),
        "contact": data.get("contact", {}),
        "rooms": data.get("rooms", []),
        "amenities": data.get("amenities", {}),
        "policies": data.get("policies", {}),
    }

    outfile = outdir / "ota.json"
    with open(outfile, "w", encoding="utf-8") as f:
        json.dump(ota, f, ensure_ascii=False, indent=2)

    print("=" * 60)
    print("HotelAIOS OTA Data Generator v1.0.0")
    print("=" * 60)
    print("物业：", args.property_id)
    print("输出：", outfile)
    print("房型：", len(ota["rooms"]))
    print("OTA 数据生成成功。")


if __name__ == "__main__":
    main()
