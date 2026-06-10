import sys
from pathlib import Path
import shutil

# Allow sibling scripts to be imported when run from the repo root
sys.path.insert(0, str(Path(__file__).parent))

from homepage import build_homepage
from project_page import build_project_page

ROOT = Path(".").resolve()
DOCS = ROOT / "site_docs"
IGNORE = {".git", ".github", "site_docs", "scripts", "site"}

if DOCS.exists():
    shutil.rmtree(DOCS)
DOCS.mkdir(parents=True, exist_ok=True)

projects = [
    folder
    for folder in sorted(ROOT.iterdir())
    if folder.is_dir()
    and folder.name not in IGNORE
    and (folder / "README.md").exists()
]

build_homepage(projects, DOCS)

for project in projects:
    build_project_page(project, DOCS)

print("CAD gallery built successfully")
