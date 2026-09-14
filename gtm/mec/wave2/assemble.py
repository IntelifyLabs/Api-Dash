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

# ---- hand-researched domains for the four directories without a WEB column --
# Only Cersaie exports websites. TCNA, Coverings, Heimtextil and TISE all export
# names alone, which blocked company enrichment outright since every downstream
# Clay step needs a domain. All 143 were resolved by hand, by web search over
# each company's own indexed pages. No Clay call was made for any of it.
#
# Each *_domains.csv carries domain, alt domain, city, a confidence marker and a
# free gate verdict per row. Rows with confidence 'none' have no website at all
# and rows with 'unresolved' need the exhibitor listing itself; both are real
# findings, not gaps, so they stay in the file and carry their reason.
def research(path):
    return {r['company']: r for r in csv.DictReader(open(path, encoding='utf-8-sig'))}

RESEARCH = {'tcna': research('tcna_domains.csv'),
            'coverings': research('coverings_domains.csv'),
            'heimtextil': research('heimtextil_domains.csv'),
            'tise': research('tise_domains.csv')}

def researched(key, name, base):
    t = RESEARCH[key][name]          # KeyError here means a raw file and its research drifted
    base.update({'website': f"https://{t['domain']}" if t['domain'] else '',
                 'domain': t['domain'],
                 'town': base['town'] or t['city'],
                 'country': base['country'] or t['country'],
                 'domain_confidence': t['confidence'],
                 'research_flag': t['gate_flag'],
                 'research_note': t['research_note']})
    return base

# ---- TCNA: US tile manufacturers, $3M+ membership --------------------------
for n in [l.strip() for l in open('tcna_raw.txt', encoding='utf-8') if l.strip()]:
    rows.append(researched('tcna', n, {
        'company': n, 'website': '', 'domain': '', 'generic_email': '',
        'country': 'US', 'town': '', 'stand': '',
        'niche': 'Decorative / Artisan Tile', 'source': 'TCNA'}))

# ---- Coverings -------------------------------------------------------------
# The research filled the country field too, which the filtered export left
# blank, and several rows sit nowhere near where the name suggests: Yukari reads
# Turkish and is Japanese-Italian, Rafias carries an Italian S.r.l. and is
# Argentine. Country comes from the research file's own country column, never
# from a two-letter subdivision code (see write_domains.py) - that guess is what
# turned Bisazza's Vicenza into the Virgin Islands three times.
for n in [l.strip() for l in open('coverings_raw.txt', encoding='utf-8') if l.strip()]:
    r = researched('coverings', n, {
        'company': n, 'website': '', 'domain': '', 'generic_email': '',
        'country': '', 'town': '', 'stand': '',
        'niche': 'Tile / Stone (verify)', 'source': 'Coverings 2027'})
    rows.append(r)

# ---- Heimtextil: hall number decides the niche and the exclusion -----------
for line in [l.strip() for l in open('heimtextil_raw.txt', encoding='utf-8') if l.strip()]:
    n, hall = line.split('|')
    n = n.strip()
    r = researched('heimtextil', n, {
        'company': n, 'website': '', 'domain': '', 'generic_email': '',
        'country': '', 'town': '', 'stand': hall.strip(),
        'niche': 'Murals & Wallcoverings' if hall.startswith('3.0') else 'Textile Design',
        'source': 'Heimtextil 2027'})
    rows.append(r)

# ---- TISE ------------------------------------------------------------------
for n in [l.strip() for l in open('tise_raw.txt', encoding='utf-8') if l.strip()]:
    r = researched('tise', n, {
        'company': n, 'website': '', 'domain': '', 'generic_email': '',
        'country': '', 'town': '', 'stand': '',
        'niche': 'Stone / Tile (verify)', 'source': 'TISE 2027'})
    rows.append(r)

