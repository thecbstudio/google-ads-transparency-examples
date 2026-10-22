# Google Ads Transparency examples

Small Python scripts for working with ads from Google's [Ads Transparency Center](https://adstransparency.google.com): pull the ads (ad copy, landing pages, UTM tags) into a CSV, then analyse them.

They use the Apify Actor [Google Ads Transparency Scraper with Ad Copy](https://apify.com/kilometric_camp/google-ads-transparency-ad-copy). I am its author. The analysis scripts work on any export with the same fields.

## Setup

```bash
pip install -r requirements.txt
export APIFY_TOKEN=<your token>   # Apify Console -> Settings -> API & Integrations
```

## Scripts

| Script | What it does |
|---|---|
| `fetch_ads.py` | Runs the Actor for one or more domains, brand names or advertiser IDs and saves the ads as CSV (and optionally raw JSON). |
| `headline_words.py` | Most common words in Search ad headlines and descriptions, and the longest-running ads. |
| `utm_report.py` | Splits the UTM tags of video ads into their building blocks to show how a brand names its campaigns. |

```bash
python fetch_ads.py nike.com --max 50 --json raw.json
python headline_words.py raw.json
python utm_report.py raw.json
```

Use `--no-details --no-text` on `fetch_ads.py` for the cheapest plain ad list (no landing pages, no ad copy).

## Example output (real data)

`headline_words.py` on 19 Nike Search text ads:

```
Most common headline words: nike (30), official (8), site (8), shoes (6), shop (6), latest (5), online (4)

Longest-running text ads (days shown):
   1824 days | The Official Nike Site - Nike - Online Store
   1824 days | Nike - Boutique en ligne - Site officiel de Nike France
   1423 days | Babies & Toddlers Kids Shoes. Nike.com
```

`utm_report.py` on 20 HubSpot video ads:

```
20 ads, 20 with UTM tags
utm_source: OTT-CTV_DV360-Multi (9), OTT-CTV_DV360-YouTube (6), audio_dv360-YoutubeSelect (4), OTT-CTV_DV360-YoutubeSelect (1)
utm_medium: paid_brandstrategy (20)
```

## Good to know

- Google keeps about 12 months of history in the date filter. This tool does not return impression, reach or spend numbers.
- Landing pages and UTM tags are available for video ads. For Search text ads Google shows only the display URL.
- Search text ads are stored as images, so the copy is read with OCR. Check the confidence value before quoting it.
- This is not affiliated with Google. "Google" and "Google Ads" are trademarks of Google LLC. Check Google's terms and the laws that apply to you before using the data.

## License

MIT
