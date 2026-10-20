"""Documents, site data and the committed sample extract say what the model says."""
import subprocess
import sys
import unittest

from erpcase import sap_extract

from .helpers import ROOT


class Docs(unittest.TestCase):
    def test_build_check_passes(self):
        result = subprocess.run([sys.executable, "scripts/build.py", "--check"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_links(self):
        result = subprocess.run([sys.executable, "scripts/check-links.py"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_committed_sample_extract_matches_generator(self):
        tables = sap_extract.read_csv(ROOT / "data/sap-extract/mock-3")
        generated = sap_extract.generate("mock-3")
        for name in ("KNA1", "MCH1", "MCHB"):
            with self.subTest(table=name):
                self.assertEqual(len(tables[name]), len(generated[name]))
                self.assertEqual(tables[name][0], {k: str(v) for k, v in generated[name][0].items()})

    def test_disclaimer_on_readme_and_site(self):
        for path in ("README.md", "site/index.html", "site/room/index.html"):
            text = (ROOT / path).read_text(encoding="utf-8")
            self.assertIn("fictieve organisatie", text.lower(), path)


if __name__ == "__main__":
    unittest.main()
