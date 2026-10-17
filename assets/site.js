(() => {
  'use strict';
  document.querySelectorAll('[data-year]').forEach(el => { el.textContent = String(new Date().getFullYear()); });
  const menuButton = document.querySelector('[data-menu-toggle]');
  const menu = menuButton && document.getElementById(menuButton.getAttribute('aria-controls'));
  const closeMenu = () => { if (!menu) return; menu.classList.remove('is-open'); menuButton.setAttribute('aria-expanded', 'false'); };
  if (menu) {
    menuButton.addEventListener('click', () => { const open = menuButton.getAttribute('aria-expanded') !== 'true'; menuButton.setAttribute('aria-expanded', String(open)); menu.classList.toggle('is-open', open); });
    menu.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') { closeMenu(); menuButton.focus(); } });
    document.addEventListener('click', e => { if (!menu.contains(e.target) && !menuButton.contains(e.target)) closeMenu(); });
    window.matchMedia('(min-width:761px)').addEventListener('change', closeMenu);
  }
  document.querySelectorAll('[data-package]').forEach(link => link.addEventListener('click', () => {
    const select = document.querySelector('select[name="package"]');
    if (select) { select.value = link.dataset.package; select.dispatchEvent(new Event('change', {bubbles:true})); }
  }));
  const makeDialog = (extraClass = '') => {
    const dialog = document.createElement('dialog'); dialog.className = extraClass;
    const close = document.createElement('button'); close.className = 'dialog-close'; close.type = 'button'; close.setAttribute('aria-label', 'Close dialog'); close.textContent = '×';
    dialog.append(close); document.body.append(dialog);
    const teardown = () => { dialog.querySelectorAll('iframe').forEach(f => f.remove()); document.documentElement.style.overflow = ''; };
    const dismiss = () => { teardown(); dialog.close(); };
    close.addEventListener('click', dismiss);
    dialog.addEventListener('cancel', teardown);
    dialog.addEventListener('click', event => { if (event.target === dialog) { const r = dialog.getBoundingClientRect(); if (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom) dismiss(); } });
    dialog.addEventListener('close', teardown);
    return dialog;
  };
  const showDialog = dialog => { dialog.showModal(); document.documentElement.style.overflow = 'hidden'; };
  let videoDialog;
  document.querySelectorAll('[data-video]').forEach(trigger => trigger.addEventListener('click', () => {
    if (!videoDialog) videoDialog = makeDialog('video-dialog');
    videoDialog.querySelectorAll('iframe, .video-fallback, h2').forEach(el => el.remove());
    const title = trigger.dataset.videoTitle || 'Stuart Warren Dansby';
    const heading = document.createElement('h2'); heading.id = 'video-title'; heading.className = 'eyebrow'; heading.textContent = title; heading.style.marginBottom = '15px';
    const iframe = document.createElement('iframe'); iframe.src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(trigger.dataset.video) + '?rel=0'; iframe.title = title; iframe.allow = 'accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share'; iframe.allowFullscreen = true; iframe.referrerPolicy = 'strict-origin-when-cross-origin';
    const p = document.createElement('p'); p.className = 'video-fallback'; p.append('Video unavailable? ');
    const link = document.createElement('a'); link.href = 'https://www.youtube.com/watch?v=' + encodeURIComponent(trigger.dataset.video); link.target = '_blank'; link.rel = 'noopener noreferrer'; link.textContent = 'Watch on YouTube ↗'; p.append(link);
    videoDialog.setAttribute('aria-labelledby', heading.id); videoDialog.append(heading, iframe, p); showDialog(videoDialog);
  }));
  document.querySelectorAll('form[data-inquiry]').forEach(form => {
    form.addEventListener('submit', event => {
      event.preventDefault();
      if (!form.reportValidity()) return;
      const values = new FormData(form);
      const value = key => String(values.get(key) || '').trim();
      const speaking = form.dataset.inquiry === 'speaking';
      const recipient = 'info@takingthefight.com';
      const subject = speaking ? 'Speaking inquiry — ' + value('organization') : 'Five Pillars seminar — invitation request';
      const labels = speaking ? [['name','Name'],['email','Reply email'],['organization','Organization'],['role','Role'],['date','Event timing'],['audience','Audience size'],['package','Experience'],['goals','Audience goals']] : [['name','Name'],['email','Reply email'],['challenge','My goal or challenge']];
      const intro = speaking ? 'Hello Taking the Fight team,\n\nI would like to discuss an event with Stuart Warren Dansby.\n' : 'Hello Taking the Fight team,\n\nPlease let me know when dates and registration are available for the introductory Five Pillars seminar.\n';
      const message = intro + '\n' + labels.filter(([key]) => value(key)).map(([key,label]) => label + ': ' + value(key)).join('\n') + '\n\nThank you,\n' + value('name');
      const dialog = makeDialog();
      const eyebrow = document.createElement('span'); eyebrow.className = 'eyebrow'; eyebrow.textContent = 'Your next step';
      const heading = document.createElement('h2'); heading.className = 'dialog-title'; heading.id = 'inquiry-title'; heading.textContent = speaking ? 'Your event conversation starts here.' : 'Your invitation request is ready.';
      const copy = document.createElement('p'); copy.className = 'dialog-copy'; copy.textContent = 'Review your draft below. Nothing has been sent yet. Open it in your email app and send it to ' + recipient + ', or copy the draft into your preferred email service.';
      const label = document.createElement('label'); label.className = 'eyebrow'; label.textContent = 'Editable email draft'; label.htmlFor = 'email-draft';
      const preview = document.createElement('textarea'); preview.id = 'email-draft'; preview.className = 'email-preview'; preview.value = message; preview.setAttribute('aria-label', 'Editable email draft');
      const actions = document.createElement('div'); actions.className = 'dialog-actions';
      const email = document.createElement('a'); email.className = 'button'; email.textContent = 'Open in email app ↗';
      const refreshHref = () => { email.href = 'mailto:' + recipient + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(preview.value); };
      refreshHref(); preview.addEventListener('input', refreshHref);
      const copyButton = document.createElement('button'); copyButton.type = 'button'; copyButton.className = 'button button-outline'; copyButton.textContent = 'Copy email draft';
      const status = document.createElement('p'); status.className = 'dialog-status'; status.setAttribute('role', 'status');
      copyButton.addEventListener('click', async () => {
        const fullDraft = 'To: ' + recipient + '\nSubject: ' + subject + '\n\n' + preview.value;
        try { await navigator.clipboard.writeText(fullDraft); status.textContent = 'Copied. Paste the draft into your email service and send it when ready.'; }
        catch { preview.focus(); preview.select(); status.textContent = 'Select and copy the draft above, then email it to ' + recipient + '.'; }
      });
      actions.append(email, copyButton); dialog.append(eyebrow, heading, copy, label, preview, actions, status); dialog.setAttribute('aria-labelledby', heading.id);
      dialog.addEventListener('close', () => { dialog.remove(); }, {once:true}); showDialog(dialog);
    });
  });
})();
