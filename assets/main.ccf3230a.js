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
// Fix language switcher: links should point to same page in other language
(function(){
  var langs = ['ru','tr','ar','fa','zh','ko','ur','fr','pt','es'];
  var path = window.location.pathname;
  
  // Extract current lang and page path
  var currentLang = '';
  var pagePath = path;
  for (var i = 0; i < langs.length; i++) {
    if (path.indexOf('/' + langs[i] + '/') === 0) {
      currentLang = langs[i];
      pagePath = path.substring(langs[i].length + 1); // remove /xx from start
      break;
    }
  }
  // pagePath is now like /for-pros/ or / (for homepage)
  
  // Update all lang switcher links
  var switches = document.querySelectorAll('#langSwitcher a, .langs a[data-lang]');
  for (var j = 0; j < switches.length; j++) {
    var lang = switches[j].getAttribute('data-lang');
    if (!lang) continue;
    if (lang === 'en') {
      switches[j].href = pagePath || '/';
    } else {
      switches[j].href = '/' + lang + pagePath;
    }
  }
})();
