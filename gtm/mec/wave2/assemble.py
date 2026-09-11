# -*- coding: utf-8 -*-
"""Assemble all wave-2 sourcing into one Clay-ready CSV.

Columns follow S7.5 (company, website, niche, source, country) plus the
S7.7 'row_type' flag so firmographic enrichment can be gated on new rows
and never re-charges the 67 seed rows.

Nothing is dropped. Rows that failed a free pre-check carry a pre_flag and
a reason, so they can be filtered in Clay rather than silently missing.
"""
import csv, re
from openpyxl import load_workbook

OUT = 'MEC_Wave2_Clay_Upload.csv'

def norm_name(s):
    s = s.lower()
    s = re.sub(r'\b(inc|llc|ltd|srl|s\.r\.l|spa|s\.p\.a|sa|s\.a|co|company|corp|the|dba|'
               r'limited|gmbh|kg|ag|nv|bv|pte|llp|pvt|sp z oo|lda|aps|as)\b', '', s)
    return re.sub(r'[^a-z0-9]', '', s)

def domain(u):
    if not u: return ''
    u = str(u).strip().lower()
    u = re.sub(r'^https?://', '', u).replace('www.', '')
    return u.split('/')[0].split('?')[0].strip()

rows = []

# ---- Cersaie: richest source, has website + email + address -----------------
wb = load_workbook('cersaie_exhibitors.xlsx', read_only=True)
for r in list(wb['export'].iter_rows(values_only=True))[1:]:
    if not r or not r[0]: continue
    d = dict(zip(('NAME','ADDRESS','ZIP','TOWN','STATE','NATION','PHONE','FAX','WEB','EMAIL','BOOTH'), r))
    rows.append({
        'company': str(d['NAME']).strip(),
        'website': str(d['WEB'] or '').strip(),
        'domain': domain(d['WEB']),
        'generic_email': str(d['EMAIL'] or '').strip(),
        'country': str(d['NATION'] or '').strip(),
        'town': str(d['TOWN'] or '').strip(),
        'stand': str(d['BOOTH'] or '').strip(),
        'niche': 'Ceramic / Tile (verify)',
        'source': 'Cersaie 2026',
    })

# ---- TCNA: US tile manufacturers, $3M+ membership --------------------------
for n in [l.strip() for l in open('tcna_raw.txt', encoding='utf-8') if l.strip()]:
    rows.append({'company': n, 'website': '', 'domain': '', 'generic_email': '',
                 'country': 'US', 'town': '', 'stand': '',
                 'niche': 'Decorative / Artisan Tile', 'source': 'TCNA'})

# ---- Coverings -------------------------------------------------------------
for n in [l.strip() for l in open('coverings_raw.txt', encoding='utf-8') if l.strip()]:
    rows.append({'company': n, 'website': '', 'domain': '', 'generic_email': '',
                 'country': '', 'town': '', 'stand': '',
                 'niche': 'Tile / Stone (verify)', 'source': 'Coverings 2027'})

# ---- Heimtextil: hall number decides the niche and the exclusion -----------
for line in [l.strip() for l in open('heimtextil_raw.txt', encoding='utf-8') if l.strip()]:
    n, hall = line.split('|')
    rows.append({'company': n.strip(), 'website': '', 'domain': '', 'generic_email': '',
                 'country': '', 'town': '', 'stand': hall.strip(),
                 'niche': 'Murals & Wallcoverings' if hall.startswith('3.0') else 'Textile Design',
                 'source': 'Heimtextil 2027'})

# ---- TISE ------------------------------------------------------------------
for n in [l.strip() for l in open('tise_raw.txt', encoding='utf-8') if l.strip()]:
    rows.append({'company': n, 'website': '', 'domain': '', 'generic_email': '',
                 'country': '', 'town': '', 'stand': '',
                 'niche': 'Stone / Tile (verify)', 'source': 'TISE 2027'})

# ---- free pre-checks: flag, never drop ------------------------------------
PATTERN_SELLER = {'avdesigninhallavaysman','clairelouisedesigns','haleystudios',
                  'kaleidoscopesurfacedesignolesjabreuer','kritikunal','leedesignstudio',
                  'onnoraadersma','sandrajacobsdesign'}
OUT_WORDS = re.compile(
    r'\b(tool|tools|machin|adhesiv|abrasiv|diamond|saw|blade|grout|mortar|sealant|primer|'
    r'packag|imballagg|logistic|freight|software|patent|publish|editor|press|consult|'
    r'quarry|limestone|granite|marble|travertin|slab|quartz|moulding|molding|louver|'
    r'parquet|legno|laminat|vinyl|lvt|spc|wpc|carpet|rug|flooring|underlay|'
    r'sanitar|rubinett|bagno|shower|doccia|import|export|wholesale|distribut)\b', re.I)

def pre_flag(r):
    key = norm_name(r['company'])
    if key in PATTERN_SELLER:
        return ('EXCLUDE', 'Heimtextil hall 4.2 textile design studio. Sells original patterns to '
                           'manufacturers, which is what the tool generates. Wrong side of the trade')
    blob = f"{r['company']} {r['website']} {r['niche']}"
    m = OUT_WORDS.search(blob)
    if m:
        return ('LIKELY OUT', f"name or domain suggests '{m.group(0)}'. Supplier, trader or wrong "
                              f"medium. Confirm on the site before spending credits")
    if not r['domain']:
        return ('NEEDS DOMAIN', 'no website from the directory. Resolve the domain before any '
                                'other enrichment, since every downstream step needs it')
    return ('NEEDS EYES', 'passes the free checks. Run gates 3 to 5 on the site')

# ---- dedupe by domain first, then by normalised name ----------------------
seen, merged = {}, []
for r in rows:
    key = r['domain'] or ('name:' + norm_name(r['company']))
    if key in seen:
        prev = seen[key]
        # a shared domain is usually one parent with several exhibiting brands
        # (Porcelanosa shows 6, Gruppo Bardelli 4). Keep one row per company per
        # S7.4, but never lose the brand names.
        prev.setdefault('_brands', []).append(r['company'])
        if r['source'] not in prev['source'].split(' + '):
            prev['source'] = prev['source'] + ' + ' + r['source']
        for f in ('website','domain','generic_email','country','town','stand'):
            if not prev[f] and r[f]: prev[f] = r[f]
        continue
    seen[key] = r
    merged.append(r)

for r in merged:
    r['also_trading_as'] = ' | '.join(r.pop('_brands', []))

for r in merged:
    r['pre_flag'], r['pre_flag_reason'] = pre_flag(r)
    r['row_type'] = 'new'          # S7.7: gate firmographic enrichment on this
    r['wave'] = 'wave2'

COLS = ['company','website','domain','country','town','niche','source','stand',
        'generic_email','also_trading_as','pre_flag','pre_flag_reason','row_type','wave']
with open(OUT, 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.DictWriter(f, fieldnames=COLS, quoting=csv.QUOTE_ALL)
    w.writeheader(); w.writerows(merged)

from collections import Counter
print(f'{OUT}: {len(merged)} rows  (from {len(rows)} raw, {len(rows)-len(merged)} merged as duplicates)')
print('\nby source:')
for k, v in Counter(r['source'] for r in merged).most_common(): print(f'  {v:>4}  {k}')
print('\nby pre_flag:')
for k, v in Counter(r['pre_flag'] for r in merged).most_common(): print(f'  {v:>4}  {k}')
print(f"\nrows with a website: {sum(1 for r in merged if r['domain'])}/{len(merged)}")
