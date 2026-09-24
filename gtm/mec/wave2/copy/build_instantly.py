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
import csv, re, unicodedata, zlib

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
    # Two rows carry a second brand after a separator, "GTILES - ROCKYLAND"
    # and "Roca / Lamosa USA". Written out in a sentence that reads as a
    # merge field, and the spaced hyphen is the one dash the copy rules do
    # not allow. In both cases the first segment is the brand the domain
    # belongs to, so that is the one the email should use.
    c = re.split(r'\s+[-–—/]\s+', c)[0].strip() or c
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

# ─── follow-ups rebuilt 20 Sept ──────────────────────────────────────
# Message 1 is approved and unchanged. Messages 2 and 3 were both still
# EXPLAINING the product at different lengths, which is why they read flat.
# Each one is now a different move rather than another paragraph of pitch.
#
#   Message 2, thread A: SHOW a lead instead of describing one. The shape of
#     the record is straight off the Showhouse page, so it is real rather than
#     imagined, and a short list scans in two seconds where a paragraph does
#     not. Nothing about it sounds like a pitch.
#   Message 2, thread B: hand over a piece of market news they can use whether
#     or not they reply. Daltile, Marazzi and white-labelled Roomvo are all
#     verified. This is also where the colleague handoff sits.
#   Message 3: say the thing they are already thinking and have not written
#     back to say. The objection differs by segment, so each gets its own, and
#     every one ends with an easy no. Thread B gets the two-line version: one
#     real question, no pitch at all.
#
# Casual register throughout, contractions included. No dashes, no filtered
# words, no signature block.

def stable(*parts):
    """CRC32, not the built-in hash().

    Python randomises string hashing per process unless PYTHONHASHSEED is set,
    so hash() reshuffled the A/B arms and every rotated subject line on each
    rebuild. That silently invalidates a running test: a contact on the revenue
    arm today could be on the cost arm after tomorrow's rebuild, and nothing in
    the output would show it moved. CRC32 is deterministic across processes and
    machines, so a rebuild reproduces the file byte for byte."""
    return zlib.crc32('\x1f'.join(str(p) for p in parts).encode())

def pick(bank, key, salt, offset=0):
    """Near-identical phrasing across a segment was copy defect four on
    campaign 2, and it creeps back wherever one argument serves 200 rows."""
    return bank[(stable(key, salt) + offset) % len(bank)]

DEMO = 'https://www.tryshowhouse.com/#book'

S2 = {
 'A': ['what one of these looks like when it lands',
       'easier to show than explain',
       'their room, their words, their email',
       'this is what turns up on your side'],
 'B': ['Daltile has one, Marazzi has one',
       'the one nobody can tell was bought in',
       'worth knowing either way',
       "what everyone else is quietly running"],
}
S3 = {
 'CA': ["why bother, you've already got one",
        'the fair question',
        'judge it yourself rather than take my word'],
 'AA': ['nobody wants a machine in the middle',
        'the bit people push back on',
        'you still get the conversation'],
 'BA': ['the renders will look fake, right',
        "the bit people don't say out loud",
        'judge it yourself rather than take my word'],
 'CB': ['one question', 'what do you know tomorrow morning', 'how many did you get a name for'],
 'AB': ['one question', 'what do you know tomorrow morning', 'how many did you get a name for'],
 'BB': ['one question', 'what do you know tomorrow morning', 'how many did you get a name for'],
}

# The record itself, written the way Showhouse writes it on its own page, so
# this is the real shape rather than an invented one. A short list scans in two
# seconds where a paragraph does not.
LEAD_RECORD = """a photo of their actual room with your product in it
their own words, something like "large format warm travertine, wide plank, matte"
the spec: herringbone, Carrara and cream, polished, 600x300
and an email address they've confirmed"""

