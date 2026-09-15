# Claygent prompt — qualifier 1 (ICP fit + existing design tool)

Rev 3, 15 Sept 2026. Two corrections from Shahwaz:

1. **3D products qualify too.** The tool is customised per business and
   branding, so the flat-2D engine constraint no longer gates anything.
2. **Catalogue and custom both qualify** (rev 2).

And the product, stated precisely, is two options:
- **Try-on:** the customer uploads a photo of their room and picks a product
  from the COMPANY'S OWN CATALOGUE to see it in place
- **Prompt:** the customer writes a description from scratch and gets a visual
  of what they have in mind

## What this does to the funnel — read this

| | Rows | |
|---|---|---|
| Qualify | **471** | 81% of 576 |
| Still out | 99 | 73 not-a-product-company · 17 under $1M · 8 other · 1 wrong company |
| Review | 6 | quarries — the buyer is a factory, not an end customer |

183 of the 288 previously cut rows come back: 60 cut on medium (sanitaryware,
furniture, doors, worktops), 63 on commodity volume, 12 middlemen, plus
hand-verified gate-3 rows.

**The ICP question has stopped discriminating.** At 81% pass, "do they fit"
is no longer a qualifier — it is a formality. Nothing wrong with the decision,
but the consequence is real: ranking has to come from somewhere else, and the
only axes left with signal are **tool_level** (17 MANUAL rows are still the
best prospects on the list), **revenue**, and **company size → who the buyer
is**. Widening the ICP did not create better prospects; it added average ones.

**Also unparks §7.10 Q3 by implication.** Rugs, stained glass and pottery were
excluded or parked purely on the flat-2D constraint. That constraint is gone,
so those niches are in and the question to Abdullah is closed.

## Run order

1. Run on the 471. Skip the 99 — settled from free text at zero cost.
2. Test the known-answer rows below first (standing rule 4).
3. Read "the comparability trap" before segmenting.

## The prompt

