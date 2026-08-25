#!/usr/bin/env python3
"""Fold Claygent batches 1-4 back into the warm-shortlist export.

Produces MEC_Warm_Shortlist_AUDITED.csv: every row carries its audit verdict,
visual-tool level, send priority and the reason, with the known data errors
corrected in the data rather than only in the notes.
"""
import pandas as pd

SRC = '3aea7153-MEC_Warm_Shortlist_SeedDefaultviewexport1787598276390.csv'
OUT = 'MEC_Warm_Shortlist_AUDITED.csv'

# row -> (verdict, visual_tool, priority, batch, note)
# verdict: KEEP / DROP / PARKED / RECHECK / FLAG
# priority: 1 lead, 2 core, 3 low, - not sendable
A = {
 1:  ('KEEP','Basic',2,1,'Upload-your-own mural; POD, in scope post-pivot'),
 2:  ('KEEP','Basic',2,1,'Clay-completed row'),
 3:  ('KEEP','Basic',2,1,'Custom murals, upload custom wallpaper'),
 4:  ('KEEP','Basic',2,4,'RE-RUN visual tool. White-label dropship programme = clearest pivot test'),
 5:  ('KEEP','Basic',2,1,'Bespoke; RAL colour picker; named hotel projects'),
 6:  ('KEEP','None',1,1,'Bespoke Design Service to professionals; zero tooling'),
 7:  ('KEEP','None',2,1,'Personalizzazione prodotti; su misura; zero tooling'),
 8:  ('KEEP','Advanced',3,1,'Has Real Wall + Live Room configurators already'),
 9:  ('KEEP','Basic',2,1,'Create a Mosaic bespoke service; Ritz-Carlton in footer'),
 10: ('KEEP','None',2,4,'Free design consultation = manual loop. Dedupe target of row 56'),
 11: ('KEEP','None',1,4,'Advertises staffed step-by-step custom loop. Revenue blank - verify'),
 12: ('KEEP','None',1,4,'STRONGEST BATCH 4. Human rendering loop, 100+ artisans, $10-25M'),
 13: ('KEEP','Basic',2,2,'Custom mosaic murals, uncut custom tile design'),
 14: ('KEEP','None',2,4,'Country corrected GB->US. Daltile/distributor channel caveat'),
 15: ('KEEP','Basic',2,2,'Tailored To bespoke customization program'),
 16: ('KEEP','None',2,2,'Bespoke pool ceramics; legit rebrand to cbdpools.com'),
 17: ('KEEP','None',2,2,'Soluzioni su misura; named venue proof'),
 18: ('KEEP','Advanced',3,2,'Bisazza App configurator exists. Country=Italy not VI'),
 19: ('KEEP','Advanced',3,2,'Mosaic Visualizer + Faucet Configurator already built'),
 20: ('KEEP','Basic',2,2,'Modular collections; shop by colour/shape'),
 21: ('KEEP','None',1,2,'Tabarka: 2-10 staff but $5-10M - the headcount lesson row'),
 22: ('KEEP','Basic',2,2,'Mosaic customization program; Scotiabank, The Mark Hotel'),
 23: ('KEEP','Basic',2,2,'Create Your Blend; Whitney Museum commission'),
 24: ('KEEP','Basic',2,2,'Project Tile layout planner at projects.motawi.com'),
 25: ('KEEP','Basic',2,2,'Custom Work category; InLine Design Cards'),
 26: ('KEEP','None',1,4,'Static http site, zero tooling. State Capitols, Harvard, Hoover Dam'),
 27: ('KEEP','None',3,4,'RE-RUN. Dealer-channel boundary case. Revenue band inflated'),
 28: ('KEEP','None',2,2,'Customize your own glaze colour; Geremia Design proof'),
 29: ('FLAG','None',3,2,'Custom offering unclear - no configurable pattern evidence'),
 30: ('KEEP','None',2,2,'Victorian patterns, specialty glazing; City of New Orleans since 2003'),
 31: ('KEEP','None',2,2,'Handmade art tile, orders accepted'),
 32: ('KEEP','Basic',2,2,'Custom Projects; David Heide Design Studio'),
 33: ('FLAG','None',3,2,'One-person studio - likely fails $1M gate, verify'),
 34: ('KEEP','None',2,4,'Custom design services; 100-piece minimum. Verify revenue'),
 35: ('KEEP','None',2,2,'19 design collections for customization'),
 36: ('KEEP','Basic',2,2,'Limited run philosophy; Joanna Gaines project'),
 37: ('KEEP','Advanced',3,2,'Concrete + Zellige simulators - strongest prior tool find'),
 38: ('KEEP','Basic',2,2,'Custom Tile and Custom Murals. HOOK weak - re-pull'),
 39: ('PARKED','Advanced',3,4,'Custom Rug Designer portal live. Bespoke path is the only gap'),
 40: ('PARKED','Basic',2,2,'Any size/shape/colour custom rug programme'),
 41: ('PARKED','Advanced','-',4,'Already has the product. Deprioritise even if rugs unpark'),
 42: ('PARKED','Basic',3,4,'RE-RUN. Sells cheap custom - licence must argue margin not speed'),
 43: ('PARKED','Advanced',3,4,'CORRECTED Basic->Advanced. Customizer w/ real-time preview exists'),
 44: ('PARKED','None',1,3,'Judson: best stained-glass row. Gensler, Hilton, Ace partners'),
 45: ('PARKED','None',1,4,'Largest stained-glass prospect, $10-25M, 15,000 buildings'),
 46: ('PARKED','Basic',3,3,'Franklin: revenue is majority retail supply. Low priority'),
 47: ('DROP','Basic','-',3,'One-person, teaching-led. Fails $1M gate + teaching exclusion'),
 48: ('DROP','Basic','-',3,'One-person studio. Same two failures as row 47'),
 49: ('KEEP','Basic',1,3,'Built a set builder for dinnerware but NOT tile - that gap is the pitch'),
 50: ('KEEP','None',2,3,'HOOK is off-site press - re-pull on-site before send'),
 51: ('FLAG','Basic',3,3,'Zia: catalog-only boundary case. Decide the rule here'),
 52: ('KEEP','Basic',1,3,'Custom printed any size; in-house print team; designer-facing'),
 53: ('DROP','None','-',3,'Signage/print shop. Wrong buyer, wrong workflow'),
 54: ('KEEP','None',1,3,'Trade-only + upload-your-own + ZERO tooling. Best gap-to-need ratio'),
 55: ('DROP','N/A','-',1,'Mosaic Studio UK - DNS dead. Resolves the FLAGGED item in S7.5'),
 56: ('DROP','N/A','-',3,'Duplicate of row 10 - delete on import'),
 57: ('KEEP','Basic',1,3,'Joomla on plain http = no internal tooling. Rebrand is a dated reason'),
 58: ('KEEP','Basic',2,3,'UAE Tier 1. Revenue unverified - manual review'),
 59: ('RECHECK','None','-',3,'Site mid-rebuild. Re-check ~8 Sept 2026; rebuild is a buying signal'),
 60: ('DROP','N/A','-',4,'Inaccessible 404. Fails $1M gate. Cambridge not Staffordshire'),
}

