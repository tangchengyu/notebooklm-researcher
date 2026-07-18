from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "normalize_last30days.py"
SPEC = importlib.util.spec_from_file_location("normalize_last30days", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class NormalizeLast30DaysTests(unittest.TestCase):
    def test_url_normalization_and_rednote_display(self) -> None:
        url = "HTTPS://Example.COM/a/?utm_source=x&b=2#fragment"
        self.assertEqual(MODULE.canonical_url(url), "https://example.com/a?b=2")

        rednote = "https://www.xiaohongshu.com/explore/abc?utm_source=x&xsec_token=keep"
        self.assertEqual(
            MODULE.display_url(rednote),
            "https://www.xiaohongshu.com/explore/abc?xsec_token=keep",
        )

    def test_duplicate_records_merge_conservatively(self) -> None:
        left = MODULE.normalize_item(
            {
                "source": "x",
                "title": "Example",
                "url": "https://x.com/example/status/1?utm_source=test",
                "summary": "short",
                "engagement": {"likes": 3},
            },
            "last30days",
        )
        right = MODULE.normalize_item(
            {
                "source": "supplement",
                "sources": ["x", "official"],
                "title": "Example source",
                "url": "https://x.com/example/status/1",
                "summary": "a longer complementary summary",
                "engagement": {"likes": 8, "reposts": 2},
                "coverage_note": "independently checked",
            },
            "supplement:test.json",
        )
        merged, removed = MODULE.dedupe_items([left, right])
        self.assertEqual(removed, 1)
        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0]["engagement"]["likes"], 8)
        self.assertEqual(merged[0]["engagement"]["reposts"], 2)
        self.assertIn("official", merged[0]["sources"])
        self.assertEqual(merged[0]["summary"], "a longer complementary summary")

    def test_cli_emits_clean_structured_markdown(self) -> None:
        report = {
            "schema_version": "1.2",
            "query": "NotebookLM workflows",
            "generated_at": "2026-07-18T00:00:00Z",
            "window_days": 30,
            "source_status": {"x": "ok", "youtube": "timeout"},
            "clusters": [{"title": "Signal", "summary": "Useful evidence", "sources": ["x"]}],
            "results": [
                {
                    "source": "x",
                    "title": "\u001b[31mPost\u001b[0m",
                    "url": "https://x.com/example/status/1",
                    "summary": "Evidence",
                }
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "agent.json"
            output = root / "pack.md"
            source.write_text(json.dumps(report), encoding="utf-8")

            old_argv = MODULE.sys.argv
            try:
                MODULE.sys.argv = [str(SCRIPT), "--input", str(source), "--output", str(output)]
                self.assertEqual(MODULE.main(), 0)
            finally:
                MODULE.sys.argv = old_argv

            text = output.read_text(encoding="utf-8")
            self.assertNotIn("\u001b", text)
            self.assertIn("## 数据源覆盖", text)
            self.assertIn("| x | 成功 | 1 |", text)
            self.assertIn("youtube：超时", text)
            self.assertEqual(text.count("https://x.com/example/status/1"), 1)


if __name__ == "__main__":
    unittest.main()
