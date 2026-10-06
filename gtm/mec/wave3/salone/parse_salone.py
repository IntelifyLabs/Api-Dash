#!/usr/bin/env python3
"""Parse the Salone del Mobile exhibitor list into rows.

The listing renders three lines per entry:

    * Alivar srl
    Italy
    Salone Internazionale del Mobile | 18 D04

So: company, country, then exhibition and the pavilion and stand.

STAND SHARING IS THE THING TO HANDLE. Salone lists brands and legal entities
as separate entries on the same stand, and the first four pages already show
it three ways:

    15 B37   Asnaghi Interiors Design
             Asnaghi Interiors srl
             Asnaghi Interiors The Art of The Italian Style Furniture Since 1916
    13 C23   Bel Mondo by Bellotti Ezio
             Bellotti Ezio Arredamenti srl
    05 A34   Arteinmotion
             Arteinmotion di Panciroli Carlo & C snc
    15 B16   Arte Veneziana
             Arte Veneziana Arredo srl
    05 A18   Anibal Carneiro Barbosa lda
             Animovel

One company, one website, one email, counted up to three times. Enriching each
separately pays for the same domain repeatedly, which is exactly the waste
that got the 126-row recovery vetoed.

So rows are grouped by (exhibition, pavilion, stand) and the group keeps ONE
primary name plus its aliases. The primary is the entry that reads most like a
brand: shortest, and preferring one with no legal suffix, because "Arteinmotion"
is what their website is called and "Arteinmotion di Panciroli Carlo & C snc"
is what their accountant calls them.

A shared stand is not always one company, though. 07 D16 holds Altacom and
Arsenale, which may be two firms sharing space rather than a brand and its
parent. Groups whose names do not share a common root are flagged
SHARED_STAND_CHECK rather than merged silently.
"""
import csv, re, sys, collections, difflib

SUFFIX = re.compile(r'\b(s\.?r\.?l\.?s?|s\.?p\.?a|snc|sas|lda|ltd|co\.?\s*ltd|gmbh|bv|nv|'
                    r'd\.?o\.?o|sp\.?\s*z\.?\s*o\.?o|a\.?s|ltd\.?\s*sti|inc|llc|'
                    r'arredamenti|interiors|mobili|design)\b\.?', re.I)
ENTRY = re.compile(r'^\*\s+(.+)$')

def norm(n):
    """Name reduced to its brand root, for the shared-stand sanity check."""
    n = SUFFIX.sub('', n.lower())
    n = re.sub(r'\b(di|by|the|art of|italian|style|furniture|since|\d{4})\b', ' ', n)
    return re.sub(r'[^a-z0-9]+', '', n)

def parse(text):
    lines = [l.rstrip() for l in text.splitlines()]
    out, i = [], 0
    while i < len(lines):
        m = ENTRY.match(lines[i].strip())
        if not m or not m.group(1).strip():
            i += 1
            continue
        company = m.group(1).strip()
        country = lines[i+1].strip() if i+1 < len(lines) else ''
        loc     = lines[i+2].strip() if i+2 < len(lines) else ''
        if '|' not in loc:               # a stray bullet in the chrome, not an entry
            i += 1
            continue
        exhibition, _, stand = loc.partition('|')
        bits = stand.strip().split()
        out.append({'company': company, 'country': country,
                    'exhibition': exhibition.strip(),
                    'pavilion': bits[0] if bits else '',
                    'stand': ' '.join(bits[1:]) if len(bits) > 1 else ''})
        i += 3
    return out

def main(paths):
    rows = []
    for p in paths:
        rows += parse(open(p, encoding='utf-8').read())

    # dedupe identical entries first, then group by stand
    uniq = {}
    for r in rows:
        uniq[(r['company'], r['pavilion'], r['stand'])] = r
    rows = list(uniq.values())

    groups = collections.defaultdict(list)
    for r in rows:
        groups[(r['exhibition'], r['pavilion'], r['stand'])].append(r)

    out = []
    for key, g in groups.items():
        names = sorted({x['company'] for x in g})
        primary = min(names, key=lambda n: (len(SUFFIX.sub('', n).strip()), len(n)))
        roots = {norm(n) for n in names}
        shared = ''
        if len(names) > 1:
            base = sorted(roots, key=len)[0]
            if not all(base in r or r in base or
                       difflib.SequenceMatcher(None, base, r).ratio() > 0.6 for r in roots):
                shared = 'SHARED_STAND_CHECK'
        out.append({'company': primary,
                    'aliases': ' ; '.join(n for n in names if n != primary),
                    'country': g[0]['country'], 'exhibition': g[0]['exhibition'],
                    'pavilion': g[0]['pavilion'], 'stand': g[0]['stand'],
                    'listings': len(names), 'flag': shared})

    out.sort(key=lambda r: r['company'].lower())
    COLS = ['company','aliases','country','exhibition','pavilion','stand','listings','flag']
    with open('salone_parsed.csv', 'w', newline='', encoding='utf-8-sig') as fh:
        w = csv.DictWriter(fh, fieldnames=COLS, quoting=csv.QUOTE_ALL)
        w.writeheader(); w.writerows(out)

    print('%d listings -> %d companies (%d duplicate listings collapsed)'
          % (len(rows), len(out), len(rows) - len(out)))
    print('exhibitions:', dict(collections.Counter(r['exhibition'] for r in out)))
    print('countries:', dict(collections.Counter(r['country'] for r in out).most_common(8)))
    merged = [r for r in out if r['listings'] > 1]
    if merged:
        print('\n%d stands held more than one listing:' % len(merged))
        for r in merged:
            print('  %s %-8s %-38s + %s %s' % (r['pavilion'], r['stand'],
                  r['company'][:38], r['aliases'][:60], r['flag']))

if __name__ == '__main__':
    main(sys.argv[1:] or ['raw.txt'])
