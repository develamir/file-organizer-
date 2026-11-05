import unittest
import tempfile
import io
import sys
from pathlib import Path
from main import organize_files


class TestOrganizeFiles(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

        self.files = {
            'image.jpg': self.root / 'image.jpg',
            'doc.pdf': self.root / 'doc.pdf',
            'script.py': self.root / 'script.py',
            'noext': self.root / 'noext',
            'another.jpg': self.root / 'another.jpg',
        }
        for name, path in self.files.items():
            path.touch()

        docs_dir = self.root / 'docs'
        docs_dir.mkdir()
        (docs_dir / 'report.txt').touch()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_organize_files(self):
        organize_files(self.root, dry_run=False)

        self.assertTrue((self.root / 'jpg').is_dir())
        self.assertTrue((self.root / 'pdf').is_dir())
        self.assertTrue((self.root / 'py').is_dir())
        self.assertTrue((self.root / 'others').is_dir())

        self.assertTrue((self.root / 'jpg' / 'image.jpg').exists())
        self.assertFalse(self.files['image.jpg'].exists())

        self.assertTrue((self.root / 'pdf' / 'doc.pdf').exists())
        self.assertFalse(self.files['doc.pdf'].exists())

        self.assertTrue((self.root / 'py' / 'script.py').exists())
        self.assertFalse(self.files['script.py'].exists())

        self.assertTrue((self.root / 'others' / 'noext').exists())
        self.assertFalse(self.files['noext'].exists())

        self.assertTrue((self.root / 'jpg' / 'another.jpg').exists())

        self.assertTrue((self.root / 'docs' / 'report.txt').exists())
        self.assertEqual(len(list((self.root / 'docs').iterdir())), 1)

    def test_dry_run(self):
        captured_output = io.StringIO()
        original_stdout = sys.stdout
        sys.stdout = captured_output
        try:
            organize_files(self.root, dry_run=True)
        finally:
            sys.stdout = original_stdout

        output = captured_output.getvalue()
        self.assertIn("Would move", output)
        self.assertIn("image.jpg", output)
        self.assertIn("doc.pdf", output)
        self.assertIn("script.py", output)
        self.assertIn("noext", output)
        self.assertIn("another.jpg", output)


if __name__ == '__main__':
    unittest.main()
