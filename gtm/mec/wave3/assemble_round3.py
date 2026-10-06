#!/usr/bin/env python3
"""Assemble round 3: Salone + Heimtextil into one list, ready for enrichment.

THREE INPUTS

  salone/salone_2026_gated.csv     850 companies, event-gated
  heimtextil/heimtextil.csv      1,412 companies, the full API pull
  the Heimtextil watchlist xlsx    494 companies Shahwaz selected BY HALL,
                                   and the only source of stand numbers

THE WATCHLIST FIXED A HOLE IN MY GATE. The category gate took 148 of 1,412.
Cross-checking it against the 494 hand-picked rows showed 368 of them skipped,
and 177 of those had booked NO CATEGORY AT ALL. My gate read an empty category
as out of scope when it means unclassified, and 30 of the 177 sitting in hall
3.0 are exactly the ICP: Erismann, York WallCoverings, Wallquest, Anstey
Wallpaper, G&B Home Living. Real wallpaper brands, missed because they had not
filled in a form.

So HALL is the fallback signal, and the halls were verified against
Heimtextil's own 2027 layout:

    3.0            wallpaper, hand-knotted rugs, premium flooring -> wallpaper
    11.0 12.0 12.1 carpets and rugs, volume manufacturers        -> rugs
    3.1            fibres, yarns, technologies                    skip, raw input
    4.2            textile and surface DESIGN studios             skip, see below
    4.0 4.1 5.0 5.1 8.0 9.0                                       skip, bed/bath/linen

HALL 4.2 IS A DISAGREEMENT, NOT A BUG. 74 of the picks are design studios:
YUNO Design Studio, Studio 1987, CD Design Studio, The PatternClub, Creantes.
They sell DESIGNS to manufacturers, so there is no catalogue a shopper browses
and no installed product to render. They are suppliers to our ICP. They are
marked 'excluded, design studio' rather than silently dropped, so the call is
visible and reversible with one edit.

RUG EXPORT HOUSES stay flagged rather than counted. 213 of the 494 picks are
India, and Bhadohi and Jaipur export houses sell to importers, not to
shoppers. Same business model that made Marmomac's quarries worthless here.
Marked 'review'.

Everything already in wave 2 or in the Salone half is dropped on domain, so
nobody gets a second sequence.
"""
import csv, re, html, collections, os, sys

HALL_STUDIO = {'3.0': 'wallpaper', '11.0': 'rugs', '12.0': 'rugs', '12.1': 'rugs'}
HALL_SKIP = {'3.1': 'fibres, yarns and textile technology',
             '4.2': 'design studio, sells designs to manufacturers'}
EXPORT_HUB = {'India', 'Pakistan', 'Egypt', 'Türkiye', 'Turkey', 'Nepal',
              'China', 'Bangladesh', 'Viet Nam', 'Vietnam'}

def dom(u):
    u = re.sub(r'^https?://', '', (u or '').strip().lower())
    return re.sub(r'^www\.', '', u).split('/')[0]

def clean(v):
    return re.sub(r'\s+', ' ', html.unescape(v or '')).strip()

def norm(n):
    return re.sub(r'[^a-z0-9]', '', clean(n).lower())

def load_watchlist(path):
    try:
        import openpyxl
    except ImportError:
        print('openpyxl missing, watchlist skipped'); return {}
    ws = openpyxl.load_workbook(path, data_only=True)['HEIMTEXTIL']
    rows = [[(str(c).strip() if c is not None else '') for c in r]
            for r in ws.iter_rows(values_only=True)]
    h = next(i for i, r in enumerate(rows) if r and r[0] == 'Organisation')
    out = {}
    for r in rows[h+1:]:
        if not r or not r[0]:
            continue
        d = dict(zip(rows[h], r))
        loc = d.get('Hall') or ''
        hall, _, stand = loc.partition(',')
        out[norm(d['Organisation'])] = {
            'hall': hall.replace('Hall', '').strip(),
            'stand': stand.strip(),
            'picked': 'yes',
        }
    return out

# ── wave 2, so nobody is emailed twice ───────────────────────────────
live = set()
for r in csv.DictReader(open('../wave2/copy/MEC_Instantly_Wave2.csv', encoding='utf-8-sig')):
    if r['website']: live.add(dom(r['website']))
    live.add(norm(r['company_name']))

COLS = ['company', 'website', 'email', 'email2', 'phone', 'country', 'city',
        'address', 'source', 'event', 'hall', 'stand', 'picked', 'categories',
        'products', 'studio', 'verdict', 'why']

out = []

# ── Salone ───────────────────────────────────────────────────────────
for r in csv.DictReader(open('salone/salone_2026_gated.csv', encoding='utf-8-sig')):
    out.append({
        'company': clean(r['company']), 'website': r['website'], 'email': r['email'],
        'email2': r['email2'], 'phone': r['phone'], 'country': r['country'],
        'city': r['town'], 'address': r['address'], 'source': 'Salone del Mobile 2026',
        'event': r['event'], 'hall': r['hall'], 'stand': r['stand'], 'picked': '',
        'categories': r['categories'], 'products': r['products'],
        'studio': r['studio'] or 'furniture',
        'verdict': 'review' if r.get('flag') else 'take',
        'why': r.get('flag') or r['why'],
    })

