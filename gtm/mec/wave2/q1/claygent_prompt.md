# Claygent prompt — qualifier 1, part B (existing design tool)

## Why Claygent and not the search method

The 95 rows already done were judged by domain-scoped web SEARCH, because the
run environment 403s every prospect domain. That carries the §7.5 defect:
search indexes a tool's landing page, not its behaviour, so "none found" is
evidence, not proof. Claygent renders the page. Use it.

## Run order (standing rules 1 and 4)

1. **Do not run on all 576.** 288 already failed the category gate on free
   text. Credits on those are wasted (standing rule 1).
2. **Run the 10-row test first** — but use the rows below, not random ones.
   They have known answers from the 104 already researched, so the test
   measures ACCURACY, not just that the column populates.
3. Then run the 193 unresearched candidates.
4. Then consider re-running the 104 (see "the comparability trap" below).

## The 10-row accuracy test — known answers

| domain | expected | must find |
|---|---|---|
| uniquedesignsolutions.com | ADVANCED | Mosaic Creator, in-room preview |
| onixmosaico.com | ADVANCED | Mosaic Creator app + 3D Rendering |
| marazziusa.com | ADVANCED | Stylizer **and** Stylizer AI |
| gruppobardelli.com | ADVANCED | MyMix, MyDegradè, MyCustom |
| quemeredesigns.com | ADVANCED | builder on designyourown. subdomain |
| restorationtile.com | MANUAL | coloured pencils on paper templates |
| rookwood.com | MANUAL | designers draw it in CAD for you |
| mcintyretile.com | MANUAL | glaze recipes tested against a sample |
| marburg.com | NONE | search + €1 samples only, no tool |
| grandecogroup.com | NONE | collections + inspiration only |

If it misses Quemere (tool sits on a subdomain) or Marazzi's AI tool, the
prompt is not aggressive enough about looking beyond the main nav.
If it returns ADVANCED for Marburg or Grandeco, it is over-claiming — the
most expensive failure here, because it kills a good prospect.

## The prompt

```
Visit {{domain}} and decide whether this company already offers its CUSTOMERS
a way to design or visualise a product before ordering.

Look for, and check these places specifically:
- the main navigation, and any "tools", "design", "inspiration" or
  "professionals" section
- a separate SUBDOMAIN or standalone app (e.g. design.example.com,
  designyourown.example.com) — tools are often not in the main nav
- product pages, which sometimes embed a picker or a room preview
- anything named visualizer, visualiser, configurator, simulator, creator,
  studio, lab, 3D, "design your own", "create your own", or an AI feature

Classify into exactly one of these four values:

ADVANCED - a working tool the customer drives: places the product in a room
  or on an uploaded photo, OR composes a pattern/blend/colourway and previews
  the result. Includes AI styling tools.
BASIC - only filtering or picking: search filters, a swatch or colour finder,
  a style quiz, a size/quantity calculator, a static palette page, a
  downloadable catalogue. No composed preview.
MANUAL - a real custom/bespoke offering that is delivered by PEOPLE: email or
  form enquiry, a rep or account manager, a design consultation or meeting,
  staff-made CAD drawings or layout simulations, posted sample books, physical
  templates, glaze or colour trials.
NONE - no design tool and no stated custom offering. Catalogue only.

Rules:
- Cookie banners often contain a "Configure" button. That is NOT a tool.
  Ignore it.
- In tile marketing "3D" usually means a RELIEF SURFACE (a textured product),
  not a 3D room tool. Only count 3D if the customer can manipulate a view.
- BIM/CAD asset libraries and downloadable 3D models are for specifiers, not
  customers. That is BASIC, not ADVANCED.
- If the tool needs the customer to already HAVE an image (upload your photo,
  send us your artwork), say so in the evidence — it matters to the pitch.
- If the site does not load, is parked, or is a different company than the
  name suggests, return NONE and say that in the evidence.

Return these fields:
  tool_level   one of ADVANCED, BASIC, MANUAL, NONE
  tool_url     the exact URL of the tool or custom-offering page. Required for
               ADVANCED, BASIC and MANUAL. Leave blank only for NONE.
  tool_evidence  one or two sentences quoting the site's own wording
  custom_offering  yes or no — does the site anywhere offer custom, bespoke,
               made-to-order or personalised product?
  site_matches_company  yes or no — does the site belong to {{company}}, or is
               it a different business with a similar name?

Do not guess. If you cannot find a tool after checking the places listed
above, return NONE. Never return a tool_url you did not actually open.
```

## The comparability trap — read before analysing results

The 95 done rows and the 193 new rows will have been judged by two DIFFERENT
methods. Claygent renders pages, search does not, so Claygent will find tools
search missed. Expect the 193 to come back with a higher ADVANCED rate for
purely methodological reasons.

**Do not conclude from that that the C/REVIEW tier is better tooled than the
A/B tier.** It is a measurement artefact.

Two options:
- Cheap: treat the 43 "NONE found" rows in the done set as unconfirmed, and
  re-run Claygent on those 43 only.
- Clean: re-run all 297 candidates through Claygent for one consistent pass.
  The 104 already done then act as a free accuracy benchmark, which is what
  standing rule 4 asks for and rarely gets.

I would spend the credits on the clean option. A tool_level column that was
produced two different ways cannot be segmented on, and segmenting on it is
the entire reason for building it.

## What NOT to ask Claygent

Do not ask it for revenue, employee count, or whether they are a maker vs a
distributor. The category gate already answered those from the enrichment
text at zero cost, for all 576 rows. Keep Claygent on the one question that
genuinely needs a browser.
