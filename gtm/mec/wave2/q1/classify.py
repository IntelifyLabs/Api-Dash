# -*- coding: utf-8 -*-
"""Qualifier 1, part A: category gate on the text already in the export.

Free. No Clay, no web searches. Runs S7.6 gates 2, 3, 4 and 6 against the
Industry, Description and Annual Revenue fields so that the paid step (web
research for an existing design tool) only touches rows that could convert.

Descriptions are Italian, Spanish, Turkish, German, Portuguese and English,
so every keyword set is multilingual. Rows are FLAGGED, never dropped.
"""
import csv, re
from collections import Counter, OrderedDict

SRC = 'clay_enriched.csv'
rows = list(csv.DictReader(open(SRC, encoding='utf-8-sig')))

def blob(r):
    """Evidence only. The 'niche' column is deliberately excluded: it is a SOURCE
    LABEL, not evidence. Every Cersaie row carries 'Ceramic / Tile (verify)', so
    including it made the core-niche test pass all 476 of them, which let a
    newspaper (El Periodico del Azulejo), a tap maker (Newform), a window joiner
    (Pail Serramenti) and a trim extruder (Progress Profiles) through as tile."""
    return ' '.join([r['company'], r.get('Name',''), r['Description'] or '',
                     r['Industry'] or '', r['domain'] or '']).lower()

# ---- industries that are the wrong business outright -----------------------
IND_OUT = {
    'Book and Periodical Publishing': 'trade magazine or publisher, not a maker',
    'Newspaper Publishing': 'trade magazine or publisher, not a maker',
    'Periodical Publishing': 'trade magazine or publisher, not a maker',
    'Machinery Manufacturing': 'plant and machinery, an explicit S7.4 exclusion',
    'Industrial Machinery Manufacturing': 'plant and machinery, an explicit S7.4 exclusion',
    'Chemical Manufacturing': 'glazes, inks, adhesives or sealants. Raw input, no pattern',
    'Mining': 'quarrying. Raw stone, no pattern',
    'Transportation, Logistics, Supply Chain and Storage': 'logistics, not a product maker',
    'Plastics Manufacturing': 'composites and plastics, wrong medium',
    'Paper and Forest Product Manufacturing': 'paper or substrate production, not pattern design',
    'Packaging and Containers Manufacturing': 'packaging, an explicit S7.4 exclusion',
    'Oil and Gas': 'wrong industry entirely',
    'Banking': 'wrong industry entirely',
    'Business Consulting and Services': 'consultancy, not a product maker',
    'Environmental Services': 'wrong industry entirely',
    'Higher Education': 'institutional, wrong buyer type',
    'Education Administration Programs': 'institutional, wrong buyer type',
    'Non-profit Organizations': 'nonprofit, wrong buyer type per S7.4',
    'Civic and Social Organizations': 'trade body or association, nobody to sell to',
}
IND_MIDDLE = {'Wholesale Building Materials', 'Wholesale', 'Retail',
              'International Trade and Development', 'Retail Building Materials and Garden Equipment'}

# ---- multilingual signal sets ---------------------------------------------
def rx(*words): return re.compile('|'.join(words), re.I)

R_MACHINE   = rx(r'\bmachiner', r'macchin', r'\bkiln\b', r'\bpress(es|ing)? line', r'impiant',
                 r'\bsaw\b', r'diamond (blade|tool)', r'\babrasiv', r'\bmoul?d(ing)? machine')
R_CHEM      = rx(r'\badhesiv', r'\bglue\b', r'\bcollant', r'\bgrout', r'\bmortar', r'\bsealant',
                 r'\bprimer\b', r'\bresin\b', r'\bpigment', r'\bink(s)?\b', r'\bcolle\b',
                 r'\bmalt(a|e)\b', r'\bsilicon', r'adesiv')
R_SANITARY  = rx(r'sanitar', r'rubinett', r'\bbagno\b', r'shower tray', r'\bdoccia\b', r'\bwc\b',
                 r'bathtub', r'\bvasca\b', r'washbasin', r'lavabo', r'\bfaucet', r'\btoilet')
