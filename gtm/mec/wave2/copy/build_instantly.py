# -*- coding: utf-8 -*-
"""Build the Instantly upload from contacts_final.csv.

One row per CONTACT, not per company, because Instantly sends to a person and
84 companies carry two decision makers.

Contact mapping is the corrected one, verified by name-to-localpart matching:
  Work Email (2)  ->  person 1  (287/299)   -> thread A
  Work Email      ->  person 2  ( 95/100)   -> thread B
The columns are crossed. Pairing them the obvious way puts every greeting on
the wrong address.

Segment comes from qualifier 1, in this order, because has_tryon outranks
tool_level: a company can read ADVANCED and still be missing the generative
half, and that cohort gets a different message from one with no tool at all.
  C  has_tryon = yes        (praise the tool, sell the missing half)
  A  tool_level = MANUAL    (a person is doing the visualising today)
  B  everything else        (no design step, or filters only)

Every opening line is that company's own words, lifted from the Claygent
evidence column as a literal quotation, which is the only construction that
stays grammatical across 390 different fragments. Where no usable quote exists
the row falls back to a neutral line that is still true of that row, and
qa_hook_quality is written as 'weak' so it can be found and hand-fixed.
"""
import csv, re, unicodedata

SRC = '../q1/contacts_final.csv'
OUT = 'MEC_Instantly_Wave2.csv'

# A quote is usable as an opening line only if it is a phrase, not a nav item.
# Rejecting trailing commas kills "Collections," / "Timeline," / "Downloads,"
# which is how the site navigation gets quoted, and those read as nonsense in
# an email. Four words is the floor: shorter fragments carry no claim.
QUOTE = re.compile(r'[“"]([^”"]{12,110})[”"]')
# Words that would trip a filter, checked against the quote as well as our own
# copy. The quote is the prospect's own marketing language, so it is exactly
# where "exclusive", "limited edition" and "special offer" turn up. A hook
# carrying one is dropped rather than cleaned, because editing somebody's words
# and still presenting them inside quotation marks is not a thing to automate.
FILTERED = ('free', 'guarantee', 'offer', 'discount', 'click here', 'act now',
            'limited', 'exclusive', 'urgent', 'risk-free', '100%', 'cash',
            'winner', 'opportunity', 'instant', 'no obligation', 'best price')

def best_quote(ev):
    """Shortest usable phrase wins, not the longest. The quote lands in email 1,
    which has a 90 word ceiling, and taking the longest match pushed 140 of 390
    rows over it. Phrases also quote better than paragraphs."""
    out = []
    for q in QUOTE.findall(ev or ''):
        # Trailing punctuation has to go, or the quote lands as
        # 'On your own site: "Solicita una reunion con nosotros.".'
        q = q.strip().rstrip(',;:.!?\u2026').strip()
        if q.endswith(','): continue
        n = len(q.split())
        if n < 4 or n > 13: continue
        if q.lower().startswith(('home ', 'about ', 'contact ')): continue
        if '—' in q or '–' in q: continue
        if any(w in q.lower() for w in FILTERED): continue
        out.append(q)
    return min(out, key=lambda s: len(s.split())) if out else ''

# Tool names worth naming back to the reader. A named tool in the subject line
# is the single strongest signal in variant C that this is not a mail merge.
KNOWN = ['Roomviewer','Roomvo','Room Viewer','Virtual Room','Virtual Viewer','Virtual Stylist',
         'Design Your Pool','Stylizer','Simulador 3D','Spark Blueprint','My Room','MyRoom',
         'Cifre Roomview','Roomview','DomuS3D','Overlapp','Cevica Lab','3D Viewer','Create 3D',
         'Visualizer','Visualiser','Configurator','Configurador','Simulator','Simulador']
def tool_name(ev, url):
    for k in KNOWN:
        if re.search(r'\b'+re.escape(k)+r'\b', ev or '', re.I):
            return k
    return ''

def clean(s):
    return re.sub(r'\s+', ' ', (s or '').strip())

