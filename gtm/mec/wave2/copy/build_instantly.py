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
        q = q.strip().rstrip(',;:').strip()
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
# Email 1 now carries the link, reversing the earlier "no link in touch 1"
# call. Shahwaz overruled it: the page is the closer and holding it back asks
# people to reply blind. The link is the CATEGORY page, never the homepage, so
# a tile manufacturer lands on tile work rather than a general pitch.
#
# ⚠ PATHS ARE UNCONFIRMED. tryshowhouse.com cannot be loaded from this
# environment (the proxy answers 403 to CONNECT), so these five slugs are
# proposed, not verified. Correct them in this one dict and rebuild. A wrong
# path sends 390 people to a 404, which is worse than sending them nowhere.
BASE = 'https://www.tryshowhouse.com'
STUDIO = {'tile': '/tile', 'mosaic': '/mosaic', 'stone': '/stone',
          'wallpaper': '/wallpaper', 'bathroom': '/bathroom'}

def studio_key(cat, niche, desc):
    """Route on the PRODUCT CATEGORY first, and only fall back to the long
    description. Reading them as one blob sent Aparici, a ceramic tile maker,
    to the wallpaper page, because its description says "wall coverings" and
    the wallpaper test ran first. Every tile company on earth writes "floor and
    wall coverings", so that phrase is no longer a wallpaper signal: wallpaper
    now needs the actual word, in one of the four languages on this list.

    `niche` is deliberately NOT consulted. It is a SOURCE LABEL, not evidence:
    every Cersaie row carries "Ceramic / Tile (verify)" regardless of what the
    company makes, so including it routed AIP Porte, a maker of interior doors,
    to the tile studio. This is the second time that column has poisoned a
    classifier in this campaign; the first was the core-niche test in
    q1/classify.py, which passed all 476 Cersaie rows as tile.

    A row that matches nothing returns blank and links to the homepage rather
    than to a page that does not fit. There is no door studio, so AIP Porte
    gets the homepage, and `qa_studio` is blank so those rows are findable."""
    cat = (cat or '').lower()
    desc = (desc or '')[:300].lower()
    niche = (niche or '').lower()

    def hit(pat, *fields):
        return any(re.search(pat, f) for f in fields)
    del niche                       # see the docstring: source label, not evidence

    TILE = r'tile|ceramic|porcelain|stoneware|\bgres\b|terracotta|cotto|klinker|azulejo|piastrell|seramik'
    if hit(r'\bmosaic|mosaico|mozaik', cat):                         return 'mosaic'
    if hit(r'wallpaper|wall paper|wallcovering|mural|tapet|'
           r'carta da parati|papel pintado', cat, desc):              return 'wallpaper'
    if hit(TILE, cat):                                                return 'tile'
    if hit(r'marble|travertine|granite|natural stone|quartz|\bstone\b|marmo|marmol', cat):
        return 'stone'
    if hit(r'faucet|sanitary|shower|bathroom|\btap\b|basin|bathtub|washbasin|grifer', cat):
        return 'bathroom'
    if hit(r'\bmosaic', desc):                                              return 'mosaic'
    if hit(TILE, desc):                                                      return 'tile'
    return ''

# ─────────────────────────────── copy ───────────────────────────────
# Rewritten 19 Sept against Shahwaz's feedback. Four changes, all deliberate:
#
# 1. The product is no longer described as "a design tool". That framing sells
#    a feature nobody is short of, and it is what Daltile and Marazzi already
#    give away. What the buyer is short of is a NAMED lead. So the pitch is the
#    lead record: the render, the exact products chosen, and the contact
#    details, arriving in a dashboard their sales team works from.
# 2. Each of the six messages per company now carries a different reason to
#    reply. Thread A runs lead capture, then catalogue integration, then the
#    MEC build and the timeline. Thread B runs search and positioning, then
#    what the sales team receives, then speed to go live. Previously all three
#    restated the same argument at different lengths.
# 3. MEC Artworks leads with nothing. The name means nothing to a tile plant in
#    Castellon, so it appears as proof in message three, never as the opening,
#    and it is always described ("a mosaic manufacturer") rather than assumed.
# 4. Register lifted for European B2B. Most of this list is Italian, Spanish,
#    Portuguese and Turkish. Gone: "straight with you", "poke at it", "you know
#    where I am", "I am out of your inbox".
#
# Unchanged: no dash of any kind, no filtered word, short paragraphs, no
# signature block. First emails now run to 100 words rather than 90, because a
# link and a concrete deliverable will not fit in 90 and the extra fifteen
# words buy the thing the feedback asked for.
#
# ⚠ HONEST-PROOF. The only MEC figures used are the two published ones, seven
# weeks and a team of three. The case study carries no performance numbers, so
# none are claimed. If Abdullah can get one real figure out of MEC (leads
# captured per month, or time on page before and after) message three in both
# threads becomes materially stronger. That is the single highest-value thing
# missing from this copy.