R_3D        = rx(r'\bfurnitur', r'\barredo', r'\bmobil(i|e) per', r'\bpottery\b', r'\bvase(s)?\b',
                 r'\bmug(s)?\b', r'tableware', r'\bkitchen(s)? manufactur', r'\bcucin(a|e)\b',
                 r'\bsof(a|à)', r'\bchair(s)?\b', r'\bcomplement(i|o) d')
R_WOOD_SOFT = rx(r'\bparquet', r'\blegno\b', r'\bhardwood', r'\blaminat', r'\bvinyl\b', r'\blvt\b',
                 r'\bspc\b', r'\bwpc\b', r'\bcarpet', r'\brug(s)? manufactur', r'\bmoquette',
                 r'\bunderlay', r'\bskirting profile')
# Narrow on purpose. The first version matched bare 'stone' patterns and killed
# Zaijian Mosaic, a 1993 art-mosaic house, as a quarry. Only extraction and
# block/slab language counts now, never 'stone mosaic' or 'lava stone'.
R_STONE_RAW = rx(r'\bquarr(y|ies|ying)', r'\bcave di marmo', r'\bblock(s)? of (marble|granite|limestone)',
                 r'\braw block', r'\bgranite block', r'\bmarble block',
                 r'\bextraction of (marble|granite|stone)', r'\bestrazione')
R_MIDDLE    = rx(r'\bdistribut', r'\bwholesal', r'\bimporter', r'\bimport(s|ing|ation)?\b',
                 r'\bexport(er|ing)\b', r'\bdealer', r'\brivendit', r'\bgrossist', r'\bmayorist',
                 r'\bdistribuidor', r'\bcommercializ', r'\bstockist', r'\btrading (company|house)',
                 r'\bithalat', r'\bsupplier of', r'we carry\b', r'authorized dealer')
R_INSTALL   = rx(r'\bwe install', r'\binstallation servic', r'\bcontractor', r'\bposa\b',
                 r'\bfabricator', r'\bcountertop fabric', r'\bimpres(a|e) di costruzion',
                 r'\bgeneral contractor', r'\bposatori')
R_MEDIA     = rx(r'\brivista\b', r'\bmagazine\b', r'\bpublish(er|ing)\b', r'\beditor(e|iale)\b',
                 r'\bperiodic', r'\btrade fair', r'\bfiera\b', r'\bassociation\b', r'\bconsorzio\b',
                 r'\bfederation\b', r'\bpromotion group')
R_SOFTWARE  = rx(r'\bsoftware\b', r'\bsaas\b', r'\berp\b', r'\bapp for\b', r'\bplatform for\b',
                 r'\bcad\b', r'\brendering software', r'\bvisualization software')
# joinery, trims and fittings kept slipping through as 'tile' on the niche label
R_NOT_SURFACE = rx(r'\bserrament', r'\bporte e finestr', r'\bwindow(s)? and door', r'\bdoor(s)? and window',
                   r'\bfalegnam', r'\bjoinery', r'\bprofil(e|i|es) (tecnic|decorativ|di finitura)',
                   r'\btechnical profile', r'\btrim(s)? and profile', r'\bskirting\b',
                   r'\bstair nosing', r'\bexpansion joint', r'\bshutter', r'\bpersian(e|a)\b',
                   r'\bventilated fa(c|ç)ade system', r'\bsubstructure', r'\bfixing system',
                   r'\braised floor(ing)? system', r'\bpedestal', r'\bled\b', r'\blighting\b',
                   r'\bfireplace', r'\bstufa\b', r'\bcamin(o|etto)\b', r'\bbarbecue')
R_PRESS     = rx(r'\bperi(o|ó)dic', r'\bprensa\b', r'\bquotidian', r'\bgiornale\b',
                 r'\bnewspaper', r'\beditorial group', r'\bgrupo prensa', r'\baudiencia\b')

# ---- the niches we do want ------------------------------------------------
R_CORE      = rx(r'\bceramic', r'\bceramic(a|he)\b', r'\bseramik', r'\bporcelain', r'\bgres\b',
                 r'\bstoneware', r'\bmosaic', r'\bmosaic(o|i)\b', r'\bmozaik', r'\btile(s)?\b',
                 r'\bpiastrell', r'\bazulejo', r'\bcarrelage', r'\bwallpaper', r'\btapet',
                 r'\bwallcovering', r'\bwall covering', r'\brivestiment', r'\bmural',
                 r'\bterracotta', r'\bcotto\b', r'\bzellige', r'\bencaustic', r'\bcement tile')
