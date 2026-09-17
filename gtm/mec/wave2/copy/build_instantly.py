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

# ─────────────────────────────── copy ───────────────────────────────
# Body text carries no dash of any kind and no filtered word. Every first
# email stays under 90 words after slot fill, which is checked at the bottom.

def variant_C(f, co, dom, tool, hook, thread, partner):
    t = tool or 'your room visualiser'
    if thread == 'A':
        s1 = f'the request {t} has to turn down'
        b1 = f"""{f},

{t} does the hard part properly. Photograph the room, choose the surface, see it straight away.

It works from what you already make. A client who wants something not in the collection yet has nowhere to put that request except an email to your team.

We built the design tool behind MEC Artworks for exactly that. Described in words, rendered in your own finishes.

Want a version running on {co} surfaces to test against {t}?"""
        s2 = f'the half {t} does not do'
        b2 = f"""{f},

The difference in short.

{t} starts from your catalogue and lets people place it. This starts from a sentence and produces something that was never in the catalogue, then puts it in the client's own photo.

You already paid for the first half, which is exactly why I wrote to you and not to a brand with nothing.

Running version: https://www.tryshowhouse.com/

Yours would sit on {co} surfaces, beside {t} rather than replacing it. Name a collection and I will set it up for you to try."""
        s3 = f'one question about {t}'
        b3 = f"""{f},

One question, then I am done.

When somebody opens {t} and what they came for is not in it, where do they go next?

If the answer is your team, that is a cost. If it is another brand's website, that is worse. If they buy anyway, I have this wrong and I would like to hear it.

https://www.tryshowhouse.com/ if you ever want to poke at the other half."""
    else:
        s1 = 'what happens after not quite this one'
        b1 = f"""{f},

{co} built {t} so a client can photograph a room and see the surface in it. Most brands have not.

The gap is one step later. When the client says not quite this one, {t} has nothing left, and it goes back to your people and a sample.

We built the design tool behind MEC Artworks for that moment. The client describes what they want and gets a layout back in your surfaces.

Shall I set one up on one of your collections?"""
        s2 = f'{partner} has this one too' if partner else 'a version on your own surfaces'
        b2 = f"""{f},

For the sake of being clear, I sent this to {partner} as well. Whichever of you it belongs to, I would rather you two decide than have me guess.

Tool: https://www.tryshowhouse.com/

The {co} version runs on your own surfaces and your naming, next to {t}, so a client never has to leave the site to imagine something.

Pick a collection and I will build it out for you to try this week.""" if partner else f"""{f},

Following up with the thing itself rather than a description of it.

https://www.tryshowhouse.com/

The {co} version runs on your own surfaces and your naming, next to {t}, so a client never has to leave the site to imagine something.

Pick a collection and I will build it out for you to try this week."""
        s3 = 'happy to be told I am wrong'
        b3 = f"""{f},

Last one.

Two things could be true. Either this belongs to somebody else, in which case send me a name and I will take it there. Or {t} already covers what your clients ask for, in which case I have overestimated the gap and that is worth knowing.

Either reply is useful to me. So is a no.

It stays at https://www.tryshowhouse.com/"""
    return s1, b1, s2, b2, s3, b3

def variant_A(f, co, dom, tool, hook, thread, partner):
    line = f'On your own site: "{hook}".' if hook else \
           f'Your site sells custom work and the way to start one is to contact your team.'
    if thread == 'A':
        s1 = 'the step before somebody picks up a pen'
        b1 = f"""{f},

{line}

A real service, and also a queue. Some of them go quiet while they wait.

We built the design tool behind MEC Artworks. It puts a first version on screen in your own materials, while the customer is still on your page, so your team only works up the jobs already decided.

Want me to load a few of your pieces in and send you a version to try?"""
        s2 = 'your own materials, already in it'
        b2 = f"""{f},

Here it is, running: https://www.tryshowhouse.com/

That is the general version. The one we set up for {co} looks like {co}. Your pieces, your finishes, your site, so a customer never feels they left.

Two ways it gets used. Somebody uploads a photo of their room and sees your product in it. Or they type what they are after and get a layout back, built from your catalogue.

Send me one collection name and I will have your version ready in a day."""
        s3 = f'wrong person at {co}?'
        b3 = f"""{f},

Two possibilities and I cannot tell from out here.

One, this sits on somebody else's desk. If the website and the customer journey belong to another name, tell me and I will take it there.

Two, I have read your process wrong. If that step is quick, or if it is the part customers are actually paying for, then I have built an argument on something that is not a problem, and you would be doing me a favour by saying so.

Either answer is worth more to me than silence. It is at https://www.tryshowhouse.com/ if you want to look first."""
    else:
        s1 = 'the visitors who never get in touch'
        b1 = f"""{f},

{line}

Most will not do that. Not because they are uninterested, but because they cannot picture what they would be asking for yet. They leave, and you never learn they were there.

We built the design tool behind MEC Artworks. That visitor builds a rough version themselves in your own materials, and the enquiry that follows arrives with a picture attached.

Want a version with your own pieces in it to try?"""
        s2 = f'I sent this to {partner} as well' if partner else 'the tool itself, rather than a description'
        b2 = (f"""{f},

Being straight with you, {partner} has this too. Easier if the two of you decide whose desk it belongs on than if I keep guessing.

The tool is here if you want a look before that conversation: https://www.tryshowhouse.com/

What we build for {co} is the same thing wearing your name. Your pieces and finishes, on {dom}, so the lead stays with you instead of going to whichever site had a picture on it.

Give me a collection and I will set your version up this week.""" if partner else f"""{f},

Rather than describe it again, here it is: https://www.tryshowhouse.com/

What we build for {co} is the same thing wearing your name. Your pieces and finishes, on {dom}, so the lead stays with you instead of going to whichever site had a picture on it.

Give me a collection and I will set your version up this week.""")
        s3 = 'one question about your custom page'
        b3 = f"""{f},

One question and then I am out of your inbox.

Of the people who land on your custom page, how many get in touch?

If it is most of them, I have this wrong and I would like to know. If it is a small share, that gap is the whole reason I wrote in the first place.

Either way it stays at https://www.tryshowhouse.com/ whenever you want it."""
    return s1, b1, s2, b2, s3, b3

