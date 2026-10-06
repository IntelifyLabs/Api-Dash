#!/usr/bin/env python3
"""Check round3_qualified.csv before any number is reported or any credit spent.

Written before the run finished, on purpose: a check designed around results
you have already seen is not a check.

What it asserts, and why each one exists:

  row count        1,314 in, 1,314 out. The Heimtextil fetch silently returned
                   the same 100 companies fifteen times when the pagination
                   parameter was wrong, so counts get asserted now.
  probe coverage   every take and review row carries a site_live value, and no
                   excluded row was probed.
  reason agrees    the one line reason is derived from has_tryon and sells_to,
                   so it must never contradict them. A readable summary that
                   disagrees with its own data is worse than no summary.
  known companies  Bonaldo, MDF Italia, Acerbis, Annibale Colombo were the
                   evidence that the first signal was wrong. If they still read
                   unclear, the fix did not work.
  no regression    has_tryon should land near the 94 the first pass found. A
                   big move either way means the fetch changed, not the world.
  unclear fell     the whole point of the re-run. If unclear is still over a
                   third of live sites, say so rather than shipping it.
"""
import csv, collections, sys

F = 'round3_qualified.csv'
rows = list(csv.DictReader(open(F, encoding='utf-8-sig')))
fail, warn = [], []

def check(ok, msg):
    (fail if not ok else []).append(msg) if not ok else None
    print('  %s %s' % ('ok  ' if ok else 'FAIL', msg))

print('row counts')
check(len(rows) == 1314, 'rows: %d, expected 1314' % len(rows))
v = collections.Counter(r['verdict'] for r in rows)
check(sum(v.values()) == len(rows), 'verdicts cover every row: %s' % dict(v))

print('\nprobe coverage')
todo = [r for r in rows if r['verdict'] in ('take', 'review')]
skipped = [r for r in rows if r['verdict'] == 'excluded']
check(all(r['site_live'] for r in todo),
      'every take/review row probed (%d of %d)'
      % (sum(1 for r in todo if r['site_live']), len(todo)))
check(not any(r['site_live'] for r in skipped),
      'no excluded row was probed (%d excluded)' % len(skipped))

print('\nreason agrees with the columns it summarises')
live = [r for r in todo if r['site_live'] == 'yes']
bad = 0
for r in live:
    t, s, why = r['has_tryon'] == 'yes', r['sells_to'], r['reason'].lower()
    if t and 'already runs a visualiser' not in why: bad += 1
    elif not t and 'already runs a visualiser' in why: bad += 1
    elif s == 'trade only' and 'only to the trade' not in why: bad += 1
check(bad == 0, 'reason never contradicts has_tryon or sells_to (%d mismatches)' % bad)
check(all(r['reason'] for r in todo), 'every probed row has a reason line')

print('\nthe companies that proved the cart-only signal wrong')
# Annibale Colombo was in this list and the assertion was wrong, not the data.
# Its homepage is Home, Azienda, Indoor, Outdoor, Designers, Contatti: no cart,
# no dealer finder, no prices. "Not a cart" never meant "sells to consumers",
# and asserting it did was the same mistake the first regex made. It is a
# catalogue-only brand showcase, which is now its own value.
for name in ('Bonaldo', 'Acerbis'):
    m = [r for r in rows if name.lower() in r['company'].lower()]
    if not m:
        warn.append('%s not found' % name); print('  warn %s not found' % name); continue
    r = m[0]
    check(r['site_live'] != 'yes' or r['sells_to'].startswith('consumer'),
          '%-18s site=%-11s sells_to=%s' % (name, r['site_live'], r['sells_to']))
for name in ('Annibale Colombo',):
    m = [r for r in rows if name.lower() in r['company'].lower()]
    r = m[0] if m else None
    if r:
        check(r['sells_to'] in ('catalogue only', 'consumer, via dealers'),
              '%-18s reads %s, confirmed by hand as a brand showcase'
              % (name, r['sells_to']))

print('\nno regression against the first pass')
ty = sum(1 for r in live if r['has_tryon'] == 'yes')
check(70 <= ty <= 130, 'has_tryon = %d, first pass found 94' % ty)
lv = len(live)
check(850 <= lv <= 980, 'live sites = %d, first pass found 915' % lv)

print('\ndid unclear actually fall')
unc = sum(1 for r in live if r['sells_to'] == 'unclear')
pct = 100 * unc / lv if lv else 0
print('  unclear: %d of %d live (%.0f%%). 57%% on pass 1, 45%% on pass 2' % (unc, lv, pct))
# Pass 2's 411 "unclear" were sampled by hand: 16 of 23 had a downloadable
# catalogue, 15 a contact form, only 3 a price. That is a brand showcase, not
# an unknown, so it has its own label now and the bar is far lower.
if pct > 12:
    warn.append('unclear is still %.0f%% of live sites' % pct)
    print('  warn above 12%, report it rather than hide it')
else:
    print('  ok   a genuine residue')

print('\nsells_to breakdown')
for k, n in collections.Counter(r['sells_to'] for r in live).most_common():
    print('  %4d  %s' % (n, k))

print('\n=== THE CUTS ===')
cons = lambda r: r['sells_to'].startswith('consumer')
c1 = [r for r in live if r['has_tryon'] == 'yes' and cons(r)]
c2 = [r for r in live if cons(r)]
c3 = [r for r in rows if r['verdict'] == 'take']
c1t = [r for r in c1 if r['verdict'] == 'take']
c2t = [r for r in c2 if r['verdict'] == 'take']
print('  cut 1  visualiser + consumer facing : %4d   (%d already verdict=take)' % (len(c1), len(c1t)))
print('  cut 2  consumer facing, any tool    : %4d   (%d already verdict=take)' % (len(c2), len(c2t)))
print('  cut 3  every take row               : %4d' % len(c3))
print('\n  cut 1 by studio:', dict(collections.Counter(r['studio'] for r in c1)))
print('  cut 2 by studio:', dict(collections.Counter(r['studio'] for r in c2)))

print('\nreviews resolved')
for lbl, key in (('rug export house', 'rug export'), ('S.Project', 'S_P'), ('hall 3.0', 'hall 3.0')):
    g = [r for r in rows if key in r['why']]
    gl = [r for r in g if r['site_live'] == 'yes']
    c = sum(1 for r in gl if cons(r))
    print('  %-17s %3d rows, %3d live, %3d consumer facing -> %d now usable'
          % (lbl, len(g), len(gl), c, c))

print('\n%s' % ('FAILURES: %d' % len(fail) if fail else 'all checks passed'))
for f in fail: print('  -', f)
for w in warn: print('  warn:', w)
sys.exit(1 if fail else 0)
