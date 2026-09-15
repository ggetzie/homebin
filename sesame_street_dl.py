#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests", "tqdm"]
# ///
"""Find and download Sesame Street episodes from the Internet Archive.

Episodes are scattered across thousands of archive.org items: single uploads
("Sesame Street Episode 4089") and large bundles holding hundreds of episodes
as separate files. This script searches every Sesame Street video item, reads
each item's file list, matches episode numbers on individual files, picks one
copy per episode (preferring original broadcast recordings, then the largest
file) and downloads it with resume support.

Examples:
    ./sesame_street_dl.py --dry-run            # build manifest.csv, no downloads
    ./sesame_street_dl.py --episodes 4001-4050
    ./sesame_street_dl.py ~/videos/sesame --all-versions
"""

import argparse
import csv
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote

import requests
from requests.adapters import HTTPAdapter
from tqdm import tqdm
from urllib3.util.retry import Retry

SCRAPE_URL = "https://archive.org/services/search/v1/scrape"
METADATA_URL = "https://archive.org/metadata/{identifier}"
DOWNLOAD_URL = "https://archive.org/download/{identifier}/{name}"
SEARCH_QUERY = '"sesame street" AND mediatype:movies'
USER_AGENT = "sesame-street-dl/1.0 (personal archive script)"

VIDEO_EXTS = {
    "mp4", "mkv", "avi", "mpg", "mpeg", "m4v", "mov", "webm", "ogv", "ts", "vob",
}
MAX_EPISODE = 5999
# Bundles can have "noise" titles but still hold real episodes; only skip
# noisy items before fetching metadata when they are smaller than this.
BUNDLE_SIZE = 20 * 1024**3

NOISE_RE = re.compile(
    r"aftermath|fan\s?made|endings?\s*#|openings?\s+(?:to|and)|closings?\s+to"
    r"|\bpromo\b|trailer|previews?\s+for|unpaved|noggin version"
    r"|online\s?video\s?cutter|voice\s?over|reaction|\breview"
    r"|sesamstra|s[eé]samo|sesame\s+park|takalani|galli\s+galli|shalom\s+sesame"
    r"|play\s+with\s+me\s+sesame|sesame\s+english|furchester|mecha\s+builders"
    r"|noggin\s*block|elmo'?s\s+world|global\s+grover|smart\s+cookies|bert\s+(?:and|&)\s+ernie'?s\s+great",
    re.I,
)
SESAME_RE = re.compile(r"sesame\s*street", re.I)
ORIGINAL_RE = re.compile(r"broadcast|airing|ptv\s+park|off\s?air|tv\s+recording", re.I)
RECREATION_RE = re.compile(
    r"recreat|remake|remaster|combination|dvd|reconstruct|edited|redub|restored"
    r"|upscal|topaz|\bchf\d|\bprob\d|\bai\s+enhance", re.I
)
EPISODE_RES = [
    re.compile(r"\bepisode\s*#?\s*(\d{1,4})(?!\d)", re.I),
    re.compile(r"\bep\.?\s*#?\s*(\d{1,4})(?!\d)", re.I),
    re.compile(r"#\s*(\d{3,4})(?!\d)"),
]
BARE_RE = re.compile(r"sesame\s*street\W{0,3}(\d{3,4})(?![\d.:/-]\d|\d)", re.I)
LEADING_RE = re.compile(r"^\W*(\d{3,4})(?![\d.:/-]\d|\d)")
YEAR_CONTEXT_RE = re.compile(r"^\s*\)?\s*(?:vhs|dvd|sesame|special|movie|live)", re.I)


@dataclass
class Candidate:
    episode: int
    identifier: str
    name: str
    size: int
    length: float | None
    title: str
    original: bool
    recreation: bool

    @property
    def url(self) -> str:
        return DOWNLOAD_URL.format(identifier=self.identifier, name=quote(self.name, safe="/"))

    @property
    def ext(self) -> str:
        return self.name.rsplit(".", 1)[-1].lower()

    @property
    def full_length(self) -> bool:
        return self.length is not None and 20 * 60 <= self.length <= 75 * 60


def make_session() -> requests.Session:
    session = requests.Session()
    retry = Retry(
        total=6,
        backoff_factor=2,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET",),
        respect_retry_after_header=True,
    )
    session.mount("https://", HTTPAdapter(max_retries=retry, pool_maxsize=32))
    session.headers["User-Agent"] = USER_AGENT
    return session


def normalize(text: str) -> str:
    """Turn identifiers and file names into space separated words."""
    return re.sub(r"[-_.+]+", " ", text).strip()


