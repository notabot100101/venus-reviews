/**
 * VENABLE REVIEWS Theme Switcher
 * Enables previewing and switching between dark themes
 */

(function() {
  'use strict';

  // Theme definitions
  const themes = {
    'default': {
      name: 'Light Theme',
      description: 'Original light theme with deep purple accents',
      cssFile: null,
      icon: '☀️'
    },
    'dark-blue': {
      name: 'Dark Blue',
      description: 'Deep charcoal with electric blue and cyan accents',
      cssFile: '/static/css/theme-dark-blue.css',
      icon: '🔵'
    },
    'dark-rose': {
      name: 'Dark Rose',
      description: 'Soft charcoal with rose pink, magenta and purple accents',
      cssFile: '/static/css/theme-dark-rose.css',
      icon: '🌸'
    },
    'dark-green': {
      name: 'Dark Green',
      description: 'Deep forest with neon green and emerald accents',
      cssFile: '/static/css/theme-dark-green.css',
      icon: '🟢'
    }
  };

  // Load order (CSS files that define the theme)
  // Must be loaded after main.css to override variables
  const themeOrder = ['default', 'dark-blue', 'dark-rose', 'dark-green'];

  // Elements to cache
  let switcherButton = null;
  let currentThemeIndex = -1;

  // Initialize
  function init() {
    createSwitcherButton();
    setupThemeSelector();
  }

  // Create theme switcher button
  function createSwitcherButton() {
    switcherButton = document.createElement('div');
    switcherButton.id = 'theme-switcher';
    switcherButton.innerHTML = `
      <button type="button" class="theme-switcher-btn" aria-label="Toggle theme preview">
        <span class="theme-switcher-icon">🎨</span>
        <span class="theme-switcher-tooltip">Preview Theme</span>
      </button>
    `;

    const btn = switcherButton.querySelector('.theme-switcher-btn');
    btn.addEventListener('click', toggleThemePreview);

    document.body.appendChild(switcherButton);

    // Check for existing theme preference
    const savedTheme = localStorage.getItem('venus_theme') || 'default';
    selectTheme(savedTheme, false); // false = don't show animation
  }

  // Toggle theme preview
  function toggleThemePreview() {
    // Cycle through themes
    let nextIndex = (currentThemeIndex + 1) % themeOrder.length;
    selectTheme(themeOrder[nextIndex].name, true);
  }

  // Select specific theme
  function selectTheme(themeName, animate) {
    currentThemeIndex = themeOrder.findIndex(t => t.name === themeName);
    localStorage.setItem('venus_theme', themeName);

    const theme = themes[themeName];
    const switcher = document.getElementById('theme-switcher');

    if (theme.cssFile && animate) {
      // Load and apply theme CSS
      const link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = theme.cssFile;
      link.id = 'venus-theme-css';
      document.head.appendChild(link);

      // Animate tooltip
      const tooltip = switcher.querySelector('.theme-switcher-tooltip');
      tooltip.textContent = `${theme.icon} ${theme.name}`;
      tooltip.style.opacity = '1';
      setTimeout(() => {
        tooltip.style.opacity = '0';
      }, 1500);
    } else if (theme.cssFile) {
      // Keep the CSS link for future activation
      let link = document.getElementById('venus-theme-css');
      if (!link) {
        link = document.createElement('link');
        link.rel = 'stylesheet';
        link.id = 'venus-theme-css';
        document.head.appendChild(link);
      }
    } else {
      // Default theme - remove theme CSS
      const link = document.getElementById('venus-theme-css');
      if (link) {
        link.remove();
      }

      const tooltip = switcher.querySelector('.theme-switcher-tooltip');
      tooltip.textContent = '☀️ Light';
      tooltip.style.opacity = '1';
      setTimeout(() => {
        tooltip.style.opacity = '0';
      }, 1500);
    }
  }

  // Setup theme selector dropdown (optional advanced feature)
  function setupThemeSelector() {
    // Create dropdown menu
    const menu = document.createElement('div');
    menu.id = 'theme-selector-menu';
    menu.className = 'theme-selector-menu';
    menu.innerHTML = `
      <h4 class="theme-selector-title">Choose Theme</h4>
      <div class="theme-options">
        <button class="theme-option-btn" data-theme="default" aria-label="${themes['default'].name}">
          <span class="theme-option-icon">☀️</span>
          <span class="theme-option-name">${themes['default'].name}</span>
        </button>
        <button class="theme-option-btn" data-theme="dark-blue" aria-label="${themes['dark-blue'].name}">
          <span class="theme-option-icon">🔵</span>
          <span class="theme-option-name">${themes['dark-blue'].name}</span>
        </button>
        <button class="theme-option-btn" data-theme="dark-rose" aria-label="${themes['dark-rose'].name}">
          <span class="theme-option-icon">🌸</span>
          <span class="theme-option-name">${themes['dark-rose'].name}</span>
        </button>
        <button class="theme-option-btn" data-theme="dark-green" aria-label="${themes['dark-green'].name}">
          <span class="theme-option-icon">🟢</span>
          <span class="theme-option-name">${themes['dark-green'].name}</span>
        </button>
      </div>
      <p class="theme-selector-info">${themes['default'].description}</p>
    `;

    const title = menu.querySelector('.theme-selector-title');
    const options = menu.querySelector('.theme-options');
    const info = menu.querySelector('.theme-selector-info');

    // Attach click handlers
    options.querySelectorAll('.theme-option-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const themeName = e.target.dataset.theme;
        selectTheme(themeName, true);

        // Close dropdown
        document.getElementById('theme-selector-menu').classList.add('hidden');
      });
    });

    // Store menu for later
    themeSelectorMenu = menu;
  }

  // Let theme selector be created when the page loads
  let themeSelectorMenu = null;
  setTimeout(() => {
    if (!document.getElementById('theme-selector-menu')) {
      setupThemeSelector();
    }
  }, 100);

  // Style for theme switcher (inject into page)
  const style = document.createElement('style');
  style.textContent = `
    #theme-switcher {
      position: fixed;
      bottom: 20px;
      right: 20px;
      z-index: 9999;
      font-family: 'Lato', sans-serif;
    }

    .theme-switcher-btn {
      width: 56px;
      height: 56px;
      border-radius: 50%;
      background: linear-gradient(135deg, #6B2C91 0%, #4a1d6b 100%);
      border: none;
      cursor: pointer;
      box-shadow: 0 4px 12px rgba(107, 44, 145, 0.3);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24px;
      transition: all 0.3s ease;
      margin: 0;
      padding: 0;
    }

    .theme-switcher-btn:hover {
      transform: scale(1.1) rotate(10deg);
      box-shadow: 0 6px 16px rgba(107, 44, 145, 0.4);
    }

    .theme-switcher-tooltip {
      position: absolute;
      bottom: 60px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(0, 0, 0, 0.9);
      color: white;
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 12px;
      white-space: nowrap;
      opacity: 0;
      transition: opacity 0.3s ease;
      pointer-events: none;
      min-width: 120px;
      text-align: center;
    }

    .theme-selector-menu {
      position: absolute;
      bottom: 70px;
      right: 0;
      background: #1a1a1a;
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 12px;
      padding: 16px;
      width: 260px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
      display: none;
      animation: slideUp 0.2s ease;
    }

    .theme-selector-menu.hidden {
      display: none;
    }

    .theme-selector-menu:not(.hidden) {
      display: block;
    }

    @keyframes slideUp {
      from {
        opacity: 0;
        transform: translateY(10px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }

    .theme-selector-title {
      margin: 0 0 12px 0;
      font-size: 14px;
      font-weight: 600;
      color: #fff;
    }

    .theme-options {
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    .theme-option-btn {
      display: flex;
      align-items: center;
      gap: 10px;
      width: 100%;
      padding: 10px 14px;
      border: none;
      border-radius: 8px;
      background: rgba(255, 255, 255, 0.05);
      color: #e0e0e0;
      font-size: 13px;
      cursor: pointer;
      transition: all 0.2s ease;
      text-align: left;
    }

    .theme-option-btn:hover {
      background: rgba(255, 255, 255, 0.15);
      transform: translateX(4px);
    }

    .theme-option-btn:active {
      background: rgba(255, 255, 255, 0.1);
      transform: translateX(2px);
    }

    .theme-option-icon {
      font-size: 18px;
    }

    .theme-selector-info {
      margin-top: 12px;
      padding-top: 10px;
      border-top: 1px solid rgba(255, 255, 255, 0.1);
      font-size: 11px;
      color: #888;
      line-height: 1.5;
    }

    /* Click outside to close */
    .theme-switcher-click-outside {
      display: none;
    }
  `;
  document.head.appendChild(style);

  // Close dropdown when clicking outside
  document.addEventListener('click', (e) => {
    const switcher = document.getElementById('theme-switcher');
    const menu = document.getElementById('theme-selector-menu');
    if (switcher && menu && !switcher.contains(e.target) && !menu.contains(e.target)) {
      menu.classList.add('hidden');
    }
  });

})();
