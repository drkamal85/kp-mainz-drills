/* print.js — Ctrl+P auf jeder Themenseite ergibt dasselbe Layout wie die PDF.
   Vor dem Druck: alle Stationen sichtbar, alle Karten offen, Stationsbänder rein.
   Nach dem Druck: Bildschirmzustand wiederhergestellt.
   Styling kommt ausschließlich aus /print.css (media="print"). */
(function () {
  var STN = {
    retrieval: 'Retrieval', grundlagen: 'Grundlagen', klinik: 'Klinik',
    diagnostik: 'Diagnostik', therapie: 'Therapie', fragen: 'KP-Fragen',
    perlen: 'KP-Perlen', protokoll: 'Fragen & Protokolle', nachfragen: 'Nachfragen'
  };
  var LEGACY = ['grundlagen', 'klinik', 'diagnostik', 'therapie', 'fragen', 'perlen', 'protokoll'];
  var opened = [];

  function band(sec, key, label, i, n) {
    if (sec.querySelector('.stationband')) return;
    var b = document.createElement('div');
    b.className = 'stationband sb-' + key;
    b.style.display = 'none';               // auf dem Bildschirm unsichtbar
    b.innerHTML = '<span class="sb-t"></span><span class="sb-n"></span>';
    b.firstChild.textContent = label;
    b.lastChild.textContent = i + ' / ' + n;
    sec.insertBefore(b, sec.firstChild);
  }

  function expand() {
    var panels = document.querySelectorAll('.panel[data-panel]');
    if (panels.length) {
      panels.forEach(function (p, i) {
        var k = p.getAttribute('data-panel');
        band(p, k, STN[k] || k, i + 1, panels.length);
      });
    } else {
      var secs = document.querySelectorAll('section.station[id]');
      var tabs = document.querySelectorAll('.tab');
      secs.forEach(function (s, i) {
        var label = tabs[i] ? tabs[i].textContent.trim() : 'Station ' + (i + 1);
        band(s, LEGACY[i % LEGACY.length], label, i + 1, secs.length);
      });
    }
    document.querySelectorAll('details:not([open])').forEach(function (d) {
      opened.push(d); d.open = true;
    });
  }

  function collapse() {
    opened.forEach(function (d) { d.open = false; });
    opened = [];
  }

  window.addEventListener('beforeprint', expand);
  window.addEventListener('afterprint', collapse);
  if (window.matchMedia) {
    var mq = window.matchMedia('print');
    (mq.addEventListener ? mq.addEventListener.bind(mq, 'change') : mq.addListener.bind(mq))(
      function (e) { (e.matches ? expand : collapse)(); }
    );
  }
})();