```
Visit {{domain}}. Answer two questions about {{company}}: does it fit our
ICP, and does it already have a customer-facing design tool.

WHAT WE SELL: a white-label AI design tool that a company embeds on its own
site, built and branded for that company. It does two things:
  1. TRY-ON - the customer uploads a photo of their own room and picks a
     product from THAT COMPANY'S catalogue to see how it looks in place
  2. PROMPT - the customer writes a description from scratch and gets a visual
     of what they have in mind
It is customised per client, so the product's shape, material or dimension is
NOT a constraint. Flat surfaces and 3D objects both work.

=== PART 1: ICP FIT ===

A company FITS if both are true:
  a) it sells a physical product that a customer looks at and chooses -
     under its own brand, its own catalogue, or made to order
  b) seeing that product in their own space, or seeing an idea visualised
     before buying, would plausibly help that customer decide

That is deliberately broad. All of these FIT:
  - tile, mosaic, ceramic, porcelain, stone, terracotta, cement tile, slabs
  - wallpaper, wallcoverings, murals, panels, decorative surfaces
  - sanitaryware, taps, basins, baths, shower trays, bathroom furniture
  - kitchens, furniture, worktops, countertops, tabletops
  - pottery, vases, tableware, lighting, fireplaces
  - rugs, carpet, parquet, wood, laminate, vinyl, LVT, SPC, flooring
  - doors, windows, profiles, trims, moulding
  - a fixed catalogue with no custom option at all - STILL FITS, that is
    exactly what try-on is for
  - a distributor, importer, wholesaler or retailer selling a catalogue on
    its own site - STILL FITS, the catalogue is theirs to show
  - a large volume manufacturer with thousands of SKUs - STILL FITS

A company does NOT fit only if one of these is true:
  - it sells no physical product: trade magazine, publisher, trade
    association or promotion body, trade fair organiser, pension fund,
    consultancy, logistics firm, software vendor, bank
  - its product is an industrial INPUT the end customer never sees or
    chooses: glazes, frits, pigments, ceramic inks, adhesives, grout,
    mortar, sealants, primers, raw chemicals, substrates
  - its product is plant, machinery or tools: kilns, presses, tile cutters,
    saws, diamond blades, abrasives, handling equipment
  - it sells showroom fixtures: display stands, sample walls, trade-fair
    stands (they sell TO our buyers - flag as a possible partner, not a
    prospect)
  - it only provides a service and sells no product line of its own:
    installation, laying, fabrication, contracting
  - the site does not load, is parked, or belongs to a different business
    than the name suggests

If a company quarries and sells raw blocks to other factories rather than
finished product to end customers, mark icp_fit REVIEW and explain.

=== PART 2: DO THEY ALREADY HAVE THE TOOL ===

Reading the main navigation is NOT ENOUGH. In the 10-row test that was the
single cause of failure: the tool existed and was reported as NONE because it
was not in the top menu. Check ALL of the following before you may answer NONE.

1. The main navigation, plus any "tools", "design", "inspiration",
   "professionals", "trade" or "area riservata" section.
2. **The FOOTER.** Design tools are very often linked only from the footer.
3. **Try these paths directly on the domain.** This is mandatory, not
   optional, and it is the cheapest way to avoid a false negative:
     /configurator  /configuratore  /configurador  /create3d  /3d
     /visualizer  /visualiser  /visualizador  /simulador  /simulatore
     /design-your-room  /designyourown  /design-tools  /tools  /lab
     /stylist  /studio  /room  /mosaic-tool  /planner
4. **A separate SUBDOMAIN or standalone app** - design.example.com,
   designyourown.example.com, mosaics.example.com. Tools are frequently
   hosted off the main site entirely.
5. **If {{company}} is a GROUP or parent company, check its BRAND sites.**
   The group domain often has no tool while the brand site does. This is
   common in Italian and Spanish ceramics: ABK Group's Virtual Stylist lives
   on abk.it, not abkgroup.it; Appiani's three configurators live under
   gruppobardelli.com/appiani/. 111 of 576 rows in this list look like groups
   or carry sibling brands, so treat it as the norm, not an edge case.
6. Product pages, which sometimes embed a picker or a room preview.
7. Anything named visualizer, visualiser, configurator, simulator, creator,
   stylist, studio, lab, planner, 3D, "design your own", "create your own",
   or any AI feature.

Classify into exactly one of four values:

ADVANCED - a working tool the customer drives: places the product in a room
  or on an uploaded photo, OR composes a pattern / blend / colourway and
  previews the result. Includes AI styling tools.
BASIC - only filtering or picking: search filters, a swatch or colour finder,
  a style quiz, a size or quantity calculator, a static palette page, a
  downloadable catalogue. No composed preview.
MANUAL - a real custom or bespoke offering delivered by PEOPLE: email or form
  enquiry, a rep or account manager, a design consultation or meeting,
  staff-made CAD drawings or layout simulations, posted sample books,
  physical templates, glaze or colour trials.
NONE - no design tool and no stated custom offering. Catalogue only.

Then say WHICH of our two options they already cover, because it decides the
pitch:
  has_tryon   yes / no - can a customer see the product in their own room or
              on an uploaded photo?
  has_prompt  yes / no - can a customer describe something in words and get a
              generated visual?

Rules:
- Cookie banners often contain a "Configure" button. That is NOT a tool.
  Ignore it.
- In tile marketing "3D" usually means a RELIEF SURFACE, a textured product,
  not a 3D room tool. Only count 3D if the customer can manipulate a view.
- BIM / CAD asset libraries and downloadable 3D models are for specifiers,
  not customers. That is BASIC, not ADVANCED.
- Note whether the tool is their own build or an embedded third party
  (Roomvo is the common one). Put it in tool_evidence if you can tell.

=== RETURN THESE FIELDS ===

  icp_fit          IN, OUT, or REVIEW
  icp_reason       one sentence. If OUT, name which exclusion applied
  product_category what they actually sell, in three or four words
  product_medium   FLAT_2D, 3D, or MIXED   (informational, NOT a gate)
  product_type     CATALOGUE, CUSTOM, or BOTH
  business_role    MAKER, MAKER_AND_DISTRIBUTOR, DISTRIBUTOR, RETAILER,
                   or OTHER   (informational, NOT a gate)
  tool_level       ADVANCED, BASIC, MANUAL, or NONE
  has_tryon        yes or no
  has_prompt       yes or no
  tool_url         the exact URL of the tool or custom-offering page.
                   Required for ADVANCED, BASIC and MANUAL. Blank only for NONE
  tool_on_domain   yes if tool_url is on {{domain}} itself; no if it is on a
                   sibling brand site or another domain of the same group
  tool_brand       if tool_on_domain is no, which brand or company the tool
                   belongs to. Blank otherwise
  tool_evidence    one or two sentences quoting the site's own wording
  site_matches_company   yes or no

Do not guess. Never return a tool_url you did not actually open. You may
only return NONE after checking all seven places listed above, INCLUDING
trying the direct paths and, for a group, the brand sites.
```

## Why has_tryon and has_prompt matter more than tool_level now

Competitors already cover one half each (see `competitive_landscape.md`):
Roomvo, Daltile Stylizer and ~10 free vendors do try-on; **Mozaico does
prompt-to-mosaic**. Almost nobody does both, branded, on the client's own
domain, over the client's own catalogue.