# A legal suffix inside an email body is the loudest merge tell there is.
# Nobody writes "Esselle Retail Limited puts out collections" to a colleague.
# Stripping it also clears the only three filtered-word hits left in the file,
# which came from Itaca Ceramic Private Limited, Esselle Retail Limited and
# KT Exclusive GmbH, all legal names rather than anything we chose to write.
SUFFIX = re.compile(r'[\s,]+('
    r'private\s+limited|limited|ltd\.?|llc|l\.l\.c\.?|inc\.?|incorporated|'
    r'co\.?|corp\.?|company|gmbh|mbh|ag|kg|gmbh\s*&\s*co\.?\s*kg|'
    r's\.?r\.?l\.?|s\.?p\.?a\.?|s\.?a\.?u?\.?|s\.?l\.?u?\.?|b\.?v\.?|n\.?v\.?|'
    r'a\.?s\.?|oy|ab|aps|sas|sarl|pvt\.?|plc|pty'
    r')\s*$', re.I)

# Lower-cased mid-name, never at the start. Without this "ABITARE LA CERAMICA"
# folds to "Abitare LA Ceramica" and "ABYSM BY OSET" to "Abysm BY Oset",
# because a naive rule keeps every short token upper case to protect acronyms.
CONNECTOR = {'and','by','la','le','el','de','del','della','di','da','du','of',
             'the','y','e','in','al','und','fur','van','von','per','con'}

def cap(w):
    """Capitalise the first LETTER, not the first character. str.capitalize()
    turns '(AZULEJOS' into '(azulejos' and '4DESIGN' into '4design', because
    both start with a non-letter and it lower-cases everything after index 0."""
    return re.sub(r'([A-Za-z])([A-Za-z]*)',
                  lambda m: m.group(1).upper() + m.group(2).lower(), w, count=1)

def person_name(n):
    """The waterfall returns names in whatever case the source held them, so
    'juan' and 'FERNANDO AGRAMUNT GORRIZ' both appear. A greeting reading
    'Hello juan,' is the tell that nobody wrote this by hand. Mixed-case names
    are left alone, because O'Brien and de Vries are correct as supplied."""
    n = clean(n)
    if not n:
        return n
    # Fold any token that is entirely one case. Checking the whole string missed
    # "Maher K." and "alessandro albasini", where one token is already correct.
    return ' '.join(w if (w != w.lower() and w != w.upper()) else cap(w)
                    for w in n.split())

def titlecase_company(c):
    """ESTUDIO CERAMICO shouted in an email body reads as a mail merge. Only
    fold rows that are fully upper case; leave 41zero42 and Cotto d'Este alone."""
    c = clean(c)
    if c.isupper() and len(c) > 3:
        out = []
        for i, w in enumerate(c.split()):
            bare = re.sub(r'[^A-Za-z]', '', w)
            if i and w.lower().strip('.,()') in CONNECTOR:
                out.append(w.lower())
            elif '.' in w and len(bare) > 1:     # A.A.T.C., S.R.L. stay as written
                out.append(w)
            elif len(bare) <= 3:                 # ABK, AIP, CIR, KWC are acronyms
                out.append(w)
            else:
                out.append(cap(w))
        c = ' '.join(out)
    prev = None
    while prev != c:                      # "Bertolotto S.p.A. Srl" needs two passes,
        prev = c                          # and stripping "AND CO." leaves a dangling
        c = SUFFIX.sub('', c).strip(' ,.')# "and" that has to go with it
        c = re.sub(r'[\s,]+(and|&|y|e)\s*$', '', c, flags=re.I).strip(' ,.')
    return c

# ─────────────────────────── studio pages ───────────────────────────
# VERIFIED against the live site on 20 Sept, replacing five guessed slugs.
# /stone and /bathroom do not exist and were sending people to a 404. The
# site's own segmentation puts stone under Tile & Stone, described as "tile
# showrooms, stone yards, surface distributors", so stone routes to /tile.
#
# Five studios are live: tile, rugs, wallpaper, countertops, mosaic.
# /furniture and /gardens have URLs in the industries list but are NOT in the
# "five live studios" block, so nothing is routed to them.
BASE = 'https://www.tryshowhouse.com'
STUDIO = {
    'tile':        ('/tile',        'Tile Studio'),
    'rugs':        ('/rugs',        'Rug Studio'),
    'wallpaper':   ('/wallpaper',   'Mural Studio'),
    'countertops': ('/countertops', 'Surface Studio'),
    'mosaic':      ('/mosaic',      'Mosaic Studio'),
}

