#!/usr/bin/env python3
"""Deliverability audit for MEC_Instantly_Wave2.csv.

Written 29 Sept against review feedback: "run every email template through
Mail Meteor's spam checker or a similar tool before finalizing. Even a couple
of trigger words can hurt deliverability across the whole campaign. Check all
three emails across all variants."

Mail Meteor's checker is a browser tool with no API, and this container has no
outbound route to it, so this runs the same classes of check locally over
EVERY message on EVERY row rather than over a sample pasted by hand. It also
writes templates_for_spamcheck.md, which is the 22 distinct template shapes in
the file, so the same set can be pasted into Mail Meteor or GlockApps for a
second opinion in a couple of minutes.

What it checks, per message:

  1. Trigger words and phrases, from the lists the public checkers use, split
     by how much each class actually costs you. Financial and urgency terms
     are what move a score; a word like "offer" in an ordinary sentence is
     noted and not treated as a failure.
  2. Structure: subject length, ALL CAPS, exclamation and question runs,
     emoji, faked Re:/Fwd:, currency and percentage symbols, phone numbers.
  3. Links: how many, whether the anchor is bare, and whether more than one
     distinct domain appears. A cold email with several links is the single
     most reliable way to land in spam.
  4. Repetition across the campaign, which no single-email checker can see:
     the largest share of rows sending an identical subject or body. A
     thousand identical sends is a stronger spam signal than any word in them.
"""
import csv, re, collections, sys

CSV = 'MEC_Instantly_Wave2.csv'

# ── trigger lexicon ──────────────────────────────────────────────────
# Graded, because a flat list produces noise and then nobody reads the output.
# HIGH is what actually moves a spam score on a cold send. MEDIUM is worth
# removing if a rewrite is cheap. LOW is only reported for completeness.
HIGH = [
    # money
    'cash bonus', 'make money', 'extra income', 'double your', 'earn per',
    'no cost', 'no fees', 'no credit check', 'free money', 'free gift',
    'free trial', 'free access', 'free consultation', 'free quote',
    'money back', 'lowest price', 'best price', 'special promotion',
    'save big', 'big bucks', 'cheap', 'bargain', 'discount', 'incredible deal',
    'price protection', 'refinance', 'credit card', 'billion', 'million dollars',
    # urgency
    'act now', 'apply now', 'buy now', 'call now', 'order now', 'sign up free',
    'click here', 'click below', 'click to', 'do it today', 'limited time',
    'expires', 'urgent', 'instant', 'while supplies last', 'once in a lifetime',
    "don't delete", 'final notice', 'last chance', 'only today',
    # hype
    'guarantee', 'guaranteed', 'risk free', 'no obligation', '100%',
    'amazing', 'unbelievable', 'miracle', 'promise you', 'congratulations',
    'winner', 'you have been selected', 'exclusive deal', 'act immediately',
]
MEDIUM = [
    'offer', 'opportunity', 'deal', 'sale', 'save', 'cheapest', 'affordable',
    'cost effective', 'no catch', 'no strings attached', 'satisfaction',
    'increase sales', 'increase traffic', 'more leads', 'boost', 'skyrocket',
    'revolutionary', 'cutting edge', 'game changer', 'game changing',
    'unsubscribe', 'opt in', 'subscribe', 'this is not spam', 'dear friend',
    'dear sir', 'to whom it may concern', 'per your request',
]
LOW = [
    'free', 'trial', 'demo', 'webinar', 'ai', 'solution', 'partner',
    'revenue', 'roi', 'conversion', 'pipeline', 'quote', 'sample',
]

# Acronyms checked by hand against each company's own site and left as
# written. A checker cannot tell these from shouting, so they are listed
# rather than folded: SIMAS and CE.SI are styled with stops on their own
# sites, ARTO and AVA are brands, TISE is the trade show's name, and the rest
# are ordinary abbreviations.
ACRONYM_OK = {'SIMAS', 'CESI', 'ARTO', 'AVA', 'TISE', 'USA', 'EU', 'WOW',
              'PDF', 'ABK', 'AIP', 'CIR', 'KWC', 'MEC', 'TCNA'}

# Trigger-word hits verified as ordinary language rather than salesmanship.
# Reported under their own heading so nobody spends time removing them:
# "sale" is inside the company name Fabbrica del Sale and inside two
# prospects' own quoted site copy, "manufacture and sale of ceramic wall and
# floor tiles"; "sample" is the whole argument of the cost-side email.
BENIGN = {'sale', 'sample'}

EMOJI = re.compile('[\U0001F300-\U0001FAFF☀-➿]')
URL   = re.compile(r'https?://[^\s)>\]]+')
MONEY = re.compile(r'[$£€¥]\s?\d')
PCT   = re.compile(r'\d+\s?%')
PHONE = re.compile(r'(?:\+\d[\d ()-]{7,}|\b\d{3}[.-]\d{3}[.-]\d{4}\b)')
FAKE  = re.compile(r'^\s*(re|fwd|fw)\s*:', re.I)

MESSAGES = [('1a', 'msg_subject_1a', 'msg_body_1a'),
            ('1b', 'msg_subject_1b', 'msg_body_1b'),
            ('2',  'msg_subject_2',  'msg_body_2'),
            ('3',  'msg_subject_3',  'msg_body_3')]

def hits(text, bank):
    low = text.lower()
    return sorted({w for w in bank if re.search(r'(?<![a-z])' + re.escape(w) + r'(?![a-z])', low)})

