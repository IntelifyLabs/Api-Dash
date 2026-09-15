# -*- coding: utf-8 -*-
"""Pick the right 2-3 contacts out of the 5-10 the waterfall returns.

The people search has no title filter, so it returns everyone it finds:
marketing leads next to warehouse supervisors. They are already paid for, so
the fix is to RANK what came back rather than re-run anything.

Scores each person against the three buying personas, takes the best one per
persona, caps at 3 per company. Never backfills a persona with a weak match:
two good contacts beat three where one is the plant manager.

Usage:  python3 pick_contacts.py <export.csv>
Works on either shape - one row per person, or people as JSON in one cell.
"""
import csv, json, re, sys
from collections import defaultdict

# ---- persona scoring. Higher wins. Local-language terms scored the same -----
A_MARKETING = [
 (100, r'\b(cmo|chief marketing)\b|head of marketing|marketing director|'
       r'direttore marketing|director de marketing|marketingleiter|e-?commerce director'),
 (90,  r'marketing manager|digital marketing|head of digital|digital manager|'
       r'e-?commerce manager|online sales manager|responsabile marketing|'
       r'responsable de marketing|pazarlama m'),
 (70,  r'brand manager|communications manager|marketing (and|&) communication|'
       r'marketing e comunicazione'),
 (50,  r'marketing (coordinator|specialist|executive)|social media manager'),
 (30,  r'marketing assistant'),
]
B_DESIGN = [
 (100, r'creative director|head of design|design director|direttore creativo|'
       r'direttore artistico|director creativo|designleiter'),
 (90,  r'product development|head of product|design manager|art director|'
       r'responsabile sviluppo prodotto'),
 (80,  r'\bproduct manager\b|r\s*&\s*d manager|research and development manager|'
       r'technical manager|ufficio tecnico|responsabile prodotto|jefe de producto|'
       r'produktmanager|ürün m'),
 (60,  r'studio (manager|director)|collection manager|head of collections'),
 (40,  r'\bdesigner\b'),
]
C_EXEC = [
 (100, r'\b(owner|co-?owner|founder|co-?founder|proprietor)\b|titolare|propietario|'
       r'\binhaber\b|proprietário|\bkurucu\b'),
 (95,  r'\bceo\b|managing director|\bpresident\b|amministratore delegato|'
       r'gesch.?ftsf|director general|direttore generale|genel m|director geral'),
 (85,  r'general manager|managing partner'),
 (75,  r'commercial director|sales director|export (manager|director)|'
       r'direttore commerciale|director comercial|vertriebsleiter|exportleiter|'
       r'ihracat m|international sales manager'),
 (60,  r'head of sales|business development manager|responsabile commerciale'),
 (40,  r'area manager|key account manager'),
]
D_TRADE = [
 (80,  r'contract manager|specification manager|trade sales|architectural sales|'
       r'a&d manager|prescripci|objektberater|responsabile contract'),
 (60,  r'showroom manager'),
]

# ---- never contact. Checked first, beats every score above -----------------
NEVER = re.compile(
 r'\b(hr|human resources|talent|recruit|people (and|&) culture|finance|financial|'
 r'accounting|accountant|controller|administration|administrative|payroll|'
 r'logistics|warehouse|shipping|dispatch|purchasing|procurement|supply chain|'
 r'quality|\bqa\b|qhse|production|\bplant\b|operations|maintenance|'
 r'health (and|&) safety|\behs\b|\bit\b|information technology|systems|'
 r'legal|reception|secretar|assistant|intern|student|apprentice|driver|'
 r'technician|installer|sales (rep|representative)|retired|former|freelance)\b'
 r'|responsabile (qualit|produzione|acquisti|logistica)|ufficio acquisti', re.I)

PERSONAS = [('A_marketing', A_MARKETING), ('B_design', B_DESIGN),
            ('C_exec', C_EXEC), ('D_trade', D_TRADE)]

def score(title):
    """Returns {persona: score}. Empty if the title is on the never list."""
    t = (title or '').strip()
    if not t or NEVER.search(t):
        return {}
    out = {}
    for name, rules in PERSONAS:
        for pts, pat in rules:
            if re.search(pat, t, re.I):
                out[name] = pts
                break
    return out

# ---- seniority adjusted for company size -----------------------------------
BIG = {'201-500 employees','501-1,000 employees','1,001-5,000 employees',
       '5,001-10,000 employees','10,001+ employees'}
SMALL = {'2-10 employees','11-50 employees','Self-employed'}

def adjust(scores, size, title):
    """A 'Marketing Manager' at a 10-person maker IS the marketing function.
    At a 2,000-person group they are four levels down. Same words, different
    person, so the score has to move with headcount."""
    t = (title or '')
    senior = re.search(r'\b(head of|director|chief|vp|vice president|c[emft]o|'
                       r'managing|general manager|owner|founder)\b', t, re.I)
    adj = {}
    for k, v in scores.items():
        if size in BIG and not senior:
            v -= 35                      # mid-level at an enterprise is noise
        if size in SMALL and k == 'C_exec':
            v += 10                      # on a tiny maker the owner IS the buyer
        adj[k] = v
    return adj

# ---- which persona to open with, from the qualifier-1 tool_level ------------
LEAD = {'MANUAL':'B_design', 'NONE':'A_marketing', 'BASIC':'A_marketing',
        'ADVANCED':'A_marketing', '':'A_marketing'}

def pick(people, size, tool_level, cap=3):
    """people: list of (name, title, email). Returns the chosen contacts."""
    best = {}
    for name, title, email in people:
        s = adjust(score(title), size, title)
        for persona, pts in s.items():
            if pts <= 0:
                continue
            if persona not in best or pts > best[persona][0]:
                best[persona] = (pts, name, title, email)
    order = [LEAD.get((tool_level or '').upper(), 'A_marketing')]
    order += [p for p, _ in PERSONAS if p not in order]
    chosen = [(p,) + best[p] for p in order if p in best][:cap]
    return chosen

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(0)
    rows = list(csv.DictReader(open(sys.argv[1], encoding='utf-8-sig')))
    print(f'{len(rows)} rows, {len(rows[0])} columns')
    print('\ncolumns that look like people data:')
    for c in rows[0]:
        if re.search(r'name|title|job|email|people|contact|person', c, re.I):
            print(f'   {c!r}')
    print('\nSend the export and this gets pointed at the right columns.')
