import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from import_articles import normalize_records  # noqa: E402


class ArticleImportContract(unittest.TestCase):
    def test_normalizes_and_classifies_without_retaining_body(self):
        rows = normalize_records([{
            "account": "示例号", "title": "MaxCompute SQL 优化与数据 Agent",
            "published_date": "2026-01-02", "url": "https://mp.weixin.qq.com/s/abc?ch=1",
            "read_status": "read", "reading_evidence": "正文段落定位", "summary": "讲解执行计划和受控工具。",
            "body": "不得进入仓库的全文", "tags": ["优化"]
        }])
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["url"], "https://mp.weixin.qq.com/s/abc")
        self.assertEqual(rows[0]["primary_category"], "数据 Agent")
        self.assertNotIn("body", rows[0])
        self.assertEqual(rows[0]["read_status"], "read")

    def test_deduplicates_urls_and_rejects_outside_window(self):
        base = {"account": "示例号", "title": "文章", "published_date": "2026-01-02",
                "url": "https://mp.weixin.qq.com/s/a", "read_status": "title_only"}
        rows = normalize_records([base, dict(base), dict(base, url="https://mp.weixin.qq.com/s/b", published_date="2025-10-31")])
        self.assertEqual(len(rows), 2)
        self.assertIn("duplicate_or_outside_window", rows[1]["import_warnings"])
        self.assertEqual(rows[1]["read_status"], "blocked")

    def test_missing_url_or_read_evidence_is_not_read(self):
        rows = normalize_records([{"account": "示例号", "title": "文章", "published_date": "2026-01-02",
                                  "url": "", "read_status": "read"}])
        self.assertEqual(rows[0]["read_status"], "blocked")
        self.assertIn("missing_url_or_evidence", rows[0]["import_warnings"])