def search_items(session: requests.Session, cache: Path, refresh: bool) -> list[dict]:
    if cache.exists() and not refresh:
        return json.loads(cache.read_text())
    items: list[dict] = []
    params = {"q": SEARCH_QUERY, "fields": "identifier,title,item_size", "count": "5000"}
    with tqdm(desc="Searching archive.org", unit=" items") as bar:
        while True:
            resp = session.get(SCRAPE_URL, params=params, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            items.extend(data.get("items", []))
            bar.update(len(data.get("items", [])))
            cursor = data.get("cursor")
            if not cursor:
                break
            params["cursor"] = cursor
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(items))
    return items


def fetch_metadata(session: requests.Session, identifier: str, cache_dir: Path, refresh: bool) -> dict:
    path = cache_dir / f"{identifier}.json"
    if path.exists() and not refresh:
        return json.loads(path.read_text())
    resp = session.get(METADATA_URL.format(identifier=identifier), timeout=60)
    resp.raise_for_status()
    data = resp.json()
    path.write_text(json.dumps(data))
    return data


def looks_like_year(match: re.Match, text: str) -> bool:
    number = int(match.group(1))
    if not 1969 <= number <= 2026:
        return False
    before = text[: match.start(1)].rstrip()
    return before.endswith("(") or bool(YEAR_CONTEXT_RE.match(text[match.end(1):]))


def extract_episode(text: str) -> int | None:
    for pattern in EPISODE_RES:
        if m := pattern.search(text):
            return int(m.group(1))
    for pattern in (BARE_RE, LEADING_RE):
        for m in pattern.finditer(text):
            if not looks_like_year(m, text):
                return int(m.group(1))
    return None


def parse_length(value: object) -> float | None:
    if value is None:
        return None
    text = str(value)
    try:
        if ":" in text:
            seconds = 0.0
            for part in text.split(":"):
                seconds = seconds * 60 + float(part)
            return seconds
        return float(text)
    except ValueError:
        return None


def collect_candidates(item: dict, metadata: dict, min_minutes: float) -> list[Candidate]:
    identifier = item["identifier"]
    title = metadata.get("metadata", {}).get("title") or item.get("title") or ""
    if isinstance(title, list):
        title = " ".join(title)
    videos = [
        f for f in metadata.get("files", [])
        if f.get("source") == "original" and f["name"].rsplit(".", 1)[-1].lower() in VIDEO_EXTS
    ]
    single = len(videos) == 1
    candidates = []
    for f in videos:
        stem = normalize(f["name"].rsplit(".", 1)[0])
        context = f"{title} {stem}" if single else stem
        if NOISE_RE.search(context):
            continue
        if not (SESAME_RE.search(stem) or SESAME_RE.search(title)):
            continue
        if single:
            episode = extract_episode(title) or extract_episode(stem) or extract_episode(normalize(identifier))
        else:
            episode = extract_episode(stem)
        if not episode or episode > MAX_EPISODE:
            continue
        size = int(f.get("size") or 0)
        length = parse_length(f.get("length"))
        if length is not None:
            if length < min_minutes * 60:
                continue
        elif size < 50 * 1024**2:
            continue
        flags_text = f"{title} {stem}"
        recreation = bool(RECREATION_RE.search(flags_text))
        candidates.append(Candidate(
            episode=episode,
            identifier=identifier,
            name=f["name"],
            size=size,
            length=length,
            title=title,
            original=bool(ORIGINAL_RE.search(flags_text)) and not recreation,
            recreation=recreation,
        ))
    return candidates


def score(c: Candidate) -> tuple:
    return (c.original, not c.recreation, c.full_length, c.size)


def choose_best(candidates: list[Candidate]) -> list[Candidate]:
    best: dict[int, Candidate] = {}
    for c in candidates:
        if c.episode not in best or score(c) > score(best[c.episode]):
            best[c.episode] = c
    return [best[ep] for ep in sorted(best)]


def destination(outdir: Path, c: Candidate, all_versions: bool) -> Path:
    folder = f"Season_{c.episode // 100:02d}" if c.episode >= 4001 else "Episodes"
    suffix = f" [{c.identifier}]" if all_versions else ""
    return outdir / folder / f"Sesame Street - Episode {c.episode:04d}{suffix}.{c.ext}"


def download_file(session: requests.Session, c: Candidate, dest: Path) -> bool:
    if dest.exists() and (not c.size or dest.stat().st_size == c.size):
        return True
    dest.parent.mkdir(parents=True, exist_ok=True)
    part = dest.with_name(dest.name + ".part")
    offset = part.stat().st_size if part.exists() else 0
    if not c.size or offset < c.size:
        headers = {"Range": f"bytes={offset}-"} if offset else {}
        with session.get(c.url, headers=headers, stream=True, timeout=120) as resp:
            if resp.status_code == 416:
                pass  # partial file already complete
            else:
                resp.raise_for_status()
                if offset and resp.status_code != 206:
                    offset = 0  # server ignored Range, start over
                with open(part, "ab" if offset else "wb") as fh, tqdm(
                    total=c.size or None, initial=offset, unit="B", unit_scale=True,
                    unit_divisor=1024, desc=dest.name, leave=False,
                ) as bar:
                    for chunk in resp.iter_content(chunk_size=1024 * 1024):
                        fh.write(chunk)
                        bar.update(len(chunk))
    if c.size and part.stat().st_size != c.size:
        tqdm.write(f"Size mismatch for {dest.name}: got {part.stat().st_size}, expected {c.size}")
        return False
    part.rename(dest)
    return True


