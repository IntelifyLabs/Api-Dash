#!/usr/bin/env python3
"""Gate 5: reproduce wave 2's remaining qualifier fields. Free, no Clay.

Wave 2's Clay qualifier produced seven things. Gate 4 covered two of them,
site_live and has_tryon. This covers the rest, because they are what the copy
was actually built on:

    Use AI Tool Level     NONE 149, BASIC 148, ADVANCED 90, MANUAL 52
    Use AI Has Tryon      yes 72, no 367
    Use AI Business Role  MAKER 298, MAKER_AND_DISTRIBUTOR 124, DISTRIBUTOR 14
    Use AI Product Type   CATALOGUE 300, BOTH 137, CUSTOM 2
    Use AI Tool Url       the link to their own tool
    Use AI Tool Evidence  the sentence that proves it
    Site Matches Company  a sanity check on the domain

TOOL LEVEL IS THE ONE THAT MATTERS. build_instantly.py derives the whole
campaign segmentation from it:

    seg = 'C' if tryon == 'yes' else ('A' if lvl == 'MANUAL' else 'B')

C already runs a visualiser, so the email names their tool and asks what
happens after the render. A has a person making mock-ups by hand, so the email
is about the week that costs them. B is everyone else. Without tool_level
there is no segment A at all, and segment A is where "somebody on your team
makes the mock-ups one at a time" comes from.

Levels, in the order they are tested:

    ADVANCED  a real room visualiser. Upload a photo, see it in your room,
              Roomvo, a 3D room configurator.
    MANUAL    a person does it. Send us your photo, our designers will prepare
              a rendering, request a free mock-up, su misura su richiesta.
    BASIC     filters, colour pickers, a product configurator with no room.
    NONE      nothing found.

THE HTML IS CACHED THIS TIME. Gate 4 took three passes because each new signal
needed another full re-fetch, and that was avoidable. Pages are written to
html_cache/ so any future signal is a re-read rather than a re-crawl.
"""
import csv, re, html as _html, collections, os, hashlib, socket, sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from visible import visible_text

UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/125.0 Safari/537.36')
socket.setdefaulttimeout(12)
CACHE = 'html_cache'
os.makedirs(CACHE, exist_ok=True)

# Named tools worth printing back at the reader. Wave 2 proved this is the
# strongest personalisation in the campaign, and also proved the trap: 247 of
# its 277 "tool names" were the generic words Visualizer and Configurator
# lifted off a nav bar, which is not personalisation. Only real brands here.
# 'Configura' used to be in this list and produced 213 hits -- the single
# largest "finding" in the gate. Every one checked was noise: the minified-JS
# tokens `configuration` and `configurable`, and Shopify's `webPixelsConfigList`.
# On visible text with a word boundary it drops to 17, and those are the Italian
# imperative "Configura il tuo ..." (configure your ...), which is a button
# label, not a vendor. Configura the company is identifiable by its product
# name, CET, so that is what is matched now.
KNOWN = ['Roomvo', 'Roomviewer', 'DomuS3D', 'Virtual Stylist', 'Room Designer',
         'Cylindo', 'Threekit', 'Marxent', 'Roomle', 'CET Designer', 'pCon',
         'Spaceroom', 'Estila', 'Modsy', 'Leaptools', 'Visualizer by',
         'Simulador 3D', 'Design Your Pool', 'Create 3D', 'Virtual Room',
         'Virtual Viewer', 'Mydecorator', 'SmartPicture', 'Houzz Visual Match']

ADVANCED = re.compile(
    r'roomvo|room ?vo|upload (a )?(photo|picture|image) of your (room|space|wall|floor)|'
    r'see (it|them) in your (room|space|home)|view in your (room|space)|'
    r'try (it )?(on|in) your (room|wall|floor)|visuali[sz]e (it )?in your|'
    r'room ?visuali[sz]er|3d room|augmented reality|\bar view\b|'
    r'raumplaner|prova (il|la) .{0,18}in casa|simulador de ambiente|'
    r'photo ?realistic render|render your room', re.I)

