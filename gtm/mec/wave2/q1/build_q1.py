# -*- coding: utf-8 -*-
"""Merge the category gate (part A) with the tool research (part B) into one
qualifier-1 result, and derive the sales angle each row actually needs.

The angle is the whole point of the exercise. Same product category, but a
company with an advanced configurator and a company whose customers design
with coloured pencils need opposite opening lines.
"""
import csv
from collections import Counter, OrderedDict
import findings

RESEARCH = {findings.ALIAS.get(f[0], f[0]): f for f in findings.F}
rows = list(csv.DictReader(open('q1a_categorised.csv', encoding='utf-8-sig')))

# tool_level -> (priority rank, what to sell)
ANGLE = OrderedDict([
 ('MANUAL', (1, 'REPLACE A HUMAN LOOP. They already sell the bespoke outcome and '
                'produce it with staff time: hand mock-ups, CAD drawings, sample '
                'books, glaze trials, meetings. The tool removes the wait, not the '
                'service. Strongest and least contested pitch')),
 ('NONE',   (2, 'NO DESIGN STEP AT ALL. Sell the capability itself, as a value-add '
                'their customers get and their competitors already offer. Confirm by '
                'eye first: search indexes tool pages, it does not prove absence')),
 ('BASIC',  (3, 'UPGRADE A PICKER. A dropdown, swatch page, colour finder or style '
                'quiz. They have accepted the idea of choosing online and stopped at '
                'filtering. Show the gap between filtering a catalogue and composing '
                'a design')),
 ('ADVANCED', (4, 'THE A/B COHORT (S11). Never say they lack a tool. Their tool PLACES '
                  'or RECOMBINES existing designs; it cannot ORIGINATE one. Pitch '
                  'generation, not visualisation')),
 ('ADVANCED-AI', (5, 'DIRECT COMPETITOR. Already ships AI styling. Do not pitch the '
                     'generic AI story, they will out-resource it. Only a pattern-'
                     'origination angle survives here, if anything does')),
])

for r in rows:
    f = RESEARCH.get(r['company'])
    if not f:
        r['tool_level'] = r['tool_evidence'] = r['sell_angle'] = r['q1_rank'] = ''
        continue
    _, level, evidence, so_what = f
    if level.startswith('OUT-'):
        r['q1_verdict'] = 'OUT'
        r['q1_category'] = level.replace('OUT-', '').lower().replace('-', ' ')
        r['q1_reason'] = 'overturned by the site research: ' + evidence
        r['tool_level'], r['tool_evidence'], r['sell_angle'], r['q1_rank'] = level, evidence, '', ''
        continue
    rank, angle = ANGLE[level]
    r['tool_level'], r['tool_evidence'] = level, evidence
    r['sell_angle'] = (so_what + ' || ' if so_what else '') + angle
    r['q1_rank'] = f'{rank}-{level}'

COLS = (['company','domain','country','town','q1_verdict','tool_level','q1_rank',
         'sell_angle','tool_evidence','q1_category','q1_reason','niche','source',
         'Annual Revenue','Size','Industry','Description'])
def write(path, data):
    with open(path,'w',newline='',encoding='utf-8-sig') as fh:
        w = csv.DictWriter(fh, fieldnames=COLS, quoting=csv.QUOTE_ALL, extrasaction='ignore')
        w.writeheader(); w.writerows(data)
    print(f'{path}: {len(data)} rows')

order = {k: v[0] for k, v in ANGLE.items()}
res = [r for r in rows if r['tool_level'] and not r['tool_level'].startswith('OUT-')]
res.sort(key=lambda r: (order[r['tool_level']], r['q1_verdict'], r['company']))
write('MEC_Q1_Researched_104.csv', res)
write('MEC_Q1_All576.csv', sorted(rows, key=lambda r: (not r['tool_level'], r['q1_verdict'], r['company'])))

print('\n== QUALIFIER 1 ==')
print(f'{len(rows)} enriched rows -> {sum(1 for r in rows if r["q1_verdict"]=="OUT")} out on category, '
      f'{len(res)} researched for the feature\n')
print('Q1: do they already have the feature?')
for k in ANGLE:
    n = sum(1 for r in res if r['tool_level'] == k)
    print(f'  {n:>3}  {k}')
print('\nQ2: same product category, so can we sell to them?')
c = Counter(r['q1_verdict'] for r in rows)
for k, v in sorted(c.items()): print(f'  {v:>3}  {k}')
print('\nnot yet researched (batch 2):')
for k, v in Counter(r['q1_verdict'] for r in rows if not r['tool_level']).most_common():
    print(f'  {v:>3}  {k}')
