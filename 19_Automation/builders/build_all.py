#!/usr/bin/env python3
"""
HotelAIOS Build Pipeline v1.0.0
Run all generators in sequence.
"""

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

STEPS = [
    ("Load Property", ROOT / "19_Automation" / "load_property_config.py"),
    ("Website", ROOT / "19_Automation" / "generators" / "website_generator.py"),
    ("SEO", ROOT / "19_Automation" / "generators" / "seo_generator.py"),
    ("OTA", ROOT / "19_Automation" / "generators" / "ota_generator.py"),
    ("AI Prompt", ROOT / "19_Automation" / "generators" / "ai_prompt_generator.py"),
]


def run_step(name, script, property_id):
    print(f"\n{'=' * 60}")
    print(f"{name}")
    print(f"{'=' * 60}")
    result = subprocess.run([sys.executable, str(script), property_id], cwd=ROOT)
    if result.returncode != 0:
        raise SystemExit(f"Build stopped at: {name}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("property_id")
    args = parser.parse_args()

    print("=" * 60)
    print("HotelAIOS Build Pipeline v1.0.0")
    print("=" * 60)

    for name, script in STEPS:
        run_step(name, script, args.property_id)

    print("\n" + "=" * 60)
    print("Build completed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()
