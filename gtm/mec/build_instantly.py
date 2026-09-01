# -*- coding: utf-8 -*-
"""Produce Instantly-ready upload CSVs.

Header rules come from S2 of the master doc, learned the hard way:
  - Custom variables must not be named like Instantly system fields.
    'email_subject' and 'email_body' collide and silently break the campaign.
  - No spaces in any header.
So every custom variable here is prefixed 'msg_' or 'dm_'.

Instantly's own built-in fields are used under their real names, which is
correct and not a collision: email, first_name, last_name, company_name,
website, personalization.

Two files out:
  MEC_Instantly_Upload.csv  - the rows cleared to send now
  MEC_Instantly_Hold.csv    - copy written but gated, load when unblocked
"""
import csv
import copy_data

SRC = 'MEC_Warm_Shortlist_FILLED.csv'
AUD = 'MEC_Warm_Shortlist_AUDITED.csv'
COPY = copy_data.COPY

HEADERS = [
    # Instantly built-ins
    'email', 'first_name', 'last_name', 'company_name', 'website',
    # custom variables, all collision-proof
    'msg_subject_one', 'msg_touch_one',
    'msg_subject_two', 'msg_touch_two',
    'msg_subject_three', 'msg_touch_three',
    'dm_job_title', 'msg_segment', 'msg_cta_type',
]
HEADERS_ALL = HEADERS + ['send_gate', 'gate_reason']

rows = list(csv.DictReader(open(SRC, encoding='utf-8')))
aud = list(csv.DictReader(open(AUD, encoding='utf-8')))
for r, a in zip(rows, aud):
    r['_verdict'], r['_priority'] = a['audit_verdict'], a['audit_priority']

def revenue_fails(v):
    return (v or '').strip() in ('0-500K', '500K-1M')

def gate(r):
    email = (r.get('Work Email') or '').strip()
    if not email: return 'NO EMAIL'
    if r['_verdict'] == 'DROP': return 'HOLD'
    dom = (r.get('Domain') or '').lower().replace('www.', '')
    ed = email.split('@')[-1].lower()
    if dom and ed != dom and ed.split('.')[0] != dom.split('.')[0]: return 'EXCLUDED'
    if revenue_fails(r['Annual Revenue']): return 'HOLD'
    if r['_verdict'] in ('PARKED', 'RECHECK'): return 'HOLD'
    return 'SEND'

def build(r):
    email = (r.get('Work Email') or '').strip()
    c = COPY[email.lower()] if email.lower() in COPY else COPY[email]
    full = (r.get('Combined Full Name') or '').strip()
    first = (r.get('Combined First Names') or '').strip()
    last = full[len(first):].strip() if full.lower().startswith(first.lower()) else ''
    # a competitor row carries no link and offers a walkthrough instead
    cta = 'walkthrough' if 'mecartworks.com' not in (c['e1'] + c['e2'] + c['e3']).lower() else 'link'
    return {
        'email': email,
        'first_name': first,
        'last_name': last,
        'company_name': (r.get('company') or '').strip(),
        'website': (r.get('website') or '').strip(),
        'msg_subject_one': c['s1'], 'msg_touch_one': c['e1'],
        'msg_subject_two': c['s2'], 'msg_touch_two': c['e2'],
        'msg_subject_three': c['s3'], 'msg_touch_three': c['e3'],
        'dm_job_title': (r.get('Title People') or r.get('Jobtitle People') or '').strip(),
        'msg_segment': (r.get('niche') or '').strip()[:40],
        'msg_cta_type': cta,
    }

def reason(r, g):
    if g == 'SEND': return 'cleared: audit passed, revenue gate passed, email domain matches'
    if revenue_fails(r['Annual Revenue']):
        return f"revenue {r['Annual Revenue']} is under the $1M gate (S7.4). Verify before sending"
    if r['_verdict'] == 'PARKED':
        return 'parked niche. Abdullah has not confirmed the engine renders rugs or stained glass'
    if r['_verdict'] == 'DROP':
        return 'outside the S7.4 ICP. Copy written on request. Decide deliberately before sending'
    if r['_verdict'] == 'RECHECK': return 'site was mid rebuild at audit. Re-check before sending'
    return 'held'

send, hold, allrows = [], [], []
for r in rows:
    email = (r.get('Work Email') or '').strip().lower()
    if email not in COPY:
        continue
    g = gate(r)
    d = build(r)
    if g == 'SEND':   send.append(d)
    elif g == 'HOLD': hold.append(d)
    allrows.append({**d, 'send_gate': g, 'gate_reason': reason(r, g)})

def write(path, data, headers=HEADERS):
    with open(path, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=headers, quoting=csv.QUOTE_ALL)
        w.writeheader(); w.writerows(data)
    print(f'{path}: {len(data)} rows')

write('MEC_Instantly_Upload.csv', send)
write('MEC_Instantly_Hold.csv', hold)
write('MEC_Instantly_All46.csv', allrows, HEADERS_ALL)

print(f'\nheaders ({len(HEADERS)}): ' + ', '.join(HEADERS))
print('\nCTA split in the send file:')
from collections import Counter
for k, v in Counter(d['msg_cta_type'] for d in send).items():
    print(f'  {k:<12} {v}')