def studio_key(cat, niche, desc):
    """Route on PRODUCT CATEGORY first, description only as fallback.

    `niche` is deliberately never consulted. It is a SOURCE LABEL, not
    evidence: every Cersaie row carries "Ceramic / Tile (verify)" whatever the
    company makes, which routed AIP Porte, a maker of interior doors, to the
    tile studio. Second time that column has broken a classifier here; the
    first was the core-niche test in q1/classify.py.

    "wall coverings" is not a wallpaper signal either. Every tile company on
    earth writes "floor and wall coverings", which sent Aparici, a ceramic tile
    maker, to the mural studio. Wallpaper needs the actual word.

    A row matching nothing returns blank. Those companies sell sanitaryware,
    taps, doors or radiators, and Showhouse has no studio for any of them, so
    they are a QUALIFICATION problem rather than a copy problem. They are
    flagged, not papered over."""
    cat = (cat or '').lower()
    desc = (desc or '')[:300].lower()
    def hit(pat, *f): return any(re.search(pat, x) for x in f)

    TILE = r'tile|ceramic|porcelain|stoneware|\bgres\b|terracotta|cotto|klinker|azulejo|piastrell|seramik'
    if hit(r'\bmosaic|mosaico|mozaik', cat):                                    return 'mosaic'
    if hit(r'wallpaper|wall paper|wallcovering|mural|tapet|carta da parati|papel pintado', cat, desc):
        return 'wallpaper'
    if hit(r'\brug\b|\brugs\b|carpet|moquette|alfombra', cat):                   return 'rugs'
    if hit(TILE, cat):                                                          return 'tile'
    if hit(r'countertop|worktop|benchtop|\bslab|quartz|granite|sintered', cat):  return 'countertops'
    if hit(r'marble|travertine|natural stone|\bstone\b|marmo|marmol', cat):      return 'tile'
    if hit(r'\bmosaic', desc):                                                  return 'mosaic'
    if hit(TILE, desc):                                                         return 'tile'
    return ''

# ─────────────────────────────── copy ───────────────────────────────
# Rewritten 20 Sept against the live Showhouse page, which corrected the angle
# a third time. The product is a white-label AI visualiser AND lead engine: a
# shopper photographs their own room, the brand's product appears in it, a
# guided finder turns their answers into a written brief, and the image unlocks
# only once they verify an email. The brand receives render, brief and a real
# address in one dashboard record.
#
# So the two previous framings were each half right and each wrong alone. The
# first sold "a design tool", which is a feature Daltile and Marazzi give away.
# The second sold the lead record, which is true but abstract in line one. The
# site itself resolves it: "A visualiser is the hook. The pipeline is the
# product." Copy therefore OPENS on the mechanic, because a customer seeing
# your tile on their own floor is instantly picturable, and CLOSES on the
# pipeline, because that is what pays for it.
#
# Three things the page fixed that no amount of rewriting would have:
#   - The product is called Showhouse. Nothing said so before.
#   - There is no self-serve trial, so "start a trial" was an offer we cannot
#     honour. The real ladder is: open a live studio, which needs no sign in,
#     then a demo where the team arrives with the prospect's catalogue loaded.
#   - The studios are openable and render a visitor's own photo. That makes
#     message one's ask genuinely free: look at a page and upload a photo.
#
# Wording is borrowed from the page wherever it is sharper than mine:
# "before they order a sample", "every wall becomes a live product page",
# "without touching anything else in the photo", "live in weeks, not quarters".

