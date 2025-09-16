/**
 * ToastMaker - A customizable toast notification system with sound effects
 * @version 1.0.0
 * @license MIT
 */

const ToastMaker = (() => {
    // Default configuration
    const defaultConfig = {
        position: 'top-right',
        duration: 5000,
        closeable: true,
        showProgress: true,
        maxToasts: 3,
        sounds: {
            info: 'https://assets.mixkit.co/active_storage/sfx/2867/2867-preview.mp3',
            success: 'https://assets.mixkit.co/active_storage/sfx/2866/2866-preview.mp3',
            warning: 'https://assets.mixkit.co/active_storage/sfx/2867/2867-preview.mp3',
            error: 'https://assets.mixkit.co/active_storage/sfx/2863/2863-preview.mp3'
        }
    };

    let config = { ...defaultConfig };
    let toastQueue = [];
    let activeToasts = 0;
    let audioContext = null;

    // Initialize audio context on user interaction
    const initAudio = () => {
        if (!audioContext) {
            audioContext = new (window.AudioContext || window.webkitAudioContext)();
        }
    };

    // Play sound for toast type
    const playSound = async (type) => {
        if (!config.sounds[type]) return;

        try {
            initAudio();
            const response = await fetch(config.sounds[type]);
            const arrayBuffer = await response.arrayBuffer();
            const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
            const source = audioContext.createBufferSource();
            source.buffer = audioBuffer;
            source.connect(audioContext.destination);
            source.start();
            console.log("Sound played");
            audioContext.resume();
        } catch (error) {
            console.warn('Failed to play sound:', error);
        }
    };

    // Create toast element
    const createToast = (title, content, options = {}) => {
        const toastId = 'toast-' + Date.now();
        const type = options.type || 'info';
        const duration = options.duration || config.duration;
        const closeable = options.closeable !== undefined ? options.closeable : config.closeable;
        const buttons = options.buttons || [];

        const toastElement = document.createElement('div');
        toastElement.id = toastId;
        toastElement.className = `toast toast-${type} ${config.position} transition-all duration-300 transform translate-x-0 opacity-100`;
        
        // Add role and aria attributes for accessibility
        toastElement.setAttribute('role', 'alert');
        toastElement.setAttribute('aria-live', 'assertive');
        toastElement.setAttribute('aria-atomic', 'true');

        // Toast header
        const header = document.createElement('div');
        header.className = 'toast-header flex items-center justify-between p-3 border-b';
        
        const titleElement = document.createElement('div');
        titleElement.className = 'toast-title font-semibold flex items-center';
        
        // Add icon based on type
        const icons = {
            info: 'info-circle',
            success: 'check-circle',
            warning: 'exclamation-triangle',
            error: 'exclamation-circle'
        };
        
        const icon = document.createElement('i');
        icon.className = `fas fa-${icons[type] || 'info-circle'} mr-2`;
        titleElement.appendChild(icon);
        titleElement.appendChild(document.createTextNode(title));
        
        header.appendChild(titleElement);

        // Close button
        if (closeable) {
            const closeButton = document.createElement('button');
            closeButton.className = 'toast-close text-gray-500 hover:text-gray-700';
            closeButton.innerHTML = '&times;';
            closeButton.setAttribute('aria-label', 'Fechar notificação');
            closeButton.onclick = () => removeToast(toastId);
            header.appendChild(closeButton);
        }

        // Toast body
        const body = document.createElement('div');
        body.className = 'toast-body p-4';
        body.textContent = content;

        // Toast footer (for buttons)
        let footer = null;
        if (buttons.length > 0) {
            footer = document.createElement('div');
            footer.className = 'toast-footer p-3 border-t flex justify-end space-x-2';
            
            buttons.forEach(btn => {
                const button = document.createElement('button');
                button.className = `px-3 py-1 text-sm rounded ${btn.className || 'bg-blue-500 text-white hover:bg-blue-600'}`;
                button.textContent = btn.text;
                button.onclick = (e) => {
                    if (typeof btn.onClick === 'function') {
                        btn.onClick(e, { close: () => removeToast(toastId) });
                    }
                };
                footer.appendChild(button);
            });
        }

        // Progress bar
        let progressBar = null;
        if (config.showProgress && duration > 0) {
            progressBar = document.createElement('div');
            progressBar.className = 'toast-progress h-1 bg-opacity-30 bg-gray-400';
            progressBar.style.width = '100%';
            progressBar.style.transition = `width ${duration}ms linear`;
        }

        // Assemble toast
        toastElement.appendChild(header);
        toastElement.appendChild(body);
        if (footer) toastElement.appendChild(footer);
        if (progressBar) toastElement.appendChild(progressBar);

        // Add to container
        const container = getToastContainer();
        container.appendChild(toastElement);

        // Animate in
        requestAnimationFrame(() => {
            toastElement.classList.add('show');
        });

        // Start progress bar
        if (progressBar) {
            requestAnimationFrame(() => {
                progressBar.style.width = '0%';
            });
        }

        // Auto-dismiss if duration is set
        let timeoutId;
        if (duration > 0) {
            timeoutId = setTimeout(() => {
                removeToast(toastId);
            }, duration);
        }

        // Play sound
        if (config.sounds[type] && !options.silent) {
            playSound(type);
        }

        return {
            id: toastId,
            element: toastElement,
            dismiss: () => removeToast(toastId),
            update: (newContent) => {
                if (newContent.title) titleElement.textContent = newContent.title;
                if (newContent.content) body.textContent = newContent.content;
                if (timeoutId) {
                    clearTimeout(timeoutId);
                    if (duration > 0) {
                        timeoutId = setTimeout(() => {
                            removeToast(toastId);
                        }, duration);
                    }
                }
            }
        };
    };

    // Remove toast with animation
    const removeToast = (toastId) => {
        const toast = document.getElementById(toastId);
        if (!toast) return;

        toast.classList.add('hide');
        setTimeout(() => {
            toast.remove();
            activeToasts--;
            processQueue();
        }, 300);
    };

    // Process toast queue
    const processQueue = () => {
        if (toastQueue.length === 0 || activeToasts >= config.maxToasts) return;
        
        const { title, content, options, resolve } = toastQueue.shift();
        const toast = createToast(title, content, options);
        activeToasts++;
        
        if (resolve) {
            resolve(toast);
        }
    };

    // Get or create toast container
    const getToastContainer = () => {
        let container = document.querySelector('.toast-container');
        if (!container) {
            container = document.createElement('div');
            container.className = `toast-container fixed z-50 flex flex-col space-y-3 ${getPositionClasses()}`;
            document.body.appendChild(container);
        }
        return container;
    };

    // Get position classes based on config
    const getPositionClasses = () => {
        const positions = {
            'top-right': 'top-4 right-4',
            'top-left': 'top-4 left-4',
            'bottom-right': 'bottom-4 right-4',
            'bottom-left': 'bottom-4 left-4',
            'top-center': 'top-4 left-1/2 transform -translate-x-1/2',
            'bottom-center': 'bottom-4 left-1/2 transform -translate-x-1/2'
        };
        return positions[config.position] || positions['top-right'];
    };

    // Public API
    return {
        /**
         * Configure ToastMaker
         * @param {Object} newConfig - Configuration object
         */
        config: (newConfig) => {
            config = { ...config, ...newConfig };
        },

        /**
         * Show a toast notification
         * @param {string} title - Toast title
         * @param {string} content - Toast content
         * @param {Object} options - Toast options
         * @returns {Promise} Resolves with toast instance when shown
         */
        toast: (title, content, options = {}) => {
            return new Promise((resolve) => {
                toastQueue.push({ title, content, options, resolve });
                if (activeToasts < config.maxToasts) {
                    processQueue();
                }
            });
        },

        /**
         * Show an info toast
         * @param {string} title - Toast title
         * @param {string} content - Toast content
         * @param {Object} options - Additional options
         * @returns {Promise} Resolves with toast instance
         */
        info: (title, content, options = {}) => {
            return this.toast(title, content, { ...options, type: 'info' });
        },

        /**
         * Show a success toast
         * @param {string} title - Toast title
         * @param {string} content - Toast content
         * @param {Object} options - Additional options
         * @returns {Promise} Resolves with toast instance
         */
        success: (title, content, options = {}) => {
            return this.toast(title, content, { ...options, type: 'success' });
        },

        /**
         * Show a warning toast
         * @param {string} title - Toast title
         * @param {string} content - Toast content
         * @param {Object} options - Additional options
         * @returns {Promise} Resolves with toast instance
         */
        warning: (title, content, options = {}) => {
            return this.toast(title, content, { ...options, type: 'warning' });
        },

        /**
         * Show an error toast
         * @param {string} title - Toast title
         * @param {string} content - Toast content
         * @param {Object} options - Additional options
         * @returns {Promise} Resolves with toast instance
         */
        error: (title, content, options = {}) => {
            return this.toast(title, content, { ...options, type: 'error' });
        },

        /**
         * Clear all toasts
         */
        clearAll: () => {
            document.querySelectorAll('.toast').forEach(toast => {
                toast.remove();
            });
            activeToasts = 0;
            toastQueue = [];
        }
    };
})();

