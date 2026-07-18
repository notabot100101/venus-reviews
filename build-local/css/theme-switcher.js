/**
 * Venus Reviews Theme Switcher
 * Implements light/dark mode with localStorage persistence
 */

(function() {
  'use strict';
  
  // Theme configuration
  const THEMES = [
    { id: 'dark-blue', name: 'Dark Blue', css: '/css/theme-dark-blue.css' },
    { id: 'dark-rose', name: 'Dark Rose', css: '/css/theme-dark-rose.css' },
    { id: 'dark-green', name: 'Dark Green', css: '/css/theme-dark-green.css' },
    { id: 'light', name: 'Light', css: '/css/theme-light.css' }
  ];
  
  const STORAGE_KEY = 'venus-theme-preference';
  const DEFAULT_THEME = 'dark-blue';
  
  // DOM elements
  let toggleButton = null;
  let currentTheme = null;
  
  /**
   * Initialize theme switcher
   */
  function init() {
    // Load saved theme or use default
    currentTheme = localStorage.getItem(STORAGE_KEY) || DEFAULT_THEME;
    
    // Apply saved theme
    applyTheme(currentTheme);
    
    // Create toggle button
    createToggleButton();
    
    // Listen for user clicks
    toggleButton?.addEventListener('click', handleToggleClick);
  }
  
  /**
   * Create floating toggle button
   */
  function createToggleButton() {
    const button = document.createElement('button');
    button.id = 'venus-theme-toggle';
    button.type = 'button';
    button.className = 'theme-toggle-btn';
    button.ariaLabel = 'Toggle light/dark mode';
    button.setAttribute('aria-expanded', 'false');
    
    button.innerHTML = `
      <svg class="theme-toggle-icon" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="5"></circle>
        <line x1="12" y1="1" x2="12" y2="3"></line>
        <line x1="12" y1="21" x2="12" y2="23"></line>
        <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
        <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
        <line x1="1" y1="12" x2="3" y2="12"></line>
        <line x1="21" y1="12" x2="23" y2="12"></line>
        <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
        <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
      </svg>
      <span class="theme-toggle-label">🌙</span>
    `;
    
    toggleButton = button;
    
    // Insert before footer
    const footer = document.querySelector('footer');
    if (footer) {
      footer.parentNode.insertBefore(button, footer);
    }
    
    // Update icon based on current theme
    updateIcon();
  }
  
  /**
   * Handle toggle button click
   */
  function handleToggleClick() {
    const newTheme = currentTheme === 'dark-blue' || currentTheme === 'dark-rose' || currentTheme === 'dark-green' 
      ? 'light'
      : 'dark-blue';
    
    applyTheme(newTheme);
  }
  
  /**
   * Apply theme
   */
  function applyTheme(themeId) {
    // Save preference
    localStorage.setItem(STORAGE_KEY, themeId);
    
    // Update body class
    document.body.className = themeId === 'light' ? 'theme-light theme-transition' : 'theme-transition';
    
    // Update toggle button label
    const label = toggleButton.querySelector('.theme-toggle-label');
    if (label) {
      label.textContent = themeId === 'light' ? '☀️' : '🌙';
    }
    
    // Update icon
    updateIcon();
    
    // Remove other theme CSS if needed
    THEMES.forEach(t => {
      const link = document.querySelector(`link[href="${t.css}"]`);
      if (link && t.id !== themeId) {
        link.remove();
      }
    });
    
    // Add current theme CSS
    const themeLink = document.createElement('link');
    themeLink.rel = 'stylesheet';
    themeLink.href = THEMES.find(t => t.id === themeId).css;
    themeLink.id = 'venus-theme-css';
    document.head.appendChild(themeLink);
    
    console.log(`Theme changed to: ${themeId}`);
  }
  
  /**
   * Update toggle icon
   */
  function updateIcon() {
    const svg = toggleButton.querySelector('svg');
    const label = toggleButton.querySelector('.theme-toggle-label');
    
    if (svg) {
      if (currentTheme === 'light') {
        // Sun icon
        svg.innerHTML = `
          <circle cx="12" cy="12" r="5"></circle>
          <line x1="12" y1="1" x2="12" y2="3"></line>
          <line x1="12" y1="21" x2="12" y2="23"></line>
          <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
          <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
          <line x1="1" y1="12" x2="3" y2="12"></line>
          <line x1="21" y1="12" x2="23" y2="12"></line>
          <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
          <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
          <line x1="16" y1="12" x2="18" y2="12"></line>
          <line x1="12" y1="16" x2="12" y2="18"></line>
        `;
      } else {
        // Moon icon
        svg.innerHTML = `
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
        `;
      }
    }
    
    if (label) {
      label.textContent = currentTheme === 'light' ? '☀️' : '🌙';
    }
  }
  
  /**
   * Detect system preference on init
   */
  function detectSystemTheme() {
    const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    return prefersDark ? 'dark-blue' : 'light';
  }
  
  /**
   * Initialize on DOM ready
   */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    // Already loaded
    init();
  }
  
  /**
   * Handle system theme changes
   */
  if (window.matchMedia) {
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', event => {
      // Only auto-switch if no saved preference
      if (!localStorage.getItem(STORAGE_KEY)) {
        const systemTheme = event.matches ? 'dark-blue' : 'light';
        applyTheme(systemTheme);
      }
    });
  }
})();