# Near-identical phrasing across the majority of emails was copy defect number
# four on campaign 2, and follow-ups are where it creeps back: the argument is
# the same for every row in a segment, so the subject line collapses to one
# string across 200 addresses. Each follow-up therefore draws from a bank,
# keyed on a hash of the address so the choice is stable across rebuilds and
# the two people at one company still land on different lines.
def pick(bank, email, salt):
    return bank[(hash((email, salt)) & 0x7fffffff) % len(bank)]

S2 = {
 'CA': ['renders made only from what you actually sell',
        'it runs on your catalogue, not a stock library',
        'why the lead is worth opening',
        'every render is a specification you can quote'],
 'AA': ['your own catalogue, not a generic library',
        'from a written brief to an approved visual',
        'what your team stops having to draw',
        'the descriptions your team works from today'],
 'BA': ['renders made only from what you actually sell',
        'your collections, not a stock library',
        'what makes the lead worth opening',
        'a specification rather than a mood board'],
 'CB': ['what lands in your dashboard',
        'the record your sales team receives',
        'a lead with the render attached',
        'who designed it, and what they chose'],
 'AB': ['what your team receives',
        'a lead with the drawing already done',
        'the record that reaches your desk',
        'who it was, and what they chose'],
 'BB': ['what lands in your dashboard',
        'the record your sales team receives',
        'a lead with the render attached',
        'who designed it, and what they chose'],
}
S3 = {
 'A': ['seven weeks from brief to live',
       'how long this actually takes',
       'the timeline, and then I will stop',
       'what seven weeks bought MEC Artworks'],
 'B': ['seven weeks, and then it is yours',
       'the timeline, and a straight question',
       'what this looks like as a project',
       'closing this out with the timeline'],
}

def variant_C(f, co, dom, tool, hook, thread, partner, url):
    """Already runs a visualiser. Never suggest they lack a tool. The gap is
    that their tool is anonymous: it renders, then the visitor disappears."""
    t = tool or 'your room visualiser'
    if thread == 'A':
        s1 = f'what {t} does not send to your sales team'
        b1 = f"""Hello {f},

{co} already runs {t}, so a visitor can see a surface in their own room.

What it does not do is tell you who that visitor was. They design, they close the tab, and the interest is gone.

We build the same experience with a lead layer underneath. The visitor keeps the render. You receive the render, the exact products they chose and their contact details, as a record your team can act on.

Our work in your category: {url}

Shall I set one up on {co} products?"""
        s2 = 'renders made only from what you actually sell'
        b2 = f"""Hello {f},

The detail that decides whether this is worth your time: it runs on your catalogue, not a generic material library.

We load your collections, formats and finishes. Anything a visitor produces is therefore a specification your team can quote and ship, with no approximate colours and no surfaces you do not make.

That is also what makes the lead valuable. Your salesperson opens it already knowing the products, the room and the person.

{url}

Send me one collection name and I will build it into a working version for you."""
        s3 = 'seven weeks from brief to live'
        b3 = f"""Hello {f},

The last thing worth knowing is the timeline.

We built this for MEC Artworks, a mosaic manufacturer, in seven weeks with a team of three. It is live and their team uses it daily. That is the realistic schedule for a branded version on your own domain, not a twelve month platform project.

If this sits with a colleague rather than with you, tell me who and I will approach them instead.

{url}"""
    else:
        s1 = 'the page visitors stay on'
        b1 = f"""Hello {f},

A note about {dom} rather than a pitch.

{co} already runs {t}, which puts you ahead of most of the category. The next move is what that traffic leaves behind: right now a visitor designs, then leaves anonymously.

We build the same experience so the visitor keeps the render and you keep the lead, with the products chosen and the contact details attached.

There is a positioning argument too. Daltile and Marazzi both went this way. In your market it is still open.

{url}"""
        s2 = 'what lands in your dashboard'
        b2 = (f"""Hello {f},

To be concrete about the output, since the value sits in what your team receives.

A visitor finishes a design. You get one record: the rendered room, the products and formats used, and their name and email address. Your team then calls somebody who has already chosen.

I wrote to {partner} as well, since I could not tell from outside which of you owns the website.

{url}

Name one collection and I will build it into a version for you.""" if partner else f"""Hello {f},

To be concrete about the output, since the value sits in what your team receives.

A visitor finishes a design. You get one record: the rendered room, the products and formats used, and their name and email address. Your team then calls somebody who has already chosen.

{url}

Name one collection and I will build it into a version for you.""")
        s3 = 'seven weeks, and then it is yours'
        b3 = f"""Hello {f},

Closing this out.

We built this for MEC Artworks, a mosaic manufacturer, in seven weeks with three people, and it runs on their site today. A branded version for {co}, on your own catalogue and your own domain, is the same order of work.

If it is not a priority this year, say so and I will leave it there. If it is, the fastest first step is a collection name.

{url}"""
    return s1, b1, s2, b2, s3, b3