// Add styles if not already added
if (!document.getElementById('toast-maker-styles')) {
    const style = document.createElement('style');
    style.id = 'toast-maker-styles';
    style.textContent = `
        .toast {
            min-width: 300px;
            max-width: 400px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            overflow: hidden;
            margin-bottom: 12px;
            opacity: 0;
            transform: translateY(20px);
            transition: opacity 0.3s, transform 0.3s;
        }

        .toast.show {
            opacity: 1;
            transform: translateY(0);
        }

        .toast.hide {
            opacity: 0;
            transform: translateY(-20px);
        }

        .toast-info {
            border-left: 4px solid var(--blue);
        }

        .toast-success {
            border-left: 4px solid var(--green);
        }

        .toast-warning {
            border-left: 4px solid var(--orange);
        }

        .toast-error {
            border-left: 4px solid var(--sos_red);
        }

        .toast-close {
            background: none;
            border: none;
            font-size: 1.5rem;
            line-height: 1;
            cursor: pointer;
            padding: 0.25rem;
            margin-left: 1rem;
        }

        @media (max-width: 640px) {
            .toast {
                min-width: 280px;
                max-width: 90%;
                margin: 0 auto 12px;
            }
            
            .toast-container {
                width: 100%;
                padding: 0 1rem;
            }
            
            .toast-container.top-right,
            .toast-container.top-left,
            .toast-container.top-center {
                top: 1rem;
            }
            
            .toast-container.bottom-right,
            .toast-container.bottom-left,
            .toast-container.bottom-center {
                bottom: 1rem;
            }
        }
    `;
    document.head.appendChild(style);
}

// Export for different module systems
if (typeof module !== 'undefined' && typeof module.exports !== 'undefined') {
    module.exports = ToastMaker;
} else if (typeof define === 'function' && define.amd) {
    define([], () => ToastMaker);
} else {
    window.ToastMaker = ToastMaker;
}