MANUAL = re.compile(
    r'send us (a )?(photo|picture|your plan)|upload your plan|'
    r'our (designers?|team|studio) will (prepare|create|draw|render)|'
    r'request (a )?(free )?(mock ?up|rendering|render|3d (project|design)|'
    r'design (service|consultation))|free design service|'
    r'progetto personalizzato|rendering su richiesta|su misura su richiesta|'
    r'servizio di progettazione|proyecto a medida|'
    r'book (a )?(free )?design (appointment|consultation)', re.I)

BASIC = re.compile(
    r'\bconfigurator\b|configuratore|configurador|konfigurator|'
    r'customi[sz]e (your|this) (product|sofa|kitchen)|'
    r'choose (your )?(finish|colour|color|fabric|material)|'
    r'filter by (colour|color|finish|size|material)|product finder|'
    r'colour picker|color picker|scegli (il|la) (finitura|colore)', re.I)

MAKER = re.compile(r'\bwe (manufactur|produce|make|craft)|our (factory|workshop|atelier|'
                   r'production)|manufactur(er|ing) (of|since)|produciamo|'
                   r'nostra produzione|fabbrica|herstell|fabricaci|\bsince \d{4}\b.{0,40}'
                   r'(manufactur|produc)', re.I)
# This labelled 121 companies DISTRIBUTOR on a list of trade-fair exhibitors,
# who are makers almost by definition. Two faults, both of them the regex
# answering a different question than the column asks:
#
#   `\bimport.{0,6}export\b` matched `"import-export-customization":true`, a
#   feature flag in the Elementor WordPress builder's config JSON. 79 of the 121.
#
#   bare `distributor` and `official dealer` match a MAKER's own pages --
#   "Distributors Network", "Become a distributor", "find an official dealer".
#   A brand recruiting distributors is not a distributor.
#
# So the column now needs a first-person or explicitly-official self-description.
# It will return blank more often. Blank is the honest answer when a homepage
# does not say; a wrong role would put the wrong sentence in the email.
DISTRIB = re.compile(
    r'we (are|re) (a|an|the) [^.]{0,30}(distributor|importer|wholesaler)|'
    r'we (distribute|import and distribute)\b|'
    r'(official|authorised|authorized|exclusive) (distributor|importer) (of|for)\b|'
    r'(distributore|importatore) (ufficiale|esclusivo)|distribuidor oficial|'
    r'siamo (un|il) (distributore|importatore)', re.I)
RETAIL = re.compile(r'\bour (store|shop|boutique)s?\b|visit our (store|shop)|'
                    r'\bretailer\b.{0,20}\bwe\b|negozio', re.I)

CUSTOM = re.compile(r'\bbespoke\b|made[- ]to[- ](order|measure)|\bcustom(ised|ized)\b|'
                    r'su misura|personalizza|sur mesure|ma.?anfertigung|a medida|'
                    r'one[- ]off|hand[- ]?(made|crafted)|artigian', re.I)
CATALOGUE = re.compile(r'\bcollection(s)?\b|collezion|kollektion|\bcatalog(ue)?\b|'
                       r'catalogo|katalog|our (range|products)', re.I)

TAGS = re.compile(r'<[^>]+>')
def strip(s):
    return re.sub(r'\s+', ' ', _html.unescape(TAGS.sub(' ', s or ''))).strip()

def cache_path(url):
    return os.path.join(CACHE, hashlib.sha1(url.encode()).hexdigest()[:20] + '.html')

