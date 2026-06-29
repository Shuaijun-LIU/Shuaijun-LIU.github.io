import * as THREE from "three";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";

const root = document.getElementById("followers-scene");
const canvas = document.getElementById("followers-canvas");

if (root && canvas) {
    const scene = new THREE.Scene();
    scene.fog = new THREE.Fog(0x0b0d15, 7, 16);

    const camera = new THREE.PerspectiveCamera(38, 1, 0.1, 100);
    camera.position.set(0, 0.5, 7.1);

    const renderer = new THREE.WebGLRenderer({
        canvas,
        antialias: true,
        alpha: false,
        powerPreference: "high-performance",
    });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.05;
    renderer.setClearColor(0x0b0d15, 1);

    const modelGroup = new THREE.Group();
    scene.add(modelGroup);

    const ambientLight = new THREE.HemisphereLight(0xffffff, 0x1f2a44, 1.6);
    scene.add(ambientLight);

    const keyLight = new THREE.DirectionalLight(0xffffff, 2.4);
    keyLight.position.set(4, 6, 6);
    scene.add(keyLight);

    const rimLight = new THREE.PointLight(0x76c7ff, 2.8, 10);
    rimLight.position.set(-3.5, 2.5, 3.5);
    scene.add(rimLight);

    const fillLight = new THREE.PointLight(0xff8c5a, 1.6, 9);
    fillLight.position.set(3.2, -1.5, 3.8);
    scene.add(fillLight);

    const pointer = new THREE.Vector2(0, 0);
    const targetPointer = new THREE.Vector2(0, 0);
    let scrollZoom = 0;
    let targetZoom = 0;
    let modelLoaded = false;

    function resize() {
        const rect = root.getBoundingClientRect();
        const width = Math.max(1, rect.width);
        const height = Math.max(1, rect.height);
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
        renderer.setSize(width, height, false);
    }

    function fitModel(object) {
        object.traverse((child) => {
            if (!child.isMesh || !child.geometry) return;
            child.geometry.computeBoundingBox();
            const size = child.geometry.boundingBox.getSize(new THREE.Vector3());
            if (Math.max(size.x, size.y, size.z) > 1200) {
                child.visible = false;
            }
        });

        object.updateWorldMatrix(true, true);
        const box = new THREE.Box3();
        object.traverse((child) => {
            if (!child.isMesh || !child.visible || !child.geometry) return;
            const childBox = child.geometry.boundingBox.clone().applyMatrix4(child.matrixWorld);
            box.union(childBox);
        });

        const size = box.getSize(new THREE.Vector3());
        const center = box.getCenter(new THREE.Vector3());
        const maxDimension = Math.max(size.x, size.y, size.z);
        const scale = maxDimension > 0 ? 3.25 / maxDimension : 1;

        object.position.sub(center);
        object.scale.setScalar(scale);
        object.rotation.set(-0.1, 0.16, 0);
        modelGroup.add(object);
    }

    function setPointer(event) {
        const rect = root.getBoundingClientRect();
        targetPointer.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
        targetPointer.y = -(((event.clientY - rect.top) / rect.height) * 2 - 1);
    }

    root.addEventListener("pointermove", setPointer);
    root.addEventListener("pointerleave", () => {
        targetPointer.set(0, 0);
    });
    root.addEventListener("pointerdown", (event) => {
        setPointer(event);
        rimLight.intensity = 4.2;
        fillLight.intensity = 2.4;
    });
    root.addEventListener("pointerup", () => {
        rimLight.intensity = 2.8;
        fillLight.intensity = 1.6;
    });
    root.addEventListener(
        "wheel",
        (event) => {
            targetZoom = THREE.MathUtils.clamp(targetZoom + event.deltaY * 0.0009, -0.65, 0.85);
        },
        { passive: true },
    );

    const loader = new GLTFLoader();
    loader.load(
        root.dataset.modelUrl,
        (gltf) => {
            fitModel(gltf.scene);
            modelLoaded = true;
            root.classList.add("is-loaded");
        },
        undefined,
        () => {
            root.classList.add("is-loaded", "is-error");
        },
    );

    function animate(time) {
        requestAnimationFrame(animate);

        const seconds = time * 0.001;
        pointer.lerp(targetPointer, 0.08);
        scrollZoom = THREE.MathUtils.lerp(scrollZoom, targetZoom, 0.08);
        const responsiveScale = camera.aspect < 0.72 ? 0.58 : camera.aspect < 1 ? 0.78 : 1;

        modelGroup.scale.setScalar(responsiveScale);
        modelGroup.rotation.y = pointer.x * 0.34 + Math.sin(seconds * 0.38) * 0.08;
        modelGroup.rotation.x = -pointer.y * 0.16 + Math.sin(seconds * 0.53) * 0.025;
        modelGroup.position.x = pointer.x * 0.16;
        modelGroup.position.y = pointer.y * 0.08 + Math.sin(seconds * 0.7) * 0.045;

        camera.position.z = 7.1 + scrollZoom;
        camera.position.x = pointer.x * 0.18;
        camera.position.y = 0.5 + pointer.y * 0.08;
        camera.lookAt(0, 0.06, 0);

        if (modelLoaded) {
            rimLight.position.x = -3.5 + pointer.x * 1.4;
            fillLight.position.y = -1.5 + pointer.y * 0.9;
        }

        renderer.render(scene, camera);
    }

    resize();
    window.addEventListener("resize", resize);
    requestAnimationFrame(animate);
}
