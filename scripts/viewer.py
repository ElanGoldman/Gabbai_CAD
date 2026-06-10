from pathlib import Path


def build_stl_viewer(project_name: str, stls: list[Path]) -> str:
    if not stls:
        return ""

    stl_array = "[" + ", ".join(f'"{s.name}"' for s in stls) + "]"

    return f"""
## 3D Viewer

<div id="stl-grid-{project_name}"></div>

<script type="module">
import * as THREE from "https://esm.sh/three@0.161.0";
import {{ OrbitControls }} from "https://esm.sh/three@0.161.0/examples/jsm/controls/OrbitControls.js";
import {{ STLLoader }} from "https://esm.sh/three@0.161.0/examples/jsm/loaders/STLLoader.js";

const grid = document.getElementById("stl-grid-{project_name}");
if (!grid) throw new Error("STL grid container not found");

Object.assign(grid.style, {{
    display: "grid",
    gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))",
    gap: "16px",
    marginTop: "10px",
}});

{stl_array}.forEach((filename) => {{
    const cell = document.createElement("div");

    const label = document.createElement("p");
    label.textContent = filename;
    Object.assign(label.style, {{ textAlign: "center", margin: "4px 0", fontSize: "0.85em", color: "#555" }});

    const viewerDiv = document.createElement("div");
    Object.assign(viewerDiv.style, {{ width: "100%", height: "320px", border: "1px solid #ccc" }});

    cell.appendChild(label);
    cell.appendChild(viewerDiv);
    grid.appendChild(cell);

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf5f5f5);

    const camera = new THREE.PerspectiveCamera(75, viewerDiv.clientWidth / viewerDiv.clientHeight, 0.1, 1000);
    camera.position.set(0, 0, 100);

    const renderer = new THREE.WebGLRenderer({{ antialias: true }});
    renderer.setSize(viewerDiv.clientWidth, viewerDiv.clientHeight);
    viewerDiv.appendChild(renderer.domElement);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;

    scene.add(new THREE.AmbientLight(0xffffff, 0.6));
    const light = new THREE.DirectionalLight(0xffffff, 0.8);
    light.position.set(10, 10, 10);
    scene.add(light);

    new STLLoader().load(filename, (geometry) => {{
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
</script>
"""