def get(url, final=''):
    """Cached. Gate 4 cost three full crawls because nothing was kept.

    69 live rows came back blank on the first run. The cause was this function
    fetching only the https:// form built from the website column, while gate 4
    had recorded in final_url the address that actually answered -- often an
    http:// host or the far end of a redirect. So the URL gate 4 proved works is
    tried as well.

    The cache key stays the constructed URL, not the final one, so the 839 pages
    already on disk are still hits.
    """
    p = cache_path(url)
    if os.path.exists(p):
        return open(p, encoding='utf-8', errors='replace').read()
    attempts = [url] + [u for u in (final, url.replace('https://', 'http://', 1))
                        if u and u != url]
    last = None
    for u in attempts:
        try:
            req = urllib.request.Request(u, headers={
                'User-Agent': UA, 'Accept': 'text/html,application/xhtml+xml',
                'Accept-Language': 'en,it;q=0.8'})
            with urllib.request.urlopen(req, timeout=15) as r:
                body = r.read(400_000).decode(
                    r.headers.get_content_charset() or 'utf-8', 'replace')
            open(p, 'w', encoding='utf-8').write(body)
            return body
        except Exception as e:
            last = e
    raise last

def evidence(m, body, n=150):
    i = max(0, m.start() - 60)
    out = strip(body[i:m.start() + n])[:190]
    # One row claimed a tool level with a blank quote, because the window around
    # the match stripped to nothing. The matched phrase itself is always better
    # than an empty cell: a level with no evidence cannot be checked by hand.
    return out or strip(m.group(0))[:190]

def probe(r):
    # has_tryon is blanked here, not left alone, and that matters on the early
    # returns below. Gate 4's value for it is known-unreliable -- it counted
    # configurators as visualisers -- so a row gate 5 cannot read must not keep
    # gate 4's answer. Two rows did: PLA.NET and Scarabeo Ceramiche came out
    # has_tryon=yes with no tool_level behind it, which is exactly the
    # unjustifiable claim the redefinition was meant to remove. Blank means
    # nobody has established it, which is the truth for these rows.
    out = {'tool_level': '', 'tool_name': '', 'tool_evidence': '',
           'business_role': '', 'product_type': '', 'site_matches': '',
           'segment': '', 'has_tryon': ''}
    site = (r['website'] or '').strip()
    if not site or r['site_live'] != 'yes':
        return out
    if not site.startswith('http'):
        site = 'https://' + site
    try:
        raw = get(site, r.get('final_url') or '')
    except Exception:
        return out

    # SCOPE EACH SIGNAL TO THE EVIDENCE THAT CAN CARRY IT.
    #
    # The first version of this gate matched everything against raw HTML and
    # invented 213 Configura installs out of minified JavaScript. The obvious
    # correction -- strip scripts, match visible text everywhere -- was measured
    # before being shipped, and it destroyed the two best findings in the file:
    # Farrow & Ball and Erismann both run Roomvo, and on both the only trace of
    # it is the widget's own <script>. Of course it is. A third-party visualiser
    # IS a script tag; that is what an integration looks like.
    #
    # So the rule is not "strip the code", it is "ask each question where its
    # answer actually lives":
    #
    #   a VENDOR is a technical fact      -> raw HTML, scripts included
    #   a CLAIM about the business is copy -> visible text only
    #
    # Getting this backwards either way loses real companies.
    text = visible_text(raw)

    # Vendor first: a named widget outranks any amount of prose, and it is the
    # one piece of personalisation wave 2 proved worth having.
    for k in KNOWN:
        if re.search(r'(?<![a-z])' + re.escape(k) + r'(?![a-z])', raw, re.I):
            out['tool_name'] = k
            break

    m = ADVANCED.search(text)
    if out['tool_name'] or m:
        out['tool_level'] = 'ADVANCED'
        out['tool_evidence'] = (evidence(m, text) if m else
                                'widget on page: ' + out['tool_name'])
    else:
        m = MANUAL.search(text)
        if m:
            out['tool_level'], out['tool_evidence'] = 'MANUAL', evidence(m, text)
        else:
            m = BASIC.search(text)
            if m:
                out['tool_level'], out['tool_evidence'] = 'BASIC', evidence(m, text)
            else:
                out['tool_level'] = 'NONE'

    # has_tryon arrives from gate 4, where it was wrong in a way that would have
    # reached the copy. Gate 4's TRYON regex carries a bare `configurator`
    # alternative, so 54 of the 61 companies it marked yes had matched the single
    # word "configurator" -- a fabric or finish picker, not a room visualiser.
    # Meanwhile gate 4's reason line told the reader "Already runs a visualiser",
    # and segment C's email names their tool and asks what happens after the
    # render. For a company with a finish picker both sentences are false.
    #
    # A configurator is real but it is BASIC, and it is a different pitch. So the
    # column is rewritten to mean what its name claims: a room visualiser, which
    # is exactly tool_level ADVANCED.
    out['has_tryon'] = 'yes' if out['tool_level'] == 'ADVANCED' else 'no'

    mk, ds, rt = MAKER.search(text), DISTRIB.search(text), RETAIL.search(text)
    out['business_role'] = ('MAKER_AND_DISTRIBUTOR' if mk and ds else
                            'MAKER' if mk else 'DISTRIBUTOR' if ds else
                            'RETAILER' if rt else '')
    cu, ca = CUSTOM.search(text), CATALOGUE.search(text)
    out['product_type'] = ('BOTH' if cu and ca else 'CUSTOM' if cu else
                           'CATALOGUE' if ca else '')

    # Does the page actually belong to this company? A parked or wrong domain
    # produces a plausible-looking row that wastes a credit.
    stem = re.sub(r'[^a-z0-9]', '', (r['company'] or '').lower())[:9]
    out['site_matches'] = 'yes' if stem and stem[:6] in re.sub(
        r'[^a-z0-9]', '', text[:200000].lower()) else 'check'

    out['segment'] = ('C' if out['has_tryon'] == 'yes' else
                      'A' if out['tool_level'] == 'MANUAL' else 'B')
    return out

