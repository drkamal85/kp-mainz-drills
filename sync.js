/* sync.js — opt-in progress reporter for review pages.
   No-ops entirely unless the user has set { api, token } via the flashcards page (same-origin localStorage).
   Marks this review as "learning" on open and offers a "gemeistert" toggle; writes to the shared store. */
(function () {
  var cfg;
  try { cfg = JSON.parse(localStorage.getItem('kp-sync') || '{}'); } catch (e) { cfg = {}; }

  var m = location.pathname.match(/\/reviews\/[a-z0-9-]+\/([a-z0-9-]+-r\d)\.html$/i);
  if (!m) return;
  var reviewId = m[1];
  var localKey = 'kp-review-' + reviewId;

  function post(body) {
    if (!cfg.api || !cfg.token) return Promise.resolve();
    return fetch(cfg.api.replace(/\/$/, '') + '/api/progress', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + cfg.token },
      body: JSON.stringify(body)
    }).catch(function () {});
  }

  // open => at least "learning" (never downgrade a local "mastered")
  if (localStorage.getItem(localKey) !== 'mastered') {
    localStorage.setItem(localKey, 'learning');
    post({ reviews: setOne(reviewId, 'learning') });
  }

  // floating toggle
  function build() {
    if (document.getElementById('kp-mastered-btn')) return;
    var btn = document.createElement('button');
    btn.id = 'kp-mastered-btn';
    btn.style.cssText = 'position:fixed;right:14px;bottom:14px;z-index:99999;border:none;border-radius:999px;padding:10px 16px;font-family:Manrope,system-ui,sans-serif;font-weight:700;font-size:.8rem;cursor:pointer;box-shadow:0 6px 18px rgba(45,122,62,.3);background:#2D7A3E;color:#fff';
    function paint() { btn.textContent = (localStorage.getItem(localKey) === 'mastered') ? '✓ Gemeistert' : 'Als gemeistert markieren'; btn.style.opacity = (cfg.api && cfg.token) ? '1' : '.55'; }
    btn.onclick = function () {
      var now = (localStorage.getItem(localKey) === 'mastered') ? 'learning' : 'mastered';
      localStorage.setItem(localKey, now); paint(); post({ reviews: setOne(reviewId, now) });
    };
    paint();
    document.body.appendChild(btn);
  }
  function setOne(id, val) { var o = {}; o[id] = val; return o; }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', build); else build();
})();
