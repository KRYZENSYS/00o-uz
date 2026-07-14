// 00o.uz global utilities
window.toast = window.toast || {
  success: (m, e) => console.log('✓', m, e),
  error: (m, e) => console.log('✗', m, e),
  info: (m, e) => console.log('ℹ', m, e)
};
window.confetti = window.confetti || function(){};

// PWA install
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js').catch(() => {});
  });
}

// Theme detection
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
document.documentElement.style.colorScheme = 'dark';
