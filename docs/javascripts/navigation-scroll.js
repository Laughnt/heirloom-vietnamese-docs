(function () {
  var NAV_SCROLLWRAP = '.md-sidebar[data-md-type="navigation"] .md-sidebar__scrollwrap';
  var rememberedScrollTop = null;
  var restorePending = false;
  var watchedScrollwrap = null;

  function getScrollwrap() {
    return document.querySelector(NAV_SCROLLWRAP);
  }

  function rememberScroll() {
    var scrollwrap = getScrollwrap();
    if (scrollwrap) {
      rememberedScrollTop = scrollwrap.scrollTop;
    }
  }

  function onSidebarScroll() {
    if (!restorePending) {
      rememberedScrollTop = this.scrollTop;
    }
  }

  function watchSidebar() {
    var scrollwrap = getScrollwrap();
    if (!scrollwrap || scrollwrap === watchedScrollwrap) {
      return;
    }
    if (watchedScrollwrap) {
      watchedScrollwrap.removeEventListener('scroll', onSidebarScroll);
    }
    watchedScrollwrap = scrollwrap;
    watchedScrollwrap.addEventListener('scroll', onSidebarScroll, { passive: true });
    if (rememberedScrollTop === null) {
      rememberedScrollTop = watchedScrollwrap.scrollTop;
    }
  }

  function isInternalLink(link) {
    if (!link || link.target || link.hasAttribute('download')) {
      return false;
    }
    var href = link.getAttribute('href') || '';
    if (!href || href.charAt(0) === '#' || /^(mailto|tel):/i.test(href)) {
      return false;
    }
    try {
      var url = new URL(link.href, window.location.href);
      return url.origin === window.location.origin;
    } catch (_error) {
      return false;
    }
  }

  function restoreScroll() {
    if (!restorePending || rememberedScrollTop === null) {
      return;
    }
    var expected = rememberedScrollTop;
    var apply = function () {
      var scrollwrap = getScrollwrap();
      if (scrollwrap) {
        scrollwrap.scrollTop = expected;
      }
    };

    window.requestAnimationFrame(function () {
      apply();
      window.requestAnimationFrame(function () {
        apply();
        restorePending = false;
      });
    });
  }

  document.addEventListener('click', function (event) {
    var target = event.target;
    if (!(target instanceof Element)) {
      return;
    }
    var link = target.closest('a[href]');
    if (!isInternalLink(link)) {
      return;
    }
    rememberScroll();
    restorePending = true;
  }, true);

  watchSidebar();
  if (window.document$ && typeof window.document$.subscribe === 'function') {
    window.document$.subscribe(function () {
      watchSidebar();
      restoreScroll();
    });
  }
})();
