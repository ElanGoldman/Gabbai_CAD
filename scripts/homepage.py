from pathlib import Path


def read_summary(readme_path: Path) -> str:
    for line in readme_path.read_text(encoding="utf8").splitlines():
        stripped = line.strip()
        if stripped:
            return stripped.lstrip("#").strip()
    return ""


def pick_preview_stl(project: Path) -> Path | None:
    stls = sorted(f for f in project.iterdir() if f.suffix.lower() == ".stl")
    if not stls:
        return None
    final = next((f for f in stls if f.stem.lower() == "final"), None)
    return final or stls[0]


def build_homepage(projects: list[Path], docs: Path) -> None:
    cards = []
    viewers = []  # (container_id, stl_url relative to site root)

    for p in projects:
        summary = read_summary(p / "README.md")
        preview = pick_preview_stl(p)
        container_id = f"preview-{p.name}"

        preview_html = ""
        if preview:
            preview_html = f'\n  <div id="{container_id}" style="width:100%; height:220px; background:#f5f5f5;"></div>'
            viewers.append((container_id, f"{p.name}/{preview.name}"))

        cards.append(f"""
<div class="card">
  <div style="padding:16px;">
    <h2><a href="{p.name}/">{p.name}</a></h2>
    <p>{summary}</p>
  </div>{preview_html}
</div>
""")

    viewer_script = _build_viewer_script(viewers) if viewers else ""

    root_readme = (docs.parent / "README.md").read_text(encoding="utf8")

    homepage = f"""
{root_readme}

---

## Projects

<div class="grid">
{''.join(cards)}
</div>

{viewer_script}

<style>
.grid {{
  display:grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap:16px;
}}

.card {{
  border:1px solid #ddd;
  border-radius:10px;
  background:white;
  box-shadow:0 2px 6px rgba(0,0,0,0.05);
  overflow:hidden;
}}
</style>
"""

    (docs / "index.md").write_text(homepage, encoding="utf8")


def _build_viewer_script(viewers: list[tuple[str, str]]) -> str:
    viewers_json = "[" + ", ".join(
        f'{{"id":"{cid}","url":"{url}"}}'
        for cid, url in viewers
    ) + "]"

    return f"""<script type="module">
import * as THREE from "https://esm.sh/three@0.161.0";
import {{ OrbitControls }} from "https://esm.sh/three@0.161.0/examples/jsm/controls/OrbitControls.js";
import {{ STLLoader }} from "https://esm.sh/three@0.161.0/examples/jsm/loaders/STLLoader.js";

{viewers_json}.forEach(({{id, url}}) => {{
    const container = document.getElementById(id);
    if (!container) return;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf5f5f5);

    const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
    camera.position.set(0, 0, 100);

    const renderer = new THREE.WebGLRenderer({{ antialias: true }});
    renderer.setSize(container.clientWidth, container.clientHeight);
    container.appendChild(renderer.domElement);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.autoRotate = true;
    controls.autoRotateSpeed = 1.5;

    scene.add(new THREE.HemisphereLight(0xffffff, 0x444444, 0.5));
    const keyLight = new THREE.DirectionalLight(0xffffff, 1.2);
    keyLight.position.set(10, 10, 10);
    scene.add(keyLight);
    const fillLight = new THREE.DirectionalLight(0xffffff, 0.3);
    fillLight.position.set(-10, -5, -10);
    scene.add(fillLight);

    new STLLoader().load(url, (geometry) => {{
        const material = new THREE.MeshStandardMaterial({{ color: 0x0077ff }});
        const mesh = new THREE.Mesh(geometry, material);

        geometry.computeBoundingBox();
        const size = new THREE.Vector3();
        geometry.boundingBox.getSize(size);
        const center = new THREE.Vector3();
        geometry.boundingBox.getCenter(center);

        mesh.position.sub(center);
        scene.add(mesh);
        camera.position.z = Math.max(size.x, size.y, size.z) * 2;
    }});

    (function animate() {{
        requestAnimationFrame(animate);
        controls.update();
        renderer.render(scene, camera);
    }})();
}});
</script>"""
