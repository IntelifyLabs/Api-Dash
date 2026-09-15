# Who to find, and how many — wave 2 DM discovery

## Two flags before you run it

**1. This changes a rule Abdullah set explicitly.** §7.1 and §7.4 both record
"one contact per company, no generic company inboxes — Abdullah was explicit."
Moving to 2–3 contacts per company is the right call for this product, but
standing rule 12 says internal stakeholders get coordinated before a pivot.
Tell him; don't ask permission, just don't let him find out from a reply.

**2. Multi-threading on email is a deliverability risk, not just a volume one.**
Two or three messages into the same domain, from a 3-week-old mailbox on
`.space`/`.site`, with similar content, is a textbook spam cluster. Campaign 2
already has an unresolved "strong opens, zero replies" that §4 flags as
possibly deliverability. So:
  - **person 1 by email, persons 2 and 3 by LinkedIn** (Shahwaz's account,
    which per §2 is still completely unused and needs no warm-up), or
  - if all three go by email, **stagger 3–4 days apart** and never send the
    same body twice into one domain.

---

## The three jobs to be done

A white-label design tool on a manufacturer's own site has three buyers, and
they care about completely different things:

| Job | Who | What they actually care about |
|---|---|---|
| **Owns the website and conversion** | Marketing / Ecommerce / Digital | sample requests, time on site, enquiry quality, cart abandonment |
| **Owns the catalogue and the design loop** | Creative / Design / Product Dev / Ufficio Tecnico | the sample book, the CAD mock-up, the glaze trial, revision rounds |
| **Signs** | Owner / Founder / MD / GM / Export Manager | revenue, the client who walks during the wait, competitive parity |

A fourth, specific to this vertical and usually missed: **trade / contract /
specification manager**. §7.4 calls a trade programme "the strongest single
free indicator" of an approval bottleneck, and that person owns it.

---

## By size band

### Under 30 employees — 153 rows
The owner designs, quotes and pays. There is nobody else to convince.
- **P1** Owner · Founder · Co-Founder · Proprietor · Titolare · Propietario
- **P2** Creative Director · Design Director · Studio Director *(often the
  founding partner)*
- **P3** whoever does marketing — frequently one part-time person

**Expect 1–2 people to exist, not 3. Do not force a third.** On this band a
found owner is worth more than three found juniors.

### 30–200 employees — 119 rows · THE SWEET SPOT
All three roles exist, are separate, and are findable. Multi-thread properly.
- **P1** Marketing Manager · Head of Marketing · Ecommerce Manager ·
  Digital Marketing Manager · Marketing & Communications Manager
- **P2** Creative Director · Product Development Manager · Design Manager ·
  R&D Manager · Head of Product
- **P3** CEO · Managing Director · General Manager · Commercial Director ·
  **Export Manager** *(on European makers the export manager often holds real
  commercial authority for a market — do not skip them)*

### 200+ employees — 109 rows · DEPRIORITISED
Tag and park per §7.4. If you do touch them:
- **P1** Head of Digital · Digital Transformation Lead · Ecommerce Director
- **P2** Head of Design · Creative Director · Product Marketing Manager
- **Never the CEO.** They will not read it, and asking signals you do not
  understand how their organisation buys. Expect procurement and a long cycle.

### Blank size — 42 rows
Default to the under-30 playbook (owner first). Artisan makers with small teams
are exactly the rows most likely to have thin firmographic data.

---

## Titles to EXCLUDE — these waste credits and burn the domain

HR · Finance · Accounting · Controlling · Logistics · Warehouse · Purchasing ·
Quality · Production Manager · Plant Manager · Health & Safety · Maintenance ·
Area Sales Rep · Sales Representative · Technician · Installer · Receptionist

Two that look right and are not:
- **IT Manager** — they implement, they do not buy. Useful later in the deal,
  wrong for first touch.
- **Any generic inbox** (info@, sales@, ventas@, commerciale@). Abdullah was
  explicit, and they do not convert.

---

## Local-language titles — 60%+ of this list is not anglophone

Clay's people search matches on title text, so search the local terms too.

| | Owner / MD | Marketing | Design / Product | Commercial / Export |
|---|---|---|---|---|
| **Italian** | Titolare · Amministratore Delegato · Presidente | Responsabile Marketing · Direttore Marketing | Direttore Creativo · Ufficio Tecnico · Responsabile Prodotto | Direttore Commerciale · Export Manager |
| **Spanish** | Propietario · Director General · Gerente | Director/Responsable de Marketing | Director Creativo · Jefe de Producto | Director Comercial · Export Manager |
| **German** | Inhaber · Geschäftsführer | Marketingleiter | Produktmanager · Designleiter | Vertriebsleiter · Exportleiter |
| **Turkish** | Genel Müdür · Kurucu | Pazarlama Müdürü | Ürün Müdürü | İhracat Müdürü |
| **Portuguese** | Proprietário · Director Geral | Director de Marketing | Director Criativo | Director Comercial |

---

## Which person leads, decided by the tool research

This is the payoff from qualifier 1 — `tool_level` tells you who to open with.

| tool_level | Lead with | Because |
|---|---|---|
| **MANUAL** (17 rows) | **Design / Product** | They are the one losing hours to CAD mock-ups, posted sample books and glaze trials. Rookwood's designers draw it in CAD; McIntyre fires test glazes. That is their week, not marketing's |
| **NONE / unconfirmed** | **Marketing / Ecommerce** | It is a site capability gap and a competitive-parity argument. Their number moves |
| **BASIC** | **Marketing / Ecommerce** | They already believe in online choosing and stopped at filters |
| **has_tryon=yes, has_prompt=no** | **Digital / Ecommerce** | They already bought a visualiser, so budget and intent are proven. They own the roadmap for the half they are missing |
| **ADVANCED both halves** | park | Competitor, or nothing left to sell |

---

## The rule that makes multi-threading work instead of backfiring

**Each person gets a different angle, never the same email.** Three copies of
one message into one company is the fastest way to look like mass mail and lose
the whole account.

- Marketing hears: *samples requested, enquiries that go quiet, the drop-off
  between "I like this" and "I'll order it"*
- Design hears: *the mock-up, the sample book, the revision round, the wait*
- Owner hears: *the client who walks during that wait, and the competitor who
  already has the tool*

Same company, same product, three different problems. That is also why
multi-threading is defensible here rather than lazy — the three genuinely do
not share a pain.

---

## Clay configuration

Run on the capped list, not all 423. Suggested cap: revenue ≥$1M, under 200
employees, ranked by tool_level → roughly 80 companies → ~160–200 people.

- Enable **both** people searches. §7.7's note stands: "Find people at company"
  fails on a third of artisan rows and "Find people at company (SMB)" rescues
  most of them. Reading only the first column overstates the gap five-fold.
- Cap at **3 people per company**, and let rows return 1 or 2 rather than
  padding with juniors.
- Keep the **right_person_check** formula (§7.7 step 9): email domain must
  match company domain. Wave 1 lost 6 rows in Campaign 1 to this.
- Email waterfall **only** where a DM was found and email is blank. It is the
  most expensive column in the architecture.
