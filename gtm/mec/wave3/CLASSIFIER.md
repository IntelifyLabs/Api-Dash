# Round 3 classifier — the rules, before they run

Free. No Clay, no credits. Runs on text we already hold.

## Why this is a new classifier, not a patch of `q1/classify.py`

The q1 classifier was built for Cersaie rows, where the only text was a
third-party company description from Clay. It had to guess a lot, and six of
its gates are now actively wrong:

| q1 gate | What it said | Why it is wrong now |
|---|---|---|
| `R_3D` | *"furniture or 3D ceramics. Engine renders flat patterns only"* | the Furniture Studio stands a piece on the floor at real size. **Would cut all 799 furniture rows** |
| `R_SANITARY` | *"sanitaryware and bathroom fittings. 3D, explicit exclusion"* | Furniture Studio handles floor-standing fixtures |
| `R_WOOD_SOFT` | *"carpet, rug manufactur, moquette"* | the Rug Studio exists. **Would cut all 30 rug rows** |
| criterion 3 | *"large fixed-SKU producer, nothing for the tool to plug into"* | it renders **from** a fixed catalogue. A big catalogue is the input, not a disqualifier |
| `R_MIDDLE` | distributor, importer, retailer → out | the Showhouse page names *"surface distributors"*, *"flooring retailers"*, *"furniture showrooms"* as its own ICP |
| `R_INSTALL` | fabricator, contractor → out | the page names *"fabricators"* under Countertops |

Round 3 also has far better input: the Salone and Heimtextil APIs give booked
**categories** and a **product list** per company, which is the exhibitor's own
declaration rather than a scraped guess.

## The ICP, stated plainly

A company qualifies when all four hold:

1. **It makes or sells a product that goes into a room** and that one of the
   seven studios can render: a surface, a floor covering, a wall covering, or
   a placed object at real size.
2. **It has a consumer-facing website with a product range** a shopper can
   browse. This is the one the visualiser sits on. No site, no pitch.
3. **It sells to end buyers**, directly or through dealers it routes leads
   to. Trade-only and import-export-only businesses have no shopper to
   capture.
4. **It is not a supplier to our ICP.** Machinery, tools, chemicals, fibres,
   yarns, raw material, pattern designs sold to manufacturers, software,
   press, associations.

## Gate 1 — category, from the exhibitor's own booking

Already applied in sourcing. Recorded here so the whole chain is in one place.

**In**

| Category | Studio |
|---|---|
| Salone: Salone Internazionale del Mobile, International Bathroom Exhibition, EuroCucina | `furniture` |
| Salone: S.Project | unresolved, see gate 4 |
| Heimtextil: Wall Decoration | `wallpaper` |
| Heimtextil: Carpets & Rugs, Flooring & Equipment | `rugs` |
| Heimtextil halls 11.0 / 12.0 / 12.1 with no category booked | `rugs` — those halls are Carpets & Rugs end to end |
| Heimtextil hall 3.0 with no category booked | `wallpaper` if the name or domain carries a product signal, else review — 3.0 mixes wallpaper with curtains and sun protection |

**Out**

Furnishing Accessories (homeware, textiles) · Technology For the Kitchen
(appliances) · Raritas (collectible one-offs) · Workplace 3.0 (office,
contract buyer) · Bed Bath & Living · Smart Bedding · Decorative & Furniture
Fabrics · Window & Interior Decoration · Fibres, Yarns, Finishing · Textile
Technology · Services & Software · Associations, institutes, publishers ·
Textile Design (sells designs to manufacturers, not products to shoppers)

## Gate 2 — the text gate, free

Runs over `categories` + `products`, which for round 3 is the exhibitor's own
words. Kills what the category gate let through.

**OUT, wrong business**

machinery, machine, maschine, macchina · tooling, abrasive, diamond tool ·
adhesive, glue, grout, sealant, primer, resin, pigment, ink · software, saas,
erp, cad · magazine, publisher, trade fair, association, consortium,
federation · logistics, freight, forwarding · packaging · laboratory, testing,
certification · consultancy, agency, services

**OUT, wrong medium**

fibre, yarn, thread, filament, non-woven, raw material, greige · curtain
tape, blind component, roller mechanism, track, pelmet · appliance, oven, hob,
extractor, dishwasher, tap, mixer, faucet (no studio) · lighting, lamp,
pendant, luminaire

**OUT, not a maker and nothing to render**

pattern design studio, design archive, surface design service, print studio
selling artwork to manufacturers

**Kept, and this is the point**

Anything whose product list names a piece of furniture, a rug, a carpet, a
wallpaper, a wallcovering, a mural, a worktop, a slab, a surface or a
sanitaryware or bathroom-furniture item. A marble dining table is furniture,
not a surface, and routes to `furniture`.

## Gate 3 — revenue and size

**Not applied.** The round 3 APIs carry no revenue or headcount. q1 used a
$1M gate from a Clay field that does not exist here. Guessing it from country
or product count would be invention. If it matters, it is a Clay field and
therefore a credit, so it is left for you to decide after the free pass.

## Gate 4 — the website pass, free, and the one that does the real work

One fetch of each company's own homepage. Produces four fields:

| Field | Values | What it decides |
|---|---|---|
| `site_live` | yes / no / redirect | no site, no pitch. Dropped before Clay |
| `has_tryon` | yes / no | already runs a visualiser. **Wave 2's strongest segment.** Roomvo, room planner, configurator, "see it in your room", AR |
| `sells_to` | consumer / trade only / unclear | cart, checkout, shop, prices vs "trade only", "dealer login", "wholesale enquiries". **This is what resolves the 194 rug export houses** rather than cutting them on geography |
| `site_quote` | a line from their own page | the `qa_hook`. Powers *"We noticed something on {company}"* |

Plus `email_pattern` inferred from the company email we already hold, so Clay
knows whether to look for `first.last@`, `f.last@` or a named mailbox.

Three sourcing judgements get **resolved by the website rather than by me**,
per your confirmation:

- the 194 rug export houses — cart or consumer shop means in
- the 47 S.Project rows — the site says whether it is surfaces or bathroom
- the 31 hall 3.0 rows — the site says wallpaper or curtains

## What is NOT decided here

The **decision maker**. Name, role and work email are the only thing left for
Clay, and the free pass exists so those credits land on a short list rather
than on 1,314 rows.