def _a2(f, co, url, seg):
    """Show the lead, do not describe it.

    Framed differently per segment, because otherwise one body went out to 300
    addresses with only the company name changing, which is campaign 2's copy
    defect four wearing a new coat. The move is the same in all three; the
    sentence around it is not."""
    if seg == 'C':
        top = ("You already know what a render looks like, so here's the only part that's new.\n\n"
               "When somebody finishes, this is what turns up on your side:")
        bottom = ("Your current one gives them the picture. This one gives you the rest of it too.")
    elif seg == 'A':
        top = ("Easier to show you than explain it.\n\n"
               "Instead of the email you'd normally get, this is what turns up:")
        bottom = ("Nobody typed out a description and nobody had to interpret one. "
                  "They'd already settled the room, the look and the size before your team said a word.")
    elif (stable(f, co) & 1):
        top = ("Easier to show you than explain it.\n\n"
               "When somebody finishes, this is what turns up on your side:")
        bottom = ("Nobody filled in a contact form. They'd told you the room, the look "
                  "and the size before anyone picked up the phone.")
    else:
        # Second framing for the largest cohort. Same move, different sentence,
        # so 139 addresses stop receiving one body with the name swapped.
        top = ("Rather than describe it, here's a lead as it actually arrives.\n\n"
               "One record, four things in it:")
        bottom = ("That's someone who has already decided, sitting in your inbox with "
                  "a picture of the room attached. Not a name on a mailing list.")
    return f"""Hello {f},

{top}

{LEAD_RECORD}

{bottom}

{url}

Want me to put {co} products in one so you can see yours?"""

def _b2(f, url, partner):
    """Market news they can use either way, plus the colleague handoff."""
    tail = (f"\n\nI sent this to {partner} too, since I couldn't tell from outside whose call it is."
            if partner else '')
    return f"""Hello {f},

Not a pitch, just something worth knowing.

Daltile has one of these. Marazzi has one. And plenty of brands you'd recognise are running Roomvo, which is white labelled, so it sits there under their own name and nobody can tell it was bought in.

The difference with ours is what happens to the visitor afterwards. They confirm an email to keep the picture, so you end up with the person rather than a page view.{tail}

{url}"""

def _b3(f, dom, url, co):
    """Two lines, one real question, no pitch. Two of them, split by row, so
    139 addresses do not receive the same body."""
    if (stable(f, co) & 1):
        return f"""Hello {f},

If somebody lands on {dom} tonight and falls for one of your collections, what do you actually know about them tomorrow morning?

If the answer is nothing, that's the whole reason I wrote.

{url}"""
    return f"""Hello {f},

A genuine question rather than a pitch.

Out of everyone who looked at {dom} last month, how many did you get a name for?

Whatever that number is, the rest of them liked something enough to look. You just never found out who.

{url}"""

# ─────────────────────── message 1, rebuilt 22 Sept ───────────────────
# Two bodies run as a live A/B, split BY COMPANY so both people at a two
# person company land in the same arm and never receive two different pitches.
#
#   Arm R, revenue side. The visitor you never meet. They already pay for that
#     traffic, so this is about turning the anonymous ones into named leads.
#   Arm C, cost side. The sample posted to somebody who was never going to
#     order. This puts the decision in front of the sample.
#
# Both carry every element the feedback asked for: the room photo mode AND
# Imagine from Scratch, the lead record (render, brief, verified email), the
# dashboard, the catalogue load, white label on their own domain, and live in
# weeks. 150 to 180 words, the ceiling before a cold reader starts skimming.
#
# THREE things vary, and all three have to, or the test is not clean:
#   the ARM decides the argument, and the subject line has to match the arm or
#     the two are testing different things at once;
#   the SEGMENT decides the opening two lines, which is where the
#     personalisation lives;
#   the THREAD decides which of the two people at a company gets which shape.
#     The first pass at this used arm and segment only, and every one of the
#     82 two-person companies received a message 1 identical apart from the
#     greeting. Thread B now opens on the outcome and closes by naming the
#     colleague, so the two read as two people writing, not one mail merge.
#
# NOTE ON DATA. Showhouse publishes no performance figures and the MEC case
# study carries none, so none are claimed. The only numbers these emails
# invoke are the READER'S own: what a sample costs them to make and post.
# Asking a manufacturer to price their own sample is a question, not a claim,
# and it beats a statistic they have no reason to believe. Replace this the
# day one real figure exists.