df = pd.read_csv(SRC)
blank = df['Use AI Site Match'].isna()
df.loc[blank, 'audit_row'] = range(1, int(blank.sum()) + 1)

for col, idx in [('audit_verdict',0), ('audit_visual_tool',1),
                 ('audit_priority',2), ('audit_batch',3), ('audit_note',4)]:
    df[col] = df['audit_row'].map(lambda r: A[int(r)][idx] if pd.notna(r) and int(r) in A else '')

# --- data corrections carried in the data, not just the notes ---
def fix(rownum, col, val):
    m = df['audit_row'] == rownum
    df.loc[m, col] = val

fix(14, 'Country', 'US')                 # Carlsbad CA, not GB/Banbury - 3rd flag
fix(14, 'Locality', 'Carlsbad, CA')
fix(18, 'Country', 'IT')                 # VI = Vicenza province, not Virgin Islands
fix(26, 'Locality', 'St. Paul, MN')
fix(27, 'Annual Revenue', '10M-25M')     # D&B/Zippia peak $10.6M; Clay band inflated
fix(60, 'Country', 'GB')

df['audit_priority'] = df['audit_priority'].astype(str)
df.to_csv(OUT, index=False)

# --- reporting ---
aud = df[df['audit_row'].notna()]
print(f'Total rows in file: {len(df)}   audited: {len(aud)}   Clay-completed: {(~blank).sum()}')
print('\nVERDICTS')
print(aud['audit_verdict'].value_counts().to_string())
print('\nSENDABLE NOW (active niches, KEEP)')
send = aud[aud.audit_verdict == 'KEEP']
print(f'  {len(send)} companies')
for p in ['1', '2', '3']:
    n = (send.audit_priority == p).sum()
    print(f'  priority {p}: {n}')
print('\nPRIORITY 1 - LEAD WITH THESE')
for _, r in send[send.audit_priority == '1'].iterrows():
    print(f"  {int(r.audit_row):>2}. {r.company:<28} {str(r['Annual Revenue']):<10} {r.audit_note}")
print('\nPARKED (await Abdullah on rendering fit)')
pk = aud[aud.audit_verdict == 'PARKED']
print(f'  {len(pk)}:', ', '.join(pk.company.astype(str)))
print('\nDROP / FLAG / RECHECK')
for v in ['DROP', 'FLAG', 'RECHECK']:
    s = aud[aud.audit_verdict == v]
    print(f'  {v} ({len(s)}):', ', '.join(s.company.astype(str)))
print('\nVISUAL TOOL DISTRIBUTION (audited rows)')
print(aud['audit_visual_tool'].value_counts().to_string())
print('\nAdvanced-tool rows (already own a configurator):')
for _, r in aud[aud.audit_visual_tool == 'Advanced'].iterrows():
    print(f"  {int(r.audit_row):>2}. {r.company}")
print(f'\nWritten -> {OUT}')