def pick(bank, email, salt):
    """Near-identical phrasing across a segment was copy defect four on
    campaign 2, and follow-ups are where it returns: one argument per segment
    collapses to one subject line across 200 addresses. Keyed on the address so
    the choice is stable across rebuilds, and the two people at one company
    still land on different lines."""
    return bank[(hash((email, salt)) & 0x7fffffff) % len(bank)]

S2 = {
 'CA': ['a visualiser is the hook, the pipeline is the product',
        'what happens after the image appears',
        'the brief arrives written, by the shopper',
        'a verified address, not a form fill'],
 'AA': ['the brief written by the client, not your team',
        'what happens after the image appears',
        'from a room photo to a written specification',
        'a verified address, not a form fill'],
 'BA': ['a visualiser is the hook, the pipeline is the product',
        'what happens after the image appears',
        'the brief arrives written, by the shopper',
        'a verified address, not a form fill'],
 'CB': ['which finishes people pick, and which nobody does',
        'every render and every drop off',
        'the part your visualiser does not record',
        'what the funnel would tell you'],
 'AB': ['the enquiry that arrives already specified',
        'every render and every drop off',
        'what your team stops having to draw',
        'what the funnel would tell you'],
 'BB': ['which finishes people pick, and which nobody does',
        'every render and every drop off',
        'the record behind each render',
        'what the funnel would tell you'],
}
S3 = {
 'A': ['live in weeks, not quarters',
       'your catalogue, already loaded',
       'the timeline, and then I will stop',
       'what the build actually involves'],
 'B': ['your catalogue, already loaded',
       'live in weeks, not quarters',
       'closing this out with the timeline',
       'a straight question before I stop'],
}

DEMO = 'https://www.tryshowhouse.com/#book'

# Message 1 needs a bank too. Variants A and C vary naturally, because their
# subjects carry the prospect's own tool name or their own quoted line, but
# variant B is 273 of the 390 rows and had one fixed string, so 220 addresses
# were receiving an identical subject. That is the campaign-2 defect exactly.
S1 = {
 'BA': ['your products, in their own room',
        'what {dom} cannot show them',
        'the room they are standing in',
        'a photograph of their room, and your tile in it'],
 'BB': ['every wall becomes a live product page',
        'the page they show their partner',
        'a catalogue is browsed and left',
        'what a visitor leaves behind'],
}

def variant_C(f, co, dom, tool, hook, thread, partner, url, lab):
    """Already runs a visualiser. Never suggest they lack one. Their tool is
    the hook; what they do not have is the pipeline behind it. This is the
    site's own argument and it lands hardest on exactly this cohort."""
    t = tool or 'your room visualiser'
    if thread == 'A':
        s1 = f'{t} shows the room, and then what'
        b1 = f"""Hello {f},

{co} already runs {t}, which puts you ahead of most of this category.

The question is what happens after the image appears. Someone renders a room, likes what they see, and leaves without a name attached.

Showhouse is the same render under your own brand and domain, except the image unlocks once the visitor verifies an email. The lead reaches you with the picture and a written brief already on it.

Open it and render a photo of your own room: {url}

Shall I have {co} products loaded before we speak?"""
        b2 = f"""Hello {f},

Anyone can put a render button on a website. What pays for it is everything after the image.

A short guided finder asks the shopper about style, colour and space. Their answers become a written brief. The image unlocks only once the email is verified, so the address reaching your team is real.

Your salesperson opens one record: the render, the brief, the products and a genuine contact.

{url}

We can load {co} products and walk you through a shopper's journey end to end: {DEMO}"""
        b3 = f"""Hello {f},

The last thing worth knowing is the timeline.

The engine is built. Most of the work is catalogue preparation and branding, so it goes live in weeks under your own logo and domain, not in quarters.

The Mosaic Studio on the site is the original build, running for MEC Artworks today.

If you would like to see it with {co} products already loaded, I can arrange that: {DEMO}"""
    else:
        s1 = 'the part a visualiser does not record'
        b1 = f"""Hello {f},

A note about {dom} rather than a pitch.

{co} already lets a visitor preview products in a room. What that does not leave you with is the record of what they tried.

Showhouse keeps all of it. Every render and every drop off, so you can see which finishes people choose and which ones nobody ever picks, alongside a verified email for each one.

The studio is open, no sign in needed: {url}

Worth a look?"""
        b2 = (f"""Hello {f},

To be concrete about the output, since that is where the value sits.

A shopper answers a few questions about style, colour and space, renders the room, then verifies an email to keep the image. You receive one record: the render, the brief in their own words, the products, and an address that is real.

I wrote to {partner} as well, since I could not tell from outside which of you owns the website.

{url}"""
              if partner else f"""Hello {f},

To be concrete about the output, since that is where the value sits.

A shopper answers a few questions about style, colour and space, renders the room, then verifies an email to keep the image. You receive one record: the render, the brief in their own words, the products, and an address that is real.

{url}

Worth twenty minutes with your own catalogue in it?""")
        b3 = f"""Hello {f},

Closing this out.

It runs under your brand on your own domain, and it goes live in weeks rather than quarters, because the engine is built and the work is catalogue preparation.

If it is not a priority this year, say so and I will leave it there. If it is, we will arrive with {co} products already loaded and walk through a shopper's journey start to finish: {DEMO}"""
    return s1, b1, pick(S2['C'+thread], f+co, 2), b2, pick(S3[thread], f+co, 3), b3

