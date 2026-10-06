#!/usr/bin/env python3
"""Pull the Salone del Mobile exhibitor catalogue from the API its own site uses.

The public exhibitor page is a React app that renders nothing server side, so
the HTML holds no companies. It calls an AWS API Gateway lambda which proxies
Salone's Azure catalogue:

    POST https://hzh2dgp2ke.execute-api.eu-west-1.amazonaws.com/main/exhibitorSearch
    {"params": "anno=2026&evento=SMI&pageSize=200&pageNumber=1"}

Found by reading sdm-breakout-config.bundle.js, the Amplify bundle the page
loads, where aws_cloud_logic_custom maps the apiName sdmAzureApi to that host
and API.azureSearch posts a plain query string to /exhibitorSearch.

WHY THIS MATTERS MORE THAN THE PAGE. The web listing shows a company, a
country and a stand. The API returns the whole record:

    nomeEspositore  company            sitoInternet   WEBSITE
    indirizzo/cap/comune/provinciaNome  email         EMAIL
    nazioneIso3AlphaCode  country iso3  emailDigitale second email
    telefono, fax                       hall, stand
    categorieE      categories, English prodottiE     products, English
    marchiDescrizione  brands           accountId     their own id

So website and email arrive free. The whole domain-research step that
write_domains.py had to do by hand for Cersaie, and the company-level Clay
enrichment behind it, is not needed here at all. Only person-level contacts
remain, and 'email' is often a real inbox rather than info@.

1,313 exhibitors for 2026 across eight events:

    SMI  Salone Internazionale del Mobile, 768
    EUC  EuroCucina, 63
    FTK  Technology For the Kitchen, 41
    RAR  Salone Raritas, 28
    ARB  bathroom (Arredobagno)
    CDA  furnishing accessories (Complemento d'Arredo)
    S_P  S.Project
    EIM  (confirm from the data)

Polite: one request per page, 200 per page, 0.4s apart. Seven calls for the
whole fair.
"""
import json, time, urllib.request, collections, csv, sys

API = 'https://hzh2dgp2ke.execute-api.eu-west-1.amazonaws.com/main/exhibitorSearch'

def call(params):
    req = urllib.request.Request(
        API, data=json.dumps({'params': params}).encode(),
        headers={'Content-Type': 'application/json'}, method='POST')
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

def fetch_year(anno=2026, page_size=200):
    out, page = [], 1
    while True:
        d = call(f'anno={anno}&pageSize={page_size}&pageNumber={page}')
        out += d.get('data') or []
        total, pages = d.get('totalRecords'), d.get('totalPages')
        print('  page %2d/%s  +%-4d total %d/%s'
              % (page, pages, len(d.get('data') or []), len(out), total), flush=True)
        if page >= (pages or 1):
            return out
        page += 1
        time.sleep(0.4)

COLS = ['company', 'website', 'email', 'email2', 'phone', 'country', 'town',
        'province', 'address', 'event', 'hall', 'stand', 'brands',
        'categories', 'products', 'account_id']

def row(r):
    return {
        'company': (r.get('nomeEspositore') or '').strip(),
        'website': (r.get('sitoInternet') or '').strip(),
        'email': (r.get('email') or '').strip(),
        'email2': (r.get('emailDigitale') or '').strip(),
        'phone': (r.get('telefono') or '').strip(),
        'country': (r.get('nazioneIso3AlphaCode') or '').strip(),
        'town': (r.get('comune') or '').strip(),
        'province': (r.get('provinciaNome') or '').strip(),
        'address': (r.get('indirizzo') or '').strip(),
        'event': (r.get('evento') or '').strip(),
        'hall': str(r.get('hall') or '').strip(),
        'stand': str(r.get('stand') or '').strip(),
        'brands': (r.get('marchiDescrizione') or '').strip(),
        'categories': (r.get('categorieE') or '').strip(),
        'products': (r.get('prodottiE') or '').strip(),
        'account_id': str(r.get('accountId') or '').strip(),
    }

if __name__ == '__main__':
    anno = int(sys.argv[1]) if len(sys.argv) > 1 else 2026
    print('fetching anno=%d' % anno)
    raw = fetch_year(anno)
    json.dump(raw, open('salone_%d_raw.json' % anno, 'w'), ensure_ascii=False)
    rows = [row(r) for r in raw]
    with open('salone_%d.csv' % anno, 'w', newline='', encoding='utf-8-sig') as fh:
        w = csv.DictWriter(fh, fieldnames=COLS, quoting=csv.QUOTE_ALL)
        w.writeheader(); w.writerows(rows)
    print('\n%d records -> salone_%d.csv' % (len(rows), anno))
    print('events:', dict(collections.Counter(r['event'] for r in rows)))
    print('with a website: %d  with an email: %d  with either: %d'
          % (sum(1 for r in rows if r['website']),
             sum(1 for r in rows if r['email'] or r['email2']),
             sum(1 for r in rows if r['website'] or r['email'] or r['email2'])))
