#!/usr/bin/env python3
"""Write the enrichment worklist for job titles.

The 29 Sept review asked for job titles in the CSV and a filter for decision
makers. There are no titles to filter on: contacts_final.csv carries 47
columns and not one of them is a title. What it does carry is a LinkedIn URL
for each person, which is the input an enrichment run needs.

So this writes titles_to_enrich.csv: one row per sending contact, with the
profile URL where we have one and an empty job_title column to fill. Drop the
filled file back in as titles.csv and build_instantly.py picks it up, tags
every row and flags the ones who cannot act on this.

Coverage is 276 of 306. The 30 without a profile need a look at the company
site, or they go out untagged, which is what happens today.
"""
import csv

SRC = '../q1/contacts_final.csv'
OUT = 'titles_to_enrich.csv'
SEND = 'MEC_Instantly_Wave2.csv'

def main():
    # Work Email (2) is person 1 and Work Email is person 2. The columns are
    # crossed in the source and reading them the obvious way is wrong.
    li, name = {}, {}
    for r in csv.DictReader(open(SRC)):
        for email_col, li_col, full_col in (('Work Email (2)', 'Linked In Url p1', 'Full Name p1'),
                                            ('Work Email',     'Linked In Url p2', 'Full Name p2')):
            e = (r.get(email_col) or '').strip().lower()
            if e:
                li[e] = (r.get(li_col) or '').strip()
                name[e] = (r.get(full_col) or '').strip()

    rows = [r for r in csv.DictReader(open(SEND, encoding='utf-8-sig'))
            if r['qa_send_flag'] == 'send']
    with open(OUT, 'w', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(['email', 'first_name', 'last_name', 'company_name',
                    'linkedin_url', 'job_title', 'source_full_name'])
        for r in rows:
            e = r['email'].strip().lower()
            w.writerow([r['email'], r['first_name'], r['last_name'],
                        r['company_name'], li.get(e, ''), '', name.get(e, '')])

    have = sum(1 for r in rows if li.get(r['email'].strip().lower()))
    print('%s: %d contacts, %d with a LinkedIn URL, %d without'
          % (OUT, len(rows), have, len(rows) - have))
    print('\nThe %d with no profile to work from:' % (len(rows) - have))
    for r in rows:
        if not li.get(r['email'].strip().lower()):
            print('  %-22s %s' % (r['first_name'], r['company_name']))

if __name__ == '__main__':
    main()
