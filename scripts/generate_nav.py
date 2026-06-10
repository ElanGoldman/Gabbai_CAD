from pathlib import Path
import shutil

ROOT = Path(".")
DOCS = ROOT / "site_docs"

IGNORE = {
    ".git",
    ".github",
    "site_docs",
    "scripts",
}

if DOCS.exists():
    shutil.rmtree(DOCS)

DOCS.mkdir()

homepage = [
  "# CAD Library",
  "",
  "Browse available projects.",
  "",
]

projects = []

for folder in sorted(ROOT.iterdir()):
    if not folder.is_dir():
        continue
    if folder.name in IGNORE:
        continue

    readme = folder / "README.md"

    if not readme.exists():
        continue

    projects.append(folder)

homepage.append("## Projects")
homepage.append("")

for project in projects:
    homepage.append(f"- [{project.name}]({project.name}/)")

(DOCS/"index.md").write_text(
    "\n".join(homepage),
    encoding="utf8"
)

for project in projects:

    dest = DOCS/project.name
    dest.mkdir()
    readme = project/"README.md"
    content = readme.read_text(encoding="utf8")
    content += "\n\n---\n\n"
    content += "# Downloads\n\n"

    for file in sorted(project.iterdir()):
        if file.is_dir():
            continue
        shutil.copy2(file,dest/file.name)
        content += f"- [{file.name}]({file.name})\n"

    (dest/"index.md").write_text(
        content,
        encoding="utf8"
    )

print("Site generated.")
