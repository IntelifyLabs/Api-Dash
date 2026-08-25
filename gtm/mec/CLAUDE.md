# TRIMINAGE — GTM MASTER STATUS

**Owner:** Shahwaz Hassan, GTM Engineer
**Last updated:** 24 August 2026
**Purpose:** single source of truth for every campaign — what was decided, what was tested, what was learned, and exactly where each workstream stopped.

---

# 0. COMPANY & OFFER

**Triminage** — Columbus, Ohio custom software agency. Senior team, US + Pakistan. Builds AI-powered web and mobile products for healthcare, fintech and SaaS.

**Model:** staff augmentation / embedded senior engineers. This *is* the outbound thesis — health-tech teams hit EMR/EHR integration work, building it in-house pulls senior engineers off core product, Triminage absorbs that load.

**Public pricing (hourly):** Engineering $30 · AI Integrations $40 · Agile Outsourcing & PM $20 · E-commerce $15

**Core differentiator:** HIPAA-compliant healthcare software with EMR/EHR integration — FHIR, HL7, Redox-type work. Plus AI development depth. Together these are the moat against generic AI agencies.

**Stack:** React, Next.js, TypeScript, Node, Python/Django/FastAPI, GraphQL, Postgres/Mongo, HuggingFace, Docker, K8s, GCP, Supabase, Firebase, Stripe.

## Team

| Person | Role |
|---|---|
| Shahwaz Hassan | GTM Engineer — outbound strategy, campaign architecture, list building |
| Haroon | Execution — email sending persona |
| Moeed | Execution |
| Abdullah | Head of Products — internal decision-maker on client-side campaign scope |

## Proof assets — cleared for outreach

**CureMD AI Medical Scribe** — public case study at triminage.com/portfolio/curemd-ai-medical-scribe
Cleared figures: **98% note accuracy · under 15 seconds · 30+ specialties · 24 weeks · 6 people · ICD-10/CPT/RxNorm**

**MEC Artworks AI** — public case study at triminage.com/portfolio/mec-artworks-ai
AI mosaic/pattern design platform, live at ai.mecartworks.com. Recorded as: built in 7 weeks with 3 people, Next.js + AI integration, canvas-based real-time rendering. **No hard performance numbers published** — the "measured results" on the page are qualitative (real-time, seconds, faster).

> ✅ **Re-verified 24 Aug 2026 against the live page.** Confirmed: **7 weeks, team of 3 (AI engineer, developer, designer).** Tech stack: Next.js, AI Integration, Canvas Rendering, Tailwind CSS. Confirmed no hard performance numbers exist — "Measured results" on the page are qualitative only (Real-time / Seconds / Faster). Full copy pulled from the page is safe to quote for outreach: problem framing ("distance between a concept and its first visual representation... closes it to seconds"), dual-audience design brief (design pros need speed/control, clients need to approve without design literacy), and the closing claim "live and in active use by the MEC Artworks team."

**Other named clients:** Floret Capitals, Oktrum (fintech) · DejaThink, Upscribe, Storia (AI/SaaS)

**Headline stats:** 20+ teams shipped for · 10+ products launched · 10+ industries

**Recurring testimonial theme:** clarity of communication, weekly updates, realistic expectations, "we don't have to chase them." Sell reliability and senior communication, not lowest price.

### Honest-proof rule
Never claim results a campaign hasn't produced. Never invent quotes, metrics or case studies. Only publicly confirmed figures go into copy. Where no public case study exists, use "recent builds we can walk through live."

---

# 1. NORTH STAR

Everything serves one goal: **book qualified meetings, convert them into opportunities.**

Funnel to optimise: connection accepts → replies → positive replies → **meetings booked with the technical team** → opportunities.

**Never optimise for:** impressions, followers, or open rates.

**Success definition:** a booked technical call is the primary win. A signed client is the stretch.

---

# 2. INFRASTRUCTURE — CURRENT STATE

## LinkedIn
- Manual outreach from **Shahwaz's personal account**
- Shahmeer's SDR account was **restricted** — caused by using a fresh account. Never repeat this.
- No Sales Navigator
- Pace: 12–15 invites/day, weekdays
- **Status: unused so far.** Campaigns 1 and 2 have run email-only. Full capacity available.

## Email
- Two Instantly mailboxes: **haroon@triminage.space** and **haroon@triminage.site**
- `.space` and `.site` are low-reputation TLDs — a known risk
- Recommendation on record: register a respectable lookalike `.com`, set SPF/DKIM/DMARC, redirect to triminage.com, warm in parallel, A/B at send
- Open tracking **not enabled** — use Instantly's Delivery Optimization instead, given domain reputation risk

### Email go-live gate (all four required)
1. Mailbox age 3+ weeks
2. Warm-up inbox rate >90%
3. SPF/DKIM/DMARC verified
4. Lookalike domains redirect live

If any fail → email waits, LinkedIn continues. One spam-flagged send costs more than two waited weeks.

## Persona bridge
Email comes from **Haroon**, LinkedIn DMs from **Shahwaz**. Every first email must reference the LinkedIn touch — *"my colleague Shahwaz reached out on LinkedIn recently"* — so both names read as one team, not two cold senders.

## Instantly — resolved technical issue
Custom variables must NOT be named like built-ins. `email_subject` and `email_body` **collide with system fields**. Headers must contain no spaces.
**Fix:** use collision-proof headers (`msg_subject_line`, `msg_first_touch`) in a **fresh** campaign, map as Custom variables, insert via the ⚡ icon.

## Clay
- Paid subscription being purchased; second account with credits available
- Previously free plan, ~2,000 credits with a 400-credit reserve rule

### Known Clay behaviours — learned the hard way
| Behaviour | Implication |
|---|---|
| Keyword matching is **semantic, not exact-phrase** | Broader matches than expected |
| `Software Development` industry filter includes agencies | Avoid it |
| AI-related **include** keywords return AI-native companies | Put AI terms in the **exclude** box instead |
| Funding filter **passes through** unknown-funding companies | Doesn't exclude them |
| Exclude Companies feature is paywalled on free plan | Manual dedupe required on free tier |
| Auto-enrichment on import | **Always disable** |

## Python / pandas — QA toolkit
Used for: fill rates, email-domain mismatch detection, duplicate domain detection, contact deduplication.
- CHPL Clay exports require `encoding='latin-1'`
- Domain joins use **normalised keys** — strip `https://`, `www.`, paths, query strings. Never join on company name.

---

# 3. CAMPAIGN 1 — US DIGITAL HEALTH

**Status:** LinkedIn execution phase. Email gated.

## ICP
US digital-health companies, ~Seed–Series A, selling into providers.
**Buyers:** Founders / CEOs / CTOs / COOs

