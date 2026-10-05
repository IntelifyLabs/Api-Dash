#!/usr/bin/env python3
"""Parse the Marmomac Brandrooms exhibitor listing into rows.

The portal renders three lines per exhibitor and nothing machine readable, so
the list arrives as pasted text:

    Hall 9 Stand B7
    ABDEEN STONE FOR MARBLE & GRANITE
    EGYPT

    Hall 7 Stand B2
    "KLINSYSTEM" SUPERABRASIVE ITALIA
    ITALY | Abruzzo | Pescara

A company with several stands puts them on the location line, truncated by the
UI: "Hall 6 Stand Avenue F - F4, Hall 7 ...". The ellipsis matters, because a
company whose FIRST stand is in scope can have a second one in a hall that is
out, and TENAX is exactly that case: Hall 6 plus Hall 7. The hall rule below
is therefore an any-match exclusion, not a first-match one.

HALL VERDICTS, from the 1,096 exhibitor listing on 5 Oct.

  OUT, no exceptions. 216 companies, 20% of the fair, removed for free before
  a single web search or credit:
    Hall 7  133  diamond tools, abrasives, resins, chemicals, sealants
    Hall 2   47  machinery, metalwork, waterjet, robotics, electronics
    Hall 5   36  sawing, polishing and handling machinery, CAD, surveying

  OUT except by name. Hall 9, 121 companies: quarries, block traders and
  marble and granite exporters. These sell raw and semi-finished stone B2B to
  fabricators, have no consumer-facing website and no catalogue a shopper
  browses, so the visualiser has nothing to sit on. Three exceptions found by
  eye, all engineered or branded surface houses that do market to end buyers,
  and they are kept by name rather than by hall.

  Hall 1, 28, is the BRAZIL PAVILION and is out. Not what I predicted: a
  Stone World piece on an earlier edition put "A Matter of Stone" there and I
  repeated it, so it went into the plan as the densest 28 rows at the fair.
  The paste says otherwise. All 28 are granite and marble houses from Espirito
  Santo, two of them openly mineracao, mining, and several comercio,
  importacao e exportacao. Fourteen share stands 10 and 10-11, which is a
  national collective booth rather than 14 brands. Same profile as hall 9:
  slab and block exporters selling B2B to fabricators, no consumer site.

  LESSON, and it cost a wrong recommendation. Hall contents cannot be
  predicted from a press article about a previous edition. The pasted listing
  is the only evidence, so no hall gets a verdict here until it has been seen.

  Still to be pasted: halls 8 (197), 6 (112), 10 (98), 11 (79), 12 (76),
  4 (40), 3 (30), Area B (41), Area D (23), Avenue E (23), Area A (20) and
  the five small ones. 731 companies, none of them predicted.
"""
import csv, re, sys, collections

HALL_OUT = {'7', '2', '5', '1'}
HALL_OUT_WHY = {
    '7': 'diamond tools, abrasives, resins and chemicals',
    '2': 'machinery, metalwork, waterjet and robotics',
    '5': 'sawing, polishing and handling machinery, CAD and surveying',
    '1': 'Brazil pavilion: granite and marble block and slab exporters',
}
# Hall 9 is quarries and block traders, out as a hall. These three are kept by
# name: engineered or branded surface houses with consumer-facing marketing.
HALL9_KEEP = {
    'CIMSTONE - AKG YALITIM VE INS. MALZ. SAN. VE TIC. A.S.': 'Cimstone, engineered quartz surface brand',
    'POKARNA LIMITED': 'Quantra quartz surfaces, brand sells to end buyers',
    'Lundhs AS': 'Lundhs Real Stone, a marketed consumer brand',
}

LOC = re.compile(r'\b(?:Hall|Area|Avenue)\s+([\w.]+)|\bS\.C\.\s*Arena|\bGM\b')
STAND = re.compile(r'Stand\s+([^,]+)')

def parse(text):
    """Group the stream into 3-line records. A record is a location line, a
    company line, then an optional country line."""
    lines = [l.strip() for l in text.splitlines()]
    out, i = [], 0
    while i < len(lines):
        l = lines[i]
        if not l or not (l.startswith(('Hall ', 'Area ', 'Avenue ', 'S.C.', 'GM')) and 'Stand' in l or l.startswith(('Hall ', 'Area ', 'Avenue '))):
            i += 1
            continue
        loc = l
        company = lines[i+1] if i+1 < len(lines) else ''
        geo = lines[i+2] if i+2 < len(lines) else ''
        if not company or company.startswith(('Hall ', 'Area ', 'Avenue ')):
            i += 1
            continue
        if geo.startswith(('Hall ', 'Area ', 'Avenue ')) or not geo:
            geo = ''
            i += 2
        else:
            i += 3
        halls = [h for h in LOC.findall(loc) if h]
        parts = [p.strip() for p in geo.split('|')]
        out.append({
            'company': company.strip().strip('"'),
            'halls': ';'.join(halls),
            'stands': ';'.join(s.strip() for s in STAND.findall(loc)),
            'truncated': 'yes' if '...' in loc else '',
            'country': parts[0] if parts and parts[0] else '',
            'region': parts[1] if len(parts) > 1 else '',
            'province': parts[2] if len(parts) > 2 else '',
        })
    return out

def verdict(r):
    halls = set(r['halls'].split(';')) - {''}
    bad = halls & HALL_OUT
    if bad:
        h = sorted(bad)[0]
        return 'OUT', f'hall {h}: {HALL_OUT_WHY[h]}'
    if r['company'] in HALL9_KEEP:
        return 'KEEP', HALL9_KEEP[r['company']]
    if '9' in halls:
        return 'OUT', 'hall 9: quarry, block trader or stone exporter. No consumer site'
    if r['truncated']:
        return 'CHECK', 'stand list was truncated by the UI, confirm no hall 2, 5 or 7 stand'
    if not halls:
        return 'CHECK', 'no stand recorded'
    return 'IN', 'in a finished-product or design hall'

def main(paths):
    rows = []
    for p in paths:
        rows += parse(open(p, encoding='utf-8').read())
    seen = {}
    for r in rows:                      # one row per company, halls merged
        k = r['company'].lower()
        if k in seen:
            h = set(seen[k]['halls'].split(';')) | set(r['halls'].split(';'))
            seen[k]['halls'] = ';'.join(sorted(h - {''}))
            seen[k]['truncated'] = seen[k]['truncated'] or r['truncated']
        else:
            seen[k] = r
    rows = list(seen.values())
    for r in rows:
        r['verdict'], r['why'] = verdict(r)
    COLS = ['company','halls','stands','country','region','province','truncated','verdict','why']
    with open('marmomac_parsed.csv', 'w', newline='', encoding='utf-8-sig') as fh:
        w = csv.DictWriter(fh, fieldnames=COLS, quoting=csv.QUOTE_ALL)
        w.writeheader(); w.writerows(rows)
    print('%d companies parsed' % len(rows))
    for v, n in collections.Counter(r['verdict'] for r in rows).most_common():
        print('  %4d  %s' % (n, v))
    print()
    for why, n in collections.Counter(r['why'] for r in rows).most_common():
        print('  %4d  %s' % (n, why))
    print('\ncountries, in-scope rows only:')
    for c, n in collections.Counter(r['country'] for r in rows if r['verdict'] in ('IN','KEEP','CHECK')).most_common(12):
        print('  %4d  %s' % (n, c))

if __name__ == '__main__':
    main(sys.argv[1:] or ['raw_halls.txt'])
