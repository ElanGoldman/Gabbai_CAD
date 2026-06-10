for project in projects:

    dest = DOCS / project.name
    dest.mkdir(parents=True, exist_ok=True)

    readme = project / "README.md"
    content = readme.read_text(encoding="utf8")

    # -------------------------
    # Find STL file (first one)
    # -------------------------
    stl_files = list(project.glob("*.stl"))

    viewer_html = ""

    if stl_files:

        stl_file = stl_files[0].name  # use first STL

        viewer_html = f"""
## 3D Preview

<div id="viewer-{project.name}" style="width:100%; height:500px; border:1px solid #ccc;"></div>

<script type="module">
import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.161.0/build/three.module.js";
import { OrbitControls } from "https://cdn.jsdelivr.net/npm/three@0.161.0/examples/jsm/controls/OrbitControls.js";
import { STLLoader } from "https://cdn.jsdelivr.net/npm/three@0.161.0/examples/jsm/loaders/STLLoader.js";

const container = document.getElementById("viewer-{project.name}");

const scene = new THREE.Scene();
scene.background = new THREE.Color(0xf5f5f5);

const camera = new THREE.PerspectiveCamera(75, container.clientWidth/container.clientHeight, 0.1, 1000);
camera.position.set(0, 0, 100);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(container.clientWidth, container.clientHeight);
container.appendChild(renderer.domElement);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;

const light1 = new THREE.AmbientLight(0xffffff, 0.6);
scene.add(light1);

const light2 = new THREE.DirectionalLight(0xffffff, 0.8);
light2.position.set(10, 10, 10);
scene.add(light2);

const loader = new STLLoader();

loader.load("{stl_file}", function (geometry) {{

    const material = new THREE.MeshStandardMaterial({{ color: 0x0077ff }});
    const mesh = new THREE.Mesh(geometry, material);

    geometry.computeBoundingBox();

    const box = geometry.boundingBox;
    const size = new THREE.Vector3();
    box.getSize(size);

    const center = new THREE.Vector3();
    box.getCenter(center);

    mesh.position.sub(center); // center model
    scene.add(mesh);

    camera.position.z = Math.max(size.x, size.y, size.z) * 2;
}});

function animate() {{
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}}

animate();
</script>
"""
    else:
        viewer_html = "## 3D Preview\n\n_No STL file found in this project._"

    # -------------------------
    # Copy files + build downloads
    # -------------------------
    content += "\n\n---\n\n"
    content += viewer_html
    content += "\n\n---\n\n"
    content += "# Downloads\n\n"

    for file in sorted(project.iterdir()):

        if file.is_dir():
            continue

        shutil.copy2(file, dest / file.name)

        content += f"- [{file.name}]({file.name})\n"

    (dest / "index.md").write_text(content, encoding="utf8")