## Sourcing
Primary source: **CHPL / ONC certified health IT data.**

**Key insight:** §170.315(g)(10) certification *guarantees* a live FHIR API. This makes the "do you have an integration method" qualification question redundant — certification answers it.

## List state
File: `DigitalHealthSmallUStriminage__tracked__final.csv`

| Stage | Count | Note |
|---|---|---|
| Companies sourced | 50 | Full company data on all 50 |
| No contact found | −7 | Dropped |
| **Contacts identified** | **43** | DMs written for all 43 |
| Manual drops | −2 | Per plan doc |
| **LinkedIn-sendable** | **41** | |
| Contacts without email | −5 | LinkedIn-only for these |
| **Work emails present** | **38** | |
| Email-domain mismatches | −6 | Must be fixed before send |
| **Clean for email** | **32** | |

*These counts reconcile cleanly — 50 → 43 → 41 → 38 → 32. Earlier confusion about "43 vs 41 vs 50" was a stage mismatch, not a data error.*

## Messaging — rebuilt
The original sequence was replaced with a fully personalised rebuild:
- **106 unique bodies**
- **Zero scaffold leaks**
- **Zero spam triggers**
- Anchored to the CureMD proof point throughout

## Blockers before email send
| # | Blocker | Detail |
|---|---|---|
| 1 | **Build breakdown asset** | The CTA promises a "build breakdown." It doesn't exist yet. Cannot send a CTA offering something we can't deliver. |
| 2 | **33 Tier A certification years unverified** | Must be checked against live CHPL data before any claim goes out |
| 3 | **6 email-domain mismatch rows** | Contact email domain ≠ company domain. Wrong-person risk. |
| 4 | Mailbox warm-up | `.space` / `.site` still warming |

## Realistic expectations, set in advance
41 contacts at typical cold-outreach rates ≈ 12–16 accepts · 3–6 genuine conversations · **1–3 meetings**

---

# 4. CAMPAIGN 2 — HOME HEALTH / HOSPICE / REFERRAL INTAKE

**Status:** mid-execution. **Diagnosed failure, fix designed, not yet confirmed resolved.**

## ICP
**Home health, hospice, and referral intake automation.**

> ### ⚠️ AUDIT FLAG — two conflicting definitions on record
>
> | Source | Definition |
> |---|---|
> | Project instructions + plan docx | US healthcare-**AI startups**, AI-native only — clinical AI, diagnostics, ambient scribes, prior-auth automation, AI triage |
> | Current working state | Home health / hospice / **referral intake automation** |
>
> These are different ICPs with different buyers. Whether Campaign 2 pivoted, or whether the home-health work is a separate campaign that inherited the label, is **not resolved in any source available.** Confirm which is true — it determines whether the AI-native list was ever built, and whether Campaign 3 (RCM) overlaps with it.

**Hard exclusion:** every Campaign-1 company excluded at sourcing.

**Angle on record for the AI-native version:** *"your ML team shouldn't burn cycles on FHIR/HL7 plumbing — that's what we're for."*

## THE RESULT — and the diagnosis

**Strong open rates. Zero replies.**

Root cause investigated and diagnosed: **body copy and offer framing.** ICP and vertical were ruled out.

> ### ⚠️ AUDIT FLAG — deliverability was never explicitly ruled out
>
> The diagnosis on record rules out ICP and vertical. It does **not** confirm deliverability was tested and cleared.
>
> This matters because: the email go-live gate required mailbox age 3+ weeks, >90% warm-up inbox rate, verified SPF/DKIM/DMARC, and live redirects. Campaign 2 sent from `.space` and `.site` — **low-reputation TLDs.** If any gate condition was unmet at send, mail may have landed in spam or promotions.
>
> **In that scenario the symptoms look identical.** Security gateways (Proofpoint, Mimecast, Barracuda) open and scan mail *in the spam folder too* — so opens register while no human ever sees the message. "Strong opens, zero replies" fits both a copy defect and a deliverability failure.
>
> **Before deploying the rebuilt copy:** check inbox placement. If copy is rebuilt and deployed into a spam-foldering domain, the fix gets blamed for a problem it was never addressing — and the real cause stays hidden for another cycle.

### The four copy defects
1. **Capability-framed** — described what Triminage can do, not what the prospect is losing
2. **High-commitment CTA** — asked for a meeting from a cold contact
3. **No proof anchoring** — no verifiable case study attached to the claim
4. **Near-identical phrasing** across the majority of emails — a spam pattern and a personalisation failure

### The fix template
A four-block structure, now standard for all campaigns:

1. **Verifiable per-company observation** — something specific and true about *that* company
2. **Commercial consequence in the buyer's terms** — what it costs them, in their language
3. **CureMD proof** — the anchored, public, verifiable case study
4. **Low-commitment CTA** — offer a build breakdown, not a meeting

## CRITICAL LEARNING — open rates are unreliable

The strong open rates were misleading. In healthcare outbound, **machine opens inflate the figure meaningfully**:
- Apple Mail Privacy Protection pre-fetches images
- Corporate security gateways — **Proofpoint, Mimecast, Barracuda** — open every link to scan it

**Measure reply rate and positive-reply rate only. Treat open rate as noise.**

## Where it stopped
The rebuilt copy approach is designed but **not yet confirmed as working.** Until a rebuilt sequence produces replies, the copy defect is unproven-fixed.

---

# 5. CAMPAIGN 3 — RCM (TRIMINAGE)

**Status:** parked, deliberately.

## ICP
Revenue cycle management companies adding AI/automation.

## Why it's strong
RCM firms are actively adding AI and automation, and they need the integration depth Triminage sells.

## Why it's parked
**New buyer type, needs fresh messaging.** And more importantly:

> **The copy defect transfers across campaigns.** Campaign 1 and 2's failure was cloned, capability-framed copy with identical CTAs. Launching Campaign 3 before the fix is *confirmed* risks cloning the same defect into a third vertical.

## What can start now
Sourcing and qualification, using free sources only: **G2, Capterra, HBMA, HIMSS/HFMA exhibitor lists, LinkedIn.**

**Messaging is held** until Campaign 2's copy issue is confirmed resolved.

---

# 6. PARKED & KILLED ICPS

| ICP | Decision | Reasoning |
|---|---|---|
| **Hospital innovation teams** | Parked — **highest long-term value** | Largest budgets on the list. Blocker is motion, not money: procurement and security review. Reopen only with a signed client + published case study. |
| **Medical billing companies** | Parked | Small service firms; custom-software budgets rarely match engagement size |
| **Private practice groups** | Parked | They buy off-the-shelf EHR/PM products. Buyer mismatch. |
| **Gulf / UAE hospitals** | Parked | Tender-driven. Never target hospitals cold. |

