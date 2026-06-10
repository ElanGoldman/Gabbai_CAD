from pathlib import Path


def build_stl_viewer(project_name: str, stls: list[Path]) -> str:
    if not stls:
        return ""

    options = "\n".join(
        [f'<option value="{s.name}">{s.name}</option>' for s in stls]
    )
    first = stls[0].name

    return f"""
## 3D Viewer

<select id="stl-select-{project_name}">
{options}
</select>

<div id="viewer-{project_name}" style="width:100%; height:500px; border:1px solid #ccc; margin-top:10px;"></div>

<script type="module">

import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.161.0/build/three.module.js";
import {{ OrbitControls }} from "https://cdn.jsdelivr.net/npm/three@0.161.0/examples/jsm/controls/OrbitControls.js";
import {{ STLLoader }} from "https://cdn.jsdelivr.net/npm/three@0.161.0/examples/jsm/loaders/STLLoader.js";

const container = document.getElementById("viewer-{project_name}");

const scene = new THREE.Scene();
scene.background = new THREE.Color(0xf5f5f5);

const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
camera.position.set(0, 0, 100);

const renderer = new THREE.WebGLRenderer({{ antialias: true }});
renderer.setSize(container.clientWidth, container.clientHeight);
container.appendChild(renderer.domElement);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;

scene.add(new THREE.AmbientLight(0xffffff, 0.6));

const light = new THREE.DirectionalLight(0xffffff, 0.8);
light.position.set(10, 10, 10);
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

document.getElementById("stl-select-{project_name}").onchange = (e) => {{
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
