// static/js/blog.js
// Blog-specific interactivity: reading progress bar + smooth-scroll to comments.

document.addEventListener('DOMContentLoaded', () => {

    // ── 1. Reading Progress Bar ───────────────────────────────────────────────
    const progressBar = document.getElementById('reading-progress-bar');

    if (progressBar) {
        const updateProgress = () => {
            const scrollTop  = window.scrollY || document.documentElement.scrollTop;
            const docHeight  = document.documentElement.scrollHeight - window.innerHeight;
            const progress   = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
            progressBar.style.width = Math.min(progress, 100).toFixed(2) + '%';
        };

        // Passive listener for better scroll performance
        window.addEventListener('scroll', updateProgress, { passive: true });
        // Run once on load in case the page is already scrolled
        updateProgress();
    }

    // ── 2. Smooth Scroll to Comments ─────────────────────────────────────────
    // Intercepts any <a href="#comments"> links and animates the scroll.
    document.querySelectorAll('a[href="#comments"]').forEach(link => {
        link.addEventListener('click', e => {
            const target = document.getElementById('comments');
            if (!target) return;
            e.preventDefault();
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            // Update URL hash without jumping
            history.pushState(null, '', '#comments');
        });
    });

    // ── 3. Copy-link button feedback ─────────────────────────────────────────
    // Provides a brief "Copied!" tooltip after the clipboard write.
    const copyBtn = document.getElementById('copy-link-btn');
    if (copyBtn) {
        copyBtn.addEventListener('click', async () => {
            try {
                await navigator.clipboard.writeText(window.location.href);
                const original = copyBtn.innerHTML;
                copyBtn.innerHTML = `
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                    </svg>
                    کپی شد!
                `;
                copyBtn.classList.add('bg-emerald-100', 'text-emerald-700');
                setTimeout(() => {
                    copyBtn.innerHTML = original;
                    copyBtn.classList.remove('bg-emerald-100', 'text-emerald-700');
                }, 2200);
            } catch {
                // Silently fail if clipboard API is not available
            }
        });
    }

});
