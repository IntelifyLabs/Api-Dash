#!/usr/bin/env python3
"""Clean the Clay decision-maker export into something safe to send.

Input is Clay's export of round3_clay_743.csv, one row per company with two
contact slots side by side. Output is one row per CONTACT, ranked, plus a
rejects file so nothing disappears silently.

WHY THIS EXISTS: 123 of the 389 contact-email cells Clay returned (32%) are
structurally invalid, and sending them would bounce.

  73  @linkedin.com        LinkedIn does not host company mail. Not addresses.
                           maria@linkedin.com was assigned to 8 different
                           companies.
  50  @qma-management.de   one German firm's domain attached to 50 unrelated
                           companies -- Italian ceramics, Dutch furniture,
                           Bosnian, Thai. The local part is the real person
                           (o.serralunga, emilio_brusaferri); the domain is a
                           waterfall guess.

A 32% hard-bounce rate from haroon@triminage.space would get the domain
blacklisted. .space and .site are already low-reputation TLDs per
gtm/mec/CLAUDE.md section 2, and section 4 records that Campaign 2's inbox
placement was never confirmed. This is the same failure waiting to happen.

Also dropped:
  * an address reused across companies whose domain matches none of them
  * the same human appearing in both contact slots (Indian Ocean's Rajesh Dhir,
    Sylvanix's Sean Wang) -- two cells, one person, would be two emails
  * contacts whose LinkedIn headline names a different employer than ours
    (Brabbu -> "CEO at Home'Society", Lyxo -> "Presidente presso VECA Spa"),
    which is the name-collision failure this project has hit repeatedly

Kept but marked REVIEW: an address on a domain that is not the company's but is
not a known-junk pattern either. Several are genuine group companies -- the
Oniro Group brands all legitimately share onirogroup.it -- so these are flagged
for an eye, not deleted.

contact_rank is 1 for the primary and 2 for a second contact at the same
company. Only 18 companies have a usable second contact, so multi-contact
sending is an edge case here, not the shape of the campaign.
"""
import collections, csv, re, sys

SRC = sys.argv[1] if len(sys.argv) > 1 else 'clay_export.csv'
JUNK = {'linkedin.com', 'qma-management.de'}

def g(r, k):
    return (r.get(k) or '').strip()

def root(d):
    d = re.sub(r'^www\.', '', (d or '').lower())
    p = d.split('.')
    if len(p) > 2 and p[-2] in ('co', 'com', 'net', 'org'):
        return p[-3]
    return p[-2] if len(p) > 1 else d

def wrong_employer(company, headline):
    """Headline says 'X at Y' / 'X presso Y' where Y is not our company."""
    if not headline:
        return False
    m = re.split(r'\s+at\s+|\s+presso\s+', headline, flags=re.I)
    if len(m) < 2:
        return False
    emp = re.sub(r'[^a-z0-9]', '', m[-1].lower())
    co = re.sub(r'[^a-z0-9]', '', company.lower())[:6]
    return bool(co and emp and co not in emp)

rows = list(csv.DictReader(open(SRC, encoding='utf-8-sig')))
carry = [c for c in rows[0] if c not in (
    'Custom Waterfall', 'Full Name', 'Full Name (2)', 'Job Title 2',
    'linkedin 2', 'Headline', 'Headline (2)', 'Firstname', 'Firstname (2)',
    'Linkedin Url', 'Work Email', 'Work Email (2)')]

seen = collections.Counter()
for r in rows:
    for s in ('Work Email', 'Work Email (2)'):
        if g(r, s):
            seen[g(r, s).lower()] += 1

# Each slot names its own email, name, first name, title, linkedin AND the
# headline to test for a wrong employer. Slot A's title IS its headline; slot B
# has both a clean job title and a separate headline, and the headline is the one
# that states the employer.
SLOTS = (('Work Email', 'Full Name', 'Firstname', 'Headline', 'Linkedin Url', 'Headline'),
         ('Work Email (2)', 'Full Name (2)', 'Firstname (2)', 'Job Title 2', 'linkedin 2', 'Headline (2)'))

out, rej = [], []
for r in rows:
    picked, names = [], set()
    for ek, nk, fk, tk, lk, hk in SLOTS:
        e = g(r, ek).lower()
        name, first, title, li = g(r, nk), g(r, fk), g(r, tk), g(r, lk)
        if not e or '@' not in e:
            continue
        dom = e.split('@')[-1]
        why = None
        if dom in JUNK:
            why = 'junk domain, would bounce'
        elif seen[e] > 1 and root(dom) != root(g(r, 'domain')):
            why = 'address reused across companies'
        elif wrong_employer(r['company'], g(r, hk)) or wrong_employer(r['company'], title):
            why = 'headline names a different employer'
        key = (name or e).lower()
        if why is None and key in names:
            why = 'same person already taken from the other slot'
        if why:
            rej.append({'company': r['company'], 'domain': g(r, 'domain'),
                        'email': e, 'name': name, 'title': title, 'reason': why})
            continue
        names.add(key)
        picked.append({
            'contact_email': e, 'contact_name': name, 'contact_first': first,
            'contact_title': title, 'contact_linkedin': li,
            'email_on_company_domain': 'yes' if root(dom) == root(g(r, 'domain')) else 'REVIEW',
        })
    for i, p in enumerate(picked, 1):
        row = {c: r[c] for c in carry}
        row.update(p)
        row['contact_rank'] = i
        row['contacts_at_company'] = len(picked)
        out.append(row)

out.sort(key=lambda r: (r['clay_priority'], r['company'].lower(), r['contact_rank']))
cols = ['company', 'domain', 'contact_first', 'contact_name', 'contact_title',
        'contact_email', 'email_on_company_domain', 'contact_rank',
        'contacts_at_company', 'contact_linkedin'] + \
       [c for c in carry if c not in ('company', 'domain')]
with open('round3_contacts_clean.csv', 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols, quoting=csv.QUOTE_ALL)
    w.writeheader(); w.writerows(out)
with open('round3_contacts_rejected.csv', 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['company','domain','email','name','title','reason'],
                       quoting=csv.QUOTE_ALL)
    w.writeheader(); w.writerows(rej)

comp = {r['company'] for r in out}
print('contacts kept      ', len(out), 'across', len(comp), 'companies')
print('  rank 1           ', sum(1 for r in out if r['contact_rank'] == 1))
print('  rank 2           ', sum(1 for r in out if r['contact_rank'] == 2))
print('  on company domain', sum(1 for r in out if r['email_on_company_domain'] == 'yes'))
print('  REVIEW domain    ', sum(1 for r in out if r['email_on_company_domain'] == 'REVIEW'))
print('\nrejected           ', len(rej))
for k, v in collections.Counter(r['reason'] for r in rej).most_common():
    print('  %4d  %s' % (v, k))
print('\nkept, by priority')
for p in ('1', '2', '3'):
    cs = {r['company'] for r in out if r['clay_priority'] == p}
    print('  priority %s: %3d companies, %3d contacts' % (
        p, len(cs), sum(1 for r in out if r['clay_priority'] == p)))
print('\ncompanies with a usable second contact:',
      len({r['company'] for r in out if r['contact_rank'] == 2}))
