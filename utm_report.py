"""How does a brand name its video campaigns? Break the UTM tags of video ads into their parts.

Works on a dataset exported from the Actor as JSON (see fetch_ads.py --json). Landing pages and UTM tags are
available for video ads (Google shows only the display URL for Search text ads).

    python utm_report.py raw.json
"""
import argparse
import collections
import json
import re


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("json_file", help="dataset items as JSON (list of ads)")
    parser.add_argument("--top", type=int, default=10, help="how many rows to show (default: 10)")
    args = parser.parse_args()

    with open(args.json_file, encoding="utf-8") as f:
        ads = json.load(f)
    tagged = [a for a in ads if a.get("utm")]
    print(f"{len(ads)} ads, {len(tagged)} with UTM tags\n")
    if not tagged:
        return

    for key in ("utm_source", "utm_medium"):
        counts = collections.Counter(a["utm"].get(key) for a in tagged if a["utm"].get(key))
        print(f"{key}:", ", ".join(f"{v} ({n})" for v, n in counts.most_common(args.top)))

    campaigns = sorted({a["utm"].get("utm_campaign", "") for a in tagged if a["utm"].get("utm_campaign")})
    parts = collections.Counter(p for c in campaigns for p in re.split(r"[_\-]", c) if p)
    print(f"\n{len(campaigns)} distinct utm_campaign values. Most common building blocks:")
    print(", ".join(f"{p} ({n})" for p, n in parts.most_common(args.top * 2)))
    print("\nSample campaign names:")
    for c in campaigns[:5]:
        print(" ", c)


if __name__ == "__main__":
    main()