if __name__ == '__main__':
    rows = list(csv.DictReader(open('round3_qualified.csv', encoding='utf-8-sig')))
    todo = [r for r in rows if r['site_live'] == 'yes']
    print('gate 5 over %d live sites (cached where gate 4 already fetched)' % len(todo), flush=True)
    done = 0
    with ThreadPoolExecutor(max_workers=8) as ex:
        for r, res in zip(todo, ex.map(probe, todo)):
            r.update(res); done += 1
            if done % 150 == 0:
                print('  %d/%d' % (done, len(todo)), flush=True)
    # has_tryon changed meaning above, and gate 4's reason line is derived from
    # it, so the sentence has to be rebuilt or the file would explain itself
    # wrongly -- "already runs a visualiser" under has_tryon=no. Gate 4's own
    # reason() is called rather than a copy of it, so the two cannot drift.
    import importlib.util as _il
    _sp = _il.spec_from_file_location('g4', os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'qualify_round3.py'))
    g4 = _il.module_from_spec(_sp); _sp.loader.exec_module(g4)
    for r in rows:
        for k in ('tool_level','tool_name','tool_evidence','business_role',
                  'product_type','site_matches','segment'):
            r.setdefault(k, '')
        if r.get('site_live'):
            r['reason'] = g4.reason(r)
    with open('round3_qualified.csv', 'w', newline='', encoding='utf-8-sig') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), quoting=csv.QUOTE_ALL)
        w.writeheader(); w.writerows(rows)
    print('\ntool_level   :', dict(collections.Counter(r['tool_level'] for r in todo)))
    print('segment      :', dict(collections.Counter(r['segment'] for r in todo)))
    print('business_role:', dict(collections.Counter(r['business_role'] or 'blank' for r in todo)))
    print('product_type :', dict(collections.Counter(r['product_type'] or 'blank' for r in todo)))
    print('named tool   :', dict(collections.Counter(r['tool_name'] for r in todo if r['tool_name'])))
    print('site_matches :', dict(collections.Counter(r['site_matches'] for r in todo)))
    print('\nwave 2 for comparison: NONE 149, BASIC 148, ADVANCED 90, MANUAL 52')
