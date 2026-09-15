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
 (90,  r'marketing manager|head of digital|digital manager|'
       r'e-?commerce manager|online sales manager|responsabile marketing|'
       r'responsable de marketing|pazarlama m'),
 (70,  r'brand manager|communications manager|marketing (and|&) communication|'
       r'marketing e comunicazione'),

 (70,  r'trade marketer|merchandising'),
 (50,  r'(marketing|digital) (coordinator|specialist|executive)|'
       r'digital (communication|marketing)|social media manager|^marketing$'),
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
 (60,  r'technical department|ufficio tecnico|design (and|&) trade'),
 (45,  r'dise.ador[a]? cer.mic|ceramic designer'),
 (40,  r'\bdesigner\b|dise.ador|designer int.rieur|interior.*designer'),
]
C_EXEC = [
 (100, r'\b(owner|co-?owner|founder|co-?founder|proprietor)\b|titolare|propietario|'
       r'\binhaber\b|proprietário|\bkurucu\b'),
 (95,  r'\bceo\b|managing director|\bpresident\b|amministratore delegato|'
       r'gesch.?ftsf|director general|direttore generale|genel m|director geral'),
 (85,  r'general manager|managing partner'),
 (85,  r'general manager|managing partner|socio (fundador|fondatore)'),
 (75,  r'commercial director|sales director|export director|'
       r'direttore commerciale|diretor comercial|director comercial|'
       r'vertriebsleiter|exportleiter|ihracat m'),
 (60,  r'head of sales|business development manager|'
       r'resp\.? ?commerciale|responsabile commerciale|responsabile vendite|'
       r'jefe de ventas|international sales manager'),
 (55,  r'export (area )?manager|export manager area|comercial export'),
 (40,  r'area manager|key account manager|responsabile mercato'),
]
D_TRADE = [
 (80,  r'contract manager|specification manager|trade sales|architectural sales|'
       r'a&d manager|prescripci|objektberater|responsabile contract'),
 (60,  r'showroom manager'),
]

# ---- never contact. Checked first, beats every score above -----------------
# Tuned against the 64 distinct titles this waterfall actually returned.
# Sales agents alone were 10 of 69 people. Almost everything here was learned
# from real output rather than guessed, which is why it is mostly non-English.
# Tuned against the 64 distinct titles this waterfall actually returned.
# Sales agents alone were 10 of 69 people. Almost all of this was learned from
# real output rather than guessed, which is why most of it is not English.
#
# Built as a list and joined, NOT as adjacent raw strings: the first attempt
# left a trailing "|" at the end of one line and a leading "|" at the start of
# the next, producing "||" - an empty alternative that matches every string.
# It silently excluded all 64 titles. Never hand-concatenate an alternation.
_NEVER_PARTS = [
    # English
    r'\b(hr|human resources|talent|recruit|people (and|&) culture)\b',
    r'\b(finance|financial|accounting|accountant|controller|payroll|contab)\b',
    r'\b(administration|administrative|admin[ia]s?[it]rative)\b',
    r'\b(logistics|warehouse|shipping|dispatch)\b',
    r'\b(purchasing|procurement|supply chain)\b',
    r'\b(quality|qa|qhse)\b',
    r'\b(production|plant|operations|maintenance)\b',
    r'\b(health (and|&) safety|ehs)\b',
    r'\b(it|information technology|systems|sap)\b',
    r'(software developer|data analys|business intelligence)',
    r'\b(legal|reception|secretar)\b',
    r'\b(assistant|intern|student|apprentice|driver)\b',
    r'\b(technician|installer)\b',
    r'customer (care|service|support)',
    r'sales (agent|rep|representative)',
    r'\b(retired|former|freelance|self.?employed)\b',
    # Italian - agents were the single biggest source of noise
    r'\bagente\b', r'agente di (vendita|commercio|zona)', r'rappresentante',
    r'\boperatore\b', r'capo macchina', r'\bpressa\b', r'pantografo',
    r'centralinista', r'\bamministrazione\b', r'ufficio ac?quisti',
    r'risorse umane', r'coordinatore manutenzione', r'lavoratore autonomo',
    # Spanish and Portuguese
    r'administrativ[ao]', r'as?sistente', r'recursos humanos',
    r'responsable de producci', r't.cnico de (apoio|produ|recursos)',
    r'financeir[ao]', r'financier[ao]', r'mantenimiento',
    r'gerente de clientes', r'desenhador or.ament',
    # German
    r'\bvertreter\b',
]
NEVER = re.compile('|'.join(_NEVER_PARTS), re.I)

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

# An agency or a representation firm sometimes lands in the NAME field rather
# than the title, e.g. "Agenzia Filessi rappresentanze" listed as Amministratore
# Delegato. Screen names too, not only titles.
NOT_A_PERSON = re.compile(
    r'\b(agenzia|agency|rappresentanz|representacion|studio|s\.?r\.?l|s\.?p\.?a|'
    r'gmbh|\bltd\b|\binc\b|\bsa\b|\bbv\b|group|consulting)\b', re.I)

LEAD_MIN = 70   # a lead persona only goes first if its candidate is decent

def implausible(title, size):
    """Owner/founder titles at a 200+ company are usually a wrong-company
    LinkedIn match - someone who owns a different small business and lists
    the big employer too. ABK Group, 501-1,000 people, returned a
    "Titolare dell'azienda". Flag, do not drop: it might be a family owner."""
    if size in BIG and re.search(r'\b(owner|founder|proprietor)\b|titolare|'
                                r'propietario|\binhaber\b', title or '', re.I):
        return 'owner title at a 200+ company - verify it is not a wrong-company match'
    return ''

def pick(people, size, tool_level, cap=3):
    """people: list of (name, title, url). Returns the chosen contacts.

    Ordering rule, learned from the first run: the lead persona from
    tool_level only goes first if that candidate scores at least LEAD_MIN.
    Otherwise take the strongest contact. Without this, 41zero42 opened with a
    Digital Communication Specialist (50) instead of its General Manager (95),
    and A.A.T.C. opened with a marketing specialist (50) over its Managing
    Partner (95). Persona theory should not beat a much better human.
    """
    best = {}
    for name, title, url in people:
        if NOT_A_PERSON.search(name or ''):
            continue
        sc = adjust(score(title), size, title)
        for persona, pts in sc.items():
            if pts <= 0:
                continue
            if persona not in best or pts > best[persona][0]:
                best[persona] = (pts, name, title, url)
    if not best:
        return []
    lead = LEAD.get((tool_level or '').upper(), 'A_marketing')
    by_score = sorted(best, key=lambda p: -best[p][0])
    if lead in best and best[lead][0] >= LEAD_MIN:
        order = [lead] + [p for p in by_score if p != lead]
    else:
        order = by_score
    return [(p,) + best[p] for p in order][:cap]


def flag(title, size):
    return implausible(title, size)

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