def variant_A(f, co, dom, tool, hook, thread, partner, url, lab):
    """A person does the visualising today, and a physical sample usually
    follows. The site's own line for this is "before they order a sample"."""
    line = f'On your own site: "{hook}".' if hook else \
           f'{co} sells bespoke work, and a client starts one by contacting your team.'
    if thread == 'A':
        s1 = 'before they order a sample'
        b1 = f"""Hello {f},

{line}

Every one of those enquiries reaches your team as words, and somebody then has to turn it into a picture before anything moves. A sample goes in the post and a week disappears.

Showhouse puts that step on your website. The client photographs their own room, your product appears in it, and it reaches you as a lead with the render and a written brief attached.

Render a photo of your own room here: {url}

Shall I have {co} products loaded before we speak?"""
        b2 = f"""Hello {f},

The part that matters is what your team stops doing.

A guided finder asks the client about style, colour and space, and their answers become a written brief. It renders only inside your catalogue, your finishes and your size rules, so nothing comes back that you cannot make.

The enquiry arrives specified, with a verified email on it, rather than as a description somebody has to interpret.

{url}

We can load {co} products and walk you through it end to end: {DEMO}"""
        b3 = f"""Hello {f},

The last thing worth knowing is the timeline.

The engine is built, so most of the work is catalogue preparation and branding. It goes live in weeks under your own logo and domain.

The Mosaic Studio on the site is the original build, running for MEC Artworks today.

If this sits with a colleague rather than with you, tell me who and I will approach them instead: {DEMO}"""
    else:
        s1 = 'the visitors who never get in touch'
        b1 = f"""Hello {f},

{line}

Most visitors will not do that. Not from lack of interest, but because they cannot picture what they would be asking for yet. They leave, and you never learn who they were.

Showhouse changes what the website does with that traffic. The visitor photographs their room, your product appears in it, and the image unlocks once they verify an email.

The studio is open, no sign in needed: {url}

Worth a look?"""
        b2 = (f"""Hello {f},

To be concrete about what reaches your team.

The shopper answers a few questions about style, colour and space, renders their own room, then verifies an email to keep the picture. You get one record: the render, the brief in their words, the products, and a real address.

I wrote to {partner} as well, since I could not tell from outside which of you owns the website.

{url}"""
              if partner else f"""Hello {f},

To be concrete about what reaches your team.

The shopper answers a few questions about style, colour and space, renders their own room, then verifies an email to keep the picture. You get one record: the render, the brief in their words, the products, and a real address.

{url}

Worth twenty minutes with your own catalogue in it?""")
        b3 = f"""Hello {f},

Closing this out.

It carries your logo, your colours and your domain, and it goes live in weeks rather than quarters, because the engine is already built.

If it is not a priority this year, say so and I will leave it there. If it is, we will arrive with {co} products already loaded and walk through a shopper's journey start to finish: {DEMO}"""
    return s1, b1, pick(S2['A'+thread], f+co, 2), b2, pick(S3[thread], f+co, 3), b3