def audit(subject, body):
    """Everything wrong with one email. Empty list means nothing found."""
    out = []
    both = subject + '\n' + body
    for label, bank in (('HIGH', HIGH), ('MEDIUM', MEDIUM), ('LOW', LOW)):
        for w in hits(both, bank):
            out.append(('VERIFIED' if w in BENIGN else label, 'trigger word', w))
    if len(subject) > 50:
        out.append(('HIGH', 'subject over 50 chars', len(subject)))
    if FAKE.match(subject):
        out.append(('HIGH', 'faked reply prefix', subject[:20]))
    for w in subject.split() + body.split():
        bare = re.sub(r'[^A-Za-z]', '', w)
        if len(bare) > 4 and bare.isupper() and bare not in ACRONYM_OK:
            out.append(('MEDIUM', 'all caps word', w))
    if '!!' in both or '??' in both:
        out.append(('HIGH', 'punctuation run', '!! or ??'))
    if both.count('!') > 1:
        out.append(('MEDIUM', 'multiple exclamation marks', both.count('!')))
    if EMOJI.search(both):
        out.append(('MEDIUM', 'emoji', EMOJI.search(both).group()))
    if MONEY.search(both):
        out.append(('HIGH', 'currency amount', MONEY.search(both).group()))
    if PCT.search(both):
        out.append(('MEDIUM', 'percentage', PCT.search(both).group()))
    if PHONE.search(both):
        out.append(('MEDIUM', 'phone number', PHONE.search(both).group()))
    links = URL.findall(body)
    if len(links) > 2:
        out.append(('HIGH', 'link count', len(links)))
    elif len(links) == 2:
        out.append(('LOW', 'link count', 2))
    doms = {re.sub(r'^https?://(www\.)?([^/]+).*', r'\2', u) for u in links}
    if len(doms) > 1:
        out.append(('HIGH', 'links to more than one domain', sorted(doms)))
    if '{' in both or '}' in both:
        out.append(('HIGH', 'unfilled merge token', both[both.find('{'):][:30]))
    words = len(body.split())
    if words > 200:
        out.append(('MEDIUM', 'body over 200 words', words))
    if words < 40:
        out.append(('LOW', 'body under 40 words', words))
    return out

def main():
    rows = list(csv.DictReader(open(CSV, encoding='utf-8-sig')))
    send = [r for r in rows if r['qa_send_flag'] == 'send']
    print('MEC_Instantly_Wave2.csv  %d rows, %d sending' % (len(rows), len(send)))
    print('%d emails audited (%d rows x 4 messages)\n' % (len(send) * 4, len(send)))

    tally = collections.Counter()
    examples, worst = {}, collections.Counter()
    for r in send:
        for name, sk, bk in MESSAGES:
            for sev, kind, detail in audit(r[sk], r[bk]):
                key = (sev, kind, str(detail))
                tally[key] += 1
                examples.setdefault(key, (name, r['company_name'], r[sk]))
                if sev == 'HIGH':
                    worst[name] += 1

    for sev in ('HIGH', 'MEDIUM', 'LOW', 'VERIFIED'):
        keys = sorted((k for k in tally if k[0] == sev), key=lambda k: -tally[k])
        print('── %s ── %s' % (sev, 'nothing found' if not keys else ''))
        for k in keys:
            msg, co, subj = examples[k]
            print('  %5d  %-32s %-24s  e.g. msg %s, %s' % (tally[k], k[1], k[2][:24], msg, co))
        print()

    print('── repetition across the campaign ──')
    for name, sk, bk in MESSAGES:
        cs = collections.Counter(r[sk] for r in send)
        cb = collections.Counter(r[bk] for r in send)
        print('  msg %-2s  %3d distinct subjects, largest %3d rows (%2.0f%%)  |  '
              '%3d distinct bodies, largest %3d (%2.0f%%)'
              % (name, len(cs), cs.most_common(1)[0][1], 100*cs.most_common(1)[0][1]/len(send),
                 len(cb), cb.most_common(1)[0][1], 100*cb.most_common(1)[0][1]/len(send)))
    print()
    print('HIGH findings by message:', dict(worst) or 'none')

    # paste-ready pack: one representative per distinct template shape
    seen, pack = set(), []
    for r in send:
        for name, sk, bk in MESSAGES:
            shape = (name, r['segment_variant'], r['contact_thread'])
            if shape in seen:
                continue
            seen.add(shape)
            pack.append((shape, r['company_name'], r[sk], r[bk]))
    pack.sort()
    with open('templates_for_spamcheck.md', 'w') as fh:
        fh.write('# Every distinct template in the file, for a second opinion\n\n')
        fh.write('%d shapes across 306 sending rows. Personalisation is filled in '
                 'from a real row, named under each heading, so what you paste is '
                 'what lands in an inbox.\n\n'
                 'Paste each body with its subject into Mail Meteor, GlockApps or '
                 'Mail Tester. `spam_audit.py` checks all %d emails; this file is '
                 'here so a human can confirm the same set by hand.\n\n'
                 % (len(pack), len(send) * 4))
        for (name, seg, thread), co, subj, body in pack:
            fh.write('## Message %s, segment %s, thread %s\n\n' % (name, seg, thread))
            fh.write('Example row: %s\n\n**Subject:** %s\n\n```\n%s\n```\n\n' % (co, subj, body))
    print('\nwrote templates_for_spamcheck.md (%d shapes)' % len(pack))

if __name__ == '__main__':
    main()
