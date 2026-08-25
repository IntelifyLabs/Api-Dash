#!/usr/bin/env python3
"""Fill the 60 blank audit rows in the Clay export from batches 1-4.

Writes into the native Clay columns (Use AI Site Match / Custom Offering /
Visual Tool / Hook / Client Proof) in Clay's own line format. The 7 rows Clay
already completed are left byte-for-byte untouched, as is every other column.
"""
import csv, re, sys

SRC = 'new_export.csv'
OUT = 'MEC_Warm_Shortlist_FILLED.csv'

BATCHES = [
    ('8e69f770-MEC_Claygent_Results.md', 1),
    ('d2419c3d-MEC_Claygent_batch2.md', 2),
    ('012b144c-MEC_Claygent_batch3.md', 3),
]
PASTEBACK = 'MEC_Claygent_batch4_pasteback.txt'

LABELS = ['SITE_MATCH', 'CUSTOM_OFFERING', 'VISUAL_TOOL', 'HOOK', 'CLIENT_PROOF']

def parse_md(path):
    """Pull `### N. ...` blocks and their 5 labelled lines out of a batch doc."""
    out = {}
    cur = None
    for line in open(path, encoding='utf-8'):
        line = line.rstrip('\n')
        m = re.match(r'^###\s+(\d+)\.', line)
        if m:
            cur = int(m.group(1))
            out.setdefault(cur, {})
            continue
        if line.startswith('##') or line.startswith('==='):
            cur = None                          # leave the row blocks; stop collecting
        if cur is None:
            continue
        for lab in LABELS:
            if line.startswith(lab + ':'):
                out[cur][lab] = line.strip()
    return out

def parse_pasteback(path):
    """Batch 4 strict-format blocks: `--- ROW N — ... ---` then 5 labelled lines."""
    out = {}
    cur = None
    for line in open(path, encoding='utf-8'):
        line = line.rstrip('\n')
        m = re.match(r'^---\s+ROW\s+(\d+)\s+', line)
        if m:
            cur = int(m.group(1))
            out.setdefault(cur, {})
            continue
        # The correction section at the end of the file carries its own
        # VISUAL_TOOL line; without this it would land on the last ROW parsed.
        if line.startswith('==='):
            cur = None
        if cur is None:
            continue
        for lab in LABELS:
            if line.startswith(lab + ':'):
                out[cur][lab] = line.strip()
    return out

findings = {}
for path, n in BATCHES:
    got = parse_md(path)
    findings.update({k: v for k, v in got.items() if v})
    print(f'batch {n}: {sum(1 for v in got.values() if v)} rows with fields')

b4 = parse_pasteback(PASTEBACK)
print(f'batch 4: {len(b4)} rows with fields (supersedes the BLOCKED placeholders)')
findings.update(b4)

# Row 59 Bigmural: batch 3 wrote CUSTOM_OFFERING/VISUAL_TOOL/CLIENT_PROOF inline on
# one line, so the line-start parser misses them. Its site is a placeholder mid-rebuild,
# which is "Inaccessible" under spec rule 2, so the early-exit rule gives N/A for the
# rest. Keep the RECHECK note in the campaign docs, not in the 5 lines.
findings[59] = {
    'SITE_MATCH': 'SITE_MATCH: Inaccessible — placeholder page, site rebuild in progress',
    'CUSTOM_OFFERING': 'CUSTOM_OFFERING: N/A',
    'VISUAL_TOOL': 'VISUAL_TOOL: N/A',
    'HOOK': 'HOOK: N/A',
    'CLIENT_PROOF': 'CLIENT_PROOF: N/A',
}

# Row 56 is the same company as row 10 (Mosaics Lab), so the findings are identical.
# Fill it rather than leave a hole, and flag the duplication inline so it is visible
# in the sheet without adding a column. Row is kept, not deleted, per instruction.
findings[56] = dict(findings[10])
findings[56]['SITE_MATCH'] = (findings[10]['SITE_MATCH'] +
                              ' [DUPLICATE of row 10 — delete before send]')

# Row 43 Jubi: batch 3 recorded Basic; batch 4 proved an advanced customizer exists.
findings[43]['VISUAL_TOOL'] = ('VISUAL_TOOL: Advanced — online customizer, 1,200 shades, '
                               '"preview and adjust... in real time" — /pages/rug-customizer')

COL = {
    'SITE_MATCH':      'Use AI Site Match',
    'CUSTOM_OFFERING': 'Use AI Custom Offering',
    'VISUAL_TOOL':     'Use AI Visual Tool',
    'HOOK':            'Use AI Hook',
    'CLIENT_PROOF':    'Use AI Client Proof',
}

rows = list(csv.DictReader(open(SRC, encoding='utf-8')))
hdr = list(rows[0].keys())

audit_n = 0
filled = touched_clay = missing = 0
missing_rows = []
for r in rows:
    if r['Use AI Site Match'].strip():          # a row Clay already did
        touched_clay += 1
        continue                                # leave completely alone
    audit_n += 1
    f = findings.get(audit_n)
    if not f:
        missing += 1
        missing_rows.append((audit_n, r['company']))
        continue
    for lab, col in COL.items():
        if lab in f:
            r[col] = f[lab]
    filled += 1

with open(OUT, 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=hdr)
    w.writeheader()
    w.writerows(rows)

print(f'\nClay rows left untouched : {touched_clay}')
print(f'Rows filled from batches : {filled}')
print(f'Rows still blank         : {missing}')
if missing_rows:
    for n, c in missing_rows:
        print(f'   row {n}: {c}')
print(f'\nWritten -> {OUT}')
