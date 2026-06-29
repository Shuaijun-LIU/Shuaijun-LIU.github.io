import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
import SplineLoader from "@splinetool/loader";

const root = document.getElementById("spline-loader-scene");

function parseVector(value, fallback) {
    if (!value) return fallback;
    const parts = value.split(",").map((part) => Number(part.trim()));
    return parts.length === 3 && parts.every(Number.isFinite) ? parts : fallback;
}

if (root) {
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(root.clientWidth, root.clientHeight);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFShadowMap;
    renderer.setClearAlpha(1);
    root.appendChild(renderer.domElement);

    const camera = new THREE.PerspectiveCamera(
        Number(root.dataset.cameraFov || 45),
        root.clientWidth / root.clientHeight,
        5,
        100000
    );
    const position = parseVector(root.dataset.cameraPosition, [-2019.8, 152.57, 1821.41]);
    const rotation = parseVector(root.dataset.cameraRotation, [-0.22, -0.31, -0.07]);
    camera.position.set(position[0], position[1], position[2]);
    camera.quaternion.setFromEuler(new THREE.Euler(rotation[0], rotation[1], rotation[2]));

    const scene = new THREE.Scene();
    scene.background = new THREE.Color("#000000");

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.125;

    const loader = new SplineLoader();
    loader.load(
        root.dataset.sceneUrl,
        (splineScene) => {
            scene.add(splineScene);
            root.classList.add("is-loaded");
        },
        undefined,
        (error) => {
            console.error(error);
            root.classList.add("is-loaded", "is-error");
        }
    );

    function resize() {
        const width = root.clientWidth;
        const height = root.clientHeight;
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
        renderer.setSize(width, height);
    }

    window.addEventListener("resize", resize);
    renderer.setAnimationLoop(() => {
        controls.update();
        renderer.render(scene, camera);
    });
}