## UAE / Gulf — recommended motion when reopened
**Subcontract to Dubai / Abu Dhabi systems integrators.** Not direct outbound. Requires a local entity and reference clients first.

---

# 7. MEC ARTWORKS AI CAMPAIGN

**Status:** workflow build phase. Sourcing about to begin. Copy blocked.

## What MEC Artworks AI is
An AI mosaic and pattern design platform Triminage built for client MEC Artworks. Live at **ai.mecartworks.com**.

User sets palette, pattern style, tile density and scale → renders mosaic visualisations in real time via canvas-based rendering. Built for two audiences at once: designers who need speed and control, and clients who need to approve concepts without design literacy.

**The pain it removes:** the gap between a concept and a client saying yes. Sketches, samples, revision rounds, days of waiting, and a customer who can walk during any of it. **This is a revenue problem, not a productivity one.**

---

## 7.1 — The Abdullah thread, in order

| When | What happened |
|---|---|
| — | Abdullah (Head of Products) opens: wants outreach for MEC. Asks if Shahwaz can fetch email addresses given a company list. |
| — | Shahwaz asks for the ICP before sourcing. |
| — | Abdullah sends a Google Sheet of ~100 companies — website URLs plus a niche label for each. Frames it as a **pilot run**. |
| — | Shahwaz enriches. **73 companies found, 10 not found.** (Note: 73 + 10 = 83, not ~100 — gap never reconciled.) |
| — | Abdullah asks for **decision-maker emails** — work preferred, personal as backup. **Not company inboxes.** One contact per company. Owner/founder for small, marketing/ecommerce lead for bigger. Verified before loading "so we don't burn the domain." |
| — | Call held. Abdullah says: **target mosaic companies.** Points to the MEC Artworks AI case study as the asset to show. |
| — | Shahwaz corrects scope: **US market**, and Campaigns 1–2 have run **email-only** — LinkedIn is fully available. |
| — | Shahwaz runs full qualification pass on the 73. Sends findings + 4 questions. |
| — | **Abdullah replies:** focus on **mosaics & murals, tiles included**, other niches later. **Geography open — not US-only.** **Competitor concern dropped entirely.** Wants the pool increased. |
| — | Shahwaz decides: **don't run the 73 as a pilot.** Build the complete workflow first, fold the 73 in as seed rows, run everything together. |

---

## 7.2 — Analysis of Abdullah's 73

**The headline finding: it was never one segment.** Abdullah described it as "mosaic companies." It was seven niches across **three different business models.**

### Niche breakdown (all 73)
| Niche | Rows |
|---|---|
| Decorative / Artisan Tile | 22 |
| Murals & Wallpaper | 17 |
| Mosaic / Pool | 10 |
| Custom Pottery | 8 |
| Custom Rugs | 7 |
| Stained Glass | 6 |
| Ceramic Tile | 3 |

### The three business models
1. **Custom 2D pattern makers** (tile, ceramic, mosaic/pool, rugs, stained glass) — **48 rows.** Design a flat custom pattern → client approves → they build it. That approval wait is our exact pain. **The real ICP.**
2. **Print-on-demand ecommerce** (murals & wallpaper) — 17 rows. Catalog of ready-made designs, printed to size. Nothing gets approved, so no delay to remove. Most already have room-preview tools.
3. **3D craft** (pottery) — 8 rows. Bowls, vases, mugs. Our engine renders flat patterns. Nothing to demo.

### Data quality errors found
| Error | Detail |
|---|---|
| **Oceanside Glasstile** | Enriched as GB / Banbury. Actually Carlsbad, CA. **Wrong-company match.** |
| **Bisazza** | Country field returned `VI` — that's the Vicenza province code, read as Virgin Islands. Company is Italian. |
| Domain mismatches (3) | MuralsWallpaper → hovia.com (legit rebrand) · Craig Bragdy Design → cbdpools.com · Pottery & Poetry .com vs .eu |

### First qualification pass — US-only, pre-Abdullah's reply
**24 KEEP · 5 HOLD · 6 REVIEW · 38 DROP**
Drops: 22 non-US · 13 off-thesis niche · 4 under $1M

The 5 HOLD were direct MEC competitors: New Ravenna, Artistic Tile, Aqua Blu Mosaics, Hakatai, Blue Water Pool Mosaics.

### Second pass — after Abdullah loosened the gates
Geography opened + murals included + competitors cleared:

**43 sendable, up from 24–29.** The pool nearly doubled with zero new sourcing.

| Niche | Rows |
|---|---|
| Artisan Tile | 18 |
| Murals | 12 |
| Mosaic / Pool | 10 |
| Ceramic Tile | 3 |

**Geography (verified against the file):**

| Country | Rows |
|---|---|
| US | 30 |
| Italy | 5 (**6 once Bisazza's `VI` tag is corrected**) |
| UK | 3 |
| `VI` — data error, actually Italy | 1 |
| Canada · Australia · Sweden · Latvia | 1 each |
| **Total** | **43** |

---

## 7.3 — Corrections made along the way

### Headcount is the wrong size filter in this vertical
**Tabarka Studio: 2–10 employees, $5–10M revenue.** Artisan makers run tiny teams on high revenue. Headcount would delete the best prospects.
**→ Gate switched to revenue ≥$1M.**

### The blanket "murals are out" call was too coarse
Opening geography exposed the error. **Wall & Deco, Glamora, Inkiostro Bianco, Instabilelab** are Italian bespoke wallcovering design houses — they commission artists, produce original collections, sell to the trade. They absolutely have the concept-to-approval bottleneck. All four had been dropped purely for being non-US.

**→ Murals stay in, with a gate:** does the company *design* original patterns, or *print* existing ones? Design houses in, catalog print shops out.

---

## 7.4 — Locked ICP (REVISED 24 Aug 2026 — see pivot note below)

**Companies that sell custom/made-to-order flat 2D pattern products — whether they design the patterns in-house, print/produce from a catalog, or let customers upload/choose — where the tool can slot in as the customer-facing (or internal) design/approval step.**

> **⚠️ PIVOT NOTE (24 Aug 2026):** the ICP was broadened on Shahwaz's call. Original version required the prospect to design original patterns in-house AND manufacture them themselves — modeled on an *internal efficiency* pitch (speeds up the prospect's own design-to-client-approval workflow, same problem MEC itself has). The revised version drops those two as hard gates and opens the door to POD/print-on-demand and catalog-plus-custom businesses too, on the logic that the tool can be sold as an **embeddable/white-label configurator on the prospect's own site** — their customers design there, which is a value-add they can offer their own customers, not just an internal speed-up.
>
> **This effectively pre-answers the "what are we selling — tool access or a custom build" question already blocking copy in §7.9/§7.10**, landing on "licensed/embeddable tool access." That's a real pivot in the pitch and CTA, not just a looser gate — **still needs a sync with Abdullah to confirm this is the intended direction** before copy gets written against it. Until confirmed, treat sourcing/qualification as proceeding on this basis but copy as still blocked.

