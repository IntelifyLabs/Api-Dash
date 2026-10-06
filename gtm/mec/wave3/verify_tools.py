"""Checks on gate 5, written before the gate finished so the expectations are
not reverse-engineered from whatever came out.

Gate 4 taught the lesson these checks are shaped by: every pass of it looked
fine in aggregate and was wrong on a named company. So each check below either
names a company whose answer is known by hand, or reproduces a formula
independently and demands exact agreement. A distribution that merely looks
plausible proves nothing.
"""
import collections, csv, re

ROWS = list(csv.DictReader(open('/home/user/Api-Dash/gtm/mec/wave3/round3_qualified.csv',
                                encoding='utf-8-sig')))
NEW = ('tool_level', 'tool_name', 'tool_evidence', 'business_role',
       'product_type', 'site_matches', 'segment')
fails, warns = [], []
def ok(m):   print('  ok   ' + m)
def bad(m):  fails.append(m); print('  FAIL ' + m)
def warn(m): warns.append(m); print('  warn ' + m)

live = [r for r in ROWS if r['site_live'] == 'yes']
print('columns')
missing = [c for c in NEW if c not in (ROWS[0].keys() if ROWS else [])]
bad('columns absent: %s' % missing) if missing else ok('all 7 gate-5 columns present')
ok('%d rows, %d live' % (len(ROWS), len(live)))

print('\nevery live row got a verdict on its tooling')
blank = [r for r in live if not r['tool_level']]
if blank:
    warn('%d live rows have blank tool_level, gate 5 could not fetch them '
         '(gate 4 reached them, so these are flaky not dead)' % len(blank))
else:
    ok('no live row left without a tool_level')
notlive = [r for r in ROWS if r['site_live'] != 'yes' and r['tool_level']]
bad('%d rows with no live site carry a tool_level' % len(notlive)) if notlive \
    else ok('no dead or missing site was given a tool_level')

print('\nevidence backs the level it is attached to')
noev = [r for r in live if r['tool_level'] in ('ADVANCED', 'MANUAL', 'BASIC')
        and not r['tool_evidence']]
bad('%d rows claim a tool level with no quoted evidence' % len(noev)) if noev \
    else ok('every ADVANCED/MANUAL/BASIC row quotes the line it matched')
ev_on_none = [r for r in live if r['tool_level'] == 'NONE' and r['tool_evidence']]
bad('%d NONE rows carry evidence' % len(ev_on_none)) if ev_on_none \
    else ok('no NONE row carries evidence')

print('\nsegment recomputed independently, must agree exactly')
# A row with no tool_level was never read, so it has no segment. That is a
# legitimate blank, distinct from a formula disagreement, and conflating the two
# made this check report 69 false failures on the first run.
def expect(r):
    if not r['tool_level']:
        return ''
    return 'C' if r['has_tryon'] == 'yes' else 'A' if r['tool_level'] == 'MANUAL' else 'B'
mis = [r for r in ROWS if r['segment'] != expect(r)]
if mis:
    bad('%d rows disagree with the wave-2 segment formula, e.g. %s' %
        (len(mis), [(r['company'][:20], r['has_tryon'], r['tool_level'], r['segment'])
                    for r in mis[:3]]))
else:
    ok('segment matches C-if-tryon / A-if-MANUAL / else-B on every row')

print('\nhas_tryon now means a room visualiser and nothing else')
# Gate 4 set has_tryon from a regex carrying a bare `configurator`, so it marked
# finish pickers as visualisers while the reason line said "already runs a
# visualiser". Gate 5 redefines it as exactly tool_level ADVANCED. That identity
# is the contract, so it is asserted rather than described.
bad_yes = [r for r in live if r['has_tryon'] == 'yes' and r['tool_level'] != 'ADVANCED']
unread = [r for r in live if not r['tool_level']]
bad_no = [r for r in live if r['has_tryon'] != 'yes' and r['tool_level'] == 'ADVANCED']
if bad_yes or bad_no:
    bad('has_tryon no longer equals ADVANCED: %d yes-but-not-ADVANCED, '
        '%d ADVANCED-but-not-yes' % (len(bad_yes), len(bad_no)))
else:
    ok('has_tryon == (tool_level ADVANCED) on every live row')
if unread:
    print('         %d live rows gate 5 could not read carry no claim either way'
          % len(unread))
nvis = sum(1 for r in live if r['has_tryon'] == 'yes')
print('         %d live rows run a real visualiser (gate 4 had claimed 93)' % nvis)

print('\nthe vendor cases, which only a script tag proves')
# Farrow & Ball and Erismann both run Roomvo and on both the ONLY trace is the
# widget's <script>. An earlier fix that matched visible text everywhere lost
# them. They are the regression guard for scoping vendors to raw HTML.
for name in ('Farrow', 'Erismann'):
    r = next((x for x in ROWS if name.lower() in x['company'].lower()), None)
    if r is None:
        warn('%s not in the file, cannot check the vendor path' % name)
    elif r['tool_name'] and r['tool_level'] == 'ADVANCED':
        ok('%-22s tool_name=%s level=%s' % (r['company'][:20], r['tool_name'], r['tool_level']))
    else:
        bad('%s reads tool_name=%r level=%r; its Roomvo widget is in a script '
            'tag, so scoping vendors to raw HTML has regressed'
            % (r['company'][:24], r['tool_name'], r['tool_level']))

