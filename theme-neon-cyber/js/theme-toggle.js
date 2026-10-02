/**
 * Venus Theme Toggle
 */
(function() {
  'use strict';
  const THEMES = { BLUE_PURPLE: 'blue-purple', ROSE_GOLD: 'rose-gold' };
  
  function initTheme() {
    const saved = localStorage.getItem('venus-theme') || THEMES.BLUE_PURPLE;
    document.body.setAttribute('data-theme', saved);
    updateBtn(saved);
  }
  
  function toggleTheme() {
    const current = document.body.getAttribute('data-theme') || THEMES.BLUE_PURPLE;
    const next = current === THEMES.BLUE_PURPLE ? THEMES.ROSE_GOLD : THEMES.BLUE_PURPLE;
    document.body.setAttribute('data-theme', next);
    localStorage.setItem('venus-theme', next);
    updateBtn(next);
  }
  
  function updateBtn(theme) {
    const btn = document.getElementById('theme-toggle');
    if (btn) btn.textContent = theme === THEMES.BLUE_PURPLE ? '🎨 Blue' : '🎨 Rose';
  }
  
  document.addEventListener('DOMContentLoaded', function() {
    initTheme();
    const btn = document.getElementById('theme-toggle');
    if (btn) btn.addEventListener('click', toggleTheme);
  });
})();
