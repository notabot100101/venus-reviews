(function() {
  'use strict';

  // Theme definitions with color swatches
  const themes = {
    'dark-rose': {
      name: 'Dark Rose',
      primary: '#ff6b9d',
      secondary: '#e91e63',
      accent: '#fdf2f7',
      preview: [
        '#ff6b9d',
        '#e91e63',
        '#9c27b0',
        '#1e1b2e'
      ]
    },
    'dark-blue': {
      name: 'Dark Blue',
      primary: '#0066ff',
      secondary: '#00bcd4',
      accent: '#e8f4f8',
      preview: [
        '#0066ff',
        '#00bcd4',
        '#00bcd4',
        '#1a1a2e'
      ]
    },
    'dark-green': {
      name: 'Dark Green',
      primary: '#39ff14',
      secondary: '#00e676',
      accent: '#1a2a1a',
      preview: [
        '#39ff14',
        '#00e676',
        '#00e676',
        '#0d1f0d'
      ]
    },
    'light': {
      name: 'Light',
      primary: '#3b82f6',
      secondary: '#60a5fa',
      accent: '#f0f9ff',
      preview: [
        '#3b82f6',
        '#60a5fa',
        '#3b82f6',
        '#ffffff'
      ]
    },
    'midnight-gold': {
      name: 'Midnight Gold',
      primary: '#fbbf24',
      secondary: '#f59e0b',
      accent: '#fef3c7',
      preview: [
        '#fbbf24',
        '#f59e0b',
        '#b45309',
        '#0f172a'
      ]
    },
    'neon-cyber': {
      name: 'Neon Cyber',
      primary: '#39ff14',
      secondary: '#00f5ff',
      accent: '#ff10f0',
      preview: [
        '#39ff14',
        '#00f5ff',
        '#ff10f0',
        '#0a0a0f'
      ]
    },
    'deep-violet': {
      name: 'Deep Violet',
      primary: '#8b5cf6',
      secondary: '#ec4899',
      accent: '#e0e7ff',
      preview: [
        '#8b5cf6',
        '#ec4899',
        '#db2777',
        '#1e1b4b'
      ]
    }
  };

  let currentTheme = localStorage.getItem('venus-theme') || 'dark-rose';

  // Create theme picker button
  function createPickerButton() {
    const button = document.createElement('button');
    button.id = 'venus-theme-picker';
    button.setAttribute('aria-label', 'Open theme picker');
    button.className = 'venus-theme-picker-button';
    button.innerHTML = `
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
        <circle cx="12" cy="12" r="2" fill="currentColor"/>
        <circle cx="6" cy="6" r="2" fill="currentColor" opacity="0.6"/>
        <circle cx="18" cy="18" r="2" fill="currentColor" opacity="0.6"/>
      </svg>
    `;
    button.style.cssText = `
      position: fixed;
      bottom: 30px;
      right: 30px;
      width: 56px;
      height: 56px;
      border-radius: 50%;
      background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-secondary) 100%);
      border: none;
      cursor: pointer;
      box-shadow: 0 4px 15px rgba(0,0,0,0.3);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 18px;
      color: white;
      z-index: 9999;
      transition: transform 0.3s ease, box-shadow 0.3s ease;
    `;

    // Add hover effect with ring animation
    button.addEventListener('mouseenter', () => {
      button.style.transform = 'scale(1.05) rotate(-5deg)';
      button.style.boxShadow = '0 6px 25px rgba(var(--color-primary), 0.4)';
    });

    button.addEventListener('mouseleave', () => {
      button.style.transform = 'scale(1) rotate(0deg)';
      button.style.boxShadow = '0 4px 15px rgba(0,0,0,0.3)';
    });

    button.addEventListener('click', () => {
      togglePickerPanel();
    });

    return button;
  }

  // Create picker panel
  function createPickerPanel() {
    const panel = document.createElement('div');
    panel.id = 'venus-theme-picker-panel';
    panel.className = 'venus-theme-picker-panel';
    panel.style.cssText = `
      position: fixed;
      bottom: 100px;
      right: 30px;
      width: 320px;
      background: rgba(15, 23, 42, 0.95);
      backdrop-filter: blur(20px);
      border-radius: 16px;
      padding: 16px;
      box-shadow: 0 8px 30px rgba(0,0,0,0.4);
      border: 1px solid rgba(255,255,255,0.1);
      display: none;
      z-index: 9998;
      animation: fadeIn 0.2s ease;
    `;

    panel.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
        <h3 style="margin: 0; font-size: 1.1rem; color: var(--color-text); font-weight: 600;">
          Theme Picker
        </h3>
        <button id="venus-picker-close" 
          style="background: none; border: none; color: var(--color-text-light); cursor: pointer; font-size: 1.25rem; padding: 4px; line-height: 1;">
          ✕
        </button>
      </div>
      <div id="venus-picker-items" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px;">
        <!-- Theme items will be inserted here -->
      </div>
    `;

    return panel;
  }

  // Create theme item
  function createThemeItem(themeKey) {
    const theme = themes[themeKey];
    const item = document.createElement('div');
    item.className = 'venus-theme-item';
    item.setAttribute('data-theme', themeKey);
    item.setAttribute('role', 'button');
    item.tabIndex = 0;
    item.setAttribute('aria-label', theme.name);

    item.innerHTML = `
      <div style="display: flex; flex-direction: column; align-items: center; gap: 6px; cursor: pointer; border-radius: 8px; padding: 8px; transition: all 0.2s ease;">
        <div style="position: relative; width: 36px; height: 36px; margin-bottom: 4px;">
          <!-- Gradient circle -->
          <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border-radius: 50%; 
            background: conic-gradient(
              from 0deg,
              ${theme.preview.map((color, i) => 
                `${color} ${(i * (360 / theme.preview.length))}, ` +
                `${color} ${((i + 1) * (360 / theme.preview.length)) - (360 / theme.preview.length / 2)}deg`
              ).join(', ')}
            );
            background: radial-gradient(circle at 30% 30%, ${theme.preview[0]}, ${theme.preview[1]}, ${theme.preview[2]}, ${theme.preview[3]});
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            border: 2px solid rgba(255,255,255,0.15);
          "></div>
          <!-- Active indicator -->
          <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
            width: 12px; height: 12px; border-radius: 50%; border: 2px solid white;
            background: rgba(255,255,255,0); transition: all 0.2s ease;"></div>
        </div>
        <span style="font-size: 0.75rem; text-align: center; color: var(--color-text); line-height: 1.2;
          text-shadow: 0 1px 2px rgba(0,0,0,0.8);">${theme.name}</span>
      </div>
    `;

    item.addEventListener('click', (e) => {
      e.stopPropagation();
      applyTheme(themeKey);
    });

    // Keyboard navigation
    item.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        applyTheme(themeKey);
      }
    });

    return item;
  }

  // Apply theme
  function applyTheme(themeKey) {
    document.documentElement.style.setProperty('--color-primary', themes[themeKey].primary);
    document.documentElement.style.setProperty('--color-secondary', themes[themeKey].secondary);
    document.documentElement.style.setProperty('--color-accent', themes[themeKey].accent);
    
    // Apply full theme CSS file
    const themeUrl = `/static/css/theme-${themeKey}.css`;
    const existingTheme = document.querySelector(`link[href="${themeUrl}"]`);
    
    if (existingTheme) {
      existingTheme.setAttribute('rel', 'stylesheet');
    }
    
    localStorage.setItem('venus-theme', themeKey);
    currentTheme = themeKey;
    
    // Update button color
    const button = document.getElementById('venus-theme-picker');
    if (button) {
      const gradient = `linear-gradient(135deg, ${themes[themeKey].primary} 0%, ${themes[themeKey].secondary} 100%)`;
      button.style.background = gradient;
    }
    
    // Close panel
    togglePickerPanel(false);
  }

  // Toggle picker panel
  function togglePickerPanel(forceShow = null) {
    const panel = document.getElementById('venus-theme-picker-panel');
    const button = document.getElementById('venus-theme-picker');
    
    if (forceShow !== null) {
      if (forceShow) {
        panel.style.display = 'block';
        button.setAttribute('aria-expanded', 'true');
      } else {
        panel.style.display = 'none';
        button.setAttribute('aria-expanded', 'false');
      }
    } else {
      const isVisible = panel.style.display === 'block';
      panel.style.display = isVisible ? 'none' : 'block';
      button.setAttribute('aria-expanded', !isVisible);
    }
  }

  // Initialize picker
  function initPicker() {
    // Check if page supports dark themes (has :root or similar)
    const rootStyles = getComputedStyle(document.documentElement);
    const hasCustomColors = rootStyles.getPropertyValue('--color-primary') !== '';
    
    if (!hasCustomColors) {
      console.warn('Theme picker requires dark theme CSS loaded first');
      return;
    }

    // Create button and panel
    const pickerButton = createPickerButton();
    const pickerPanel = createPickerPanel();
    
    // Populate theme items
    const itemsContainer = pickerPanel.querySelector('#venus-picker-items');
    Object.keys(themes).forEach(themeKey => {
      const item = createThemeItem(themeKey);
      itemsContainer.appendChild(item);
    });

    // Close on clicking outside
    document.addEventListener('click', (e) => {
      if (!e.target.closest('#venus-theme-picker') && 
          !e.target.closest('#venus-theme-picker-panel')) {
        togglePickerPanel(false);
      }
    });

    // Close button handler
    const closeBtn = pickerPanel.querySelector('#venus-picker-close');
    closeBtn.addEventListener('click', () => {
      togglePickerPanel(false);
    });

    // Set initial button color
    applyTheme(currentTheme);
    
    // Add to document
    document.body.appendChild(pickerButton);
    document.body.appendChild(pickerPanel);
    
    // Store references for global access
    window.venusThemePicker = {
      toggle: togglePickerPanel,
      apply: applyTheme,
      themes: themes
    };
    
    console.log('🦉 Venus Theme Picker initialized with', Object.keys(themes).length, 'themes');
  }

  // Wait for DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initPicker);
  } else {
    initPicker();
  }

  // CSS for the picker elements (injected via style tag)
  const pickerStyles = `
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.7; }
    }

    .venus-theme-picker-button {
      border-radius: 50%;
      padding: 12px;
      box-shadow: 0 4px 15px rgba(0,0,0,0.3);
      transition: all 0.3s ease;
    }

    .venus-theme-picker-panel {
      animation: fadeIn 0.2s ease;
    }

    .venus-theme-item {
      position: relative;
      border-radius: 8px;
      transition: all 0.2s ease;
    }

    .venus-theme-item:hover {
      transform: scale(1.05);
      box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }

    .venus-theme-item.active {
      background: rgba(255,255,255,0.1);
    }
  `;

  // Inject picker styles
  const style = document.createElement('style');
  style.textContent = pickerStyles;
  document.head.appendChild(style);

})();