def variant_B(f, co, dom, tool, hook, thread, partner, basic, url, lab):
    """No design step, or filters only. Open on what they promise, never on
    what they lack: qualifier 1 records NONE as none found, not none exists."""
    if hook:
        line = f'On your own site: "{hook}".'
    elif basic:
        line = f'{dom} lets a visitor filter and browse, which helps them find a product.'
    else:
        line = f'{dom} presents the collections well, and the visit ends at a catalogue.'
    if thread == 'A':
        s1 = pick(S1['BA'], f + co, 1).format(dom=dom)
        b1 = f"""Hello {f},

{line}

What it cannot do is show somebody your product in the room they are standing in. So they browse, form an opinion and leave, and you never learn who they were.

Showhouse does that on your own site. They photograph the room, your product appears in it without touching anything else in the picture, and the image unlocks once they verify an email.

Render a photo of your own room here: {url}

Shall I have {co} products loaded before we speak?"""
        b2 = f"""Hello {f},

Anyone can put a render button on a website. What pays for it is everything after the image.

A guided finder asks the shopper about style, colour and space, and their answers become a written brief. It renders only inside your catalogue and your size rules, so every result is something you can quote and ship.

Your salesperson opens one record: the render, the brief, the products, and a verified address.

{url}

We can load {co} products and walk you through a shopper's journey end to end: {DEMO}"""
        b3 = f"""Hello {f},

The last thing worth knowing is the timeline.

The engine is built, so most of the work is catalogue preparation and branding. It goes live in weeks under your own logo and domain, on {dom}, not in quarters.

The Mosaic Studio on the site is the original build, running for MEC Artworks today.

If this sits with a colleague rather than with you, tell me who and I will approach them instead: {DEMO}"""
    else:
        s1 = pick(S1['BB'], f + co, 1).format(dom=dom)
        b1 = f"""Hello {f},

A note about {dom} rather than a pitch.

A catalogue website is browsed and left. Showhouse lets a visitor photograph their own room and see your product in it, so the page stops being a brochure and becomes the thing they show their partner.

Underneath it sits the commercial part. Every image unlocks against a verified email, so each render reaches you as a lead with a written brief on it.

The studio is open, no sign in needed: {url}

Worth a look?"""
        b2 = (f"""Hello {f},

To be concrete about the output, since that is where the value sits.

A shopper answers a few questions about style, colour and space, renders their own room, then verifies an email to keep the image. You receive one record: the render, the brief in their own words, the products, and an address that is real.

I wrote to {partner} as well, since I could not tell from outside which of you owns the website.

{url}"""
              if partner else f"""Hello {f},

To be concrete about the output, since that is where the value sits.

A shopper answers a few questions about style, colour and space, renders their own room, then verifies an email to keep the image. You receive one record: the render, the brief in their own words, the products, and an address that is real.

{url}

Worth twenty minutes with your own catalogue in it?""")
        b3 = f"""Hello {f},

Closing this out.

It runs under your brand on your own domain, and it goes live in weeks rather than quarters, because the engine is built and the work is catalogue preparation.

If it is not a priority this year, say so and I will leave it there. If it is, we will arrive with {co} products already loaded and walk through a shopper's journey start to finish: {DEMO}"""
    return s1, b1, pick(S2['B'+thread], f+co, 2), b2, pick(S3[thread], f+co, 3), b3

# ─────────────────────────────── build ───────────────────────────────
rows = list(csv.DictReader(open(SRC, encoding='utf-8-sig')))
COLS = ['email','first_name','last_name','company_name','website','contact_thread',
        'segment_variant','send_day_1','send_day_2','send_day_3',
        'msg_subject_1','msg_body_1','msg_subject_2','msg_body_2','msg_subject_3','msg_body_3',
        'studio_url','qa_send_flag',
        'qa_tool_level','qa_has_tryon','qa_tool_name','qa_studio','qa_hook_quality','qa_hook',
        'qa_partner_email','qa_country','qa_size','qa_evidence']
