// Create and inject styles for the MPV button
const style = document.createElement('style');
style.textContent = `
.mpv-container {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    pointer-events: none;
    z-index: 1000000;
}
.mpv-play-button {
    position: absolute;
    top: 6px;
    left: 6px;
    background: rgba(34, 34, 34, 0.4);
    color: white;
    border: none;
    padding: 4px 8px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 13px;
    opacity: 0;
    pointer-events: auto;
    transition: all 0.2s ease;
    backdrop-filter: blur(4px);
    display: flex;
    align-items: center;
    gap: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
    mix-blend-mode: multiply;
}

/* Add MPV icon */
.mpv-play-button::before {
    content: "";
    display: inline-block;
    width: 14px;
    height: 14px;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='white'%3E%3Cpath d='M8 5v14l11-7z'/%3E%3C/svg%3E");
    background-size: contain;
    background-repeat: no-repeat;
    vertical-align: middle;
}

.mpv-play-button:hover {
    background: rgba(66, 66, 66, 0.6);
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.mpv-play-button:active {
    transform: translateY(0);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
}

/* Track hover state of all possible video containers */
.bili-video-card:hover .mpv-container .mpv-play-button,
.video-card:hover .mpv-container .mpv-play-button,
.bili-video-card__wrap:hover .mpv-container .mpv-play-button,
.video-item:hover .mpv-container .mpv-play-button,
.media-list-item:hover .mpv-container .mpv-play-button,
a.video-awesome-img:hover .mpv-container .mpv-play-button {
    opacity: 1;
}`;
document.head.appendChild(style);

// Add search page specific styles
if (window.location.hostname === 'search.bilibili.com') {
    const searchStyle = document.createElement('style');
    searchStyle.textContent = `
    .bili-video-card__skeleton--cover,
    .bili-video-card__skeleton--info,
    .bili-video-card__skeleton--right,
    .bili-video-card__skeleton--text,
    .bili-video-card__skeleton--light {
        display: none !important;
    }`;
    document.head.appendChild(searchStyle);
}

// Function to add MPV button to a video thumbnail
function addMpvButton(container) {
    // Skip if:
    // 1. Button already exists
    // 2. Container is a skeleton
    // 3. Container is inside a carousel/swiper
    // 4. Container has no actual video content
    if (container.querySelector('.mpv-container') ||
        container.classList.contains('bili-video-card__skeleton') ||
        container.closest('.bili-video-card__skeleton') ||
        container.closest('.recommended-swipe-core') ||
        container.closest('.vui_carousel') ||
        container.closest('.carousel')) return;

    // Find the video link - handle container being the <a> element itself
    const videoLink = container.matches('a[href*="/video/"]') ? container : container.querySelector('a[href*="/video/"]');
    if (!videoLink) return;

    // Get full URL for relative paths
    const href = new URL(videoLink.href, window.location.href).href;
    if (!href) return;

    const videoPattern = /\/video\/(BV\w+)/i;
    const match = href.match(videoPattern);
    if (!match) return;

    // Create container for the button
    const buttonContainer = document.createElement('div');
    buttonContainer.className = 'mpv-container';

    // Create MPV button
    const button = document.createElement('button');
    button.className = 'mpv-play-button';
    button.textContent = 'MPV';

    // Handle click
    button.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        console.info('Opening video in MPV:', href);

        chrome.runtime.sendMessage({
            action: 'openInMpv',
            url: href
        });
    });

    // Add button to container
    buttonContainer.appendChild(button);

    // Find appropriate wrapper
    let wrapper = container;
    if (!container.style.position || container.style.position === 'static') {
        container.style.position = 'relative';
    }
    wrapper.appendChild(buttonContainer);
}

// Function to observe DOM changes for dynamically loaded content
function observeVideoThumbnails() {
    // Process existing thumbnails
    const selectors = [
        '.bili-video-card',
        '.video-card',
        '.bili-video-card__wrap',
        '.video-item',
        '.media-list-item',
        '.video-awesome-img'
    ];

    selectors.forEach(selector => {
        document.querySelectorAll(selector).forEach(el => {
            addMpvButton(el);
        });
    });

    // Create an observer for dynamic content
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            mutation.addedNodes.forEach((node) => {
                if (node.nodeType === 1) { // Element node
                    selectors.forEach(selector => {
                        if (node.matches?.(selector)) {
                            addMpvButton(node);
                        }
                        node.querySelectorAll(selector).forEach(el => {
                            addMpvButton(el);
                        });
                    });
                }
            });
        });
    });

    // Start observing
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
}

// Start observing when DOM is loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', observeVideoThumbnails);
} else {
    observeVideoThumbnails();
}
