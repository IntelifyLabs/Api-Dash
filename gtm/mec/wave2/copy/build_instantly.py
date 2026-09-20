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

# ─── humanised 20 Sept ───────────────────────────────────────────────
# Structure, order, arguments, CTAs and links are unchanged and approved.
# Only the sentences changed. Four things were making it read as written
# rather than typed:
#   - abstract subjects. "The question is what happens after the image
#     appears" became "the bit that's missing is what happens next".
#   - stiff openers. "To be concrete about the output, since that is where
#     the value sits" became "here's what actually reaches you".
#   - no contractions anywhere, which is the single loudest tell. They are
#     used normally now.
#   - formal asks. "Shall I have X products loaded before we speak" became
#     "want me to load some X products in first".
# Long words were swapped for short ones throughout: "catalogue preparation"
# to "loading your catalogue", "genuine contact" to "a person to call",
# "specification" to "spec". Sentences are shorter and more of them start
# with you.

def pick(bank, email, salt):
    """Near-identical phrasing across a segment was copy defect four on
    campaign 2, and it creeps back wherever one argument serves 200 rows.
    Keyed on the address so the choice is stable across rebuilds, and the two
    people at one company still land on different lines."""
    return bank[(hash((email, salt)) & 0x7fffffff) % len(bank)]

DEMO = 'https://www.tryshowhouse.com/#book'

S1 = {
 'BA': ['your products, in their own room',
        "what {dom} can't show them",
        "the room they're standing in",
        'their room photo, your tile in it'],
 'BB': ['every wall becomes a live product page',
        'the page they show their partner',
        'a catalogue gets looked at and closed',
        'what a visitor leaves behind'],
}
S2 = {
 'CA': ['a visualiser is the hook, the pipeline is the product',
        'what comes after the picture',
        'the brief writes itself',
        'a real email, not a form fill'],
 'AA': ['the brief your client writes, not your team',
        'what comes after the picture',
        'from a room photo to a proper spec',
        'a real email, not a form fill'],
 'BA': ['a visualiser is the hook, the pipeline is the product',
        'what comes after the picture',
        'the brief writes itself',
        'a real email, not a form fill'],
 'CB': ['which finishes people go for, and which nobody touches',
        'every render, every drop off',
        "the part your visualiser doesn't keep",
        'what the numbers would tell you'],
 'AB': ['the enquiry that turns up already spelled out',
        'every render, every drop off',
        'what your team stops having to draw',
        'what the numbers would tell you'],
 'BB': ['which finishes people go for, and which nobody touches',
        'every render, every drop off',
        "what's behind each picture",
        'what the numbers would tell you'],
}
S3 = {
 'A': ['live in weeks, not quarters',
       'your catalogue, already loaded',
       'last thing, on timing',
       'what the build actually looks like'],
 'B': ['your catalogue, already loaded',
       'live in weeks, not quarters',
       'wrapping this up',
       'one straight question and then I stop'],
}

# Shared closers. Message 2 thread B and message 3 thread B make the same
# point in every segment, so they live in one place rather than three.
def _b2(f, url, partner):
    if partner:
        return f"""Hello {f},

Here's what actually reaches you.

Someone answers a few quick questions about style, colour and space, renders their room, then confirms their email to keep the picture. You get one record: the image, what they asked for in their own words, the products, and a real address.

I sent this to {partner} too, since I couldn't tell from outside whose call it is.

{url}"""
    return f"""Hello {f},

Here's what actually reaches you.

Someone answers a few quick questions about style, colour and space, renders their room, then confirms their email to keep the picture. You get one record: the image, what they asked for in their own words, the products, and a real address.

{url}

Worth twenty minutes with your own products in it?"""

def _b3(f, co):
    return f"""Hello {f},

Wrapping this up.

It runs under your own name on your own site, and it's live in weeks rather than quarters, because the engine is built and the work is loading your catalogue.

If it's not something for this year, tell me and I'll leave it there. If it is, we'll turn up with {co} products already in it and walk you through what a shopper sees: {DEMO}"""

def variant_C(f, co, dom, tool, hook, thread, partner, url, lab):
    """Already runs a visualiser. Never suggest they lack one. Theirs is the
    hook; what they haven't got is the pipeline behind it."""
    t = tool or 'your room visualiser'
    if thread == 'A':
        s1 = f'{t} shows the room, and then what'
        b1 = f"""Hello {f},

You already run {t}, so someone can see your products in their own room. Most brands still can't do that.

The bit that's missing is what happens next. They render a room, like it, and leave. You never find out who they were.

Showhouse does the same thing under your own name, except the picture only unlocks once they confirm their email. So the render reaches you, with what they asked for attached.

Have a go on a photo of your own room: {url}

Want me to load some {co} products in first?"""
        b2 = f"""Hello {f},

A render button is easy. The useful part is what comes after the picture.

Before they see it, a few quick questions ask what style, colour and space they're working with. Those answers turn into a short brief. Then they confirm their email to keep the image, so the address you get is a real one.

Your salesperson opens one thing and sees the room, the brief, the products and a person to call.

{url}

Happy to put {co} products in and show you the whole journey: {DEMO}"""
        b3 = f"""Hello {f},

Last thing, in case timing is what you're weighing up.

The engine already exists. What takes time is getting your catalogue in and making it look like you. That's weeks, not quarters.

The Mosaic Studio on the site is the first one we built. It has been running for MEC Artworks ever since.

If it would help to see it with {co} products in it, I can set that up: {DEMO}"""
    else:
        s1 = "the part a visualiser doesn't keep"
        b1 = f"""Hello {f},

Quick thought about {dom} rather than a pitch.

People can already preview your products in a room. What you don't get back is any record of what they tried.

Showhouse keeps all of it. Every render and every drop off, so you can see which finishes people go for and which ones nobody touches. Each one comes with a confirmed email.

The studio is open, nothing to sign into: {url}

Worth a look?"""
        b2 = _b2(f, url, partner)
        b3 = _b3(f, co)
    return (s1, b1, pick(S2['C'+thread], f+co, 2), b2, pick(S3[thread], f+co, 3), b3)

