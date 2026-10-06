#!/usr/bin/env python3
"""Pull the Heimtextil exhibitor directory and gate it to our ICP.

HOW THE API WAS FOUND. The exhibitor-search page embeds a config blob naming
API_URL and API_EVENT_ID=HEIMTEXTIL, but that host 404s. The real base is in
exhibitorsearch.messefrankfurt.com/assets/main.js:

    apiBaseUrl('prd') + '/esb_api'
      -> https://api.messefrankfurt.com/service/esb_api
    SEARCH_API_URL = apiUrl + '/exhibitor-service/api/2.1/public/exhibitor/search'
    requests carry a header:  apikey: <key>

The bundle ships four keys. Two are APIKEY_PRIVATE_*, which the code only
uses when SSR is true, i.e. server side. Those are not ours to use even
though they are sitting in a public file. APIKEY_PUBLIC_PRD is the one every
visitor's browser sends for this public directory, so that is the one here.

Same shape of win as Salone: the record carries homepage and
address.email, so website and email arrive free and no domain research or
company-level enrichment is needed.

THE GATE. Heimtextil is mostly textiles, which we have no studio for, so the
13 top-level categories do the work. Filtering by category through the API
did not take, the parameter name is not `categories` and guessing it was
wasting calls, so all 1,412 records are pulled once and gated here. One pass,
15 requests.

    TAKE
      Wall Decoration            -> /wallpaper   the Mural Studio's exact ICP
      Carpets & Rugs             -> /rugs        fills a studio that has zero
      Flooring & Equipment       -> /rugs        checked against subcategories
      Textile Design             -> /wallpaper   surface pattern studios

    SKIP
      Window & Interior Decoration   curtains, blinds, sun protection
      Decorative & Furniture Fabrics upholstery fabric by the metre
      Smart Bedding                  bedding
      Bed, Bath & Living             linen and towels
      Fibres and Yarns, Finishing    raw input, no pattern
      Textile Technology             machinery
      Services & Software            not a maker
      Associations, institutes...    nobody to sell to
      Functional features            a property, not a product line

A company can book several categories, so TAKE wins over SKIP: a wallpaper
house that also books Bed, Bath & Living stays in.
"""
import json, time, csv, collections, urllib.request, urllib.parse, re, sys, html as _html

KEY = 'LXnMWcYQhipLAS7rImEzmZ3CkrU033FMha9cwVSngG4vbufTsAOCQQ=='
SEARCH = ('https://api.messefrankfurt.com/service/esb_api'
          '/exhibitor-service/api/2.1/public/exhibitor/search')
EVENT = 'HEIMTEXTIL'

TAKE = {
    'Wall Decoration':      'wallpaper',
    'Carpets & Rugs':       'rugs',
    'Flooring & Equipment': 'rugs',
}
# Textile Design was in TAKE and should not have been. Looking at who is in it
# settles it: Atelier Zabel, Artwork Portfolio, Banafshe Schippel, AD Design &
# Color Concept. They are surface pattern studios that sell DESIGNS to
# manufacturers. There is no catalogue a shopper browses and no installed
# product to render into a room, so they are suppliers to our ICP rather than
# our ICP. 58 rows out.
DESIGN_STUDIO = 'Textile Design'

# Carpets & Rugs is 127 rows and 90 of them are India: Achal Amit, Akara, Ali
# Arts, Ansari Floor Rugs, Artex Home Fashions. These are Bhadohi and Jaipur
# export houses selling to importers and retailers, which is a different
# business model from a brand with its own shoppers, and it is the same trap
# as Marmomac's quarries and the Chinese stone traders. Not excluded on
# geography, because some will have a retail arm, but flagged for a look
# rather than counted as prospects. The 37 non-hub rows, Germany 11, Belgium
# 7, Italy, Spain, are the ones that read as brands.
EXPORT_HUB = {'India', 'Pakistan', 'Egypt', 'Türkiye', 'Turkey', 'Nepal',
              'China', 'Bangladesh'}
SKIP = {'Window & Interior Decoration', 'Decorative & Furniture Fabrics',
        'Smart Bedding', 'Bed, Bath & Living', 'Textile Technology',
        'Fibres and Yarns, Textile Materials, Finishing', 'Services & Software',
        'Associations, institutes, publishers', 'Functional features'}

def get(page, size=100):
    # pageNumber, NOT page, and it is 1-based. Passing `page` is silently
    # ignored: 15 requests came back as the same 100 companies, which read as
    # 1,500 exhibitors and produced category counts that were all multiples of
    # 15. The giveaway was fetching 1,500 of a stated 1,412.
    q = urllib.parse.urlencode({'findEventVariable': EVENT, 'language': 'en-GB',
                                'pageSize': size, 'pageNumber': page})
    req = urllib.request.Request(SEARCH + '?' + q,
                                 headers={'apikey': KEY, 'Accept': 'application/json'})
    with urllib.request.urlopen(req, timeout=90) as f:
        return json.load(f)['result']

def fetch_all():
    """One probe for the count, then one call for the lot.

    The app's own postAllExhibitorsToWatchlist does exactly this, pageNumber=1
    with pageSize set to totalResults, so a single large page is a supported
    use rather than something being abused. Falls back to paging if the big
    call is refused."""
    total = get(1, 1)['metaData']['hitsTotal']
    print('  %d exhibitors, fetching in one call' % total, flush=True)
    try:
        hits = get(1, total).get('hits') or []
        if len(hits) >= total:
            return [h['exhibitor'] for h in hits]
        print('  one-shot returned %d, paging instead' % len(hits), flush=True)
    except Exception as err:
        print('  one-shot refused (%s), paging instead' % err, flush=True)
    out, page = [], 1
    while len(out) < total:
        hits = get(page, 100).get('hits') or []
        if not hits:
            break
        out += [h['exhibitor'] for h in hits]
        print('  page %2d  +%-4d total %d/%d' % (page, len(hits), len(out), total), flush=True)
        page += 1
        time.sleep(0.4)
    return out

