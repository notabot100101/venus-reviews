/**
 * Venus Reviews Theme Switcher
 *
 * Rebuilt 2026-07-21 - the previous version never actually worked: it called
 * applyTheme() before createToggleButton() existed, so applyTheme()'s own
 * reference to the (still-null) toggle button threw an uncaught exception on
 * every page load, which aborted execution before the button was ever
 * created or the theme CSS ever actually swapped (confirmed live: body class
 * changed but the toggle button never appeared in the DOM and the CSS link
 * never changed from whatever was hardcoded in baseof.html).
 *
 * Only 6 of the site's 9 theme CSS files are wired in here. The other 3
 * (theme-light.css, theme-blue-purple.css, theme-rose-gold.css) use two
 * DIFFERENT, mutually incompatible scoping mechanisms (body.theme-light
 * class-scoped overrides, and [data-theme="..."] attribute selectors) that
 * this switcher's mechanism - swapping which <link> is loaded, relying on
 * main.css's own selectors reading the swapped :root --color-* variables -
 * does not support. Rather than ship a half-working picker with 3 dead
 * entries, those 3 are left out until someone rewrites them onto the same
 * --color-* :root convention as the other 6.
 */
(function() {
  'use strict';

  const THEMES = [
    { id: 'dark-blue', name: 'Dark Blue', css: '/css/theme-dark-blue.css', swatch: '#0066ff' },
    { id: 'dark-rose', name: 'Dark Rose', css: '/css/theme-dark-rose.css', swatch: '#ff6b9d' },
    { id: 'dark-green', name: 'Dark Green', css: '/css/theme-dark-green.css', swatch: '#39ff14' },
    { id: 'neon-cyber', name: 'Neon Cyber', css: '/css/theme-neon-cyber.css', swatch: '#39ff14' },
    { id: 'deep-violet', name: 'Deep Violet', css: '/css/theme-deep-violet.css', swatch: '#8b5cf6' },
    { id: 'midnight-gold', name: 'Midnight Gold', css: '/css/theme-midnight-gold.css', swatch: '#fbbf24' },
  ];

  const STORAGE_KEY = 'venus-theme-preference';
  const DEFAULT_THEME = 'dark-blue';
  const THEME_LINK_ID = 'venus-theme-css';

  let panelOpen = false;

  function currentThemeId() {
    return localStorage.getItem(STORAGE_KEY) || DEFAULT_THEME;
  }

  function applyTheme(themeId) {
    const theme = THEMES.find(t => t.id === themeId) || THEMES[0];
    localStorage.setItem(STORAGE_KEY, theme.id);

    let link = document.getElementById(THEME_LINK_ID);
    if (!link) {
      link = document.createElement('link');
      link.id = THEME_LINK_ID;
      link.rel = 'stylesheet';
      document.head.appendChild(link);
    }
    link.href = theme.css;

    document.body.classList.add('theme-transition');
    updateSwatchSelection(theme.id);
  }

  function updateSwatchSelection(themeId) {
    document.querySelectorAll('.venus-theme-swatch').forEach(el => {
      el.setAttribute('aria-pressed', el.dataset.themeId === themeId ? 'true' : 'false');
    });
  }

  function buildPanel() {
    const panel = document.createElement('div');
    panel.id = 'venus-theme-panel';
    panel.className = 'venus-theme-panel';
    panel.setAttribute('role', 'menu');
    panel.hidden = true;

    THEMES.forEach(theme => {
      const swatch = document.createElement('button');
      swatch.type = 'button';
      swatch.className = 'venus-theme-swatch';
      swatch.dataset.themeId = theme.id;
      swatch.title = theme.name;
      swatch.setAttribute('aria-label', `Switch to ${theme.name} theme`);
      swatch.setAttribute('role', 'menuitemradio');
      swatch.style.setProperty('--swatch-color', theme.swatch);
      swatch.addEventListener('click', () => {
        applyTheme(theme.id);
        closePanel();
      });
      panel.appendChild(swatch);
    });

    return panel;
  }

  function openPanel() {
    const panel = document.getElementById('venus-theme-panel');
    const button = document.getElementById('venus-theme-toggle');
    if (!panel || !button) return;
    panel.hidden = false;
    button.setAttribute('aria-expanded', 'true');
    panelOpen = true;
  }

  function closePanel() {
    const panel = document.getElementById('venus-theme-panel');
    const button = document.getElementById('venus-theme-toggle');
    if (!panel || !button) return;
    panel.hidden = true;
    button.setAttribute('aria-expanded', 'false');
    panelOpen = false;
  }

  function togglePanel() {
    if (panelOpen) closePanel(); else openPanel();
  }

  function buildToggleButton() {
    const button = document.createElement('button');
    button.id = 'venus-theme-toggle';
    button.type = 'button';
    button.className = 'venus-theme-toggle-btn';
    button.setAttribute('aria-label', 'Choose color theme');
    button.setAttribute('aria-expanded', 'false');
    button.setAttribute('aria-haspopup', 'true');
    button.textContent = '\u{1F3A8}'; // 🎨
    button.addEventListener('click', (event) => {
      event.stopPropagation();
      togglePanel();
    });
    return button;
  }

  function init() {
    // Apply the saved/default theme first - this only swaps a <link>, no
    // dependency on the toggle button existing.
    applyTheme(currentThemeId());

    const wrapper = document.createElement('div');
    wrapper.id = 'venus-theme-switcher';
    wrapper.appendChild(buildToggleButton());
    wrapper.appendChild(buildPanel());

    const footer = document.querySelector('footer');
    if (footer && footer.parentNode) {
      footer.parentNode.insertBefore(wrapper, footer);
    } else {
      document.body.appendChild(wrapper);
    }

    updateSwatchSelection(currentThemeId());

    document.addEventListener('click', (event) => {
      const switcher = document.getElementById('venus-theme-switcher');
      if (panelOpen && switcher && !switcher.contains(event.target)) {
        closePanel();
      }
    });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && panelOpen) closePanel();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