R_BESPOKE   = rx(r'\bbespoke', r'\bmade[- ]to[- ]order', r'\bcustom(ised|ized|isation|ization|-made)?\b',
                 r'\bsu misura', r'\bpersonalizza', r'\bpersonaliz', r'\bhandmade', r'\bhand[- ]made',
                 r'\bhandcraft', r'\bfatto a mano', r'\bartigian', r'\bhecho a mano', r'\bartesan',
                 r'\bcommission', r'\bone[- ]off', r'\bunique piece', r'\bhand[- ]painted',
                 r'\bdipint(o|i) a mano', r'\bmanufaktur', r'\batelier\b')
R_DESIGNHOUSE = rx(r'\bcollection(s)?\b', r'\bcollezion', r'\bcolecci', r'\bdesign(ed)? (by|in house)',
                   r'\bour design(er)?s?\b', r'\bdesign studio', r'\bcreative studio',
                   r'\bto the trade\b', r'\btrade program', r'\barchitect(s)? and designer')

REV_FAIL = {'0-500K', '500K-1M'}

def verdict(r):
    b, ind = blob(r), (r['Industry'] or '').strip()
    rev = (r['Annual Revenue'] or '').strip()

    # A hand verdict from the 14 Sept research was already eyeballed, so it
    # outranks every keyword rule below - in BOTH directions. Honouring only the
    # negatives was an asymmetry bug: it killed Marburger (1845, 290 people,
    # named international designers) and A.S. Creation (2,000 designs a year,
    # already runs a room visualiser) as "commodity volume", because their
    # third-party descriptions happen not to use the words the rules look for.
    pf = (r.get('pre_flag') or '').strip()
    hand = (r.get('pre_flag_reason') or '')
    if pf in ('EXCLUDE', 'LIKELY OUT'):
        return 'OUT', 'hand-verified', f'{pf} on the 14 Sept research: {hand[:200]}'
    if hand.startswith('PASS priority'):
        return 'CANDIDATE A', 'in scope', f'hand-verified priority on 14 Sept: {hand[:180]}'
    if hand.startswith(('PASS', 'FLAG')):
        return 'CANDIDATE B', 'in scope', f'hand-verified on 14 Sept: {hand[:180]}'

    # gate 2 / wrong business -------------------------------------------------
    if ind in IND_OUT:            return 'OUT', 'wrong business', IND_OUT[ind]
    # press beats the niche label: a Castellon tile newspaper is not a tile maker
    if R_PRESS.search(b):
        return 'OUT', 'wrong business', 'newspaper or press group covering the tile trade, not in it'
    if R_NOT_SURFACE.search(b) and not R_CORE.search(b):
        return 'OUT', 'wrong medium', ('joinery, trims, profiles, fixing systems, lighting or '
                                       'fireplaces. Not a designed flat surface')
    if R_MEDIA.search(b) and not R_CORE.search(b):
        return 'OUT', 'wrong business', 'magazine, trade fair or association. Nobody here buys a tool'
    if R_MACHINE.search(b) and not R_CORE.search(b):
        return 'OUT', 'wrong business', 'plant and machinery. Explicit S7.4 exclusion'
    if R_CHEM.search(b) and not R_CORE.search(b):
        return 'OUT', 'wrong business', 'adhesive, grout, glaze or ink. Raw input with no pattern'
    if R_SOFTWARE.search(b) and not R_CORE.search(b):
        return 'OUT', 'wrong business', 'software vendor. Possibly a competitor, not a prospect'
    if R_STONE_RAW.search(b) and not R_CORE.search(b):
        return 'OUT', 'wrong medium', 'quarrying or raw stone blocks and slabs. No pattern to design'

    # gate 4 / wrong medium ---------------------------------------------------
    if R_SANITARY.search(b) and not R_CORE.search(b):
        return 'OUT', 'wrong medium', 'sanitaryware and bathroom fittings. 3D, explicit exclusion'
    if R_3D.search(b) and not R_CORE.search(b):
        return 'OUT', 'wrong medium', 'furniture or 3D ceramics. Engine renders flat patterns only'
    if R_WOOD_SOFT.search(b) and not R_CORE.search(b):
        return 'OUT', 'wrong medium', 'wood, resilient or textile flooring. Not a designed flat pattern'

    desc = (r['Description'] or '').strip()
    if len(desc) < 40 and not (r['Industry'] or '').strip():
        return 'NO DATA', 'nothing to gate on', ('no description and no industry came back. Cannot be '
                                                 'categorised from text at all, so it goes to web research')
    core = bool(R_CORE.search(b))
    if not core:
        return 'REVIEW', 'niche unclear', ('nothing in the description names tile, ceramic, mosaic, '
                                           'wallcovering or mural. Needs eyes before any spend')

    # gate 3 / maker not middleman -------------------------------------------
    mid = R_MIDDLE.search(b); inst = R_INSTALL.search(b)
    made = R_BESPOKE.search(b) or re.search(r'\b(manufactur|produc|fabbric|produzion|we make|our factory|'
                                            r'our kiln|fabricaci|üretim|herstell)', b, re.I)
    # 'wholesale' in a description does not outrank explicit making language.
    # LIVDEN designs its own 50-tile line and was being cut as a distributor.
    if R_BESPOKE.search(b) or R_DESIGNHOUSE.search(b):
        mid_kills = False
    else:
        mid_kills = True
    if mid_kills and (ind in IND_MIDDLE or mid) and not made:
        return 'OUT', 'middleman', (f"gate 3: reads as distributor, importer or retailer "
                                    f"({(mid.group(0) if mid else ind)}) with no making language")
    if mid_kills and inst and not made:
        return 'OUT', 'middleman', 'gate 3: installer, contractor or fabricator, not a maker'

    # gate 6 / revenue -------------------------------------------------------
    if rev in REV_FAIL:
        return 'OUT', 'revenue', f'{rev} is under the $1M gate (S7.4)'

    # criterion 3: a big catalogue factory with no bespoke and no collections
    # language is a fixed-SKU producer. Nothing for the tool to plug into
    big = (r['Size'] or '') in ('201-500 employees', '501-1,000 employees',
                                '1,001-5,000 employees', '5,001-10,000 employees', '10,001+ employees')
    if big and not R_BESPOKE.search(b) and not R_DESIGNHOUSE.search(b):
        return 'OUT', 'commodity volume', ('criterion 3: large fixed-SKU producer, no bespoke, custom '
                                           'or own-collection language anywhere in the description')

    # what is left is a real candidate; rank it ------------------------------
    sig = []
    if R_BESPOKE.search(b):     sig.append('bespoke/handmade language')
    if R_DESIGNHOUSE.search(b): sig.append('own collections or trade-facing')
    if mid:                     sig.append('also distributes, confirm the maker share')
    if not rev:                 sig.append('revenue blank, manual review per S7.4')
    both = len(set(sig) & {'bespoke/handmade language', 'own collections or trade-facing'}) == 2
    tier = 'A' if both else 'B' if R_BESPOKE.search(b) or R_DESIGNHOUSE.search(b) else 'C'
    if big: sig.append('200+ employees, long cycle per the S7.4 decision-maker table')
    return f'CANDIDATE {tier}', 'in scope', '; '.join(sig) or 'core niche, no bespoke signal in the text'

for r in rows:
    v, cat, why = verdict(r)
    r['q1_verdict'], r['q1_category'], r['q1_reason'] = v, cat, why

OUTC = Counter(r['q1_verdict'] for r in rows)
print('QUALIFIER 1A - category gate, no searches spent')
for k in sorted(OUTC, key=lambda k: (not k.startswith('CANDIDATE'), k)):
    print(f'  {OUTC[k]:>4}  {k}')
print('\nwhy rows were cut:')
for k, v in Counter(r['q1_category'] for r in rows if r['q1_verdict'] == 'OUT').most_common():
    print(f'  {v:>4}  {k}')

COLS = list(rows[0].keys())
with open('q1a_categorised.csv', 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.DictWriter(f, fieldnames=COLS, quoting=csv.QUOTE_ALL)
    w.writeheader(); w.writerows(rows)
cand = [r for r in rows if r['q1_verdict'].startswith('CANDIDATE')
        or r['q1_verdict'] in ('REVIEW', 'NO DATA')]
print(f'\nto research for an existing design tool: {len(cand)} of {len(rows)}')