So the segment that matters is **has_tryon = yes AND has_prompt = no** — a
company that has already paid for visualisation, proving budget and intent,
and is missing the half that is genuinely hard to buy elsewhere. That is a
far sharper cut than tool_level alone.

## The known-answer test

| domain | tool_level | must find |
|---|---|---|
| uniquedesignsolutions.com | ADVANCED | Mosaic Creator, in-room preview |
| onixmosaico.com | ADVANCED | Mosaic Creator app + 3D Rendering |
| marazziusa.com | ADVANCED | Stylizer **and** Stylizer AI |
| gruppobardelli.com | ADVANCED | MyMix, MyDegradè, MyCustom |
| quemeredesigns.com | ADVANCED | builder on a designyourown. subdomain |
| restorationtile.com | MANUAL | coloured pencils on paper templates |
| rookwood.com | MANUAL | designers draw it in CAD for you |
| mcintyretile.com | MANUAL | glaze recipes tested against a sample |
| marburg.com | NONE | search + EUR 1 samples only, no tool |
| grandecogroup.com | NONE | collections + inspiration only |

ICP controls, all of which must come back **OUT**: foncer.it (pension fund) ·
sigmaitalia.com (tile cutters) · sicer.it (glazes and inks) · insca.com and
polcart.it (showroom display stands) · norafin.de (technical nonwovens).

And two that must now come back **IN**, having been wrongly cut before:
aliceceramica.com and olympiaceramica.it (sanitaryware — 3D, and both already
have configurators).

Watch two for over-claiming: **quemeredesigns.com**, whose tool sits on a
subdomain outside the nav, and **marburg.com / grandecogroup.com**, which
genuinely have nothing. An ADVANCED on either of the last two silently kills
a good prospect.

## The comparability trap

The 95 rows already done were judged by domain-scoped web SEARCH, because this
environment 403s every external domain. Claygent renders pages, so it will
find tools search missed and the new batch will show a higher ADVANCED rate
for methodological reasons alone. Do not read that as a real difference
between tiers. Prefer re-running all candidates in one consistent pass; a
column produced two different ways cannot be segmented on.

## Keep off Claygent's plate

Revenue, employee count and headcount came back with the enrichment and cost
nothing to gate on.


## 10-row test results (16 Sept) — 8 clean, 1 misfiled, 1 real miss

Accuracy was good and the two ICP catches Claygent made unprompted were
correct: **ACIMAC** is the trade association for Italian ceramic machinery
makers, and **4Puntozero / I Love Parquet** is a registered journalism portal.
Both correctly OUT. **41zero42** came back NONE, which independently matches
the search-based research — two different methods agreeing on one row.

### Not an error: ABK

Reported ADVANCED, has_tryon yes, url `abk.it/it/configuratore`. Shahwaz
checked and could not find it. **Claygent was right.** ABK's Virtual Stylist
is live — it matches surfaces, colours and formats onto images of real rooms,
and a customer can upload a photo of their own space. There is a second Easy
Living Configurator too.

The confusion is that the row's domain is **abkgroup.it** (the parent) and the
tool is on **abk.it** (the brand). Hence the new `tool_on_domain` and
`tool_brand` fields: the finding was correct, it was just unfalsifiable from
the row as written.

### A real error: AB (Azulejos Benadresa) — FALSE NEGATIVE

Reported NONE, evidence "site navigation lists Company, Product, Downloads,
News, Contact; no customer-facing visualizer is identified."

**It has one, on its own domain:** `azulejosbenadresa.com/en/create3d/` — the
3D Superb program. Build your own 3D settings from the full tile range with
multiple laying options and furniture for bathrooms, kitchens, living rooms,
bedrooms and offices, in two versions, HOME for everyone and PRO restricted to
professionals. There is also `/3d/version-hogar/`.

Claygent read the top menu and stopped. `create3d` is not in it. This is the
expensive direction of error: it silently deletes a company from the A/B
cohort and would have had us open with "you have no design tool" to a company
that segments its tool by audience.

Same row also returned business_role DISTRIBUTOR; Benadresa is a Castellón
manufacturer. A second inaccuracy on the one row Claygent read least of.

### What to do

The nav-only read is the whole problem, and both rows are explained by it. The
revised Part 2 above makes the footer, the direct path guesses and the brand
sites mandatory before NONE is allowed.

**Re-run the 10 after the prompt change, and add `quemeredesigns.com`** — its
builder sits on a `designyourown.` subdomain outside the nav, so it is the
canary for exactly this failure. If Quemere and AB both come back ADVANCED,
the prompt is fixed. Then spot-check 10 of the NONE rows from the full run
before trusting that column, because NONE is now the value most likely to be
wrong.
