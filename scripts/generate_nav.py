from pathlib import Path
import shutil

ROOT = Path(".").resolve()
DOCS = ROOT / "site_docs"

IGNORE = {
    ".git",
    ".github",
    "site_docs",
    "scripts",
    "site",
}

# Clean output
if DOCS.exists():
    shutil.rmtree(DOCS)

DOCS.mkdir(parents=True, exist_ok=True)

# -------------------------
# 1. Build homepage from ROOT README
# -------------------------

readme = ROOT / "README.md"

if readme.exists():
    homepage_content = readme.read_text(encoding="utf8")
else:
    homepage_content = "# CAD Library\n\nNo root README.md found."

homepage_content += "\n\n---\n\n"
homepage_content += "# Projects\n\n"

# -------------------------
# 2. Detect projects
# -------------------------

projects = []

for folder in sorted(ROOT.iterdir()):
    if not folder.is_dir():
        continue
    if folder.name in IGNORE:
        continue
    if not (folder / "README.md").exists():
        continue
    projects.append(folder)

# Add project list to homepage
for p in projects:
    homepage_content += f"- [{p.name}]({p.name}/)\n"

# Write homepage as index.md (THIS is what fixes your issue)
(DOCS / "index.md").write_text(homepage_content, encoding="utf8")

# -------------------------
# 3. Build project pages
# -------------------------

for project in projects:

    dest = DOCS / project.name
    dest.mkdir(parents=True, exist_ok=True)

    readme = project / "README.md"

    content = readme.read_text(encoding="utf8")

    content += "\n\n---\n\n"
    content += "# Downloads\n\n"

    for file in sorted(project.iterdir()):

        if file.is_dir():
            continue

        shutil.copy2(file, dest / file.name)

        content += f"- [{file.name}]({file.name})\n"

    (dest / "index.md").write_text(content, encoding="utf8")

print("Homepage now uses root README.md")
