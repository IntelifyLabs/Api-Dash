#!/usr/bin/env python3
"""Round 3 text gate. Free, no Clay. Rules are in CLASSIFIER.md.

Runs over `categories` + `products`, which for round 3 is the exhibitor's own
booking rather than a scraped third-party description, so it can be strict
without guessing.

Gate 1, the category gate, already ran during sourcing. This is gate 2: it
kills what gate 1 let through. Gate 3, revenue, is deliberately not applied,
because the round 3 APIs carry no revenue field and inventing one from country
or product count would be invention. Gate 4 is the website pass and runs next.
"""
import csv, re, collections

def rx(*w): return re.compile('|'.join(w), re.I)

# ── wrong business: a supplier to our ICP, or not a maker at all ─────
OUT_BUSINESS = [
    (rx(r'\bmachin', r'maschine', r'macchin', r'\bcnc\b', r'production line',
        r'\bkiln\b', r'press(es|ing) line'),            'machinery'),
    (rx(r'\babrasiv', r'diamond tool', r'\btooling\b', r'grinding wheel',
        r'saw blade'),                                   'tools and abrasives'),
    (rx(r'\badhesiv', r'\bglue\b', r'\bgrout\b', r'\bsealant', r'\bprimer\b',
        r'\bresin\b', r'\bpigment', r'\bink(s)?\b', r'mortar'), 'chemicals'),
    (rx(r'\bsoftware\b', r'\bsaas\b', r'\berp\b', r'\bcad\b',
        r'rendering software'),                          'software'),
    (rx(r'\bmagazine\b', r'publish(er|ing)', r'trade fair', r'\bassociation\b',
        r'consorzio', r'federation', r'\binstitute\b'),  'press or association'),
    (rx(r'\blogistic', r'\bfreight\b', r'forwarding', r'\bpackaging\b'), 'logistics or packaging'),
    (rx(r'laborator', r'\btesting\b', r'certification body'), 'testing or certification'),
]

# ── wrong medium: nothing any studio can render ──────────────────────
OUT_MEDIUM = [
    (rx(r'\bfibre', r'\bfiber', r'\byarn', r'\bthread\b', r'filament',
        r'non.?woven', r'\bgreige\b', r'raw material'),  'fibres, yarns, raw material'),
    (rx(r'curtain tape', r'\bblind(s)? component', r'roller mechanism',
        r'\bpelmet', r'curtain track'),                  'curtain and blind components'),
    (rx(r'\bappliance', r'\boven\b', r'\bhob\b', r'extractor hood',
        r'dishwasher', r'\bfaucet', r'\btap(s)? and mixer', r'thermostatic'), 'appliances or taps, no studio'),
    (rx(r'\blighting\b', r'\bluminaire', r'\bpendant lamp', r'\blamp(s)?\b',
        r'chandelier'),                                  'lighting, no studio'),
    (rx(r'pattern design service', r'design archive', r'surface design studio',
        r'print studio'),                                'sells designs to manufacturers'),
]

# ── what we are looking FOR, so a mixed description is not killed ────
IN_PRODUCT = rx(
    r'\bsofa', r'armchair', r'\bchair\b', r'\bstool\b', r'\btable\b', r'\bbed\b',
    r'wardrobe', r'bookcase', r'sideboard', r'cabinet', r'\bvanit', r'washbasin',
    r'bathroom furniture', r'kitchen furniture', r'\bcupboard', r'\bshelv',
    r'\brug(s)?\b', r'\bcarpet', r'moquette', r'\bkilim', r'dhurrie', r'\btufted\b',
    r'wallpaper', r'wallcovering', r'wall covering', r'\bmural', r'\btapet',
    r'\bworktop', r'countertop', r'\bslab(s)?\b', r'\bsurface(s)?\b',
    r'\btile(s)?\b', r'\bstone\b', r'\bmarble\b', r'porcelain', r'ceramic',
    r'\bflooring\b', r'parquet', r'\bdecking\b', r'sanitaryware',
)

def gate2(r):
    """Returns (verdict, reason). Only ever tightens gate 1."""
    txt = (r['categories'] or '') + ' ' + (r['products'] or '') + ' ' + (r['company'] or '')
    if not txt.strip():
        return r['verdict'], r['why']
    wants = bool(IN_PRODUCT.search(txt))
    for bank, label in OUT_BUSINESS:
        m = bank.search(txt)
        if m:
            return 'excluded', 'gate 2, wrong business: %s (%s)' % (label, m.group(0))
    for bank, label in OUT_MEDIUM:
        m = bank.search(txt)
        # A maker whose list ALSO names a product we render stays in: a
        # bathroom furniture house that happens to list a tap is still a
        # bathroom furniture house.
        if m and not wants:
            return 'excluded', 'gate 2, wrong medium: %s (%s)' % (label, m.group(0))
    return r['verdict'], r['why']

rows = list(csv.DictReader(open('round3_companies.csv', encoding='utf-8-sig')))
before = collections.Counter(r['verdict'] for r in rows)
moved = []
for r in rows:
    if r['verdict'] == 'excluded':
        continue
    v, w = gate2(r)
    if v != r['verdict']:
        moved.append((r['company'], w))
        r['verdict'], r['why'] = v, w

with open('round3_companies.csv', 'w', newline='', encoding='utf-8-sig') as fh:
    out = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), quoting=csv.QUOTE_ALL)
    out.writeheader(); out.writerows(rows)

after = collections.Counter(r['verdict'] for r in rows)
print('gate 2, the free text gate\n')
print('  before:', dict(before))
print('  after :', dict(after))
print('\n  %d rows moved out by gate 2:' % len(moved))
for why, n in collections.Counter(w for _, w in moved).most_common():
    print('    %3d  %s' % (n, why))
print('\n  examples:')
for c, w in moved[:10]:
    print('    %-40s %s' % (c[:40], w[:64]))