# Plain text, no block and no logo image, per the 22 Sept call: a blocked
# remote image renders as a broken box and wrecks the image-to-text ratio.
# The company is Triminage, not Showhouse. Showhouse is the product the email
# is about, and signing as the product reads as if the brand is writing to
# them rather than a person at the agency that built it.
SENDER = 'Regards,\n\nHaroon\nTriminage'

# Subject banks are keyed by ARM then SEGMENT. Keeping them arm-aware matters:
# a cost-side subject over a revenue-side body would mean the A/B is measuring
# two changes at once and neither result would be readable.
# ── message 1 subject lines ──────────────────────────────────────────
# Rewritten 24 Sept. The previous set drifted onto the lead-capture half of
# the product, badge scans and dashboards. Showhouse is a VISUALISER: the
# customer photographs their own room and the brand's product appears in it.
# Every line below says that, and the trade show is only the timing wrapper.
#
# The two banks are paired to their bodies so subject and first line make the
# same promise:
#   PILOT 3 -> arm R, the revenue body. They cannot picture it, so they leave.
#   PILOT 1 -> arm C, the cost body. Before the next show, stop posting samples.
#
# Show labels come from the row's own source directory. Cersaie 2026 ran 21 to
# 25 September 2026, so the forward reference is the 2027 edition: for a
# manufacturer who just came off a stand, that is the planning window rather
# than a deadline a year out. Rows with no show, the 20 TCNA ones, drop the
# options carrying a show token and keep the rest.
SHOW_LABEL = {'cersaie': 'Cersaie 2027', 'coverings': 'Coverings 2027',
              'heimtextil': 'Heimtextil 2027', 'tise': 'TISE 2027'}

PILOT3 = ["Your catalogue can't show their room",
          'Stop asking them to imagine it',
          'A PDF, or their actual bathroom',
          "They can't picture it. That is the problem",
          'Your collections, in their own room']

PILOT1 = ['Before {show}, let them see it',
          'Your products in their rooms by {show}',
          'Before {show}',
          'Stop posting samples before {show}',
          # The 20 TCNA rows carry no show, so every line above drops out for
          # them. With one survivor left, both people at a two person company
          # were getting the same subject, which is the one thing that makes a
          # multi threaded campaign read as a mail merge. These four hold the
          # same cost side promise without naming a date, and they also pull
          # down the share of arm C sitting on a single line.
          '12 months to stop sending samples',
          'Before the next sample goes out',
          'Let them see it before you post it',
          'The samples that never become orders']

def show_subject(arm, show, co, thread):
    """Arm picks the bank, the row's show fills the token, thread decides which
    of the two people at a company gets which line."""
    bank = PILOT1 if arm == 'C' else PILOT3
    label = SHOW_LABEL.get(show, '')
    if not label:
        bank = [b for b in bank if '{show}' not in b] or bank
    off = 0 if thread == 'A' else 1
    out = pick(bank, co, 's' + arm, off).format(show=label)
    if len(out) <= 50:
        return out
    fits = sorted((b.format(show=label) for b in bank), key=len)
    return fits[off % len(fits)]

def show_key(source):
    """Cersaie wins on a combined row: most recent, and the one just finished."""
    src = (source or '').lower()
    if 'cersaie' in src:    return 'cersaie'
    if 'heimtextil' in src: return 'heimtextil'
    if 'tise' in src:       return 'tise'
    if 'coverings' in src:  return 'coverings'
    return ''

def hall_of(stand):
    m = re.match(r'\s*(Hall\s+\w+)', stand or '', re.I)
    return m.group(1) if m else ''

