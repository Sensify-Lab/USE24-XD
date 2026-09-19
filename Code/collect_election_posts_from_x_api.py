"""Collect original English election posts with an X API bearer token."""

import argparse
import os
from pathlib import Path

import pandas as pd

from locate_release_data import default_release_directory


SEARCH_URL = "https://api.twitter.com/2/tweets/search/recent"


def bearer_token() -> str:
    token = os.environ.get("X_BEARER_TOKEN", "").strip()
    if not token:
        raise RuntimeError("Set X_BEARER_TOKEN before collecting posts.")
    return token


def main() -> None:
    release_dir = default_release_directory()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", default="election 2024")
    parser.add_argument("--page-size", type=int, default=100)
    parser.add_argument("--output-csv", type=Path, default=release_dir / "Collected_Data" / "election_posts.csv")
    args = parser.parse_args()
    if not 10 <= args.page_size <= 100:
        raise ValueError("--page-size must be between 10 and 100.")
    import requests

    response = requests.get(SEARCH_URL, headers={"Authorization": f"Bearer {bearer_token()}"}, params={"query": f"{args.query} lang:en -is:retweet -has:images", "max_results": args.page_size, "tweet.fields": "author_id,public_metrics,created_at,lang,possibly_sensitive", "expansions": "author_id", "user.fields": "username,verified,location"}, timeout=60)
    response.raise_for_status()
    posts = pd.json_normalize(response.json().get("data", []))
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    posts.to_csv(args.output_csv, index=False)
    print(f"Collected {len(posts):,} posts in {args.output_csv}")


if __name__ == "__main__":
    main()