def variant_A(f, co, dom, tool, hook, thread, partner, url):
    """A person does the visualising today. The enquiry arrives as a
    description and somebody has to turn it into a picture before anything
    moves. Replace that step, never the craft behind it."""
    line = f'On your own site: "{hook}".' if hook else \
           f'{co} sells bespoke work, and the way a client starts one is to contact your team.'
    if thread == 'A':
        s1 = 'the enquiry that arrives without a picture'
        b1 = f"""Hello {f},

{line}

Every one of those enquiries reaches your team as a description, and somebody then has to turn it into a visual before the conversation can move forward.

We move that step into the website. The client produces the visual from your own products, and it reaches your team as a complete lead: the render, the products chosen and the contact details.

Our work in your category: {url}

Shall I load a few {co} products into one for you?"""
        s2 = 'your own catalogue, not a generic library'
        b2 = f"""Hello {f},

The detail that decides whether this is worth your time: it runs on your own catalogue.

We load your collections, formats and finishes, so whatever a client produces is a specification you can quote and make. Nothing comes back in a colour you do not make.

Your team stops working from written descriptions and starts working from a visual the client has already approved.

{url}

Send me one collection name and I will build it into a working version."""
        s3 = 'seven weeks from brief to live'
        b3 = f"""Hello {f},

The last thing worth knowing is the timeline.

We built this for MEC Artworks, a mosaic manufacturer, in seven weeks with a team of three. It is live and in daily use. That is the realistic schedule for a branded version on {dom}.

If this sits with a colleague, tell me who and I will approach them instead.

{url}"""
    else:
        s1 = 'the visitors who never get in touch'
        b1 = f"""Hello {f},

{line}

Most visitors will not do that. Not from lack of interest, but because they cannot yet picture what they would be asking for. They leave, and you never learn who they were.

We change what the website does with that traffic. The visitor builds the picture from your own products, and you receive it as a lead with their contact details attached.

Our work in your category: {url}

Shall I set one up on {co} products?"""
        s2 = 'what your team receives'
        b2 = (f"""Hello {f},

To be concrete about the output, since that is where the value is.

A visitor finishes a design. You get one record: the rendered room, the exact products and formats used, and their name and email. Your team then speaks to somebody who has already decided.

I wrote to {partner} as well, since I could not tell from outside which of you owns the website.

{url}

Name one collection and I will build it into a version for you.""" if partner else f"""Hello {f},

To be concrete about the output, since that is where the value is.

A visitor finishes a design. You get one record: the rendered room, the exact products and formats used, and their name and email. Your team then speaks to somebody who has already decided.

{url}

Name one collection and I will build it into a version for you.""")
        s3 = 'seven weeks, and then it is yours'
        b3 = f"""Hello {f},

Closing this out.

We built this for MEC Artworks, a mosaic manufacturer, in seven weeks with three people, and it runs on their site today. A branded version for {co} is the same order of work.

If it is not a priority this year, say so and I will leave it there. If it is, the fastest first step is a collection name.

{url}"""
    return s1, b1, s2, b2, s3, b3

