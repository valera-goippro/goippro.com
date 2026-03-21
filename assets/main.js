// Mobile menu toggle
document.addEventListener('DOMContentLoaded', function() {
  var burger = document.querySelector('.burger');
  var nav = document.querySelector('.nav');

  if (burger && nav) {
    burger.addEventListener('click', function() {
      nav.classList.toggle('open');
    });

    // Close menu on link click
    nav.querySelectorAll('a').forEach(function(link) {
      link.addEventListener('click', function() {
        nav.classList.remove('open');
      });
    });
  }

  // Accordion
  document.querySelectorAll('.accordion-btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
      var item = this.closest('.accordion-item');
      var wasOpen = item.classList.contains('open');
      // Close all
      document.querySelectorAll('.accordion-item').forEach(function(el) {
        el.classList.remove('open');
      });
      // Toggle current
      if (!wasOpen) {
        item.classList.add('open');
      }
    });
  });
});
