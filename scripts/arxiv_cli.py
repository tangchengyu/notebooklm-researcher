#!/usr/bin/env python3
"""Search arXiv and download open-access PDFs from the command line."""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

API_URL = "https://export.arxiv.org/api/query"
USER_AGENT = "notebooklm-research-arxiv-cli/1.0 (mailto:local-research@example.invalid)"
NS = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}


def request(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as response:
        return response.read()


def clean(value: str | None) -> str:
    return " ".join((value or "").split())


def paper_id(value: str) -> str:
    match = re.search(r"(?:abs|pdf)/([^/?#]+)", value)
    result = (match.group(1) if match else value).removesuffix(".pdf")
    if not re.fullmatch(r"(?:[a-z-]+(?:\.[A-Z]{2})?/\d{7}|\d{4}\.\d{4,5})(?:v\d+)?", result, re.I):
        raise ValueError(f"Invalid arXiv ID or URL: {value}")
    return result


def parse_feed(data: bytes) -> list[dict[str, object]]:
    root = ET.fromstring(data)
    papers = []
    for entry in root.findall("atom:entry", NS):
        identifier = clean(entry.findtext("atom:id", namespaces=NS)).rsplit("/", 1)[-1]
        papers.append(
            {
                "arxiv_id": identifier,
                "title": clean(entry.findtext("atom:title", namespaces=NS)),
                "authors": [clean(a.findtext("atom:name", namespaces=NS)) for a in entry.findall("atom:author", NS)],
                "summary": clean(entry.findtext("atom:summary", namespaces=NS)),
                "published": clean(entry.findtext("atom:published", namespaces=NS)),
                "updated": clean(entry.findtext("atom:updated", namespaces=NS)),
                "doi": clean(entry.findtext("arxiv:doi", namespaces=NS)) or None,
                "primary_category": (entry.find("arxiv:primary_category", NS).attrib.get("term") if entry.find("arxiv:primary_category", NS) is not None else None),
                "abs_url": f"https://arxiv.org/abs/{identifier}",
                "pdf_url": f"https://arxiv.org/pdf/{identifier}.pdf",
            }
        )
    return papers


def search(query: str, max_results: int) -> list[dict[str, object]]:
    params = urllib.parse.urlencode(
        {"search_query": f"all:{query}", "start": 0, "max_results": max_results, "sortBy": "relevance", "sortOrder": "descending"}
    )
    return parse_feed(request(f"{API_URL}?{params}"))


def safe_name(value: str) -> str:
    return re.sub(r'[<>:"/\\|?*]+', "_", value).strip(" .")[:140]


def download(identifier: str, output_dir: Path, title: str | None = None) -> Path:
    identifier = paper_id(identifier)
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{identifier.replace('/', '_')} - {safe_name(title)}.pdf" if title else f"{identifier.replace('/', '_')}.pdf"
    target = output_dir / filename
    target.write_bytes(request(f"https://arxiv.org/pdf/{urllib.parse.quote(identifier, safe='/')}.pdf"))
    if not target.read_bytes().startswith(b"%PDF"):
        target.unlink(missing_ok=True)
        raise RuntimeError(f"arXiv did not return a PDF for {identifier}")
    return target


def write_results(papers: list[dict[str, object]], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "arxiv_search.json").write_text(json.dumps(papers, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# arXiv search results", ""]
    for index, item in enumerate(papers, 1):
        lines.extend(
            [
                f"## {index}. {item['title']}",
                f"- arXiv ID: {item['arxiv_id']}",
                f"- Authors: {', '.join(item['authors'])}",
                f"- Published: {item['published']}",
                f"- Updated: {item['updated']}",
                f"- DOI: {item['doi'] or 'N/A'}",
                f"- Abstract: {item['abs_url']}",
                f"- PDF: {item['pdf_url']}",
                "",
                str(item["summary"]),
                "",
            ]
        )
    (output_dir / "arxiv_search.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Search arXiv and download lawful open-access PDFs.")
    sub = parser.add_subparsers(dest="command", required=True)
    search_parser = sub.add_parser("search")
    search_parser.add_argument("query")
    search_parser.add_argument("--max-results", type=int, default=10)
    search_parser.add_argument("--output", type=Path, required=True)
    search_parser.add_argument("--download", type=int, default=0, metavar="N")
    download_parser = sub.add_parser("download")
    download_parser.add_argument("arxiv_id")
    download_parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    if args.command == "download":
        print(download(args.arxiv_id, args.output))
        return 0

    papers = search(args.query, max(1, min(args.max_results, 100)))
    write_results(papers, args.output)
    for item in papers[: max(0, args.download)]:
        print(download(str(item["arxiv_id"]), args.output, str(item["title"])))
        time.sleep(3)
    print(json.dumps({"count": len(papers), "output": str(args.output)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"arXiv CLI error: {exc}", file=sys.stderr)
        raise SystemExit(1)
