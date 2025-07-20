/**
 * Toggles the navbar's background between transparent and solid
 * depending on scroll position relative to the page_header height.
 */
document.addEventListener('DOMContentLoaded', function() {
  const navbar = document.getElementById('main-navbar');

  const headerBlock = document.querySelector('.page-header');
  const threshold = headerBlock ? headerBlock.offsetHeight : 0;

  /**
   * Checks the current scroll position (window.scrollY) against
   * the threshold. If scrolled past the header, apply 
   * the solid background class. Otherwise, transparent.
   */
  function updateNavbar() {
    if (window.scrollY > threshold) {
      navbar.classList.remove('navbar-transparent');
      navbar.classList.add('navbar-solid');
    } else {
      navbar.classList.remove('navbar-solid');
      navbar.classList.add('navbar-transparent');
    }
  }

  // run on scroll
  window.addEventListener('scroll', updateNavbar);
  // run on load in case user reloads mid‑page
  updateNavbar();
});