def variant_B(f, co, dom, tool, hook, thread, partner, basic):
    if hook:
        line = f'On your own site: "{hook}".'
    elif basic:
        line = f'{dom} lets somebody filter and browse, which helps them find a product.'
    else:
        line = f'I went through {dom} looking for a way to see a piece in a room before ordering, and did not find one.'
    if thread == 'A':
        s1 = f'the last click on {dom}'
        b1 = f"""{f},

{line}

That works for a buyer who already chose you. It does nothing for one comparing four brands in an afternoon, and that gets settled on a picture.

We built the design tool behind MEC Artworks. Your collections drop into the client's own room photo, on your site, while they decide.

Want one of your collections put into a working version so you can see it?"""
        s2 = f'a {co} version, not a demo'
        b2 = f"""{f},

Here is the working tool: https://www.tryshowhouse.com/

The part that matters is that yours is yours. Your collection names, your colours, your domain. A visitor should not be able to tell anybody else built it.

It does two jobs. A photo of the room with your product in it, or a written description turned into a layout using your pieces.

Reply with one collection and I will have your version up in a day or so."""
        s3 = 'tell me if I have this backwards'
        b3 = f"""{f},

You may be selling to people who do not need to see it. Buyers who know the brand, order from the catalogue, and are perfectly happy.

If that is the truth, say so and I will stop. It is genuinely useful for me to learn which parts of this market do not have the problem.

If it is more that nobody has had time to build it, that is the usual answer, and it is why MEC's took seven weeks rather than a year.

https://www.tryshowhouse.com/ whenever."""
    else:
        s1 = 'a collection nobody can put on their own wall'
        b1 = f"""{f},

{co} puts out collections with real work behind them. A visitor can read about one, see a photograph and download a catalogue.

What they cannot do is see it in their own room. So it comes down to a posted sample and a week of waiting, long enough to pick somebody else.

We built the design tool behind MEC Artworks. It puts a collection into the customer's own photo, or builds a layout from a description.

Want to see one of your collections in it?"""
        s2 = f'{partner} has this too' if partner else 'the working version'
        b2 = (f"""{f},

Straight with you. I sent this to {partner} as well, since I could not tell from outside whose call it is.

The tool: https://www.tryshowhouse.com/

The {co} version would be built around your catalogue, which is the whole point. Generic room planners are everywhere. One that shows only your pieces is a reason for somebody to stay on your site instead of opening three others.

Name a collection and I will set it up.""" if partner else f"""{f},

The tool, rather than another description of it: https://www.tryshowhouse.com/

The {co} version would be built around your catalogue, which is the whole point. Generic room planners are everywhere. One that shows only your pieces is a reason for somebody to stay on your site instead of opening three others.

Name a collection and I will set it up.""")
        s3 = 'three of the four let her see it'
        b3 = f"""{f},

Last note, and there is something useful in it whether you reply or not.

Daltile runs a visualiser. Marazzi runs one. A lot of mid sized makers run Roomvo, which is white labelled, so it appears under the maker's own name and the visitor never knows it was bought in.

So when a designer compares four brands on a Tuesday, three of them let her see it and one asks her to imagine it.

If you ever want to be one of the three: https://www.tryshowhouse.com/"""
    return s1, b1, s2, b2, s3, b3

# ─────────────────────────────── build ───────────────────────────────
rows = list(csv.DictReader(open(SRC, encoding='utf-8-sig')))
COLS = ['email','first_name','last_name','company_name','website','contact_thread',
        'segment_variant','send_day_1','send_day_2','send_day_3',
        'msg_subject_1','msg_body_1','msg_subject_2','msg_body_2','msg_subject_3','msg_body_3',
        'qa_tool_level','qa_has_tryon','qa_tool_name','qa_hook_quality','qa_hook',
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

    firsts = {th: (nm.split()[0] if nm else '') for _, nm, th in people}
    for email, name, thread in people:
        if email in seen:
            continue
        seen.add(email)
        parts = name.split()
        first = parts[0] if parts else ''
        last = ' '.join(parts[1:]) if len(parts) > 1 else ''
        other = 'B' if thread == 'A' else 'A'
        partner = firsts.get(other, '')
        partner_email = next((e for e, _, th in people if th == other), '')

        if seg == 'C':
            s1,b1,s2,b2,s3,b3 = variant_C(first, co, dom, tool, hook, thread, partner)
        elif seg == 'A':
            s1,b1,s2,b2,s3,b3 = variant_A(first, co, dom, tool, hook, thread, partner)
        else:
            s1,b1,s2,b2,s3,b3 = variant_B(first, co, dom, tool, hook, thread, partner, lvl == 'BASIC')

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
            qa_tool_level=lvl, qa_has_tryon=tryon, qa_tool_name=tool,
            qa_hook_quality=hq, qa_hook=hook, qa_partner_email=partner_email,
            qa_country=clean(r['country']), qa_size=clean(r['Size']), qa_evidence=ev))

with open(OUT, 'w', newline='', encoding='utf-8-sig') as fh:
    w = csv.DictWriter(fh, fieldnames=COLS)
    w.writeheader()
    w.writerows(out)
print('rows:', len(out))
