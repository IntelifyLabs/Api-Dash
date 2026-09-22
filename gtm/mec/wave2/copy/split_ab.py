# -*- coding: utf-8 -*-
"""Split the master file into the two A/B upload files.

Instantly's own A/B feature cannot run this test. It randomises between two
step variants typed into the UI, but every row here carries its own body, so
there is nothing to type. The split has to happen in the data instead: two
campaigns, one per arm, each with its audience already decided.

Only `send` rows are written. The 84 HOLD rows sell taps, radiators, doors and
bathroom furniture, which Showhouse has no studio for, and putting them in
either arm would add noise to both.
"""
import csv

SRC = 'MEC_Instantly_Wave2.csv'
rows = [r for r in csv.DictReader(open(SRC, encoding='utf-8-sig'))
        if r['qa_send_flag'] == 'send']
cols = list(rows[0])

for arm, letter, name in (('R revenue', 'R', 'MEC_Instantly_ArmR_revenue.csv'),
                          ('C cost',    'C', 'MEC_Instantly_ArmC_cost.csv')):
    sel = [r for r in rows if r['ab_arm'] == arm]
    with open(name, 'w', newline='', encoding='utf-8-sig') as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(sel)
    print(f'{name:36} {len(sel):3} contacts, '
          f'{len({r["company_name"] for r in sel})} companies')
