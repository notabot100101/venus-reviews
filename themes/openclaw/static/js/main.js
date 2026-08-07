// OpenClaw — minimal site JS
document.addEventListener('DOMContentLoaded', function () {
  // Mobile nav toggle
  const toggle = document.querySelector('.nav-toggle');
  const navList = document.querySelector('.nav-list');

  if (toggle && navList) {
    toggle.addEventListener('click', function () {
      navList.classList.toggle('open');
    });

    // Close on outside click
    document.addEventListener('click', function (e) {
      if (!e.target.closest('.site-nav')) {
        navList.classList.remove('open');
      }
    });
  }

  // Highlight current nav item
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-list a').forEach(function (link) {
    const href = link.getAttribute('href');
    if (href === '/') {
      if (currentPath === '/' || currentPath === '') link.setAttribute('aria-current', 'page');
    } else if (currentPath.startsWith(href)) {
      link.setAttribute('aria-current', 'page');
    }
  });
});