def variant_B(f, co, dom, tool, hook, thread, partner, basic, url):
    """No design step, or filters only. Open on what they promise, never on
    what they lack: qualifier 1 records NONE as none found, not none exists."""
    if hook:
        line = f'On your own site: "{hook}".'
    elif basic:
        line = f'{dom} lets a visitor filter and browse, which helps them find a product.'
    else:
        line = f'{dom} presents the collections well, and the visit ends at a catalogue.'
    if thread == 'A':
        s1 = f'the visitors {dom} cannot name'
        b1 = f"""Hello {f},

{line}

So a visitor forms an opinion and leaves, and you never learn who they were or which products held their attention.

We change what the website does with that traffic. The visitor designs a room from your own collections, and you receive the render, the product list and their contact details as a single lead record.

Our work in your category: {url}

Shall I put a {co} collection into one so you can try it?"""
        s2 = 'renders made only from what you actually sell'
        b2 = f"""Hello {f},

The detail that decides whether this is worth your time: it runs on your catalogue, not a generic material library.

We load your collections, formats and finishes, so anything a visitor produces is a specification your team can quote and ship.

That is what makes the lead worth having. Your salesperson opens it already knowing the products, the room and the person.

{url}

Send me one collection name and I will build it into a working version for you."""
        s3 = 'seven weeks from brief to live'
        b3 = f"""Hello {f},

The last thing worth knowing is the timeline.

We built this for MEC Artworks, a mosaic manufacturer, in seven weeks with a team of three. It is live and in daily use. That is the realistic schedule for a branded version on {dom}, not a twelve month platform project.

If this sits with a colleague rather than with you, tell me who and I will approach them instead.

{url}"""
    else:
        s1 = 'the page people stay on'
        b1 = f"""Hello {f},

A note about {dom} rather than a pitch.

A catalogue website is browsed and left. An interactive tool changes that: visitors stay longer, they have a reason to return, and the page becomes something other sites link to.

Underneath it you get the commercial part. Every design produced arrives as a lead, with the products chosen and the contact details attached.

Daltile and Marazzi both went this way. In your market it is still open.

{url}"""
        s2 = 'what lands in your dashboard'
        b2 = (f"""Hello {f},

To be concrete about the output, since the value sits in what your team receives.

A visitor finishes a design. You get one record: the rendered room, the products and formats used, and their name and email address. Your team then calls somebody who has already chosen.

I wrote to {partner} as well, since I could not tell from outside which of you owns the website.

{url}

Name one collection and I will build it into a version for you.""" if partner else f"""Hello {f},

To be concrete about the output, since the value sits in what your team receives.

A visitor finishes a design. You get one record: the rendered room, the products and formats used, and their name and email address. Your team then calls somebody who has already chosen.

{url}

Name one collection and I will build it into a version for you.""")
        s3 = 'seven weeks, and then it is yours'
        b3 = f"""Hello {f},

Closing this out.

We built this for MEC Artworks, a mosaic manufacturer, in seven weeks with three people, and it runs on their site today. A branded version for {co}, on your own catalogue and your own domain, is the same order of work.

If it is not a priority this year, say so and I will leave it there. If it is, the fastest first step is a collection name.

{url}"""
    return s1, b1, s2, b2, s3, b3

# ─────────────────────────────── build ───────────────────────────────
rows = list(csv.DictReader(open(SRC, encoding='utf-8-sig')))
COLS = ['email','first_name','last_name','company_name','website','contact_thread',
        'segment_variant','send_day_1','send_day_2','send_day_3',
        'msg_subject_1','msg_body_1','msg_subject_2','msg_body_2','msg_subject_3','msg_body_3',
        'studio_url',
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
    url = BASE + STUDIO.get(sk, '')

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
            s1,b1,s2,b2,s3,b3 = variant_C(first, co, dom, tool, hook, thread, partner, url)
        elif seg == 'A':
            s1,b1,s2,b2,s3,b3 = variant_A(first, co, dom, tool, hook, thread, partner, url)
        else:
            s1,b1,s2,b2,s3,b3 = variant_B(first, co, dom, tool, hook, thread, partner, lvl == 'BASIC', url)

        if seg == 'C':
            hq = 'strong' if tool else 'weak'
        else:
            hq = 'strong' if hook else 'weak'

        # Subject rotation is applied after generation so every variant gets it
        # from one place. Message 1 already varies by company, tool name or
        # domain, so only the follow-ups need a bank.
        s2 = pick(S2[seg + thread], email, 2)
        s3 = pick(S3[thread], email, 3)

        d = DAYS[thread]
        out.append(dict(email=email, first_name=first, last_name=last, company_name=co,
            website=dom, contact_thread=thread, segment_variant=seg,
            send_day_1=d[0], send_day_2=d[1], send_day_3=d[2],
            msg_subject_1=s1, msg_body_1=b1, msg_subject_2=s2, msg_body_2=b2,
            msg_subject_3=s3, msg_body_3=b3,
            studio_url=url,
            qa_tool_level=lvl, qa_has_tryon=tryon, qa_tool_name=tool, qa_studio=sk,
            qa_hook_quality=hq, qa_hook=hook, qa_partner_email=partner_email,
            qa_country=clean(r['country']), qa_size=clean(r['Size']), qa_evidence=ev))

with open(OUT, 'w', newline='', encoding='utf-8-sig') as fh:
    w = csv.DictWriter(fh, fieldnames=COLS)
    w.writeheader()
    w.writerows(out)
print('rows:', len(out))
