(function () {
    const desktopQuery = window.matchMedia("(min-width: 992px)");
    const reduceMotionQuery = window.matchMedia("(prefers-reduced-motion: reduce)");

    if (!desktopQuery.matches || reduceMotionQuery.matches) return;

    const slot = document.querySelector(".portrait-animation-slot");
    if (!slot) return;

    const videos = Array.from(slot.querySelectorAll(".portrait-animation-video"));
    if (!videos.length) return;

    const randomDelay = () => 10000 + Math.random() * 20000;
    const hideVideo = (video) => {
        video.pause();
        try {
            video.currentTime = 0;
        } catch (error) {
            // The video may not have loaded metadata yet.
        }
        video.classList.remove("is-active");
    };

    const startVideo = (video, fallback) => {
        try {
            video.currentTime = 0;
        } catch (error) {
            // Some browsers reject currentTime before metadata is available.
        }

        video.play().catch(() => {
            window.clearTimeout(fallback);
            hideVideo(video);
            scheduleNext();
        });
    };

    const playOne = () => {
        const video = videos[Math.floor(Math.random() * videos.length)];

        videos.forEach((item) => {
            if (item !== video) hideVideo(item);
        });

        if (!video.src) {
            video.src = video.dataset.src;
            video.load();
        }

        video.classList.add("is-active");

        const fallback = window.setTimeout(() => {
            hideVideo(video);
            scheduleNext();
        }, 5000);

        video.onended = () => {
            window.clearTimeout(fallback);
            hideVideo(video);
            scheduleNext();
        };

        if (video.readyState >= 1) {
            startVideo(video, fallback);
        } else {
            video.onloadedmetadata = () => startVideo(video, fallback);
        }
    };

    const scheduleNext = () => {
        window.setTimeout(playOne, randomDelay());
    };

    scheduleNext();
})();