S1 = {
 'R': {
  'C': ["What {tool} doesn't tell you",
        "{tool} renders it, then they're gone",
        'After the render, who was it?',
        '{tool}, and the name behind it',
        'Every render, and nobody to call',
        "The part {dom} does not record"],
  'A': ['The enquiries {dom} never gets',
        'Interested, but never in touch',
        'Why most visitors never ask',
        'The ones who never make contact'],
  'B': ['Your products, in their own room',
        "What {dom} can't show a buyer",
        "The room they're standing in",
        "Traffic {dom} can't put a name to",
        'Browsed, closed, gone'],
 },
 'C': {
  'C': ['Who is serious, before you ship',
        '{tool}, and the samples that follow',
        'The samples {dom} would stop posting',
        'Samples, before or after {tool}',
        'Before the next sample goes out'],
  'A': ['Before the sample goes in the post',
        'The week you lose to a sample',
        'Samples {dom} did not need to send',
        'Samples that were never going to land',
        'The cost of quoting from a description'],
  'B': ['The samples that never convert',
        'Before the sample goes in the post',
        'Samples {dom} did not need to send',
        'Who is serious, before you ship',
        'The week between sample and answer'],
 },
}

def subject1(arm, seg, f, co, dom, tool, thread='A', show='', hall=''):
    """Pick and fill a message 1 subject, then guard the 50 character ceiling.

    {tool} and {dom} are both variable length, so a line that measures fine on
    one row overflows on another; anything over 50 falls back to the shortest
    option in the same bank rather than going out truncated. Rows with no tool
    name detected drop the options that name one, since the fallback phrase
    reads wrong at the start of a subject."""
    return show_subject(arm, show, co, thread)
    bank = S1[arm][seg]
    if not tool:
        bank = [b for b in bank if '{tool}' not in b] or bank
    t = tool or 'your visualiser'
    # Base index from the COMPANY, then step one along for thread B. Hashing
    # the person's name instead left 18 of the 82 two-person companies with
    # both people on the same subject, which is what a four-option bank gives
    # you by chance. The offset makes a clash impossible rather than unlikely.
    off = 0 if thread == 'A' else 1
    out = pick(bank, co, 1, off).format(dom=dom, tool=t)
    if len(out) <= 50:
        return out
    # Falling back to the single shortest option put both people at a company
    # on the same subject. Rank what fits and keep the thread offset.
    fits = sorted((b.format(dom=dom, tool=t) for b in bank), key=len)
    return fits[off % len(fits)]

def hook1(seg, co, dom, tool, hook, basic):
    """The opening two lines. Segment aware, because the reason they are
    losing the visitor is different in each one, and that is the whole of the
    personalisation."""
    if seg == 'C':
        t = tool or 'your room visualiser'
        return (f"You already run {t}, so someone can see your products in a room. "
                f"Most of this category still can't do that.\n\n"
                f"What it doesn't do is tell you who they were. They render, they like it, "
                f"and they leave with no name attached.")
    if seg == 'A':
        first = f'On your own site: "{hook}".' if hook else \
                f'{co} sells bespoke work, and the way in is to contact your team.'
        return (f"{first}\n\nEvery one of those arrives as words, and someone on your side "
                f"has to turn it into a picture before anything moves.")
    first = (f'On your own site: "{hook}".' if hook else
             f'{dom} lets people filter and browse, which helps them find a product.' if basic
             else f'{dom} shows the collections well, and then the visit ends at a catalogue.')
    return (f"{first}\n\nWhat it can't do is show someone your product in the room "
            f"they're standing in. So they look, decide, and go.")

