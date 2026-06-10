from pathlib import Path
import shutil

from viewer import build_stl_viewer


def build_project_page(project: Path, docs: Path) -> None:
    dest = docs / project.name
    dest.mkdir(parents=True, exist_ok=True)

    content = (project / "README.md").read_text(encoding="utf8")

    stls = [f for f in project.iterdir() if f.suffix.lower() == ".stl"]
    viewer = build_stl_viewer(project.name, stls)

    content += "\n\n---\n\n"
    content += viewer
    content += "\n\n---\n\n"
    content += "# Downloads\n\n"

    for f in sorted(project.iterdir()):
        if f.is_dir():
            continue
        shutil.copy2(f, dest / f.name)
        content += f"- [{f.name}]({f.name})\n"

    (dest / "index.md").write_text(content, encoding="utf8")