# ── Heimtextil ───────────────────────────────────────────────────────
WL = load_watchlist(sys.argv[1]) if len(sys.argv) > 1 else {}
for r in csv.DictReader(open('heimtextil/heimtextil.csv', encoding='utf-8-sig')):
    key = norm(r['company'])
    wl = WL.get(key, {})
    hall = (wl.get('hall') or (r['halls'] or '').split(';')[0] or '').strip()
    studio, verdict, why = r['studio'], r['verdict'], r['why']

    # The fix: an empty category is unclassified, so fall back to the hall.
    #
    # The hall is a weaker signal than a booked category and it has to be
    # treated that way. Hall 3.0 holds wallpaper AND curtains AND sun
    # protection, so routing on 3.0 alone recovered Erismann, Anstey Wallpaper
    # and Brink & Campman, all real brands, but also Fotoba International,
    # which makes digital cutting machines, and Attica Narrow Fabrics, whose
    # domain is curtaintapes.gr. So a hall-routed row is TAKE only when its
    # name or domain carries a product signal, and REVIEW otherwise. Review is
    # not rejection: Erismann's own name says nothing, and it is a 1838
    # wallpaper house.
    if not studio:
        if hall in HALL_STUDIO and not r['categories']:
            studio = HALL_STUDIO[hall]
            if hall == '3.0':
                # Only 3.0 is mixed, so only 3.0 needs the name check.
                txt = (r['company'] + ' ' + r['website']).lower()
                strong = re.search(r'wallpaper|wallcover|tapet|mural|decopr|'
                                   r'\brug\b|rugs|carpet|teppich|moquette|flooring', txt)
                verdict = 'take' if strong else 'review'
                why = ('hall 3.0 and a wallpaper or floor signal in the name'
                       if strong else
                       'hall 3.0 is wallpaper plus curtains and sun protection, '
                       'confirm which this is')
            else:
                # 11.0, 12.0 and 12.1 are Carpets & Rugs end to end in Messe
                # Frankfurt's own 2027 layout, nothing else books them, so the
                # hall alone is enough. The export-house check below still
                # applies on top.
                verdict = 'take'
                why = 'no category booked, hall %s is Carpets & Rugs only' % hall
        elif hall in HALL_SKIP:
            verdict, why = 'excluded', HALL_SKIP[hall]
    if studio and hall in HALL_SKIP:
        verdict, why = 'excluded', HALL_SKIP[hall]
    if verdict in ('take',) and studio == 'rugs' and r['country'] in EXPORT_HUB:
        verdict = 'review'
        why = 'rug export house, confirm it sells to end buyers and not only to importers'
    if verdict == 'skip':
        continue

    out.append({
        'company': clean(r['company']), 'website': r['website'], 'email': r['email'],
        'email2': '', 'phone': r['phone'], 'country': r['country'], 'city': r['city'],
        'address': r['street'], 'source': 'Heimtextil 2027', 'event': 'HEIMTEXTIL',
        'hall': hall, 'stand': wl.get('stand', ''), 'picked': wl.get('picked', ''),
        'categories': r['categories'], 'products': r['products'],
        'studio': studio, 'verdict': verdict, 'why': why,
    })

# ── dedupe and drop anything already live ────────────────────────────
seen, final = set(), []
for r in out:
    k = dom(r['website']) or norm(r['company'])
    if not k or k in seen:
        continue
    if dom(r['website']) in live or norm(r['company']) in live:
        continue
    seen.add(k); final.append(r)

final.sort(key=lambda r: (r['verdict'] != 'take', r['studio'], r['company'].lower()))
with open('round3_companies.csv', 'w', newline='', encoding='utf-8-sig') as fh:
    w = csv.DictWriter(fh, fieldnames=COLS, quoting=csv.QUOTE_ALL)
    w.writeheader(); w.writerows(final)

print('%d rows assembled\n' % len(final))
print('verdict: ', dict(collections.Counter(r['verdict'] for r in final)))
print('source:  ', dict(collections.Counter(r['source'] for r in final)))
print('studio:  ', dict(collections.Counter(r['studio'] for r in final)))
print()
tak = [r for r in final if r['verdict'] == 'take']
print('TAKE: %d | website %d | email %d' % (len(tak),
      sum(1 for r in tak if r['website']), sum(1 for r in tak if r['email'] or r['email2'])))
print('  studio:', dict(collections.Counter(r['studio'] for r in tak)))
print('  from your watchlist pick:', sum(1 for r in tak if r['picked']))
print()
print('by verdict and why:')
for (v, why), n in collections.Counter((r['verdict'], r['why'][:62]) for r in final).most_common(14):
    print('  %-8s %4d  %s' % (v, n, why))
