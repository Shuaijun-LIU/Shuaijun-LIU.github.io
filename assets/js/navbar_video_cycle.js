(function () {
    const desktopQuery = window.matchMedia("(min-width: 992px)");
    const reduceMotionQuery = window.matchMedia("(prefers-reduced-motion: reduce)");

    if (!desktopQuery.matches || reduceMotionQuery.matches) return;

    document.querySelectorAll(".navbar-video-cycle").forEach((slot) => {
        const videos = Array.from(slot.querySelectorAll(".navbar-video-cycle-item"));
        if (!videos.length) return;

        const randomDuration = () => 10000 + Math.random() * 20000;
        let activeIndex = Math.floor(Math.random() * videos.length);
        let switchTimer = null;

        const resetVideo = (video) => {
            video.pause();
            try {
                video.currentTime = 0;
            } catch (error) {
                // The video may not have loaded metadata yet.
            }
            video.classList.remove("is-active");
        };

        const playVideo = (video) => {
            try {
                video.currentTime = 0;
            } catch (error) {
                // Some browsers reject currentTime before metadata is available.
            }

            video.play().catch(() => {
                resetVideo(video);
                switchToNext();
            });
        };

        const showActive = () => {
            const video = videos[activeIndex];

            videos.forEach((item) => {
                if (item !== video) resetVideo(item);
            });

            if (!video.src) {
                video.src = video.dataset.src;
                video.load();
            }

            video.classList.add("is-active");

            if (video.readyState >= 1) {
                playVideo(video);
            } else {
                video.onloadedmetadata = () => playVideo(video);
            }

            window.clearTimeout(switchTimer);
            switchTimer = window.setTimeout(switchToNext, randomDuration());
        };

        const switchToNext = () => {
            const previousIndex = activeIndex;
            if (videos.length > 1) {
                while (activeIndex === previousIndex) {
                    activeIndex = Math.floor(Math.random() * videos.length);
                }
            }
            showActive();
        };

        showActive();
    });
})();
