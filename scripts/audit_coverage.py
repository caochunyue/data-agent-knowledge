#!/usr/bin/env python3
"""Audit whether a WeChat article inventory is closed and every item was read."""

import argparse
import json
from collections import Counter
from datetime import date
from pathlib import Path

START = date.fromisoformat("2025-11-01")
END = date.fromisoformat("2026-11-01")
TRUSTED_HISTORY_SOURCES = {"official_history", "publisher_export"}


def _valid_date(value):
    try:
        parsed = date.fromisoformat(value)
    except (TypeError, ValueError):
        return None
    return parsed if START <= parsed <= END else None


def audit(accounts, articles, expected_accounts=36):
    """Return a proof-oriented coverage report; unknown totals remain null."""
    account_ids = [item.get("id") for item in accounts]
    duplicate_account_ids = {key for key, count in Counter(account_ids).items() if key and count > 1}
    known_accounts = set(account_ids)
    global_errors = []
    if len(accounts) != expected_accounts:
        global_errors.append("account_count_mismatch")
    if None in known_accounts or "" in known_accounts or duplicate_account_ids:
        global_errors.append("invalid_or_duplicate_account_id")

    article_ids = [item.get("id") for item in articles]
    duplicate_article_ids = {key for key, count in Counter(article_ids).items() if key and count > 1}
    urls = [item.get("url") for item in articles]
    duplicate_urls = {key for key, count in Counter(urls).items() if key and count > 1}
    if duplicate_article_ids or duplicate_urls:
        global_errors.append("duplicate_article")
    if any(item.get("account_id") not in known_accounts for item in articles):
        global_errors.append("article_unknown_account")

    rows = []
    for account in accounts:
        errors = []
        account_id = account.get("id")
        pushes = account.get("pushes") or []
        inventory_closed = all([
            account.get("identity_verified") is True,
            bool(account.get("identity_evidence")),
            account.get("history_source") in TRUSTED_HISTORY_SOURCES,
            bool(account.get("history_evidence")),
            account.get("history_complete") is True,
            account.get("lower_boundary_checked") is True,
            account.get("cutoff_checked") is True,
        ])
        if not inventory_closed:
            errors.append("inventory_not_closed")

        push_ids = [push.get("id") for push in pushes]
        if any(not value for value in push_ids) or len(push_ids) != len(set(push_ids)):
            errors.append("invalid_or_duplicate_push")
        expected_articles = None
        if inventory_closed:
            valid_pushes = True
            expected_articles = 0
            for push in pushes:
                count = push.get("item_count")
                if not _valid_date(push.get("published_date")) or isinstance(count, bool) or not isinstance(count, int) or count < 1 or not push.get("evidence"):
                    valid_pushes = False
                else:
                    expected_articles += count
            if not valid_pushes:
                errors.append("invalid_push_evidence")

        account_articles = [item for item in articles if item.get("account_id") == account_id]
        positions = set()
        full_read = 0
        push_by_id = {push.get("id"): push for push in pushes}
        for item in account_articles:
            push = push_by_id.get(item.get("push_id"))
            key = (item.get("push_id"), item.get("position"))
            if key in positions:
                errors.append("duplicate_push_position")
            positions.add(key)
            item_date = _valid_date(item.get("published_date"))
            position = item.get("position")
            try:
                checked_at = date.fromisoformat(item.get("version_checked_at"))
            except (TypeError, ValueError):
                checked_at = None
            push_count = push.get("item_count") if push else None
            valid_item = bool(
                push
                and isinstance(item.get("id"), str)
                and item.get("id").strip()
                and item_date
                and push.get("published_date") == item.get("published_date")
                and isinstance(position, int)
                and not isinstance(position, bool)
                and isinstance(push_count, int)
                and not isinstance(push_count, bool)
                and 1 <= position <= push_count
                and item.get("title")
                and str(item.get("url", "")).startswith("https://mp.weixin.qq.com/")
                and item.get("read_status") == "read"
                and item.get("reading_evidence")
                and item.get("visuals_checked") is True
                and checked_at
                and item_date <= checked_at <= END
            )
            if valid_item:
                full_read += 1
            else:
                errors.append("invalid_or_unread_article")

        if expected_articles is not None and len(account_articles) != expected_articles:
            errors.append("article_count_mismatch")
        complete = inventory_closed and not errors and full_read == expected_articles
        rows.append({
            "id": account_id,
            "name": account.get("name"),
            "expected_articles": expected_articles,
            "enumerated_articles": len(account_articles),
            "full_read": full_read,
            "complete": complete,
            "errors": sorted(set(errors)),
        })

    all_complete = not global_errors and len(rows) == expected_accounts and all(row["complete"] for row in rows)
    return {
        "window": {"start": START.isoformat(), "end": END.isoformat()},
        "expected_accounts": expected_accounts,
        "account_count": len(rows),
        "all_complete": all_complete,
        "global_errors": sorted(set(global_errors)),
        "accounts": rows,
    }


def render_markdown(report):
    lines = [
        "# 微信全年文章覆盖报告",
        "",
        f"窗口：{report['window']['start']} 至 {report['window']['end']}。完整账号："
        f"{sum(row['complete'] for row in report['accounts'])}/{report['expected_accounts']}。",
        "",
        "`?` 表示历史边界未闭合，总数未知；不能按 0 篇或 100% 处理。",
        "",
        "| 账号 | 应有文章 | 已枚举 | 已完整阅读 | 完成 | 阻塞 |",
        "|---|---:|---:|---:|---|---|",
    ]
    for row in report["accounts"]:
        expected = "?" if row["expected_articles"] is None else str(row["expected_articles"])
        errors = "、".join(row["errors"]) or "-"
        lines.append(
            f"| {row['name']} | {expected} | {row['enumerated_articles']} | "
            f"{row['full_read']} | {'是' if row['complete'] else '否'} | {errors} |"
        )
    lines.extend(["", "本报告由账本一致性检查生成；它不能代替对微信页面和正文的人工证据核验。", ""])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--accounts", required=True, type=Path)
    parser.add_argument("--articles", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--markdown-output", type=Path)
    parser.add_argument("--expected-accounts", type=int, default=36)
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()
    report = audit(json.loads(args.accounts.read_text()), json.loads(args.articles.read_text()), args.expected_accounts)
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
    else:
        print(rendered, end="")
    if args.markdown_output:
        args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_output.write_text(render_markdown(report))
    return 1 if args.require_complete and not report["all_complete"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
