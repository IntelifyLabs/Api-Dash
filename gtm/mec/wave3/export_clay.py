#!/usr/bin/env python3
"""The 743 rows to run in Clay for decision-makers: take rows, priority 1-3.

746 before deduping three domains entered twice -- see the dedupe note below.

Priority 5 is excluded here deliberately -- 14 of those rows have no website and
83 did not answer when crawled, so Clay has nothing to key on and a credit spent
is a credit lost. They stay in round3_take_843.csv for a hand pass.

TWO COLUMNS ADDED, both for one reason: KEY THE CLAY RUN ON THE DOMAIN, NOT THE
COMPANY NAME.

  domain               the bare host, no scheme, no www, ready to paste
  domain_matches_name  'yes' where the domain echoes the registered name,
                       'brand' where it does not

77 rows read 'brand', because the entity that books the stand is often not the
name over the shop: Acerbis sits on mdfitalia.com, Barlow Tyrie on teak.com,
1825 srl on serralunga.com, Dis Prod srl on bydurieux.com. These are real
holding-company and brand-portfolio relationships, ordinary at a furniture fair.
Keyed on the registered name, those 77 miss or match the wrong company. Keyed on
the domain, they resolve.

These domains came from the exhibitors' OWN registration forms in the Salone and
Heimtextil APIs, not from web searching, which is why the wrong-company risk here
is far below wave 2's -- that list was hand-researched and produced the Mosaic
Studio, Contrado and Intrend Tile collisions.

ON THE site_matches COLUMN, CARRIED THROUGH BUT NOT TO BE FILTERED ON: it tests
whether the company name appears in the page's visible text, and visible_text()
strips alt attributes, so a homepage showing its name only as a logo image fails
it. Caimi Brevetti spa / caimi.com and Antrax It srl / antrax.com are both
flagged 'check' and both plainly fine. 139 of these 746 are flagged; the
domain-against-name test below clears 669. Use domain_matches_name instead.
"""
import csv, collections, re

LEGAL = (r'\b(srl|s r l|spa|s p a|nv|bv|gmbh|co kg|ltd|llc|ltda|sasu|sas|as|a s|'
         r'sb|sl|inc|plc|oy|ab|aps|doo|d o o|uab|pty|pvt|private limited|group|'
         r'industries|industria|mobilya|moveis|co|company)\b')

def norm(s):
    return re.sub(r'[^a-z0-9]', '', (s or '').lower())

def host(r):
    raw = (r['final_url'] or r['website'] or '').split('//')[-1]
    return re.sub(r'^www\.', '', raw.split('/')[0]).strip().lower()

def name_echoes_domain(company, dom):
    dtok = norm(dom.split('.')[0])
    if not dtok:
        return False
    stripped = re.sub(LEGAL, ' ', ' ' + (company or '').lower() + ' ')
    full = norm(stripped)
    if full and (full in dtok or dtok in full):
        return True
    words = [norm(w) for w in re.split(r'[^A-Za-z0-9]+', stripped) if len(norm(w)) >= 3]
    return any(w in dtok or (len(w) >= 5 and dtok in w) for w in words)

with open('round3_take_843.csv', encoding='utf-8-sig', newline='') as f:
    rd = csv.DictReader(f)
    cols, rows = rd.fieldnames, list(rd)

keep = [r for r in rows if r['clay_priority'] in ('1', '2', '3')]
for r in keep:
    d = host(r)
    r['domain'] = d
    r['domain_matches_name'] = 'yes' if name_echoes_domain(r['company'], d) else 'brand'

# Three domains appear twice, each the same company entered under both its legal
# entity and its trading name, at the SAME stand number -- Mobilduenne srl /
# Nucci at B24, Bellotti Ezio Arredamenti / Bel Mondo at C23, Grifoni Silvano /
# Silvano Grifoni at C36. One company, two directory rows, and Clay would bill
# for both. Keep the trading name, since that is what the email should address.
# Tiebreak is explicit and stable rather than dict order: prefer the row whose
# name echoes the domain, then the one with more fields filled, then the name
# itself alphabetically, so a rerun always drops the same row.
by_domain = collections.defaultdict(list)
for r in keep:
    by_domain[r['domain']].append(r)
dropped = []
deduped = []
for d, group in by_domain.items():
    if len(group) == 1:
        deduped.append(group[0]); continue
    group.sort(key=lambda r: (r['domain_matches_name'] != 'yes',
                              -sum(1 for v in r.values() if v),
                              r['company'].lower()))
    deduped.append(group[0])
    dropped.extend(group[1:])
keep = sorted(deduped, key=lambda r: (r['clay_priority'], r['studio'], r['company'].lower()))

out = ['company', 'domain', 'domain_matches_name'] + \
      [c for c in cols if c not in ('company',)]
with open('round3_clay_743.csv', 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=out, quoting=csv.QUOTE_ALL)
    w.writeheader(); w.writerows(keep)

print('rows written        ', len(keep))
print('every row has domain', all(r['domain'] for r in keep))
print('blank company       ', sum(1 for r in keep if not r['company']))
print('duplicate domains   ', sum(c - 1 for c in
      collections.Counter(r['domain'] for r in keep).values() if c > 1))
print('deduped away        ', len(dropped))
for r in dropped:
    print('    dropped %-36s kept the trading-name row on %s' % (r['company'][:34], r['domain']))
print()
print('domain_matches_name ', dict(collections.Counter(r['domain_matches_name'] for r in keep)))
print('clay_priority       ', dict(sorted(collections.Counter(r['clay_priority'] for r in keep).items())))
print('studio              ', dict(collections.Counter(r['studio'] or '-' for r in keep)))
print('already has email   ', sum(1 for r in keep if r['email'] or r['email2']))
print('country, top 8      ', dict(collections.Counter(r['country'] for r in keep).most_common(8)))
