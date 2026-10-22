"""Which words does a brand use in its Search ad headlines, and which ads have stayed live the longest?

Works on a dataset exported from the Actor as JSON (see fetch_ads.py --json).

    python headline_words.py raw.json
"""
import argparse
import collections
import json
import re

STOP = {
    "the", "and", "for", "with", "your", "you", "our", "all", "are", "from", "that", "this", "get", "now",
    "can", "more", "out", "new", "has", "have", "will", "his", "her", "its", "one", "any", "not", "but",
}


def words(text: str) -> list[str]:
    return [w for w in re.findall(r"[a-zA-Z][a-zA-Z'&-]+", (text or "").lower()) if w not in STOP and len(w) > 2]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("json_file", help="dataset items as JSON (list of ads)")
    parser.add_argument("--top", type=int, default=12, help="how many words / ads to show (default: 12)")
    args = parser.parse_args()

    with open(args.json_file, encoding="utf-8") as f:
        ads = json.load(f)
    text_ads = [a for a in ads if a.get("headline")]
    print(f"{len(ads)} ads, {len(text_ads)} Search text ads with a headline\n")

    heads = collections.Counter(w for a in text_ads for w in words(a["headline"]))
    descs = collections.Counter(w for a in text_ads for w in words(a.get("description", "")))
    print("Most common headline words:", ", ".join(f"{w} ({n})" for w, n in heads.most_common(args.top)))
    print("Most common description words:", ", ".join(f"{w} ({n})" for w, n in descs.most_common(args.top)))

    print("\nLongest-running text ads (days shown):")
    for a in sorted(text_ads, key=lambda a: a.get("daysShown") or 0, reverse=True)[: args.top // 2]:
        print(f"  {a.get('daysShown'):>5} days | {a['headline']}")


if __name__ == "__main__":
    main()