def parse_episode_filter(spec: str) -> set[int]:
    episodes: set[int] = set()
    for chunk in spec.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "-" in chunk:
            start, end = chunk.split("-", 1)
            episodes.update(range(int(start), int(end) + 1))
        else:
            episodes.add(int(chunk))
    return episodes


def compress_ranges(numbers: list[int]) -> str:
    ranges = []
    for n in numbers:
        if ranges and n == ranges[-1][1] + 1:
            ranges[-1][1] = n
        else:
            ranges.append([n, n])
    return ", ".join(f"{a:04d}" if a == b else f"{a:04d}-{b:04d}" for a, b in ranges)


def write_manifest(path: Path, chosen: list[Candidate], outdir: Path, all_versions: bool) -> None:
    with open(path, "w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["episode", "identifier", "file", "size_bytes", "length_min",
                         "original", "recreation", "title", "url", "dest"])
        for c in chosen:
            writer.writerow([
                f"{c.episode:04d}", c.identifier, c.name, c.size,
                f"{c.length / 60:.1f}" if c.length else "", c.original, c.recreation,
                c.title, c.url, destination(outdir, c, all_versions),
            ])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("outdir", nargs="?", default="sesame_street", type=Path)
    parser.add_argument("--dry-run", action="store_true", help="write manifest and summary, download nothing")
    parser.add_argument("--episodes", help="only these episodes, e.g. 4001-4050,0001")
    parser.add_argument("--all-versions", action="store_true", help="download every copy, not just the best")
    parser.add_argument("--min-minutes", type=float, default=20, help="minimum video length (default 20)")
    parser.add_argument("--workers", type=int, default=8, help="parallel metadata requests (default 8)")
    parser.add_argument("--refresh", action="store_true", help="ignore cached search and metadata")
    args = parser.parse_args()

    outdir: Path = args.outdir.expanduser()
    cache_dir = outdir / ".cache"
    meta_dir = cache_dir / "meta"
    meta_dir.mkdir(parents=True, exist_ok=True)
    session = make_session()

    items = search_items(session, cache_dir / "search.json", args.refresh)
    items = [
        i for i in items
        if not (NOISE_RE.search(str(i.get("title", ""))) and int(i.get("item_size") or 0) < BUNDLE_SIZE)
    ]

    candidates: list[Candidate] = []
    failures = 0
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(fetch_metadata, session, i["identifier"], meta_dir, args.refresh): i
            for i in items
        }
        for future in tqdm(as_completed(futures), total=len(futures), desc="Reading item metadata", unit=" items"):
            item = futures[future]
            try:
                candidates.extend(collect_candidates(item, future.result(), args.min_minutes))
            except (requests.RequestException, ValueError) as exc:
                failures += 1
                tqdm.write(f"Metadata failed for {item['identifier']}: {exc}")

    if args.episodes:
        wanted = parse_episode_filter(args.episodes)
        candidates = [c for c in candidates if c.episode in wanted]

    if args.all_versions:
        chosen = sorted(sorted(candidates, key=score, reverse=True), key=lambda c: c.episode)
    else:
        chosen = choose_best(candidates)

    manifest = outdir / "manifest.csv"
    write_manifest(manifest, chosen, outdir, args.all_versions)
    found = sorted({c.episode for c in chosen})
    total_gb = sum(c.size for c in chosen) / 1024**3
    print(f"\n{len(found)} distinct episodes, {len(chosen)} files, {total_gb:,.1f} GiB")
    print(f"Manifest: {manifest}")
    if failures:
        print(f"{failures} items failed metadata lookup (re-run to retry)")
    if found:
        missing = sorted(set(range(found[0], found[-1] + 1)) - set(found))
        (outdir / "missing.txt").write_text(compress_ranges(missing) + "\n")
        print(f"{len(missing)} episode numbers missing between {found[0]:04d} and {found[-1]:04d}"
              f" (see {outdir / 'missing.txt'})")

    if args.dry_run:
        return 0

    errors = 0
    for c in tqdm(chosen, desc="Episodes", unit=" ep"):
        dest = destination(outdir, c, args.all_versions)
        try:
            if not download_file(session, c, dest):
                errors += 1
        except requests.RequestException as exc:
            errors += 1
            tqdm.write(f"Download failed for episode {c.episode:04d} ({c.url}): {exc}")
    print(f"Done. {len(chosen) - errors} ok, {errors} failed.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
