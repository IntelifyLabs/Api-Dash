"""Re-decide only the rows gate 4 labelled 'trade portal, gated'.

Why only those rows, and why this is complete rather than a shortcut:

GATED is consulted in exactly one branch of probe(), `elif trade or gated`,
which is reached only after `shop` and `dealer` have both come back false.
Tightening GATED can only ever turn a True into a False. So a row can only move
if it is sitting in that branch today -- i.e. if its sells_to currently reads
'trade portal, gated'. Every other row either never reached the branch or
reached it with trade and gated both already false. Nothing else can change,
so re-fetching 1,114 sites a fourth time would churn the file to re-confirm
1,072 rows that cannot move.

The re-decision calls qualify_round3.probe() and .reason() directly instead of
reimplementing the cascade, so this file cannot drift from the qualifier.

A row whose site will not answer after 3 tries is LEFT EXACTLY AS IT WAS and
named in the report. A flaky fetch must not quietly demote a live site to
unreachable.
"""
import csv, importlib.util, sys, time
import concurrent.futures as cf

HERE = '/home/user/Api-Dash/gtm/mec/wave3/'
spec = importlib.util.spec_from_file_location('q', HERE + 'qualify_round3.py')
q = importlib.util.module_from_spec(spec); spec.loader.exec_module(q)

PATH = HERE + 'round3_qualified.csv'
with open(PATH, encoding='utf-8-sig', newline='') as f:
    rd = csv.DictReader(f)
    cols, rows = rd.fieldnames, list(rd)

targets = [r for r in rows if r['sells_to'] == 'trade portal, gated']
print(f'{len(targets)} rows to re-decide')

def redo(r):
    for attempt in range(3):
        try:
            out = q.probe(r)
        except Exception:
            out = {'site_live': 'unreachable'}
        if out.get('site_live') == 'yes':
            return r, out, None
        time.sleep(1.5 * (attempt + 1))
    return r, None, out.get('site_note', 'no answer in 3 tries')

with cf.ThreadPoolExecutor(6) as ex:
    results = list(ex.map(redo, targets))

changed, kept, failed = [], [], []
for r, out, err in results:
    if out is None:
        failed.append((r['company'], err)); continue
    before = r['sells_to']
    for k, v in out.items():
        r[k] = v
    r['reason'] = q.reason(r)
    (changed if r['sells_to'] != before else kept).append((r['company'], before, r['sells_to']))

with open(PATH, 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols, quoting=csv.QUOTE_ALL)
    w.writeheader(); w.writerows(rows)

from collections import Counter
print(f'\nmoved   {len(changed)}')
for c, b, a in sorted(changed): print(f'  {c[:34]:36} {b}  ->  {a}')
print(f'\nstill gated {len(kept)}')
for c, b, a in sorted(kept): print(f'  {c[:34]:36} {a}')
print(f'\nleft untouched, site would not answer: {len(failed)}')
for c, e in failed: print(f'  {c[:34]:36} {e}')
print('\nnew sells_to across the file')
for k, v in Counter(r['sells_to'] for r in rows if r['sells_to']).most_common():
    print(f'  {v:5}  {k}')
