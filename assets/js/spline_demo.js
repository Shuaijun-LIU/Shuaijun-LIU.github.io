import { Application } from "@splinetool/runtime";

const root = document.getElementById("followers-scene");
const canvas = document.getElementById("followers-canvas");

if (root && canvas) {
    const app = new Application(canvas);

    app.load(root.dataset.sceneUrl)
        .then(() => {
            root.classList.add("is-loaded");
        })
        .catch((error) => {
            console.error(error);
            root.classList.add("is-loaded", "is-error");
        });

    window.addEventListener("beforeunload", () => {
        app.dispose();
    });
}