def variant_A(f, co, dom, tool, hook, thread, partner, url, lab):
    """A person does the visualising today and a sample usually follows."""
    line = f'On your own site: "{hook}".' if hook else \
           f'{co} sells bespoke work, and the way in is to contact your team.'
    if thread == 'A':
        s1 = 'before they order a sample'
        b1 = f"""Hello {f},

{line}

Every one of those comes in as words, and then somebody on your side has to turn it into a picture. A sample goes in the post and a week disappears.

Showhouse puts that step on your website instead. They photograph their own room, your product shows up in it, and it reaches you with the picture and a short brief already attached.

Try it on a photo of your own room: {url}

Want me to load some {co} products in first?"""
        b2 = f"""Hello {f},

The point is what your team stops doing.

A few questions about style, colour and space turn into a written brief. It only renders what is in your catalogue, your finishes and your sizes, so nothing comes back that you cannot actually make.

The enquiry lands already spelled out, with a confirmed email on it, instead of a description somebody has to decode.

{url}

Happy to load {co} products and take you through it: {DEMO}"""
        b3 = f"""Hello {f},

Last thing, on timing.

The engine is already built. What takes time is getting your catalogue in and making it look like yours. Weeks, not quarters.

The Mosaic Studio on the site was the first one. It has been running for MEC Artworks since.

If this belongs with somebody else, tell me who and I will go to them instead: {DEMO}"""
    else:
        s1 = 'the visitors who never get in touch'
        b1 = f"""Hello {f},

{line}

Most people won't. Not because they aren't interested, but because they can't picture what they would even be asking for. So they leave, and you never know they were there.

Showhouse changes what your site does with them. They photograph the room, your product appears in it, and the picture unlocks when they confirm their email.

The studio is open, nothing to sign into: {url}

Worth a look?"""
        b2 = _b2(f, url, partner)
        b3 = _b3(f, co)
    return (s1, b1, pick(S2['A'+thread], f+co, 2), b2, pick(S3[thread], f+co, 3), b3)

def variant_B(f, co, dom, tool, hook, thread, partner, basic, url, lab):
    """No design step, or filters only. Open on what they promise, never on
    what they lack: qualifier 1 records NONE as none found, not none exists."""
    if hook:
        line = f'On your own site: "{hook}".'
    elif basic:
        line = f'{dom} lets people filter and browse, which helps them find a product.'
    else:
        line = f'{dom} shows the collections well, and then the visit ends at a catalogue.'
    if thread == 'A':
        s1 = pick(S1['BA'], f + co, 1).format(dom=dom)
        b1 = f"""Hello {f},

{line}

What it can't do is show somebody your product in the room they are standing in. So they look, make their mind up and go, and you never find out who they were.

Showhouse does that on your own site. They take a photo of the room, your product appears in it and nothing else in the picture moves, and the image unlocks when they confirm their email.

Try it on a photo of your own room: {url}

Want me to load some {co} products in first?"""
        b2 = f"""Hello {f},

A render button is easy. The useful part is what comes after the picture.

A few questions about style, colour and space turn into a short brief. It only renders what is in your catalogue and your sizes, so everything that comes back is something you can quote and ship.

Your salesperson opens one thing: the image, the brief, the products, and a confirmed email.

{url}

Happy to load {co} products and show you the whole journey: {DEMO}"""
        b3 = f"""Hello {f},

Last thing, on timing.

The engine is already built. What takes time is getting your catalogue in and making it look like yours, on {dom}. Weeks, not quarters.

The Mosaic Studio on the site was the first one. It has been running for MEC Artworks since.

If this belongs with somebody else, tell me who and I will go to them instead: {DEMO}"""
    else:
        s1 = pick(S1['BB'], f + co, 1).format(dom=dom)
        b1 = f"""Hello {f},

Quick thought about {dom} rather than a pitch.

A catalogue gets looked at and closed. Showhouse lets somebody photograph their own room and see your product in it, which turns the page into the thing they show their partner.

Underneath that sits the part that pays. Every picture unlocks against a confirmed email, so each one reaches you as a lead with a short brief on it.

The studio is open, nothing to sign into: {url}

Worth a look?"""
        b2 = _b2(f, url, partner)
        b3 = _b3(f, co)
    return (s1, b1, pick(S2['B'+thread], f+co, 2), b2, pick(S3[thread], f+co, 3), b3)

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
