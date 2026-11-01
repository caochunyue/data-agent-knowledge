#!/usr/bin/env python3
"""Normalize an approved article export without storing article bodies."""

import argparse
import json
from datetime import date
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

START = date.fromisoformat("2025-11-01")
END = date.fromisoformat("2026-11-01")
CATEGORIES = ("数据研发", "资产检索答疑", "数据分析", "数据 Agent")
KEYWORDS = {
    "数据 Agent": ("agent", "智能体", "harness", "text-to-sql", "mcp"),
    "资产检索答疑": ("资产", "元数据", "血缘", "检索", "问数", "指标口径"),
    "数据分析": ("分析", "报表", "洞察", "指标", "kaggle", "可视化"),
    "数据研发": ("数仓", "sql", "maxcompute", "hive", "flink", "数据研发", "治理", "优化"),
}


def clean_url(value):
    if not isinstance(value, str) or not value.strip():
        return ""
    parts = urlsplit(value.strip())
    # Tracking parameters are not article identity. Keep the path/query only for stable IDs.
    kept = [(key, val) for key, val in parse_qsl(parts.query) if key in {"mid", "idx", "sn"}]
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(kept), ""))


def category_for(record):
    explicit = record.get("primary_category")
    if explicit in CATEGORIES:
        return explicit
    text = " ".join(str(record.get(key, "")) for key in ("title", "summary", "body", "tags")).lower()
    for category, words in KEYWORDS.items():
        if any(word in text for word in words):
            return category
    return "数据研发"


def normalize_records(records):
    output = []
    seen = set()
    for raw in records:
        row = dict(raw)
        warnings = list(row.get("import_warnings") or [])
        url = clean_url(row.get("url"))
        try:
            published = date.fromisoformat(row.get("published_date", ""))
        except (TypeError, ValueError):
            published = None
        duplicate = bool(url and url in seen)
        outside = not published or not (START <= published <= END)
        if duplicate:
            continue
        if not url or outside:
            warnings.append("duplicate_or_outside_window")
        seen.add(url) if url else None
        evidence = row.get("reading_evidence")
        status = row.get("read_status")
        if status == "read" and (not url or not evidence):
            status = "blocked"
            warnings.append("missing_url_or_evidence")
        if outside:
            status = "blocked"
        if status not in {"read", "read_relevant_sections", "title_only", "blocked", "unread"}:
            status = "unread"
        result = {
            "id": row.get("id") or (url.rsplit("/", 1)[-1] if url else ""),
            "publisher": row.get("publisher") or row.get("account"),
            "title": row.get("title"),
            "published_date": published.isoformat() if published else None,
            "url": url or None,
            "read_status": status,
            "reading_evidence": evidence or None,
            "primary_category": category_for(row),
            "tags": sorted(set(row.get("tags") or [])),
            "summary": row.get("summary") or None,
            "import_warnings": sorted(set(warnings)),
            "source_channel": row.get("source_channel") or "approved_export",
        }
        output.append(result)
    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    rows = normalize_records(json.loads(args.input.read_text()))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
