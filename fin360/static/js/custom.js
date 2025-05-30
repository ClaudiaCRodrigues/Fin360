
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.has-submenu > a').forEach(function (toggle) {
    toggle.addEventListener('click', function (e) {
      e.preventDefault();
      const parent = this.closest('.nav-item');
      parent.classList.toggle('open');
    });
  });
});