def halls(e):
    return ';'.join(h.get('id', '') for h in
                    ((e.get('exhibition') or {}).get('exhibitionHall') or []))

def cats(e):
    return [c.get('name') for c in (e.get('categories') or []) if c.get('name')]

def subcats(e):
    out = []
    for c in (e.get('categories') or []):
        for s in (c.get('subCategories') or []):
            if s.get('name'):
                out.append(s['name'])
    return out

COLS = ['company','website','email','phone','country','city','zip','street',
        'halls','categories','subcategories','products','rewrite_id',
        'verdict','why','studio']

def clean(v):
    """The API returns HTML entities in names: "Erfurt &amp; Sohn KG",
    "Hohenberger Manufaktur f&uuml;r Tapeten". Those would go straight into a
    subject line and a greeting."""
    return re.sub(r'\s+', ' ', _html.unescape(v or '')).strip()

def row(e):
    a = e.get('address') or {}
    c = cats(e)
    taken = [TAKE[x] for x in c if x in TAKE]
    p = e.get('products') or {}
    return {
        'company': clean(e.get('name')),
        'website': (e.get('homepage') or '').strip(),
        'email': (a.get('email') or '').strip(),
        'phone': (a.get('tel') or '').strip(),
        'country': ((a.get('country') or {}).get('label') or '').strip(),
        'city': clean(a.get('city')),
        'zip': (a.get('zip') or '').strip(),
        'street': clean(a.get('street')),
        'halls': halls(e),
        'categories': ' | '.join(c),
        'subcategories': ' | '.join(sorted(set(subcats(e)))[:12]),
        'products': str(p.get('countTotal') or 0),
        'rewrite_id': e.get('rewriteId') or '',
        'verdict': '', 'why': '', 'studio': taken[0] if taken else '',
    }

def dom(u):
    u = re.sub(r'^https?://', '', (u or '').strip().lower())
    return re.sub(r'^www\.', '', u).split('/')[0]

def load_known():
    """Wave 2 and Salone are already being sourced, and four wallpaper houses
    here are in wave 2 already from the original 23-row Heimtextil capture:
    Erfurt & Sohn, Hohenberger, KT Exclusive, Marburger. A second sequence to
    the same company is the one mistake that cannot be undone."""
    known = set()
    for path, col in (('../../wave2/copy/MEC_Instantly_Wave2.csv', 'website'),
                      ('../salone/salone_2026_gated.csv', 'website')):
        try:
            for r in csv.DictReader(open(path, encoding='utf-8-sig')):
                if r.get(col): known.add(dom(r[col]))
        except FileNotFoundError:
            pass
    return known

KNOWN = load_known()

def judge(r, cats_list):
    if r['website'] and dom(r['website']) in KNOWN:
        return 'already live', 'already sourced in wave 2 or Salone'
    if not r['studio']:
        if DESIGN_STUDIO in cats_list:
            return 'skip', 'Textile Design: sells designs to manufacturers, not products to shoppers'
        return 'skip', (', '.join(cats_list) or 'no category booked')
    if 'Carpets & Rugs' in cats_list and r['country'] in EXPORT_HUB:
        return 'review', 'rug export house, confirm it sells to end buyers and not only to importers'
    return 'take', ', '.join(sorted({x for x in cats_list if x in TAKE}))

if __name__ == '__main__':
    print('fetching Heimtextil')
    raw = fetch_all()
    seen, uniq = set(), []
    for e in raw:
        k = (e.get('rewriteId') or e.get('name') or '').lower()
        if k and k not in seen:
            seen.add(k); uniq.append(e)
    if len(uniq) != len(raw):
        print('  deduped %d repeated records' % (len(raw) - len(uniq)))
    raw = uniq
    rows = []
    for e in raw:
        r = row(e)
        r['verdict'], r['why'] = judge(r, cats(e))
        rows.append(r)
    with open('heimtextil.csv', 'w', newline='', encoding='utf-8-sig') as fh:
        w = csv.DictWriter(fh, fieldnames=COLS, quoting=csv.QUOTE_ALL)
        w.writeheader(); w.writerows(rows)
    take = [r for r in rows if r['verdict'] in ('take', 'review')]
    with open('heimtextil_gated.csv', 'w', newline='', encoding='utf-8-sig') as fh:
        w = csv.DictWriter(fh, fieldnames=COLS, quoting=csv.QUOTE_ALL)
        w.writeheader(); w.writerows(take)
    print('\n%d exhibitors' % len(rows))
    print('  ', dict(collections.Counter(r['verdict'] for r in rows)))
    print('studio:', dict(collections.Counter(r['studio'] for r in take)))
    print('take only, by studio:', dict(collections.Counter(
        r['studio'] for r in rows if r['verdict']=='take')))
    print('website: %d of %d | email: %d of %d'
          % (sum(1 for r in take if r['website']), len(take),
             sum(1 for r in take if r['email']), len(take)))
    print('\ntop categories overall:')
    cc = collections.Counter()
    for r in rows:
        for x in r['categories'].split(' | '):
            if x: cc[x] += 1
    for k, v in cc.most_common(): print('  %4d  %-46s %s' % (v, k, 'TAKE' if k in TAKE else ''))
    print('\ncountries, taken:', dict(collections.Counter(r['country'] for r in take).most_common(10)))