DAYS = {'A': ('1','6','13'), 'B': ('3','9','16')}

out, seen = [], set()
for r in rows:
    co_raw = clean(r['company'])
    co  = titlecase_company(co_raw)
    dom = clean(r['domain']).split()[0] if clean(r['domain']) else ''
    ev  = clean(r['Use AI Tool Evidence'])
    lvl = clean(r['Use AI Tool Level'])
    tryon = clean(r['Use AI Has Tryon']).lower()
    tool = tool_name(ev, r['Use AI Tool Url'])
    hook = best_quote(ev)
    seg = 'C' if tryon == 'yes' else ('A' if lvl == 'MANUAL' else 'B')
    sk  = studio_key(r['Use AI Product Category'], r['niche'], r['Description'])
    path, lab = STUDIO.get(sk, ('', 'Mosaic Studio'))
    url = BASE + path

    people = []
    for col, nmcol, thread in (('Work Email (2)','Full Name p1','A'), ('Work Email','Full Name p2','B')):
        e = clean(r[col]).lower()
        nm = clean(r[nmcol])
        if e and '@' in e:
            people.append((e, nm, thread))
    # A single-contact company runs thread A only, whichever column it arrived in,
    # so the stronger opening is never wasted on the only person we can reach.
    if len(people) == 1:
        people = [(people[0][0], people[0][1], 'A')]

    firsts = {th: (person_name(nm).split()[0] if nm else '') for _, nm, th in people}
    for email, name, thread in people:
        if email in seen:
            continue
        seen.add(email)
        parts = person_name(name).split()
        first = parts[0] if parts else ''
        last = ' '.join(parts[1:]) if len(parts) > 1 else ''
        other = 'B' if thread == 'A' else 'A'
        partner = firsts.get(other, '')
        partner_email = next((e for e, _, th in people if th == other), '')

        if seg == 'C':
            s1,b1,s2,b2,s3,b3 = variant_C(first, co, dom, tool, hook, thread, partner, url, lab)
        elif seg == 'A':
            s1,b1,s2,b2,s3,b3 = variant_A(first, co, dom, tool, hook, thread, partner, url, lab)
        else:
            s1,b1,s2,b2,s3,b3 = variant_B(first, co, dom, tool, hook, thread, partner, lvl == 'BASIC', url, lab)

        if seg == 'C':
            hq = 'strong' if tool else 'weak'
        else:
            hq = 'strong' if hook else 'weak'

        d = DAYS[thread]
        out.append(dict(email=email, first_name=first, last_name=last, company_name=co,
            website=dom, contact_thread=thread, segment_variant=seg,
            send_day_1=d[0], send_day_2=d[1], send_day_3=d[2],
            msg_subject_1=s1, msg_body_1=b1, msg_subject_2=s2, msg_body_2=b2,
            msg_subject_3=s3, msg_body_3=b3,
            studio_url=url,
            # No studio means Showhouse has no page for what they sell: taps,
            # sanitaryware, doors, radiators, bathroom furniture. The link
            # still resolves, to the homepage, but the pitch does not. This is
            # a QUALIFICATION result, not a copy problem, and it is the single
            # most useful filter in the file: hold these until someone decides
            # whether a company that sells no installed surface belongs here.
            qa_send_flag=('send' if sk else 'HOLD no studio'),
            qa_tool_level=lvl, qa_has_tryon=tryon, qa_tool_name=tool, qa_studio=sk,
            qa_hook_quality=hq, qa_hook=hook, qa_partner_email=partner_email,
            qa_country=clean(r['country']), qa_size=clean(r['Size']), qa_evidence=ev))

with open(OUT, 'w', newline='', encoding='utf-8-sig') as fh:
    w = csv.DictWriter(fh, fieldnames=COLS)
    w.writeheader()
    w.writerows(out)
print('rows:', len(out))