def msg1(arm, thread, seg, f, co, dom, tool, hook, basic, url, partner):
    if thread == 'A':
        top = hook1(seg, co, dom, tool, hook, basic)
        if arm == 'R':
            mid = (f"Showhouse sits on {dom} under your own branding, so nobody sees our name. "
                   f"A visitor photographs their room and your product appears in it. Or they "
                   f"describe what they're imagining and it's generated from your real "
                   f"collections and finishes.\n\n"
                   f"The image only unlocks once they confirm their email. So you get a lead: "
                   f"the render, a short brief in their own words, and a verified address, all "
                   f"in one dashboard.\n\n"
                   f"Visitors also stay on the page instead of bouncing, and every render "
                   f"builds content around your own products.\n\n"
                   f"We load your actual catalogue first, so nothing renders that you can't "
                   f"make. It goes live in weeks.")
            cta = (f"Try it on a photo of your own room: {url}\n\n"
                   f"Want one with {co} products in it? Send me a collection name.")
        else:
            mid = (f"Every sample you post costs you something, and most of them go to people "
                   f"who were never going to order.\n\n"
                   f"Showhouse puts the decision before the sample. On {dom}, under your own "
                   f"branding, a visitor photographs their room and sees your product in it, or "
                   f"describes what they want and gets it generated from your real collections.\n\n"
                   f"They confirm an email to keep the image. You get the render, a brief in "
                   f"their words and a verified address in one dashboard, so you know who's "
                   f"serious before anything ships.\n\n"
                   f"Your own catalogue goes in first, so nothing renders that you don't make. "
                   f"Live in weeks.")
            cta = (f"Have a go on your own room photo: {url}\n\n"
                   f"Want one loaded with {co} products? Just name a collection.")
        return f"Hello {f},\n\n{top}\n\n{mid}\n\n{cta}\n\n{SENDER}"

    # Thread B. Same arm, opposite shape: it opens on the outcome and works
    # back to the mechanism, so the colleague reading both sees two messages
    # rather than one merge with a different name at the top.
    note = (f"\n\nI've written to {partner} as well, since I couldn't tell from outside "
            f"which of you this sits with." if partner else '')
    if arm == 'R':
        return (f"Hello {f},\n\n"
                f"A quick one about {dom}.\n\n"
                f"Imagine a visitor leaves you their name, a photo of their own room with your "
                f"product rendered into it, and a short brief saying what they were after. "
                f"That is what lands in the dashboard, and the email is verified before the "
                f"image unlocks.\n\n"
                f"Showhouse is how they get there. It runs on your own domain under your "
                f"branding, so nobody sees our name. They photograph a room and your product "
                f"appears in it, or they describe what they're picturing and it's generated "
                f"from your real collections.\n\n"
                f"We load your catalogue first, so nothing comes back in a finish you don't "
                f"make, and the whole thing is live in weeks rather than quarters. Your logo, "
                f"your colours, your domain.{note}\n\n"
                f"Try it on your own room photo: {url}\n\n{SENDER}")
    return (f"Hello {f},\n\n"
            f"A quick one about {dom}.\n\n"
            f"Right now you find out who's serious after the sample has shipped. Packing, "
            f"courier and a week of waiting, mostly for people who were never going to order.\n\n"
            f"Showhouse moves that to the website. Under your own branding, on your own domain, "
            f"a visitor photographs their room and sees your product in it, or describes what "
            f"they want and gets it generated from your real collections. They confirm an email "
            f"to keep the image.\n\n"
            f"You get the render, a brief in their words and a verified address in one "
            f"dashboard, so the samples go to the people worth sending them to.\n\n"
            f"Your catalogue goes in first, so nothing renders that you don't make, and it's "
            f"live in weeks rather than quarters. Your logo, your colours, your domain.{note}\n\n"
            f"Have a look: {url}\n\n{SENDER}")

def variant_C(f, co, dom, tool, hook, thread, partner, url, lab, variant, show='', hall=''):
    """Already runs a visualiser. Never suggest they lack one."""
    t = tool or 'your room visualiser'
    if thread == 'A':
        s1 = subject1(variant, 'C', f, co, dom, tool, thread, show, hall)
        b1 = msg1(variant, thread, 'C', f, co, dom, tool, hook, False, url, partner)
        b2 = _a2(f, co, url, 'C')
        b3 = f"""Hello {f},

You've already got the render part, so the fair question is why bother at all.

It's only the bit afterwards. Yours shows the picture and the visitor goes. Ours holds the picture back until they've confirmed an email, so you end up with a person to ring instead of a number in your analytics.

Have a look and judge it yourself: {url}

And if it's a no, just say no. I'll leave you be."""
    else:
        s1 = subject1(variant, 'C', f, co, dom, tool, thread, show, hall)
        b1 = msg1(variant, thread, 'C', f, co, dom, tool, hook, False, url, partner)
        b2 = _b2(f, url, partner)
        b3 = _b3(f, dom, url, co)
    return (s1, b1, pick(S2[thread], f+co, 2), b2, pick(S3['C'+thread], f+co, 3), b3)

