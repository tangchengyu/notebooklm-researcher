import unittest
from pathlib import Path


class ObsidianExportContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill_root = Path(__file__).resolve().parents[1]
        cls.skill_text = (cls.skill_root / "SKILL.md").read_text(encoding="utf-8")
        cls.resolver_text = (
            cls.skill_root / "scripts" / "resolve_research_root.ps1"
        ).read_text(encoding="utf-8")

    def test_complete_pipeline_is_explicit(self):
        for phrase in (
            "收集信息",
            "导入 NotebookLM",
            "保存到 Obsidian",
            "briefing.md",
            "infographic.png",
            "mind-map.json",
            "learning-path.md",
        ):
            self.assertIn(phrase, self.skill_text)

    def test_root_resolution_preserves_portability_and_local_vault(self):
        self.assertIn("NOTEBOOKLM_RESEARCH_ROOT", self.resolver_text)
        self.assertIn("G:\\obsidian_vault\\Obsidian Vault", self.resolver_text)
        self.assertIn("NotebookLM Research", self.resolver_text)


if __name__ == "__main__":
    unittest.main()
