#!/usr/bin/env python3
"""Gate 4: the website pass. Free, and the one that does the real work.

One fetch of each company's own homepage, to produce the four things wave 2
paid Clay for at company level:

    site_live      no site, no pitch. Dropped before a credit is spent.
    has_tryon      already runs a visualiser. Wave 2's strongest segment, and
                   the sharpest subject line in the campaign.
    sells_to       consumer, trade only, or unclear. This is what resolves the
                   193 rug export houses, rather than cutting them on country,
                   which would have been a guess dressed as a rule.
    site_quote     a line from their own page, for the "We noticed something
                   on {company}" subject.

Plus email_pattern, inferred from the company email already in hand, so Clay
knows whether to look for first.last@, f.last@ or a named mailbox.

Polite: one request per domain, 8 at a time, 12s timeout, a browser user
agent, and failures recorded rather than retried in a loop.
"""
import csv, re, html, collections, sys, socket
import urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/125.0 Safari/537.36')
socket.setdefaulttimeout(12)

TRYON = re.compile(
    r'roomvo|room ?vo|visuali[sz]er|visuali[sz]e your|room ?planner|room ?designer|'
    r'see it in your (room|space|home)|view in your (room|space)|try (it )?in your room|'
    r'augmented reality|\bar view|3d (room|configurator|visuali)|configurator|'
    r'simulador|simulatore|raumplaner|raumgestalter|prova in casa|'
    r'design your (room|space)|mock ?up your', re.I)

CONSUMER = re.compile(
    r'add to (cart|basket|bag)|aggiungi al carrello|a.adir al carrito|'
    r'\bcheckout\b|/cart|/basket|woocommerce|shopify|prestashop|magento|'
    r'\bmy account\b|\bwishlist\b|free (shipping|delivery)|buy (it )?now|'
    r'shop (now|online|all)', re.I)

# A brand site that routes shoppers to dealers IS consumer facing, and the
# first run missed that completely. Bonaldo, MDF Italia, Acerbis and Annibale
# Colombo all came back "unclear" because the regex looked for a cart. High-end
# Italian furniture has no cart anywhere: it markets hard to consumers and ends
# the journey at a dealer locator. That is not ambiguity, it is the ideal
# customer, since routing that shopper to a dealer is exactly what the lead
# engine does.
DEALER = re.compile(
    r'find (a |your )?(dealer|retailer|stockist|store|showroom)|store ?locator|'
    r'where to buy|dealer locator|find us|our (dealers|retailers|stockists|showrooms)|'
    r'punti vendita|rivenditor|trova (il )?rivenditore|dove (siamo|acquistare)|'
    r'h.ndler ?suche|fachh.ndler|distribuidor|revendedor|point de vente|'
    r'revendeur|verkooppunt|showroom locator', re.I)

# The 411 that came back "unclear" were not unclear. Sampling 23 of them
# found 16 with a downloadable catalogue, 15 with a contact form, 9 publishing
# collections, and only 3 showing a price. Annibale Colombo is the type: Home,
# Azienda, Indoor, Outdoor, Designers, Contatti. No cart, no dealer finder, no
# prices anywhere.
#
# That is a BRAND SHOWCASE, and it is the exact shape the campaign body opens
# on: "your site shows the collections well, and then the visit ends at a
# catalogue". Labelling it unclear buried the segment the copy was written for.
#
# One honesty caveat kept in the label: a homepage cannot tell you whether
# those visitors are homeowners or architects. The shape is certain, the
# audience is not, so the value says catalogue only rather than consumer.
CATALOGUE = re.compile(
    r'\bcatalog(ue|o|ues|s)?\b|katalog|\bcollection(s)?\b|collezion|kollektion|'
    r'coleccion|cole..o|\bdownload', re.I)
CONTACTABLE = re.compile(
    r'\bcontact\b|contatt|kontakt|contacto|contato|request (a )?(quote|information)|'
    r'richiedi informazioni|\bnewsletter\b|\benquir|\binquir', re.I)