def variant_A(f, co, dom, tool, hook, thread, partner, url, lab, variant, show='', hall=''):
    """A person does the visualising today and a sample usually follows."""
    line = f'On your own site: "{hook}".' if hook else \
           f'{co} sells bespoke work, and the way in is to contact your team.'
    if thread == 'A':
        s1 = subject1(variant, 'A', f, co, dom, tool, thread, show, hall)
        b1 = msg1(variant, thread, 'A', f, co, dom, tool, hook, False, url, partner)
        b2 = _a2(f, co, url, 'A')
        b3 = f"""Hello {f},

The thing people usually push back on is that they don't want a machine sitting between them and the client. Which is fair, that conversation is the job.

This isn't that. It just means the client turns up having already seen something, so you start at "can we do that in this glaze" instead of "what do you make".

Have a look and see what you think: {url}

If it's a no, say so and I'll leave you alone."""
    else:
        s1 = subject1(variant, 'A', f, co, dom, tool, thread, show, hall)
        b1 = msg1(variant, thread, 'A', f, co, dom, tool, hook, False, url, partner)
        b2 = _b2(f, url, partner)
        b3 = _b3(f, dom, url, co)
    return (s1, b1, pick(S2[thread], f+co, 2), b2, pick(S3['A'+thread], f+co, 3), b3)

def variant_B(f, co, dom, tool, hook, thread, partner, basic, url, lab, variant, show='', hall=''):
    """No design step, or filters only. Open on what they promise, never on
    what they lack: qualifier 1 records NONE as none found, not none exists."""
    if hook:
        line = f'On your own site: "{hook}".'
    elif basic:
        line = f'{dom} lets people filter and browse, which helps them find a product.'
    else:
        line = f'{dom} shows the collections well, and then the visit ends at a catalogue.'
    if thread == 'A':
        s1 = subject1(variant, 'B', f, co, dom, tool, thread, show, hall)
        b1 = msg1(variant, thread, 'B', f, co, dom, tool, hook, basic, url, partner)
        b2 = _a2(f, co, url, 'B')
        # Two objections, split by row. One body was going to 139 addresses,
        # which is the phrasing pattern that sank campaign 2.
        if (stable(f, co) & 1):
            b3 = f"""Hello {f},

Here's the bit people don't usually write back to say.

The worry is normally one of two things. Either the renders come out looking fake, or your products are too particular for something like this to get right.

Both fair. It's why it only ever renders what's actually in your catalogue, your finishes and your sizes, and why the studio is sitting there open so you can judge it rather than take my word for it.

{url}

If it's a no, just say no and I'll leave you be."""
        else:
            b3 = f"""Hello {f},

The usual reason this goes nowhere isn't that people dislike the idea. It's that it sounds like a project, and nobody has a spare quarter to give it.

It isn't one. We do the catalogue work, it goes up under your name, and your side of it is mostly telling us which collections matter.

Have a look at the studio first and see if it's even worth the conversation: {url}

And if it isn't, tell me and I'll stop."""
    else:
        s1 = subject1(variant, 'B', f, co, dom, tool, thread, show, hall)
        b1 = msg1(variant, thread, 'B', f, co, dom, tool, hook, basic, url, partner)
        b2 = _b2(f, url, partner)
        b3 = _b3(f, dom, url, co)
    return (s1, b1, pick(S2[thread], f+co, 2), b2, pick(S3['B'+thread], f+co, 3), b3)