# ---- free pre-checks: flag, never drop ------------------------------------
# The hall-4.2 pattern-seller set that used to live here is gone: all 23
# Heimtextil rows now carry a hand verdict, which supersedes it. The research
# also corrected one of its calls. Claire Louise Designs was excluded here as a
# studio selling patterns to manufacturers; she in fact designs AND prints onto
# her own cushions and kitchenware for John Lewis, so she is on the right side
# of the trade and fails on revenue instead. Same verdict, wrong reason.
OUT_WORDS = re.compile(
    r'\b(tool|tools|machin|adhesiv|abrasiv|diamond|saw|blade|grout|mortar|sealant|primer|'
    r'packag|imballagg|logistic|freight|software|patent|publish|editor|press|consult|'
    r'quarry|limestone|granite|marble|travertin|slab|quartz|moulding|molding|louver|'
    r'parquet|legno|laminat|vinyl|lvt|spc|wpc|carpet|rug|flooring|underlay|'
    r'sanitar|rubinett|bagno|shower|doccia|import|export|wholesale|distribut)\b', re.I)

def pre_flag(r):
    """A hand verdict outranks the keyword heuristics. Order matters here:
    a row that already fails gate 3 needs no domain resolved at all, so
    LIKELY OUT is checked before the missing-domain case. Standing rule 1."""
    rf = r.get('research_flag')
    if rf:
        head = rf.split()[0].rstrip(',')
        reason = f"{rf}. {r['research_note']}"
        if head == 'EXCLUDE':   return ('EXCLUDE', reason)
        if head == 'LIKELY':    return ('LIKELY OUT', reason)
        if not r['domain']:     return ('NEEDS DOMAIN', reason)
        return ('NEEDS EYES', reason)
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
        # Wakei & Company matched the Cersaie exhibitor X-IS on wa-kei.com, which is
        # the whole point of resolving domains: name matching would never have caught
        # it. The surviving row keeps its own verdict, but the research behind the
        # duplicate is the reason the merge happened, so it must not vanish.
        if r.get('research_note') and not prev.get('research_note'):
            prev['merge_note'] = f"{r['company']}: {r['research_note']}"
        continue
    seen[key] = r
    merged.append(r)

for r in merged:
    r['also_trading_as'] = ' | '.join(r.pop('_brands', []))

for r in merged:
    r['pre_flag'], r['pre_flag_reason'] = pre_flag(r)
    if r.get('merge_note'):
        r['pre_flag_reason'] += ' || merged duplicate, researched separately as ' + r['merge_note']
    r['row_type'] = 'new'          # S7.7: gate firmographic enrichment on this
    r['wave'] = 'wave2'
    # directory rows are trusted as given; only hand-researched rows carry a marker
    r.setdefault('domain_confidence', 'directory' if r['domain'] else '')
    r['gate_flag'] = r.get('research_flag', '')   # filterable in Clay on its own

COLS = ['company','website','domain','domain_confidence','country','town','niche','source',
        'stand','generic_email','also_trading_as','pre_flag','gate_flag','pre_flag_reason',
        'row_type','wave']
with open(OUT, 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.DictWriter(f, fieldnames=COLS, quoting=csv.QUOTE_ALL, extrasaction='ignore')
    w.writeheader(); w.writerows(merged)

from collections import Counter
print(f'{OUT}: {len(merged)} rows  (from {len(rows)} raw, {len(rows)-len(merged)} merged as duplicates)')
print('\nby source:')
for k, v in Counter(r['source'] for r in merged).most_common(): print(f'  {v:>4}  {k}')
print('\nby pre_flag:')
for k, v in Counter(r['pre_flag'] for r in merged).most_common(): print(f'  {v:>4}  {k}')
print(f"\nrows with a website: {sum(1 for r in merged if r['domain'])}/{len(merged)}")
print('\ndomain confidence:')
for k, v in Counter(r['domain_confidence'] or 'none recorded' for r in merged).most_common():
    print(f'  {v:>4}  {k}')
print('\nhand-researched sources, gate verdict from the research alone:')
for src in ('TCNA', 'Coverings', 'Heimtextil', 'TISE'):
    sub = [r for r in merged if src in r['source']]
    have = sum(1 for r in sub if r['domain'])
    c = Counter(r['gate_flag'].split()[0].rstrip(',') for r in sub if r['gate_flag'])
    print(f"  {src:<11} {len(sub):>3} rows, {have:>3} with a domain   " +
          '  '.join(f'{k}:{v}' for k, v in sorted(c.items())))