# A dealer login with no cart and no public locator means the shopper journey
# is gated, so the visitor is a dealer, not a buyer.
#
# Pass 3 shipped this with a bare `area riservat|reserved area` alternative and
# it was wrong on 30 of the 42 rows it labelled. Annibale Colombo caught it: its
# footer reads "Area riservata | Modelli 3D", a link to a 3D-model download
# portal sitting between an Instagram icon and a newsletter form. In Italian
# `area riservata` is the ordinary label for ANY login-protected resource area
# -- press kits, CAD files, downloads, a plain customer account. It says a login
# exists. It does not say who it is for, and it does not say the shopper journey
# is gated. Reading it as trade-only is the same mistake as reading a nav-bar
# "Visualizer" as a product feature: a word in the chrome taken for a fact about
# the funnel.
#
# So the reserved-area wording now only counts when a trade word sits within 120
# characters of it. That keeps the rows where it means what it says -- Target
# Point's "Area riservata agenti", Ceramica Cielo -- and drops the 30 brand
# showcases that merely have a download login, which fall through to the
# catalogue-only / unclear branches where they belong.
GATED = re.compile(
    r'\b(dealer|reseller|retailer|partner|b2b)\s*(login|log in|area|portal|zone)|'
    r'\bmy ?account\b.{0,40}(dealer|reseller)|'
    r'bereich f.r h.ndler|espace revendeur|'
    r'(?:area riservat|reserved area)[\s\S]{0,120}?'
    r'(rivendit|agent|dealer|reseller|retailer|grossist|wholesal|b2b)|'
    r'(rivendit|agent|dealer|reseller|retailer|grossist|wholesal|b2b)'
    r'[\s\S]{0,120}?(?:area riservat|reserved area)', re.I)

TRADE = re.compile(
    r'trade only|to the trade\b|wholesale (only|enquir|inquir)|dealer (login|portal|area)|'
    r'reseller (login|portal)|b2b (portal|only|login)|retailer (login|area)|'
    r'request (a )?(price list|catalogue) .{0,20}trade|solo per (rivenditori|operatori)|'
    r'riservata ai rivenditori|professionals only', re.I)

QUOTE_META = re.compile(
    r'<meta[^>]+(?:property=["\']og:description["\']|name=["\']description["\'])'
    r'[^>]+content=["\']([^"\']{25,220})["\']', re.I)
QUOTE_H1 = re.compile(r'<h1[^>]*>(.{12,160}?)</h1>', re.I | re.S)
TAGS = re.compile(r'<[^>]+>')

def strip(s):
    return re.sub(r'\s+', ' ', html.unescape(TAGS.sub(' ', s or ''))).strip()

def fetch(url):
    req = urllib.request.Request(url, headers={
        'User-Agent': UA, 'Accept': 'text/html,application/xhtml+xml',
        'Accept-Language': 'en,it;q=0.8'})
    with urllib.request.urlopen(req, timeout=12) as r:
        raw = r.read(400_000)
        enc = r.headers.get_content_charset() or 'utf-8'
        return r.geturl(), raw.decode(enc, 'replace')

def pattern(email):
    l = (email or '').split('@')[0].lower()
    if not l: return ''
    if re.fullmatch(r'[a-z]+\.[a-z]+', l):   return 'first.last'
    if re.fullmatch(r'[a-z]\.[a-z]+', l):    return 'f.last'
    if re.fullmatch(r'[a-z]+_[a-z]+', l):    return 'first_last'
    if re.fullmatch(r'[a-z]{2,}[a-z]+', l) and l in (
        'info','sales','contact','office','mail','admin','hello','export',
        'marketing','commerciale','ufficio','vendite','enquiries'): return 'role inbox'
    return 'other'

