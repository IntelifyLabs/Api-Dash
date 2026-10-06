#!/usr/bin/env python3
"""Export the 843 verdict=take rows for a Clay decision-maker run.

Every column is carried through unchanged -- this is a row filter, not a
projection. One column is ADDED, clay_priority, and the file is sorted by it.

Why add it: Clay credits are the binding constraint, and Clay needs a domain to
find anybody. 1-4 are ordered by how much a visualiser pitch can land; 5 is the
rows where a credit is likely to be wasted, kept in the file rather than dropped
so the decision stays yours.

  1  consumer-facing, live site   the shopper journey a visualiser plugs into
  2  catalogue only, live site    collections shown, then the visit ends -- the
                                  shape the campaign body was written for
  3  unclear or gated, live site  needs a look before a credit
  4  live site, nothing read      gate 5 could not fetch it
  5  no website, or unreachable   Clay has nothing to work from. Hand check
"""
import csv, collections

CONSUMER = ('consumer, sells online', 'consumer, via dealers')

def priority(r):
    if r['site_live'] != 'yes':
        return 5
    if r['sells_to'] in CONSUMER:
        return 1
    if r['sells_to'] == 'catalogue only':
        return 2
    if r['sells_to'] in ('unclear', 'trade portal, gated'):
        return 3
    return 4

with open('round3_qualified.csv', encoding='utf-8-sig', newline='') as f:
    rd = csv.DictReader(f)
    cols, rows = rd.fieldnames, list(rd)

take = [r for r in rows if r['verdict'] == 'take']
for r in take:
    r['clay_priority'] = priority(r)
take.sort(key=lambda r: (r['clay_priority'], r['studio'], r['company'].lower()))

out = cols + ['clay_priority']
with open('round3_take_843.csv', 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=out, quoting=csv.QUOTE_ALL)
    w.writeheader(); w.writerows(take)

print('rows written      ', len(take))
print('has website       ', sum(1 for r in take if r['website']))
print('NO website        ', sum(1 for r in take if not r['website']))
print('has email already ', sum(1 for r in take if r['email'] or r['email2']))
print()
print('clay_priority')
for k, v in sorted(collections.Counter(r['clay_priority'] for r in take).items()):
    print('  %d  %4d' % (k, v))
print()
print('by studio         ', dict(collections.Counter(r['studio'] or '-' for r in take)))
print('priority 1 studio ', dict(collections.Counter(
    r['studio'] or '-' for r in take if r['clay_priority'] == 1)))
