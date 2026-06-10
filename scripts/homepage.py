from pathlib import Path


def read_summary(readme_path: Path) -> str:
    text = readme_path.read_text(encoding="utf8")
    lines = text.strip().splitlines()
    return lines[0] if lines else ""


def build_homepage(projects: list[Path], docs: Path) -> None:
    cards = []

    for p in projects:
        stls = [f for f in p.iterdir() if f.suffix.lower() == ".stl"]
        summary = read_summary(p / "README.md")
        stl_list = "<br>".join([f"🧩 {s.name}" for s in stls]) if stls else "No STL"

        cards.append(f"""
<div class="card">
  <h2><a href="{p.name}/">{p.name}</a></h2>
  <p>{summary}</p>
  <p style="font-size:0.9em;color:#666">{stl_list}</p>
</div>
""")

    homepage = f"""
# CAD Library

<div class="grid">
{''.join(cards)}
</div>

<style>
.grid {{
  display:grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap:16px;
}}

.card {{
  border:1px solid #ddd;
  padding:16px;
  border-radius:10px;
  background:white;
  box-shadow:0 2px 6px rgba(0,0,0,0.05);
}}
</style>
"""

    (docs / "index.md").write_text(homepage, encoding="utf8")