def probe(r):
    site = (r['website'] or '').strip()
    out = {'site_live': 'no site', 'final_url': '', 'has_tryon': '',
           'sells_to': '', 'site_quote': '', 'site_note': ''}
    if not site:
        return out
    if not site.startswith('http'):
        site = 'https://' + site
    try:
        final, body = fetch(site)
    except Exception as e:
        try:
            final, body = fetch(site.replace('https://', 'http://', 1))
        except Exception as e2:
            out['site_live'] = 'unreachable'
            out['site_note'] = str(e2)[:70]
            return out
    out['site_live'] = 'yes'
    out['final_url'] = final[:120]
    out['has_tryon'] = 'yes' if TRYON.search(body) else 'no'
    shop, dealer, trade = (bool(CONSUMER.search(body)), bool(DEALER.search(body)),
                           bool(TRADE.search(body)))
    gated = bool(GATED.search(body))
    showcase = bool(CATALOGUE.search(body)) and bool(CONTACTABLE.search(body))
    if shop:
        out['sells_to'] = 'consumer, sells online'
    elif dealer:
        out['sells_to'] = 'consumer, via dealers'
    elif trade or gated:
        out['sells_to'] = 'trade portal, gated'
    elif showcase:
        out['sells_to'] = 'catalogue only'
    else:
        out['sells_to'] = 'unclear'
    q = QUOTE_META.search(body) or QUOTE_H1.search(body)
    if q:
        t = strip(q.group(1))
        if 12 <= len(t) <= 200:
            out['site_quote'] = t
    return out

def reason(r):
    """One line a human can read, so the file explains itself instead of
    needing four columns decoded."""
    if r['site_live'] == 'no site':
        return 'No website on file, so nothing for a visualiser to sit on. Skip'
    if r['site_live'] == 'unreachable':
        return 'Site did not respond, check it by hand before spending a credit'
    tryon = r['has_tryon'] == 'yes'
    sells = r['sells_to']
    who = {'consumer, sells online': 'sells direct to shoppers',
           'consumer, via dealers': 'markets to shoppers and routes them to dealers',
           'trade portal, gated': 'gates its catalogue behind a dealer login',
           'catalogue only': 'publishes collections and a catalogue with a contact form '
                             'as the only way in',
           'unclear': 'no catalogue, cart or contact route found'}[sells]
    if tryon and sells.startswith('consumer'):
        return ('Already runs a visualiser and %s, so the gap is what happens '
                'after the render. Sharpest segment' % who)
    if tryon:
        return ('Already runs a visualiser but %s, so confirm there is a '
                'shopper to capture' % who)
    if sells == 'trade portal, gated':
        return ('Catalogue sits behind a dealer login, so the visitor is a dealer '
                'rather than a buyer')
    if sells == 'catalogue only':
        return ('Publishes collections with a contact form as the only way in, which '
                'is the exact problem the email opens on. Audience unconfirmed')
    if sells == 'unclear':
        return 'Live site but no catalogue, cart or contact route found, needs a look'
    return 'No visualiser yet and %s, so this is the full pitch rather than an upgrade' % who

if __name__ == '__main__':
    rows = list(csv.DictReader(open('round3_companies.csv', encoding='utf-8-sig')))
    todo = [r for r in rows if r['verdict'] in ('take', 'review')]
    print('probing %d sites, 8 at a time' % len(todo), flush=True)
    done = 0
    with ThreadPoolExecutor(max_workers=8) as ex:
        for r, res in zip(todo, ex.map(probe, todo)):
            r.update(res)
            r['email_pattern'] = pattern(r['email'])
            r['reason'] = reason(r)
            done += 1
            if done % 100 == 0:
                print('  %d/%d' % (done, len(todo)), flush=True)
    for r in rows:
        for k in ('site_live','final_url','has_tryon','sells_to','site_quote',
                  'site_note','email_pattern','reason'):
            r.setdefault(k, '')
    cols = list(rows[0].keys())
    with open('round3_qualified.csv', 'w', newline='', encoding='utf-8-sig') as fh:
        w = csv.DictWriter(fh, fieldnames=cols, quoting=csv.QUOTE_ALL)
        w.writeheader(); w.writerows(rows)
    print('\nsite_live:', dict(collections.Counter(r['site_live'] for r in todo)))
    live = [r for r in todo if r['site_live'] == 'yes']
    print('has_tryon:', dict(collections.Counter(r['has_tryon'] for r in live)))
    print('sells_to :', dict(collections.Counter(r['sells_to'] for r in live)))
    print('quote captured:', sum(1 for r in live if r['site_quote']), 'of', len(live))
    print('email_pattern:', dict(collections.Counter(r['email_pattern'] for r in todo)))
    print()
    print('reason lines:')
    for k, n in collections.Counter(r['reason'][:68] for r in todo).most_common():
        print('  %4d  %s' % (n, k))