# ─────────────────────────────── build ───────────────────────────────
rows = list(csv.DictReader(open(SRC, encoding='utf-8-sig')))
COLS = ['email','first_name','last_name','company_name','website','contact_thread',
        'segment_variant','send_day_1','send_day_2','send_day_3',
        'msg_subject_1a','msg_body_1a','msg_subject_1b','msg_body_1b',
        'msg_subject_2','msg_body_2','msg_subject_3','msg_body_3',
        'studio_url','ab_arm','qa_show','qa_send_flag',
        'qa_tool_level','qa_has_tryon','qa_tool_name','qa_studio','qa_hook_quality','qa_hook',
        'qa_partner_email','qa_country','qa_size','qa_evidence']
DAYS = {'A': ('1','6','13'), 'B': ('3','9','16')}

# ── A/B arm assignment, stratified by segment ────────────────────────
# A plain coin flip per company left segment C at 33 revenue against 41 cost
# and segment A at 17 against 12. That is ordinary random noise, but it breaks
# the test: if one segment replies better than the others and happens to be
# over-represented in an arm, that arm wins for a reason that has nothing to do
# with the copy. So companies are bucketed by segment, ordered inside the
# bucket by a stable hash, and dealt alternately. Each segment then splits as
# close to even as its own row count allows, and the assignment still survives
# a rebuild because the ordering key is CRC32 rather than hash().
_by_seg = {}
for r in rows:
    tryon = clean(r['Use AI Has Tryon']).lower()
    lvl_  = clean(r['Use AI Tool Level'])
    seg_  = 'C' if tryon == 'yes' else ('A' if lvl_ == 'MANUAL' else 'B')
    _by_seg.setdefault(seg_, set()).add(clean(r['company']))
ARM = {}
for seg_, names in _by_seg.items():
    for i, name in enumerate(sorted(names, key=lambda n: stable('arm', seg_, n))):
        ARM[name] = 'R' if i % 2 == 0 else 'C'

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
    # A/B arm for message 1, assigned per COMPANY rather than per contact, so
    # the two people at a two-person company never receive different pitches.
    variant = ARM[co_raw]
    sk  = studio_key(r['Use AI Product Category'], r['niche'], r['Description'])
    show = show_key(r.get('source'))
    hall = hall_of(r.get('stand'))
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

        # Both arms are generated for EVERY row and written to their own
        # columns, so one Instantly campaign can hold both as step 1 variants
        # and randomise between them natively. That beats two campaigns: same
        # mailboxes, same schedule, same daily volume, so the only difference
        # measured is the copy. Two campaigns can drift apart on send rate and
        # then the result is unreadable.
        #
        # Only message 1 differs. The follow-ups are identical in both arms on
        # purpose, because a test with two moving parts answers nothing.
        gen = {'C': variant_C, 'A': variant_A}.get(seg)
        both = {}
        for arm in ('R', 'C'):
            if gen:
                both[arm] = gen(first, co, dom, tool, hook, thread, partner, url, lab, arm, show, hall)
            else:
                both[arm] = variant_B(first, co, dom, tool, hook, thread, partner,
                                      lvl == 'BASIC', url, lab, arm, show, hall)
        s1a, b1a = both['R'][0], both['R'][1]
        s1b, b1b = both['C'][0], both['C'][1]
        _, _, s2, b2, s3, b3 = both['R']

        if seg == 'C':
            hq = 'strong' if tool else 'weak'
        else:
            hq = 'strong' if hook else 'weak'

        d = DAYS[thread]
        out.append(dict(email=email, first_name=first, last_name=last, company_name=co,
            website=dom, contact_thread=thread, segment_variant=seg,
            send_day_1=d[0], send_day_2=d[1], send_day_3=d[2],
            msg_subject_1a=s1a, msg_body_1a=b1a,
            msg_subject_1b=s1b, msg_body_1b=b1b,
            msg_subject_2=s2, msg_body_2=f'{b2}\n\n{SENDER}',
            msg_subject_3=s3, msg_body_3=f'{b3}\n\n{SENDER}',
            studio_url=url, qa_show=(show or 'none'),
            # Kept as a balanced fallback. If Instantly randomises step 1 this
            # column is ignored; if you would rather control the split by hand,
            # filter on it, because it is stratified by segment and a random
            # split is not.
            ab_arm=('R revenue' if variant == 'R' else 'C cost'),
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
