/* KP-Mainz — shared 25-minute focus timer.
   Floating widget on every page, state synced across pages/tabs via localStorage. */
(function () {
  'use strict';
  if (window.__kpFocus) return; window.__kpFocus = true;

  var KEY = 'kp_focus_v1';
  var DURATION = 25 * 60; // seconds

  function load() { try { return JSON.parse(localStorage.getItem(KEY)); } catch (e) { return null; } }
  function save(s) { try { localStorage.setItem(KEY, JSON.stringify(s)); } catch (e) {} }

  // resolve the live state from what's stored
  function current() {
    var s = load();
    if (!s || s.mode === 'idle') return { mode: 'idle', remaining: DURATION };
    if (s.mode === 'paused') return { mode: 'paused', remaining: s.remaining };
    if (s.mode === 'done') return { mode: 'done', remaining: 0 };
    var rem = Math.round((s.endsAt - Date.now()) / 1000);        // running
    if (rem <= 0) return { mode: 'running-done', remaining: 0 }; // just crossed zero
    return { mode: 'running', remaining: rem };
  }

  var css = '\
.kp-focus{position:fixed;right:16px;bottom:calc(16px + env(safe-area-inset-bottom,0px));z-index:2147483000;\
display:inline-flex;align-items:center;gap:7px;font-family:ui-monospace,"JetBrains Mono",Menlo,monospace;\
font-size:13px;font-weight:600;color:#5A544B;background:rgba(255,253,248,.96);backdrop-filter:blur(8px);\
-webkit-backdrop-filter:blur(8px);border:1px solid #E0D9CC;border-radius:12px;padding:9px 12px;cursor:pointer;\
box-shadow:0 6px 20px rgba(0,0,0,.14);line-height:1;-webkit-tap-highlight-color:transparent;user-select:none;\
transition:border-color .15s,color .15s,background .15s,box-shadow .2s}\
.kp-focus:hover{box-shadow:0 8px 26px rgba(0,0,0,.2)}\
.kp-focus-ico{font-size:14px}\
.kp-focus-lbl{font-variant-numeric:tabular-nums;min-width:40px;text-align:center}\
.kp-focus-rst{display:none;font-size:14px;opacity:.5;padding:0 1px}\
.kp-focus.on .kp-focus-rst{display:inline}\
.kp-focus-rst:hover{opacity:1}\
.kp-focus.run{border-color:#2D7A3E;color:#2D7A3E;background:rgba(232,244,236,.96)}\
.kp-focus.fin{border-color:#B45309;color:#B45309;background:rgba(254,243,220,.97);animation:kpFocusPulse 1.1s ease-in-out infinite}\
@keyframes kpFocusPulse{0%,100%{opacity:1}50%{opacity:.5}}\
@media(prefers-color-scheme:dark){.kp-focus{color:#B8B0A2;background:rgba(30,27,22,.94);border-color:#3A342B;box-shadow:0 6px 22px rgba(0,0,0,.5)}}';

  function build() {
    var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

    var el = document.createElement('button');
    el.type = 'button'; el.className = 'kp-focus'; el.setAttribute('aria-label', '25-Minuten-Fokus');
    el.title = '25-Minuten-Fokus — tippen zum Starten oder Pausieren';
    el.innerHTML = '<span class="kp-focus-ico">\uD83C\uDF45</span><span class="kp-focus-lbl">25:00</span><span class="kp-focus-rst" title="Zur\u00FCcksetzen">\u21BA</span>';
    document.body.appendChild(el);

    var lbl = el.querySelector('.kp-focus-lbl'), rst = el.querySelector('.kp-focus-rst');
    var fin = false, tick = null;

    function fmt(s) { var m = Math.floor(s / 60), ss = s % 60; return m + ':' + (ss < 10 ? '0' : '') + ss; }
    function notify() {
      try { if (navigator.vibrate) navigator.vibrate([180, 90, 180]); } catch (e) {}
      if (window.Notification && Notification.permission === 'granted') {
        try { new Notification('Fokus fertig \uD83C\uDF45', { body: '25 Minuten geschafft \u2014 kurze Pause.' }); } catch (e) {}
      }
    }
    function paint() {
      var c = current();
      var running = c.mode === 'running';
      var done = c.mode === 'done' || c.mode === 'running-done';
      el.classList.toggle('run', running);
      el.classList.toggle('fin', done);
      el.classList.toggle('on', c.mode !== 'idle');
      lbl.textContent = done ? 'Fertig' : fmt(c.remaining);
      if (c.mode === 'running-done') { save({ mode: 'done' }); if (!fin) { fin = true; notify(); } }
      else if (c.mode !== 'done') { fin = false; }
      if (running && !tick) tick = setInterval(paint, 500);
      else if (!running && tick) { clearInterval(tick); tick = null; }
    }

    el.addEventListener('click', function () {
      var c = current();
      if (c.mode === 'done' || c.mode === 'running-done') { save({ mode: 'idle' }); fin = false; paint(); return; }
      if (c.mode === 'running') { save({ mode: 'paused', remaining: c.remaining }); paint(); return; }
      var rem = (c.mode === 'paused') ? c.remaining : DURATION; // start / resume
      save({ mode: 'running', endsAt: Date.now() + rem * 1000 });
      if (window.Notification && Notification.permission === 'default') { try { Notification.requestPermission(); } catch (e) {} }
      paint();
    });
    rst.addEventListener('click', function (e) { e.stopPropagation(); save({ mode: 'idle' }); fin = false; paint(); });
    window.addEventListener('storage', function (e) { if (e.key === KEY) paint(); });

    paint();
  }

  if (document.body) build();
  else document.addEventListener('DOMContentLoaded', build);
})();
