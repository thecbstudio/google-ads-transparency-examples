"""Run "Google Ads Transparency Scraper with Ad Copy" on Apify and save the ads as CSV (and optionally JSON).

Examples:
    python fetch_ads.py nike.com --max 50
    python fetch_ads.py HubSpot "adidas.com" --region GB --max 100 --json raw.json
    python fetch_ads.py nike.com --no-details --no-text      # cheapest: plain ad list
"""
import argparse
import csv
import json
import os
import sys

from apify_client import ApifyClient

ACTOR_ID = "kilometric_camp/google-ads-transparency-ad-copy"
COLUMNS = [
    "advertiserName", "format", "headline", "description", "displayUrl", "landingUrl",
    "utm_campaign", "firstShown", "lastShown", "daysShown", "adUrl",
]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("queries", nargs="+", help="domains, brand names or advertiser IDs, e.g. nike.com HubSpot")
    parser.add_argument("--region", default="US", help="2-letter country code or ANYWHERE (default: US)")
    parser.add_argument("--max", type=int, default=50, help="max ads per query (default: 50)")
    parser.add_argument("--no-details", action="store_true", help="skip creative details (cheaper, no landing pages)")
    parser.add_argument("--no-text", action="store_true", help="skip reading Search ad copy (cheaper)")
    parser.add_argument("--out", default="ads.csv", help="CSV file to write (default: ads.csv)")
    parser.add_argument("--json", help="also save the raw items to this JSON file")
    args = parser.parse_args()

    token = os.environ.get("APIFY_TOKEN")
    if not token:
        sys.exit("Set the APIFY_TOKEN environment variable (Apify Console -> Settings -> API & Integrations).")

    client = ApifyClient(token)
    run = client.actor(ACTOR_ID).call(run_input={
        "queries": args.queries,
        "region": args.region,
        "maxAdsPerQuery": args.max,
        "includeDetails": not args.no_details,
        "extractAdText": not args.no_text,
    }, logger=None)
    if run is None:
        sys.exit("The run did not finish in time - open it in the Apify Console to see its status.")
    # apify-client 3.x returns a Run object, older versions a dict
    dataset_id = getattr(run, "default_dataset_id", None) or run["defaultDatasetId"]
    items = list(client.dataset(dataset_id).iterate_items())

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        for ad in items:
            row = {key: ad.get(key, "") for key in COLUMNS}
            row["utm_campaign"] = (ad.get("utm") or {}).get("utm_campaign", "")
            writer.writerow(row)
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)

    formats = {}
    for ad in items:
        formats[ad.get("format")] = formats.get(ad.get("format"), 0) + 1
    print(f"{len(items)} ads saved to {args.out}  {formats}")


if __name__ == "__main__":
    main()
