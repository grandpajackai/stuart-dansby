(function(){
  var C = window.TTF_CONFIG || {}, d = document, email = C.CONTACT_EMAIL || 'info@takingthefight.com';
  d.documentElement.classList.remove('no-js');
  // header
  var hdr = d.querySelector('.hdr'), btn = d.querySelector('.menu-btn'), nav = d.getElementById('nav');
  function onScroll(){ hdr && hdr.classList.toggle('scrolled', window.scrollY > 24); }
  onScroll(); window.addEventListener('scroll', onScroll, {passive:true});
  function closeMenu(){ hdr.classList.remove('open'); btn.setAttribute('aria-expanded','false'); btn.setAttribute('aria-label','Open menu'); }
  if (btn) {
    btn.addEventListener('click', function(){ var o = !hdr.classList.contains('open'); hdr.classList.toggle('open', o); btn.setAttribute('aria-expanded', String(o)); btn.setAttribute('aria-label', o ? 'Close menu' : 'Open menu'); if (o) { var f = nav.querySelector('a'); setTimeout(function(){ f && f.focus(); }, 60); } });
    nav.addEventListener('click', function(e){ if (e.target.closest('a')) closeMenu(); });
    d.addEventListener('keydown', function(e){ if (e.key === 'Escape' && hdr.classList.contains('open')) { closeMenu(); btn.focus(); } });
    window.addEventListener('resize', function(){ if (window.innerWidth > 860) closeMenu(); });
  }
  // booking links
  var subj = 'Discovery call request: Stuart Warren Dansby speaking';
  var body = 'Hi Stuart,\n\nI would like to schedule a 20-minute discovery call about a speaking engagement.\n\nOrganization:\nAudience and size:\nEvent date or timeframe:\nLocation:\nBest times for a call:\n\nThank you,';
  d.querySelectorAll('[data-book]').forEach(function(a){
    var kind = a.getAttribute('data-book');
    if (C.BOOKING_URL) { a.href = C.BOOKING_URL; a.target = '_blank'; a.rel = 'noopener'; }
    else { var s = kind === 'edu' ? 'Discovery call request: Taking the Fight for students' : subj; a.href = 'mailto:' + email + '?subject=' + encodeURIComponent(s) + '&body=' + encodeURIComponent(body); }
  });
  d.querySelectorAll('[data-email]').forEach(function(a){ a.href = 'mailto:' + email; a.textContent = email; });
  // course price / checkout
  d.querySelectorAll('[data-price]').forEach(function(el){ if (C.COURSE_PRICE) { el.textContent = C.COURSE_PRICE; el.classList.add('on'); } });
  d.querySelectorAll('[data-checkout]').forEach(function(el){ if (C.COURSE_CHECKOUT_URL) { el.href = C.COURSE_CHECKOUT_URL; el.hidden = false; } });
  // reveal
  var rv = d.querySelectorAll('.rv');
  if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var io = new IntersectionObserver(function(es){ es.forEach(function(e){ if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }); }, {rootMargin:'0px 0px -8% 0px'});
    rv.forEach(function(el){ io.observe(el); });
  } else rv.forEach(function(el){ el.classList.add('in'); });
  // video
  var dlg = d.getElementById('video'), last;
  d.querySelectorAll('[data-video]').forEach(function(t){
    t.addEventListener('click', function(e){
      if (!dlg || !dlg.showModal) return; // falls back to YouTube link
      e.preventDefault(); last = t;
      var f = d.createElement('iframe');
      f.src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(C.REEL_YOUTUBE_ID || t.dataset.video) + '?autoplay=1&rel=0';
      f.title = 'Stuart Warren Dansby speaker reel'; f.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen'; f.allowFullscreen = true; f.referrerPolicy = 'strict-origin-when-cross-origin';
      dlg.querySelector('.frame').replaceChildren(f); dlg.showModal(); dlg.querySelector('.x').focus();
    });
  });
  if (dlg) {
    dlg.querySelector('.x').addEventListener('click', function(){ dlg.close(); });
    dlg.addEventListener('click', function(e){ if (e.target === dlg) dlg.close(); });
    dlg.addEventListener('close', function(){ dlg.querySelector('.frame').replaceChildren(); last && last.focus(); });
  }
  // forms -> pre-filled email (until a form service is connected)
  d.querySelectorAll('form[data-mail]').forEach(function(form){
    var status = form.querySelector('.form-status');
    form.addEventListener('submit', function(e){
      e.preventDefault(); var ok = true, firstBad = null;
      form.querySelectorAll('[required]').forEach(function(inp){
        var err = d.getElementById(inp.getAttribute('aria-describedby')), bad = !inp.checkValidity();
        inp.setAttribute('aria-invalid', String(bad));
        if (err) err.textContent = bad ? (inp.validity.typeMismatch ? 'Please enter a valid email address.' : 'This field is required.') : '';
        if (bad) { ok = false; firstBad = firstBad || inp; }
      });
      if (!ok) { status.className = 'form-status'; status.textContent = 'Please fix the highlighted fields.'; firstBad.focus(); return; }
      var lines = [];
      form.querySelectorAll('input,select,textarea').forEach(function(i){ if (i.name && i.value.trim()) lines.push(i.dataset.label + ': ' + i.value.trim()); });
      var href = 'mailto:' + email + '?subject=' + encodeURIComponent(form.dataset.mail) + '&body=' + encodeURIComponent(lines.join('\n') + '\n');
      status.className = 'form-status ok';
      status.innerHTML = 'Opening your email app with everything filled in. Just press send. If nothing opens, email <a href="mailto:' + email + '">' + email + '</a>.';
      window.location.href = href;
    });
  });
  var y = d.getElementById('yr'); if (y) y.textContent = new Date().getFullYear();
})();
