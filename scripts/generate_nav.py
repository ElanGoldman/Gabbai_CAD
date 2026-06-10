from pathlib import Path
import shutil

ROOT = Path(".").resolve()
DOCS = ROOT / "site_docs"

IGNORE = {".git", ".github", "site_docs", "scripts", "site"}

# Clean output
if DOCS.exists():
    shutil.rmtree(DOCS)

DOCS.mkdir(parents=True, exist_ok=True)

# -------------------------
# Collect projects
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

# -------------------------
# Helper: extract summary
# -------------------------

def read_summary(readme_path: Path):
    text = readme_path.read_text(encoding="utf8")
    lines = text.strip().splitlines()
    return lines[0] if lines else ""

# -------------------------
# HOMEPAGE (CARD GALLERY)
# -------------------------

cards = []

for p in projects:

    stls = list(p.glob("*.stl"))
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

(DOCS / "index.md").write_text(homepage, encoding="utf8")

# -------------------------
# PROJECT PAGES
# -------------------------

for project in projects:

    dest = DOCS / project.name
    dest.mkdir(parents=True, exist_ok=True)

    readme = project / "README.md"
    content = readme.read_text(encoding="utf8")

    # -------------------------
    # Collect STLs
    # -------------------------
    stls = list(project.glob("*.stl"))

    viewer = ""

    if stls:

        options = "\n".join(
            [f'<option value="{s.name}">{s.name}</option>' for s in stls]
        )

        first = stls[0].name

        viewer = f"""
## 3D Viewer

<select id="stl-select-{project.name}">
{options}
</select>

<div id="viewer-{project.name}" style="width:100%; height:500px; border:1px solid #ccc; margin-top:10px;"></div>

<script type="module">

import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.161.0/build/three.module.js";
import {{ OrbitControls }} from "https://cdn.jsdelivr.net/npm/three@0.161.0/examples/jsm/controls/OrbitControls.js";
import {{ STLLoader }} from "https://cdn.jsdelivr.net/npm/three@0.161.0/examples/jsm/loaders/STLLoader.js";

const container = document.getElementById("viewer-{project.name}");

const scene = new THREE.Scene();
scene.background = new THREE.Color(0xf5f5f5);

const camera = new THREE.PerspectiveCamera(75, container.clientWidth/container.clientHeight, 0.1, 1000);
camera.position.set(0, 0, 100);

const renderer = new THREE.WebGLRenderer({{ antialias: true }});
renderer.setSize(container.clientWidth, container.clientHeight);
container.appendChild(renderer.domElement);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;

scene.add(new THREE.AmbientLight(0xffffff, 0.6));

const light = new THREE.DirectionalLight(0xffffff, 0.8);
light.position.set(10,10,10);
scene.add(light);

const loader = new STLLoader();

let mesh = null;

function loadModel(file) {{

    loader.load(file, function (geometry) {{

        if (mesh) scene.remove(mesh);

        const material = new THREE.MeshStandardMaterial({{ color: 0x0077ff }});
        mesh = new THREE.Mesh(geometry, material);

        geometry.computeBoundingBox();

        const box = geometry.boundingBox;
        const size = new THREE.Vector3();
        box.getSize(size);

        const center = new THREE.Vector3();
        box.getCenter(center);

        mesh.position.sub(center);

        scene.add(mesh);

        camera.position.z = Math.max(size.x, size.y, size.z) * 2;

    }});
}}

loadModel("{first}");

document.getElementById("stl-select-{project.name}").onchange = (e) => {{
    loadModel(e.target.value);
}};

function animate() {{
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}}

animate();

</script>
"""

    # -------------------------
    # Copy files + downloads
    # -------------------------

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

print("CAD gallery built successfully")
