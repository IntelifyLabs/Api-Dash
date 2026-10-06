// Paste into the browser console on salonemilano.it, while logged in.
// Change EVENTO per exhibition: SMI, EUC, bathroom, S.Project (take the code
// from the URL after clicking that exhibition in the Exhibition filter).
// Leave categoria OUT unless you want it filtered.
(async () => {
  const EVENTO = 'SMI';
  const BASE = `https://www.salonemilano.it/en/exhibitors?anno=2026&evento=${EVENTO}`;

  // The fetched HTML has no layout, so innerText returns no line breaks.
  // Parking it in a real (offscreen) node in the live document fixes that and
  // gives exactly the three-line shape the page shows on screen.
  const host = document.createElement('div');
  host.style.cssText = 'position:absolute;left:-99999px;top:0';
  document.body.appendChild(host);

  const out = [];
  for (let p = 1; p <= 60; p++) {
    const res = await fetch(`${BASE}&pageNumber=${p}`, { credentials: 'include' });
    host.innerHTML = await res.text();
    const items = [...host.querySelectorAll('li')]
      .map(li => li.innerText.trim())
      .filter(t => t.includes('|') && /\d/.test(t) && t.split('\n').length >= 3);
    if (!items.length) { console.log('no rows on page', p, '- stopping'); break; }
    for (const t of items) {
      const [company, country, ...rest] = t.split('\n').map(s => s.trim());
      out.push(`* ${company}\n${country}\n${rest.join(' ')}`);
    }
    console.log('page', p, '->', items.length, 'rows, total', out.length);
    await new Promise(r => setTimeout(r, 300));   // be polite to their server
  }
  host.remove();

  const txt = out.join('\n');
  try { copy(txt); console.log('DONE:', out.length, 'rows copied to clipboard'); }
  catch (e) { console.log('DONE:', out.length, 'rows - clipboard blocked, use the string below'); console.log(txt); }
  return out.length;
})();