print('\nthe configurator reclassification')
cfg = [r for r in live if r['tool_level'] == 'BASIC']
print('  %d live rows read BASIC, a configurator or picker but no room view' % len(cfg))
print('  these are the rows gate 4 would have told "you already run a visualiser"')

print('\nthe wave-2 trap: a tool name that is just a nav-bar word')
GENERIC = {'visualizer', 'visualiser', 'configurator', 'configuratore', '3d',
           'room planner', 'product finder'}
hit = collections.Counter(r['tool_name'] for r in live if r['tool_name'])
junk = [n for n in hit if n.strip().lower() in GENERIC]
bad('generic words leaked into tool_name: %s' % junk) if junk \
    else ok('no bare generic word in tool_name (%d rows named a tool)' % sum(hit.values()))
SOFT = {'Room Designer', 'Virtual Room', 'Create 3D', 'Simulador 3D', 'Virtual Viewer'}
soft = {n: c for n, c in hit.items() if n in SOFT}
if soft:
    warn('borderline names, check one before quoting it in copy: %s' % soft)

print('\ncompanies whose answer is known by hand')
def find(name):
    return next((r for r in ROWS if name.lower() in r['company'].lower()), None)
r = find('Annibale Colombo')
if not r: bad('Annibale Colombo missing from the file')
elif r['tool_level'] in ('BASIC', 'ADVANCED'):
    ok('Annibale Colombo  tool_level=%s, its page does say "Utilizza il '
       'configuratore"' % r['tool_level'])
else:
    bad('Annibale Colombo reads tool_level=%s, but its homepage carries a real '
        'QUADRO CONFIGURATOR' % r['tool_level'])

print('\ndistributions, wave 2 beside them')
for col, w2 in (('tool_level', 'NONE 149, BASIC 148, ADVANCED 90, MANUAL 52'),
                ('business_role', 'MAKER 298, MAKER_AND_DISTRIBUTOR 124, DISTRIBUTOR 14, RETAILER 3'),
                ('product_type', 'CATALOGUE 300, BOTH 137, CUSTOM 2'),
                ('segment', 'A 52, B 315, C 72')):
    c = collections.Counter(r[col] or 'blank' for r in live)
    print('  %-14s %s' % (col, dict(c.most_common())))
    print('  %-14s wave 2: %s' % ('', w2))

blankrole = sum(1 for r in live if not r['business_role'])
if blankrole > len(live) * 0.4:
    warn('business_role blank on %d of %d live rows (%.0f%%), the MAKER lexicon '
         'is English/Italian and much of this list is neither'
         % (blankrole, len(live), 100 * blankrole / len(live)))

print('\nsite_matches')
sm = collections.Counter(r['site_matches'] for r in live)
print('  ' + str(dict(sm)))
if sm.get('check', 0) > len(live) * 0.25:
    warn('site_matches=check on %d rows; the test is a 6-char name stem so it '
         'is noisy, treat it as a hint not a verdict' % sm['check'])

print('\n=== CUTS, now split by segment ===')
CONSUMER = ('consumer, sells online', 'consumer, via dealers')
cut2 = [r for r in ROWS if r['sells_to'] in CONSUMER]
cut1 = [r for r in cut2 if r['has_tryon'] == 'yes']
take = [r for r in ROWS if r['verdict'] == 'take']
for nm, cut in (('cut 1  visualiser + consumer facing', cut1),
                ('cut 2  consumer facing, any tool  ', cut2),
                ('cut 3  every take row             ', take)):
    seg = collections.Counter(r['segment'] or '-' for r in cut)
    lvl = collections.Counter(r['tool_level'] or '-' for r in cut)
    print('  %s %5d   segment %s' % (nm, len(cut), dict(sorted(seg.items()))))
    print('  %s         tools   %s' % (' ' * len(nm), dict(lvl.most_common())))

print('\n  cut 2 by studio x segment')
bs = collections.Counter((r['studio'] or '-', r['segment'] or '-') for r in cut2)
for (st, sg), n in sorted(bs.items()):
    print('    %-10s %s  %4d' % (st, sg, n))

named = [r for r in cut2 if r['tool_name']]
print('\n  cut 2 rows naming a real tool (strongest personalisation): %d' % len(named))
for r in named[:12]:
    print('    %-30s %-18s %s' % (r['company'][:28], r['tool_name'], r['studio']))

print('\nFAILURES: %d' % len(fails))
for f in fails: print('  - ' + f)
if not fails: print('all checks passed')
for w in warns: print('  warn: ' + w)
