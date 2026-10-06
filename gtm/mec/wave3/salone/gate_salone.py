#!/usr/bin/env python3
"""Apply the event gate to the Salone catalogue and report what is left.

Event codes, confirmed from the data rather than guessed. EIM was the only one
that needed identifying by hand and its categories settle it: Acoustics,
Office accessories, Seating for offices and public spaces. That is
Workplace 3.0.

    TAKE                                                      rows
    SMI  Salone Internazionale del Mobile, the main fair        768
    ARB  Arredobagno, the International Bathroom Exhibition     173
    S_P  S.Project, decorative and technical interior           69
    EUC  EuroCucina                                             63

    SKIP
    CDA  Complemento d'Arredo, furnishing accessories           146
         homeware and textiles. A vase in a room photo is not a
         buying decision.
    FTK  Technology For the Kitchen                              41
         appliances. No studio renders an oven.
    RAR  Salone Raritas                                          28
         curated collectible design, one-off pieces, no catalogue.
    EIM  Workplace 3.0                                           25
         office and contract. Sells to facilities managers, no
         consumer web traffic, so the whole mechanic fails.

Studio routing is by event, with the product text as a tiebreak: ARB and EUC
and SMI go to /furniture, and S_P splits because it carries both surfaces and
bathroom fittings.
"""
import csv, collections, re, json

TAKE = {'SMI': 'Salone Internazionale del Mobile',
        'ARB': 'International Bathroom Exhibition',
        'S_P': 'S.Project',
        'EUC': 'EuroCucina'}
SKIP = {'CDA': 'furnishing accessories, homeware and textiles',
        'FTK': 'kitchen technology and appliances',
        'RAR': 'Raritas, collectible one-off design',
        'EIM': 'Workplace 3.0, office and contract'}

# Routing by product text was a trap. Matching "marble" or "stone" against
# the product list flagged 208 rows as surfaces, and they are furniture:
# "Marble dining tables", "Metal and glass dining tables", "Wooden side
# tables". A marble table top is a piece of furniture, not a worktop, and the
# Furniture Studio is what stands it on the floor at its real size.
#
# S_P carries no usable signal either. All 69 rows share one category string,
# "Decorative, furnishing and technical proposals and solutions for interior
# and exterior architecture", so it cannot be split by text at all. Those rows
# are routed to furniture and flagged for a look, since S.Project genuinely
# mixes surfaces with bathroom fittings and some of them belong in
# /countertops or /tile.
SURFACE = re.compile(r'\b(wall ?covering|wallpaper|mural|worktop|countertop|'
                     r'kitchen top|slab|sintered|porcelain stoneware)', re.I)
RUG     = re.compile(r'\b(rug|carpet|moquette)', re.I)

def studio(r):
    txt = (r['categories'] or '') + ' ' + (r['products'] or '')
    if RUG.search(txt):      return 'rugs'
    if SURFACE.search(txt):  return 'countertops'
    return 'furniture'

def dom(u):
    u = re.sub(r'^https?://', '', (u or '').strip().lower())
    return re.sub(r'^www\.', '', u).split('/')[0].strip()

# Companies already being emailed in wave 2 must not receive a second
# sequence. 26 of them exhibit here too, Atlas Concorde and Laminam and Roca
# among them, because a tile or sanitaryware brand shows at Cersaie AND at
# Salone. Matched on domain first, then on name.
LIVE = '../../wave2/copy/MEC_Instantly_Wave2.csv'
try:
    live = list(csv.DictReader(open(LIVE, encoding='utf-8-sig')))
    LIVE_DOM = {dom(r['website']) for r in live if r['website']}
    LIVE_NAME = {r['company_name'].strip().lower() for r in live}
except FileNotFoundError:
    LIVE_DOM, LIVE_NAME = set(), set()

rows = list(csv.DictReader(open('salone_2026.csv', encoding='utf-8-sig')))
for r in rows:
    if r['event'] not in TAKE:
        r['verdict'], r['why'] = 'skip', SKIP.get(r['event'], 'unknown event code')
    elif dom(r['website']) in LIVE_DOM or r['company'].strip().lower() in LIVE_NAME:
        r['verdict'], r['why'] = 'already live', 'already in the wave 2 campaign'
    else:
        r['verdict'], r['why'] = 'take', TAKE[r['event']]
    r['studio'] = studio(r) if r['verdict'] == 'take' else ''
    r['flag'] = 'S_P, check studio by hand' if r['verdict'] == 'take' and r['event'] == 'S_P' else ''

take = [r for r in rows if r['verdict'] == 'take']

# One record per company. A firm exhibiting at both SMI and ARB is one website
# and one mailbox, so paying for it twice is the waste that got the 126-row
# recovery vetoed last week.
by = {}
for r in sorted(take, key=lambda x: list(TAKE).index(x['event'])):
    k = (r['website'] or r['company']).strip().lower().replace('www.', '')
    if k in by:
        if r['event'] not in by[k]['event']:
            by[k]['event'] += ';' + r['event']
        continue
    by[k] = dict(r)
uniq = sorted(by.values(), key=lambda r: r['company'].lower())

COLS = ['company','website','email','email2','phone','country','town','province',
        'address','event','hall','stand','brands','categories','products',
        'account_id','verdict','why','studio','flag']
with open('salone_2026_gated.csv','w',newline='',encoding='utf-8-sig') as fh:
    w = csv.DictWriter(fh, fieldnames=COLS, quoting=csv.QUOTE_ALL)
    w.writeheader(); w.writerows(uniq)

print('%d catalogue rows' % len(rows))
print('  take %d, skip %d' % (len(take), len(rows)-len(take)))
print('  after collapsing companies listed at more than one event: %d' % len(uniq))
print()
print('by event, taken:', dict(collections.Counter(r['event'] for r in take)))
print('by event, skipped:', dict(collections.Counter(r['event'] for r in rows if r['verdict']=='skip')))
print('already live, excluded:', sum(1 for r in rows if r['verdict']=='already live'))
print('studio:', dict(collections.Counter(r['studio'] for r in uniq)))
print()
print('website present : %d of %d' % (sum(1 for r in uniq if r['website']), len(uniq)))
print('email present   : %d of %d' % (sum(1 for r in uniq if r['email']), len(uniq)))
print('second email    : %d' % sum(1 for r in uniq if r['email2'] and r['email2']!=r['email']))
print('country:', dict(collections.Counter(r['country'] for r in uniq).most_common(10)))
