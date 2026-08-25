# -*- coding: utf-8 -*-
"""Build the outreach-ready workbook: the audited Clay export + per-prospect copy.

Sheet 1 "Outreach"  — every row, with 3 subject lines + 3 email bodies added.
Sheet 2 "Send List" — just the rows cleared to send, in priority order.
Sheet 3 "Excluded"  — rows deliberately left without copy, and why.
"""
import csv
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import copy_data

SRC   = 'MEC_Warm_Shortlist_FILLED.csv'
AUD   = 'MEC_Warm_Shortlist_AUDITED.csv'
OUT   = 'MEC_Outreach_Ready.xlsx'
COPY  = copy_data.COPY

HEAD_FILL = PatternFill('solid', fgColor='0D6E79')
HEAD_FONT = Font(name='Arial', size=10, bold=True, color='FFFFFF')
BASE      = Font(name='Arial', size=10)
MONO      = Font(name='Arial', size=9)
BOLD      = Font(name='Arial', size=10, bold=True)
THIN      = Side(style='thin', color='D6DCDE')
BORDER    = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
FILL_SEND = PatternFill('solid', fgColor='E2F1E8')   # green  — clear to send
FILL_HOLD = PatternFill('solid', fgColor='FDF3DC')   # amber  — written, do not send yet
FILL_STOP = PatternFill('solid', fgColor='F8E4DC')   # clay   — no copy written

rows = list(csv.DictReader(open(SRC, encoding='utf-8')))
aud  = list(csv.DictReader(open(AUD, encoding='utf-8')))
for r, a in zip(rows, aud):                       # positional: survives the Mosaics Lab dupe
    r['_verdict']  = a['audit_verdict']
    r['_priority'] = a['audit_priority']
    r['_note']     = a['audit_note']

def revenue_fails(v):
    return (v or '').strip() in ('0-500K', '500K-1M')

def status_for(r):
    """Why this row can or cannot be sent. Copy exists only for SEND and HOLD rows."""
    email = (r.get('Work Email') or '').strip()
    if not email:
        return 'NO EMAIL', 'No work email on this row — LinkedIn or enrichment needed'
    if r['_verdict'] == 'DROP':
        return 'EXCLUDED', f"Audit verdict DROP — {r['_note']}"
    dom = (r.get('Domain') or '').lower().replace('www.', '')
    edom = email.split('@')[-1].lower()
    if dom and edom and edom != dom and edom.split('.')[0] != dom.split('.')[0]:
        return 'EXCLUDED', f'Email domain ({edom}) does not match company domain ({dom}) — wrong-person risk'
    if revenue_fails(r['Annual Revenue']):
        return 'HOLD - REVENUE', f"Revenue {r['Annual Revenue']} is below the $1M gate (S7.4) — verify before sending"
    if r['_verdict'] == 'PARKED':
        return 'HOLD - PARKED', 'Parked niche (rugs / stained glass) — needs Abdullah on rendering fit before send'
    if r['_verdict'] == 'RECHECK':
        return 'HOLD - RECHECK', r['_note']
    return 'SEND', 'Cleared: audit KEEP/FLAG, revenue gate passed, email domain matches'

NEWCOLS = ['send_status', 'send_note',
           'email_1_subject', 'email_1_body',
           'email_2_subject', 'email_2_body',
           'email_3_subject', 'email_3_body']

for r in rows:
    st, note = status_for(r)
    r['send_status'], r['send_note'] = st, note
    c = COPY.get((r.get('Work Email') or '').strip().lower()) or COPY.get((r.get('Work Email') or '').strip())
    for i, k in enumerate(('s1', 's2', 's3'), 1):
        r[f'email_{i}_subject'] = c[k] if c else ''
    for i, k in enumerate(('e1', 'e2', 'e3'), 1):
        r[f'email_{i}_body'] = c[k] if c else ''

src_cols = list(csv.DictReader(open(SRC, encoding='utf-8')).fieldnames)
wb = Workbook()

# ── narrow, human-readable column set for the working sheets ──
KEY = ['company', 'Work Email', 'Combined Full Name', 'Title People', 'niche',
       'Annual Revenue', 'Country', 'Website']

def write_sheet(ws, data, cols, widths, wrap_cols=()):
    ws.append(cols)
    for j, c in enumerate(cols, 1):
        cell = ws.cell(row=1, column=j)
        cell.fill, cell.font = HEAD_FILL, HEAD_FONT
        cell.alignment = Alignment(vertical='center', wrap_text=True)
        ws.column_dimensions[get_column_letter(j)].width = widths.get(c, 18)
    ws.row_dimensions[1].height = 30
    for r in data:
        ws.append([r.get(c, '') for c in cols])
        i = ws.max_row
        fill = (FILL_SEND if r['send_status'] == 'SEND'
                else FILL_STOP if r['send_status'] in ('EXCLUDED', 'NO EMAIL')
                else FILL_HOLD)
        for j, c in enumerate(cols, 1):
            cell = ws.cell(row=i, column=j)
            cell.font = MONO if c.endswith('_body') else BASE
            cell.border = BORDER
            cell.alignment = Alignment(vertical='top',
                                       wrap_text=(c in wrap_cols or c.endswith('_body') or c.endswith('_subject')))
            if c == 'send_status':
                cell.fill = fill
                cell.font = BOLD
        ws.row_dimensions[i].height = 92 if any(r.get(c) for c in cols if c.endswith('_body')) else 18
    ws.freeze_panes = 'B2'
    ws.auto_filter.ref = ws.dimensions

W = {'company': 26, 'Work Email': 30, 'Combined Full Name': 20, 'Title People': 24,
     'niche': 20, 'Annual Revenue': 13, 'Country': 8, 'Website': 26,
     'send_status': 15, 'send_note': 44,
     'email_1_subject': 30, 'email_2_subject': 30, 'email_3_subject': 30,
     'email_1_body': 68, 'email_2_body': 68, 'email_3_body': 68}

# Sheet 1 — everything, all original columns preserved, copy appended
ws1 = wb.active; ws1.title = 'Outreach'
write_sheet(ws1, rows, src_cols + NEWCOLS, W, wrap_cols=('send_note',))

# Sheet 2 — the send list only
send = [r for r in rows if r['send_status'] == 'SEND']
send.sort(key=lambda r: (r['_priority'] or '9', r['company']))
ws2 = wb.create_sheet('Send List')
write_sheet(ws2, send, KEY + NEWCOLS, W, wrap_cols=('send_note',))

# Sheet 3 — held and excluded, with the reason
rest = [r for r in rows if r['send_status'] != 'SEND']
rest.sort(key=lambda r: (r['send_status'], r['company']))
ws3 = wb.create_sheet('Held & Excluded')
write_sheet(ws3, rest, KEY + ['send_status', 'send_note'], W, wrap_cols=('send_note',))

wb.save(OUT)

from collections import Counter
c = Counter(r['send_status'] for r in rows)
print(f'{OUT}\n  sheets: Outreach ({len(rows)}) · Send List ({len(send)}) · Held & Excluded ({len(rest)})')
print(f'  columns: {len(src_cols)} original + {len(NEWCOLS)} new = {len(src_cols)+len(NEWCOLS)}')
for k, v in c.most_common():
    print(f'  {k:<16} {v}')
wrote = sum(1 for r in rows if r['email_1_body'])
print(f'  rows carrying copy: {wrote}')
