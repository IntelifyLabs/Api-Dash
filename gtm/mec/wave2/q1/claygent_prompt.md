# Claygent prompt — qualifier 1 (ICP fit + existing design tool)

Revised 15 Sept after Shahwaz confirmed: **catalogue sellers AND custom/
made-to-order sellers both qualify.** The product does try-on against the
company's OWN catalogue as well as generation from a customer prompt, so a
fixed-SKU catalogue is no longer a disqualifier - it is a use case.

## This materially reopens the OUT pile

The category gate cut 288 of 576 on the old rule. Under the new rule roughly
**107 of those come back**:

| Cut reason | Rows | Under the new rule |
|---|---|---|
| commodity volume (large fixed-SKU producer) | 63 | **back in** - a catalogue is now a use case |
| middleman (distributor / importer / retailer) | 12 | **back in** - they have a catalogue to try on |
| hand-verified gate-3 fails from 14 Sept | ~32 | **back in** - same reason |
| wrong business (magazine, machinery, chemicals, pension fund, association, tools, software) | 76 | stays out |
| wrong medium (sanitaryware, furniture, pottery, wood/vinyl/carpet, raw stone) | 60 | stays out |
| revenue under $1M | 17 | stays out |
| wrong company | 1 | stays out |

**Candidates go from 288 to about 395.** The two gates that still bite are
MEDIUM (the engine renders flat 2D patterns) and NOT-A-PRODUCT-COMPANY.

## Run order

1. Run on the ~395 candidates. Skip the ~181 that still fail medium, business
   or revenue - those are settled from free text (standing rule 1).
2. Test the 10 known-answer rows below first (standing rule 4).
3. See "the comparability trap" at the end before segmenting the results.

## The prompt

```
Visit {{domain}}. Answer two questions about {{company}}: does it fit our
ICP, and does it already have a customer-facing design tool.

We sell an AI design tool for FLAT 2D SURFACE products. It does two things:
customers try a product on a photo of their own room, and customers describe
an idea in words and the tool generates an original pattern from it.

=== PART 1: ICP FIT ===

A company fits if BOTH are true:
  a) it sells a FLAT 2D SURFACE product under its own brand or catalogue -
     tile, mosaic, ceramic, porcelain, stone tile, terracotta, cement tile,
     wallpaper, wallcovering, murals, panels, flat decorative surfaces
  b) a customer CHOOSES something - either from a catalogue of designs, or as
     a custom / bespoke / made-to-order piece. EITHER ONE QUALIFIES.

Important: a plain fixed-catalogue business DOES qualify. So does a
distributor, importer or retailer that sells a catalogue under its own site.
Do not mark them out for being catalogue-only or for not manufacturing.

A company does NOT fit if any of these is true:
  - the product is 3D, not a flat surface: sanitaryware, WCs, basins, baths,
    taps, shower trays, furniture, kitchens, worktops, countertops, tableware,
    pottery vessels, vases, mouldings, frames, profiles, trims
  - the surface is not a designed pattern: raw stone blocks or slabs,
    quarrying, paintable or woodchip wallpaper, plain nonwovens, wood,
    parquet, laminate, vinyl, LVT, SPC, carpet, rugs
  - it is not a product company at all: trade magazine, publisher, trade
     association or promotion body, trade fair, pension fund, consultancy,
     machinery or plant maker, tool maker, adhesive / grout / glaze / ink /
     pigment supplier, showroom display or stand maker, software vendor
  - it only installs, lays or fabricates and sells no product of its own

=== PART 2: DO THEY ALREADY HAVE THE TOOL ===

Check these places specifically:
- the main navigation, and any "tools", "design", "inspiration" or
  "professionals" section
- a separate SUBDOMAIN or standalone app (e.g. design.example.com,
  designyourown.example.com) - tools are often not in the main nav
- product pages, which sometimes embed a picker or a room preview
- anything named visualizer, visualiser, configurator, simulator, creator,
  studio, lab, 3D, "design your own", "create your own", or an AI feature

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

Rules:
- Cookie banners often contain a "Configure" button. That is NOT a tool.
  Ignore it.
- In tile marketing "3D" usually means a RELIEF SURFACE, a textured product,
  not a 3D room tool. Only count 3D if the customer can manipulate a view.
- BIM / CAD asset libraries and downloadable 3D models are for specifiers,
  not customers. That is BASIC, not ADVANCED.
- If the tool needs the customer to already HAVE an image (upload your photo,
  send us your artwork), say so in the evidence. It matters to the pitch.
- If the site does not load, is parked, or belongs to a different business
  than the name suggests, return icp_fit OUT and say that in icp_reason.

=== RETURN THESE FIELDS ===

  icp_fit          IN or OUT
  icp_reason       one sentence. If OUT, name which exclusion above applied
  product_medium   FLAT_2D, 3D, or MIXED
  product_type     CATALOGUE, CUSTOM, or BOTH
  business_role    MAKER, MAKER_AND_DISTRIBUTOR, DISTRIBUTOR, RETAILER,
                   or OTHER  (informational, not a disqualifier)
  tool_level       ADVANCED, BASIC, MANUAL, or NONE
  tool_url         the exact URL of the tool or custom-offering page.
                   Required for ADVANCED, BASIC and MANUAL. Blank only for NONE
  tool_evidence    one or two sentences quoting the site's own wording
  site_matches_company   yes or no

Do not guess. If you cannot find a tool after checking the places listed
above, return NONE. Never return a tool_url you did not actually open.
```

## The 10-row accuracy test - known answers

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

Also worth adding as ICP controls, all of which must come back **OUT**:
foncer.it (pension fund) · sigmaitalia.com (tile cutters) · sicer.it (glazes
and inks) · insca.com (showroom display stands) · aliceceramica.com and
olympiaceramica.it (sanitaryware) · erfurt.com (paintable woodchip wallpaper,
no pattern) · norafin.de (technical nonwovens).

Two rows to watch for over-claiming: **quemeredesigns.com**, whose tool is on
a subdomain and not in the nav, and **marburg.com / grandecogroup.com**, which
genuinely have nothing. An ADVANCED on either of those last two is the
expensive failure, because it silently kills a good prospect.

## The comparability trap

The 95 rows already done were judged by domain-scoped web SEARCH, because this
environment 403s every prospect domain. Claygent renders pages, so it will
find tools search missed and the new batch will show a higher ADVANCED rate
for purely methodological reasons. Do not read that as a real difference
between tiers.

Either re-run Claygent on just the 43 "none found" rows, or re-run all
candidates in one consistent pass. Prefer the second: a column produced two
different ways cannot be segmented on, and segmenting on it is the point.

## Keep off Claygent's plate

Do not ask it for revenue, employee count or headcount. Those came back with
the enrichment and cost nothing to gate on.
