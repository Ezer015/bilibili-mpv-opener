// Define styles for the MPV button
const mpvStyles = `
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
    width: 12px;
    height: 12px;
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
.card-box:hover .mpv-container .mpv-play-button,
.video-card:hover .mpv-container .mpv-play-button {
    opacity: 1;
}`;
// Function to inject styles
function injectStyles() {
    // Inject to main document
    const mainStyle = document.createElement('style');
    mainStyle.textContent = mpvStyles;
    document.head.appendChild(mainStyle);

    // Inject to Shadow DOM if available
    const bewly = document.querySelector('#bewly');
    if (bewly && bewly.shadowRoot) {
        const shadowStyle = document.createElement('style');
        shadowStyle.textContent = mpvStyles;
        bewly.shadowRoot.appendChild(shadowStyle);
    }

    // Watch for Shadow Root changes
    const styleObserver = new MutationObserver(() => {
        const bewly = document.querySelector('#bewly');
        if (bewly && bewly.shadowRoot && !bewly.shadowRoot.querySelector('style')) {
            const shadowStyle = document.createElement('style');
            shadowStyle.textContent = mpvStyles;
            bewly.shadowRoot.appendChild(shadowStyle);
        }
    });

    styleObserver.observe(document.body, {
        childList: true,
        subtree: true
    });
}

// Inject styles
injectStyles();

// Function to add MPV button to a video thumbnail
function addMpvButton(container) {
    if (container.querySelector('.mpv-container')) return;

    // Find the video link - handle container being the <a> element itself and check for shadow root
    const videoLink = container.matches('a[href]') ? container :
        (container.shadowRoot?.querySelector('a[href]') || container.querySelector('a[href]'));
    if (!videoLink) return;

    // Get full URL for relative paths
    const href = new URL(videoLink.href, window.location.href).href;
    if (!href) return;

    const videoPattern = /\/video\/(BV\w+)/i;
    const livePattern = /live.bilibili.com\/(\d+)/i;
    if (!href.match(videoPattern) && !href.match(livePattern)) return;

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

// Function to get elements from Shadow DOM
function queryAllShadowHosts(root, selector) {
    const elements = [];
    const shadowHost = document.querySelector('#bewly');

    if (shadowHost && shadowHost.shadowRoot) {
        // Search in the bewly shadow root
        elements.push(...shadowHost.shadowRoot.querySelectorAll(selector));
    }

    // Also search in regular DOM as fallback
    elements.push(...document.querySelectorAll(selector));

    return elements;
}

// Function to observe DOM changes for dynamically loaded content
function observeVideoThumbnails() {
    // Process existing thumbnails
    const selectors = [
        '.bili-video-card',
        '.card-box',
        '.video-card'
    ];

    selectors.forEach(selector => {
        queryAllShadowHosts(document, selector).forEach(el => {
            addMpvButton(el);
        });
    });

    // Create observers
    const shadowRootObserver = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            mutation.addedNodes.forEach((node) => {
                if (node.nodeType === 1) { // Element node
                    selectors.forEach(selector => {
                        if (node.matches?.(selector)) {
                            addMpvButton(node);
                        }
                        // Check within the added node
                        node.querySelectorAll(selector).forEach(el => {
                            addMpvButton(el);
                        });
                    });
                }
            });
        });
    });

    // Observe both regular DOM and Shadow DOM
    const bewlyElement = document.querySelector('#bewly');
    if (bewlyElement && bewlyElement.shadowRoot) {
        shadowRootObserver.observe(bewlyElement.shadowRoot, {
            childList: true,
            subtree: true
        });
    }

    // Also observe regular DOM as fallback
    shadowRootObserver.observe(document.body, {
        childList: true,
        subtree: true
    });

    // Watch for shadow root attachment
    const rootObserver = new MutationObserver(() => {
        const bewly = document.querySelector('#bewly');
        if (bewly && bewly.shadowRoot) {
            shadowRootObserver.observe(bewly.shadowRoot, {
                childList: true,
                subtree: true
            });
            // Process any existing elements in the shadow root
            selectors.forEach(selector => {
                bewly.shadowRoot.querySelectorAll(selector).forEach(el => {
                    addMpvButton(el);
                });
            });
        }
    });

    // Observe for shadow root attachment
    rootObserver.observe(document.body, {
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