### Core criteria
| # | Criterion | Reasoning |
|---|---|---|
| 1 | Has (or obviously would benefit from) a customer-facing design/choice step before ordering — original design, POD, upload-your-own, or pick-from-collection all qualify | This is the surface the tool plugs into, regardless of who designs the pattern |
| 2 | Output is flat / 2D | Engine renders flat patterns; 3D can't be shown — technical constraint, unaffected by the pivot |
| 3 | Sells custom / bespoke / made-to-order / configurable — not a pure fixed-SKU catalog with zero customer input | A company with literally no customer design/choice offering has nothing for the tool to enhance |
| 4 | Revenue ≥$1M | Budget floor |

**Dropped as hard gates (was #1, #2, #7 in the prior version):** "designs original patterns in-house," "makes the product themselves," "sells to trade." These now only matter as signals (see below), not disqualifiers — a POD reseller or non-trade direct-to-consumer shop is now a valid target as long as criterion 1 and 3 hold.

**Still hard-excludes (per Shahwaz's own carve-out):** pure wholesalers/distributors and construction-material/supply companies that offer **no customer design input at all** — nothing for the tool to plug into.

### Niches
| Status | Niches |
|---|---|
| **Active** | Mosaic/pool · Decorative & artisan tile · Ceramic tile · Bespoke murals & wallcoverings/wallpaper (incl. POD/print-to-order businesses now, per pivot) |
| **Parked** | Custom rugs · Stained glass — separate question from the ICP pivot: still blocked on whether the *engine* can render these mediums, needs Abdullah's answer |
| **Excluded** | Pottery/ceramics (3D — technical constraint, unaffected by pivot) · pure wholesalers/distributors/retailers with no customer design offering · construction-material suppliers (adhesive, tools, machinery) · nonprofit/institutional buyers (wrong buyer type for a paid commercial tool) · restoration-only workshops · teaching studios |

### Firmographics
| Field | Rule |
|---|---|
| Revenue | ≥$1M. Blank → manual review, never auto-drop |
| Employee count | **Not a filter** |
| Geography | Open. Tier 1: US, UK, CA, AU, UAE · Tier 2: Italy, Spain · Tier 3: rest |
| Age | No filter |
| Funding | No filter — data is empty and misleading for this vertical |

### Decision maker
| Size | Target | Reasoning |
|---|---|---|
| Under 30 | Owner / Founder / Creative Director | Designs *and* pays — no one else to convince |
| 30–200 | Marketing or Ecommerce lead | Owns conversion targets, holds budget |
| 200+ | Head of Design / Digital lead | Long cycle — tag separately, deprioritise |

One contact per company. **No generic company inboxes** — Abdullah was explicit.

### Signals — hooks only, never gates
| Signal | Why it matters |
|---|---|
| "To the trade" / trade program on site | **Strongest single free indicator** of an approval bottleneck |
| Recently launched a collection | Design cycle active right now |
| Exhibiting at a trade show | Has marketing budget, actively selling |
| Hiring a designer or visualiser | Already feeling the capacity pain |
| Already has a configurator | Proven willingness to buy — different angle, **not a rejection** |

---

## 7.5 — Sourcing plan

### Yield reality
**Trade show exhibitor lists survive at ~40–50%. Open web search survives at ~15–20%.** A company paying for a booth is a manufacturer with a marketing budget — two gates cleared before you open the site.

### Sources, verified
| # | Source | Link | Filters | Notes |
|---|---|---|---|---|
| 1 | **Cersaie** | cersaie.it/en/e_dettaglio.php?CODICE=700 | Product category: Mosaic, Ceramic tile, Porcelain stoneware, Decorated tile. Skip machinery, adhesives, raw materials, sanitaryware | **Has Export (xlsx) button.** ~2,868 exhibitors total in the 2026 edition — but that's **unfiltered**. A filtered category view on the site returned 595. Expect the mosaic/decorative-tile subset to be a few hundred, not thousands |
| 2 | **Tile of Spain** | tileofspain-cersaie.com | Pre-filtered to Spanish tile makers | **Has Download List** |
| 3 | **TCNA** | tcnatile.com/member-and-product-locator/ | Tick **tile manufacturer** membership only. Untick installation materials, equipment, raw materials, importers, distributors | **Full membership requires $3M+ sales — revenue gate pre-passed.** ~200 members |
| 4 | **Coverings** | coverings.com/exhibitors/ | Product category: tile, mosaic, decorative. Manufacturer type if available | 1,000+ exhibitors but **dirtier** — includes distributors, retailers, fabricators, contractors |
| 5 | **TISE** | intlsurfaceevent.com | Tile + Stone neighborhood only. Ignore flooring/carpet | 650+ exhibitors |
| 6 | **Heimtextil** | heimtextil.messefrankfurt.com/frankfurt/en/search.html | Product category: wallpapers / wall coverings only | **Extra care** — full of bulk textile makers who don't design. Only keep those mentioning collections, design studio, designers, bespoke |
| 7 | **Google Maps** | via Clay | See settings below | Skews to businesses with storefronts — misses trade-only manufacturers |

### Do NOT buy lists
exhibitorsdata.com (~$340 for Cersaie), visitorslist.com and similar. Official directories are free and more current. Paid "attendee databases" are scraped, stale, and will hurt domain reputation.

### Google Maps via Clay — exact settings
| Setting | Value | Why |
|---|---|---|
| Search mode | **Free text** | Google's business-type categories lump manufacturers, retailers and installers together |
| Primary business type | **Any** | Setting it re-introduces retailers |
| Location mode | Single location, one city per run | — |
| Location matching | Selected area only | — |
| Limit per location | **50** | Past ~40, Maps pads results with hardware stores and grout suppliers to fill the count |
| Radius | ~25 miles, or Rectangle over the metro | Default 3040 ft covers a few blocks |

**Search terms — run separately:**
`handmade tile studio` · `art tile studio` · `mosaic studio` · `custom tile manufacturer` · `ceramic tile manufacturer` · `tile design studio`

**Never use:** `tile store` · `tile shop` · `tile installation` · `flooring` · `tile contractor` · `tile and stone`

**Cities, priority order:** Los Angeles · San Francisco/Sonoma · Minneapolis · Portland OR · Detroit/Ann Arbor · Santa Fe/Albuquerque · Seattle · Austin
*(American art tile clusters historically around old Arts-and-Crafts studios; successors set up nearby.)*

### Apify assessment
| Source | Verdict |
|---|---|
| Cersaie, Tile of Spain | **Don't scrape** — download buttons exist |
| TCNA | **Don't scrape** — ~200 rows, and membership checkboxes need eyeballing |
| Google Maps | Clay's native source is easier than an Apify actor |
| Coverings, TISE | Apify viable if needed |
| Heimtextil | JavaScript-heavy, may cost more time than copying |

**Rule:** if a source has under ~300 rows or offers a download, do it manually.

### Clay "Find with filters" company-search recipe (24 Aug 2026)
Supplementary to the exhibitor-directory downloads, not a replacement — Clay's company DB has weak coverage for artisan makers and European studios (cross-campaign learning #6). Run as two passes:

**Company attributes**
| Field | Value |
|---|---|
| Industries to include | Blank, or test "Glass, Ceramics & Concrete Manufacturing" on 10 rows first |
| Industries to exclude | Construction, Wholesale |
| Company sizes | Blank — not a filter in this ICP |
| Annual revenue | Min $1M, no max |
| Funding raised | Blank — empty/misleading data for this vertical |
| Estimated employee count | Blank |
| Company types | Privately held |
| Description keywords to include | handmade tile, art tile studio, mosaic studio, custom tile manufacturer, ceramic tile manufacturer, tile design studio, bespoke mosaic, custom wallcovering, mural design studio |
| Description keywords to exclude | tile store, tile shop, tile installation, flooring, tile contractor, tile and stone, distributor, wholesale, authorized dealer, we install |
| Minimum estimated audience size | Blank |

**Location — run as two passes**
- Pass 1 (Tier 1): US, UK, Canada, Australia, UAE. Headquarters only = ON.
- Pass 2 (Tier 2, after Pass 1 qualified): Italy, Spain.
- Leave regions/cities/states/postal codes blank — city-level drill-down stays on the Google Maps sweep below.

**Exclude companies:** paywalled on current plan — if the Clay upgrade unlocks it, load master list + 73 seed domains here; otherwise keep using the pandas dedupe QA step.

**Company identifiers (Domains/URLs):** use in reverse — paste known domains from Cersaie/TCNA/Tile of Spain exports here to enrich exact matches, not for open search.

Test the keyword set on ~10 rows before scaling, per standing rule #4.

**Pass 1 results (24 Aug 2026):** only 15 raw companies returned from Tier 1 countries — confirms weak Clay coverage for this vertical (learning #6), not a query error. Qualification: **6 KEEP · 3 REVIEW · 6 DROP.** 2 of the 6 drops were pure name collisions ("Mosaic Studio" matched by company name, not industry — one a branding agency, one a media producer). Full row-by-row verdicts tracked in `MEC_Sourcing_Master.csv` in this folder.

**Pass 2 keyword fix:** add `media production, video, branding agency, marketing agency` to Description keywords to exclude, and add `Wholesale Building Materials` to Industries to exclude (caught Transworld Tile and correlates with the catalog/factory pattern seen in COBSA and the Azuvi review case).

**Takeaway:** this channel alone won't hit volume targets — lean harder on Cersaie/TCNA/Coverings/TISE for volume; use this filtered search as supplementary, not primary, exactly as flagged going in.

### Full merge + dedupe (24 Aug 2026)
Merged Abdullah's seed table with the Clay filter search results in one Clay table; consolidated master now in `MEC_Sourcing_Master.csv` in this folder (~90 rows, all niches incl. parked/excluded, full verdicts + reasoning).

**Dedupe:** 2 real duplicates caught by domain-key match (Mosaics Lab, Tiles of Ezra) — both were already in Abdullah's seed. Only 7 of the 10 Clay-filter-search companies were genuinely new.

**Data errors still present, need fixing before outreach:** Oceanside Glasstile (wrong country - GB/Banbury, actually Carlsbad CA) and Bisazza (Country="VI" is Vicenza province code, not Virgin Islands - correct to Italy). Both already flagged once in S7.2; recurring in fresh exports.

**New wrong-company enrichment matches found:** Contrado → resolved to an unrelated Australian fashion brand; Ian Leino Design → resolved to an unrelated apparel/merch brand. Same failure pattern as the earlier Mosaic Studio (UK) case - Clay matches on name text, not business identity. Mosaic Studio (UK) itself is still unresolved/flagged, pending a site check.

**Active-niche verdict counts:** 24 KEEP · 23 REVIEW · 11 DROP · 7 NOT_FOUND (Clay enrichment failed) · 1 FLAGGED (Mosaic Studio UK).

**Next step recommended:** the 23-company REVIEW bucket has descriptions too thin to gate manually (blank, one-liner, or Clay filler text) - run Claygent on it with the custom-vs-catalog question per S7.7's own plan, rather than manual site visits one by one.

**Parked niches (rugs, stained glass):** 7 strong candidates identified and tagged PARKED, ready to activate once Abdullah confirms rendering fit.

### Claygent site audit — COMPLETE (25 Aug 2026)

All **60 blank rows** of `MEC_Warm_Shortlist_Seed-Default-view-export-1787598276390.csv` are audited across four batches. **Zero blocked rows remain.** Consolidated output: `MEC_Warm_Shortlist_AUDITED.csv` — every row carries verdict, visual-tool level, send priority and reason.

| Verdict | Count |
|---|---|
| **KEEP — active niches, sendable** | **42** (9 priority-1, 28 priority-2, 5 priority-3) |
| PARKED — rugs / stained glass | 8 |
| DROP | 6 |
| FLAG — manual decision | 3 (Seneca, Ravenstone, Zia) |
| RECHECK | 1 (Bigmural, ~8 Sept) |

**Priority-1 lead list (9):** New Ravenna · Area Environments · Glamora · US Vinyl · Look Walls · Heath Ceramics · North Prairie Tileworks · Blue Water Pool Mosaics · Tabarka Studio.
The shared trait: all nine sell bespoke *and* have **no customer-facing design tool**, so the gap is real rather than assumed.

**Batch 4 method caveat — carries into copy.** The 12 rows blocked in batches 1–3 (403s, TLS failures, JS-only rendering) could not be re-run in a browser: the run environment blocked outbound HTTP to prospect domains entirely. They were resolved by **web search over each company's own indexed pages** instead. SITE_MATCH, CUSTOM_OFFERING and HOOK are reliable; **VISUAL_TOOL is not** — search indexes a tool's landing page, not its behaviour, so "None" there means *no tool page found*, not *no tool exists*. **4 rows need an eyeball pass before any copy references their tooling: 4 Fancy Walls · 12 New Ravenna · 27 Sonoma · 42 The Perfect Rug.**

### ⚠️ The rugs finding — this changes §7.10 Q3

Batch 3 called Jubi Rugs "the strongest row" on the premise that its "Rug Plan" is a hand-staffed design loop a configurator would replace. **That premise was wrong** — Jubi has an online customizer with a 1,200-shade palette and real-time preview. Row 43 corrected Basic → Advanced.

That correction exposed a pattern. **All three rug companies with tooling data have advanced configurators** — Jubi (43), The Rug Company (39, a "Custom Rug Designer" portal over 100+ designs), Rug Artisan (41, ~300 preset colourways). **Custom rugs has already adopted this tooling.** Stained glass shows **zero** configurators across all three audited rows (44 Judson, 45 Willet, 46 Franklin) despite all three selling bespoke commission work.

> **So Q3 to Abdullah is the wrong question as written.** It asks whether the *engine renders* rugs and stained glass. For rugs, rendering is no longer the binding constraint — **market saturation is**; we would be selling into a solved problem. **If one parked niche unparks, the evidence favours stained glass.** Rugs looked like the strongest parked niche on batch 3's evidence and is the weakest on batch 4's.

**Also worth noting:** 7 of 60 audited companies already own an advanced configurator (Instabilelab, Bisazza, Fireclay, Popham, Jubi, The Rug Company, Rug Artisan). Per §7.4 that's a hook, not a rejection — but it is a **7-company A/B cohort** available for free: does "you already built one, here's what it's missing" outperform "you don't have one"? Worth running as a fourth test alongside the three in §11.

### Data corrections applied in `MEC_Warm_Shortlist_AUDITED.csv`
| Row | Field | From | To |
|---|---|---|---|
| 14 Oceanside | Country | `GB`/Banbury | **`US`, Carlsbad CA** — third time flagged; fixed in data now, not just notes |
| 18 Bisazza | Country | `VI` | `IT` — Vicenza province code |
| 26 North Prairie | Locality | Minneapolis | St. Paul, MN |
| 27 Sonoma | Annual Revenue | `25M-75M` | `10M-25M` — D&B/Zippia peak $10.6M (2024); Clay band inflated, do not prioritise on it |
| 56 Mosaics Lab | — | — | **DROP** — duplicate of row 10 |
| 60 Jill Campion | verdict | pending | **DROP** — Companies House 02699570 is a Cambridge residential address, **not Staffordshire** as the niche column claims; 500K–1M fails the $1M gate; domain 404s |

### Scope decision (24 Aug 2026)
Shahwaz decided: take the current 67-company list (66 once the Mosaics Lab duplicate is deleted) all the way through the workflow to outreach-ready before sourcing more. Additional sourcing (Cersaie export, TCNA, Coverings, TISE, Google Maps sweeps) is deliberately deferred to a phase 2 expansion, not dropped — do not start new sourcing until this batch is through.

**Remaining steps to outreach-ready, in standing-rule order:**
1. Delete Mosaics Lab duplicate (true count 66)
2. Clay enrichment per S7.7 - decision maker, email waterfall, right-person check
3. Copy - BLOCKED on Abdullah on two questions now: (a) tool access vs custom build + price (S7.9, asked twice already), (b) does he agree with the 24 Aug ICP pivot to an embeddable/white-label configurator angle
4. Sending domain + 3-week warm-up - not yet started, still the one uncompressible item on the critical path per S11, should start now in parallel rather than waiting on copy
5. LinkedIn launch first per S7.8 (no warm-up needed), email second once warm-up clears

### Volume target
| Wave | Raw | Survival | Sendable |
|---|---|---|---|
| Seed (Abdullah's 73) | 73 | 59% | **43** |
| Exhibitor lists | ~200 | ~45% | ~90 |
| Open web / Maps | ~100 | ~18% | ~18 |
| **Total** | **~373** | | **~150** |

**Collection sheet columns — nothing else at this stage:**
`company · website · niche · source · country`

---

## 7.6 — Qualification gates

Run in order. Stop as soon as one fails. ~3 minutes per company. **All free, all outside Clay.**

| # | Gate | Check | Kills |
|---|---|---|---|
| 1 | Dedupe | Domain match against master list + the 73 seed | — |
| 2 | Niche fit | One of the 4 active niches | ~15% |
| 3 | **Maker not middleman** | Keep: *we make, handcrafted, our studio, fired in our kiln, our workshop, manufactured*, workshop photos. Kill: *installation, we install, contractor, distributor, we carry brands, authorized dealer* | **~40%** |
| 4 | **Designs not prints** | Keep: *collections, named designers, bespoke, custom design, to the trade*. Kill: catalog with size picker and checkout | ~10% |
| 5 | Custom offering exists | A custom / bespoke / commission / made-to-order page | ~10% |
| 6 | Revenue ≥$1M | Blank → manual review | **~30%** |

**Gate 3 is the highest-kill gate and the most commonly skipped.** It's why open-web lists come back full of tile installers. If a list looks suspiciously clean, gate 3 wasn't applied.

**Delete disqualified rows. Do not hide them** — hidden rows can still consume credits.

---

## 7.7 — Clay enrichment architecture

### Critical: two row types
The 73 seed rows **already have** Employee Count, Size, Industry, Country, Revenue, LinkedIn URL. New rows don't.
**Add a `source` column marked seed/new. Gate every firmographic column on `source = new`** — otherwise you pay twice for 43 rows.

### Column order and conditional logic
| # | Column | Costs credits | Conditional run |
|---|---|---|---|
| 1 | company, website, niche, source, geo_tier | No | — |
| 2 | `segment` formula | No | tile/mosaic · murals |
| 3 | Enrich Company | **Yes** | only if `source = new` |
| 4 | `revenue_pass` formula | No | ≥$1M or blank |
| 5 | `size_band` formula | No | <30 / 30–200 / 200+ |
| 6 | **Find decision maker** | **Yes** | only if `revenue_pass = true` |
| 7 | **Email waterfall** | **Yes — most expensive** | only if DM found AND email blank |
| 8 | Email verify | **Yes** | only if email found |
| 9 | `right_person_check` formula | No | email domain == company domain |
| 10 | `has_existing_tool` (Claygent) | **Yes — highest cost** | last, top rows only |

**Test every new column on 10 rows before scaling. Disable auto-enrichment on import.**

**Now that budget isn't binding:** Claygent becomes viable across the list for the one question that's hard to check at scale — *does this company do custom/bespoke work?* Prompt it to visit the site and return yes/no plus the page found. Automates gate 5 and part of gate 3. Still test on 10 first.

### Pre-send QA
1. Fill rate on every outreach-critical column
2. Email-to-domain cross-check — flag emails resolving to unrelated domains
3. Duplicate domain detection — catches companies sourced from two lists
4. Geography vs domain — verify against the site's contact page, not the LinkedIn location field

### Export format
Instantly-clean, no spaces, no built-in collisions:
`msg_subject_line · msg_first_touch · msg_linkedin_dm · dm_first_name · company_name · segment`

---

## 7.8 — Channel plan

**LinkedIn first.** Three reasons:
1. The best asset is a **live clickable tool**. In cold email a link is a spam risk; in a LinkedIn DM after an accept it's normal.
2. **These people get almost no LinkedIn outreach.** A tile studio owner in Portland isn't getting 40 sales messages a day like a tech CTO.
3. **No warm-up needed.** LinkedIn works today; email needs 3 weeks.

**Cadence:** connection request → DM on accept → wait 3–4 days → touch 2 (one *new specific* thing, never "just bumping") → wait 4–5 days → touch 3 / soft breakup. **Never follow up within 48 hours.**

**Pace:** 12–15 invites/day, weekdays.

**Timezone advantage:** Europe morning ≈ 1–3 PM PKT · US morning ≈ 6–10 PM PKT. Split the sending day rather than cramming one window — safer for the account.

**Email second**, after warm-up gate clears. Target LinkedIn non-responders first.

**Instagram** — worth considering as backup for small studios. This industry lives on Instagram and small studios often reply to DMs faster than LinkedIn. Not a primary channel.

**GDPR:** EU cold email needs a legitimate-interest basis. Workable for B2B, but lead with LinkedIn in Tier 2 and 3 markets.

---

## 7.9 — Copy plan (BLOCKED)

> **BLOCKED on Abdullah:** what are we selling — licensed/white-label tool access, or a custom build at agency rates? And at what price? "Try our tool" and "we'll build you one" are different pitches, to different buyers, with different CTAs.

**Pain frame:** the gap between a concept and a client saying yes. Not "we build AI tools."

### Three copy variants — one pipeline
| Variant | Seed rows | Framing |
|---|---|---|
| Tile / Mosaic / Ceramic | 31 | Demo *is* their product. **Run first.** |
| Murals & bespoke wallcoverings | 12 | Same pattern engine, wall scale |
| *(parked)* Rugs, stained glass | 13 | "Same engine, your medium" — needs Abdullah's answer |

**Why one pipeline, not one per niche:** gates, decision-maker logic and enrichment are identical across niches. Only the framing changes. Splitting into five pipelines gives five samples of five — none large enough to conclude anything from.

### CTA
**Lowest commitment available:** *"want the link — try it on one of your own patterns?"*
Not a demo request. Not a call booking. The tool is live and clickable — that's the strongest asset in the campaign, and it doubles as qualification. Anyone who clicks and plays has self-identified.

### Message quality bar
- LinkedIn invite note ≤280 characters · first-touch email ≤90 words
- No signature blocks · no links in cold email first touch
- **Vary the CTA** — 3–4 variants. Identical closing lines are a spam pattern.
- One ask per message
- Honest-proof rule: **the MEC case study has no hard numbers.** A working link beats a claimed statistic.

---

## 7.10 — MEC open questions

| # | Question | Status |
|---|---|---|
| 1 | Competitor clearance / IP ownership | ✅ **Answered** — Abdullah dropped the concern entirely |
| 2 | **What are we selling — tool access or a build? What price?** | ❌ **STILL BLOCKING** — asked twice |
| 3 | ~~Does the tool render usefully for rugs / stained glass / murals?~~ **RE-FRAMED 25 Aug:** murals confirmed in scope. For **rugs**, don't ask about rendering — ask whether we want to sell into a vertical where all 3 audited companies already run configurators. For **stained glass**, 3 of 3 audited companies do bespoke commissions with **zero** tooling — this is the unpark candidate | ⚠️ Re-framed, still open |
| 4 | Pilot the 43 first, or source a full wave? | ✅ **Answered** — Shahwaz decided: build the complete workflow first, run everything together |
| 5 | Sending domain approval | ❌ Not confirmed |
| 6 | The 73 + 10 = 83 vs ~100 gap | ❌ Never reconciled |

---

# 8. CROSS-CAMPAIGN LEARNINGS

| # | Learning |
|---|---|
| 1 | **The copy defect transfers across campaigns.** Campaign 1/2's failure was cloned, capability-framed copy with identical CTAs — not ICP selection. Any new campaign launched before the fix is confirmed risks cloning the defect. |
| 2 | **Open rates are unreliable in healthcare outbound.** Apple Mail Privacy Protection and corporate gateways (Proofpoint, Mimecast, Barracuda) generate machine opens that inflate figures meaningfully. Measure replies only. |
| 3 | **Proof must be verifiable.** Only publicly confirmed figures go in copy. Where none exist, a working demo link beats a claimed statistic. |
| 4 | **Revenue > headcount as a size filter in artisan verticals.** Small teams regularly exceed $1M. Headcount kills the best rows. |
| 5 | **Qualify before enriching.** Credits fire only on survivors of the manual gate sequence. Claygent runs last, on top rows only. |
| 6 | **Trade show directories outperform open web search** for artisan verticals. Booth = manufacturer + marketing budget. Clay's B2B database has weak coverage for artisan makers and European studios — it's built around funded tech companies. |
| 7 | **Gate 3 (maker not middleman) is the highest-kill gate and the most skipped.** Must run manually before any credit spend. |
| 8 | **A certification can replace a qualification question.** §170.315(g)(10) guarantees a live FHIR API — no need to ask about integration method. |
| 9 | **Never use a fresh LinkedIn account for outreach.** That's what got Shahmeer's account restricted. |

---

# 9. STANDING RULES

1. Qualify before enriching. Credits never fire on unqualified rows.
2. **Workflow sequence is strict:** infrastructure → sourcing → qualification (manual gates) → Clay enrichment → outreach execution.
3. Auto-enrichment always disabled on Clay import.
4. Every new column tested on 10 rows before scaling.
5. **Disqualified rows are deleted, not hidden** — credits can leak to hidden rows.
6. LinkedIn runs first in every campaign. Email second, after warm-up clears.
7. Human reviews every row.
8. Never invent facts, quotes, or results. No claimed results before a campaign has run.
9. One persona per prospect across channels.
10. Verify geography against domain, not the LinkedIn location field.
11. Respect sensitivity flags — e.g. Rappore's founder works on veteran suicide prevention; honour the mission, never reference suicide in outreach.
12. Internal stakeholders (Haroon, Moeed, Abdullah) coordinated before major pivots.
13. **Copy follows the four-block structure:** verifiable observation → commercial consequence → CureMD proof → low-commitment CTA.

## Upgrade triggers
| Trigger | Action |
|---|---|
| Clay credits <400 with qualified companies waiting | **Clay Starter** ← *currently firing; purchase in progress* |
| Warm-up done, free-tier variable/sequence limits hit | Instantly paid |
| Combined sendable list >~150, manual sending is the bottleneck | HeyReach + an **aged, warmed** LinkedIn account — never a fresh one |

---

# 10. WHERE EVERYTHING STANDS — ACTION LIST

## Campaign 1 — US Digital Health
| # | Action | Blocked by |
|---|---|---|
| 1 | Build the "build breakdown" asset promised in CTAs | Nothing — **do this** |
| 2 | Verify 33 Tier A certification years against live CHPL | Nothing |
| 3 | Fix 6 email-domain mismatch rows | Nothing |
| 4 | Complete mailbox warm-up | Time |
| 5 | Launch LinkedIn phase (channel is unused) | Nothing |

## Campaign 2 — Home Health / Hospice
| # | Action | Blocked by |
|---|---|---|
| 1 | **Check inbox placement before anything else** — seed test to Gmail/Outlook/Yahoo, confirm not spam or promotions | Nothing — **do this first** |
| 2 | Pull actual send volume and open rate from Instantly | Nothing |
| 3 | Deploy the rebuilt four-block sequence | Build breakdown asset |
| 4 | **Confirm the copy fix works** — measure replies, not opens | #1, #3 |

*#1 comes before #3 deliberately. Deploying rebuilt copy into a spam-foldering domain wastes the fix and hides the real cause.*

## Campaign 3 — RCM
| # | Action | Blocked by |
|---|---|---|
| 1 | Source and qualify via free sources (G2, Capterra, HBMA, HIMSS/HFMA, LinkedIn) | Nothing |
| 2 | Write messaging | **Campaign 2 copy fix confirmed** |

## MEC Artworks AI
| # | Action | Blocked by |
|---|---|---|
| 1 | Register dedicated sending domain, start 3-week warm-up | **Abdullah approval — critical path** |
| 2 | Complete Clay subscription purchase | In progress |
| 3 | Build Clay table per §7.7 architecture | Nothing |
| 3a | ✅ **DONE 25 Aug** — Claygent site audit, all 60 rows, zero blocked. `MEC_Warm_Shortlist_AUDITED.csv` | — |
| 3b | **Eyeball VISUAL_TOOL on 4 rows** (4, 12, 27, 42) from an unrestricted network before copy cites tooling | Nothing — **do this** |
| 3c | Decide the **catalog-only boundary rule** once, for rows 27 + 51, and apply it to every future catalog row | Shahwaz's call |
| 4 | Load 43 seed survivors tagged `source = seed` | Nothing |
| 5 | Cersaie xlsx export + Tile of Spain download | Nothing — **easiest win available** |
| 6 | TCNA manual copy (~200 rows, revenue pre-qualified) | Nothing |
| 7 | Google Maps city sweeps via Clay, limit 50 | #2 |
| 8 | Run gates 1–6 on all new rows | #5, #6, #7 |
| 9 | Run enrichment on survivors | #8 |
| 10 | **Write copy** | **Abdullah — offer + price** |
| 11 | QA pass and export | #9, #10 |
| 12 | LinkedIn launch | #11 |
| 13 | Email launch | #12 + warm-up gate |

## UAE / Gulf
Parked. When reopened: subcontract to Dubai/Abu Dhabi systems integrators, not direct outbound. Needs local entity + reference clients.

---

# 10b. ASSUMPTIONS & UNVERIFIED ITEMS

Everything in this document is either verified against a file or listed here. Nothing else is assumed.

## Estimates, not measurements
| Figure | Status |
|---|---|
| Exhibitor-list survival ~40–50% | **Estimate.** Not yet measured. Recalculate after the first real batch |
| Open-web survival ~15–20% | **Estimate** |
| Gate kill rates (gate 3 ~40%, gate 6 ~30%, etc.) | **Estimates**, derived from the seed list only |
| Volume plan (~373 raw → ~150 sendable) | Built on the above estimates. Will move |
| Campaign 1 expectation: 12–16 accepts, 3–6 conversations, 1–3 meetings | Industry-range figures, not promises |

**The seed list survived at 59% (73 → 43). Do not expect that on wild-sourced lists** — Abdullah's sheet was pre-filtered and contained no contractors or installers. Gate 3 hadn't needed to fire.

## Unresolved factual gaps
| # | Gap |
|---|---|
| 1 | **Campaign 2 send volume and open rate are unknown.** "Zero replies from 40 sends" and "zero replies from 400" are different problems requiring different responses |
| 2 | **Campaign 2 inbox placement never confirmed** — see the audit flag in §4 |
| 3 | **Campaign 2's true ICP** — AI-native startups or home health? See §4 |
| 4 | **Abdullah's original sheet: 73 found + 10 not found = 83, but he said ~100.** 17 companies unaccounted for |
| 5 | **Whether Campaign 1's LinkedIn phase ran at all.** Plan and project instructions say LinkedIn is the active channel; current statement is that both campaigns ran email-only. These contradict |
| 7 | Clay credit cost per row for Google Maps sourcing — never measured. Test at limit 5 first |

## Documents now stale
| Source | What's out of date |
|---|---|
| Project instructions | Describe Campaign 2 as "building" and LinkedIn as the active channel. Also state Clay is on free tier — a paid plan is being purchased |
| Plan docx (Jul–Aug) | 30-day plan whose window has passed. LinkedIn-first sequencing was not followed |
| Prior MEC notes | Recorded murals/wallpaper as **disqualified**. Abdullah has since ruled murals **in scope**. This document is correct; older notes are not |

---

# 11. THE THREE THINGS THAT MATTER MOST RIGHT NOW

1. **Build the "build breakdown" asset.** It's promised in Campaign 1 and 2 CTAs and it doesn't exist. Every healthcare send is blocked behind it, and it's entirely within your control.
2. **Get Abdullah's answer on what MEC is selling.** Asked twice. Everything in the MEC campaign except copy can proceed without it — but copy is the campaign.
3. **Register the MEC domain today.** The 3-week warm-up is the only thing in any plan here that cannot be compressed. Starting it now means it finishes when the list is ready.

## Open A/B tests to run
| Campaign | Test |
|---|---|
| MEC | Demo link in touch-1 vs. held to touch-2. Standing rule says no links in first touch — but here the proof *is* the link. |
| MEC | Trade-program companies vs. non-trade-program as lead cut. Should predict reply rate better than niche or revenue, and it's free to check. |
| MEC | Artisan tile vs. stained glass as lead segment (once unparked) — same structural pain, very different buyer temperament. |
| MEC | **Has-a-configurator vs. has-none.** 7 audited companies already own an advanced tool (Instabilelab, Bisazza, Fireclay, Popham, Jubi, The Rug Company, Rug Artisan). Does "you built one — here's what it's missing" beat "you don't have one"? A free 7-row cohort, and it tests the §7.4 signal claim that an existing tool is a hook rather than a rejection. |
| Campaign 1 | `.com` vs `.space`/`.site` deliverability at send |
