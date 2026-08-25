# MEC — Claygent site-audit, Batch 4 (the 12 blocked rows + row 60 domain resolution)

Run 25 Aug 2026. Clears every outstanding item from the batch-3 "Still outstanding" list.
Row numbers = position among the 60 blank rows in
`MEC_Warm_Shortlist_Seed-Default-view-export-1787598276390.csv`, consistent with batches 1–3.

---

## ⚠️ METHOD CAVEAT — READ BEFORE USING THESE ROWS

Batches 1–3 were direct site visits. **Batch 4 was not.** These 13 rows were blocked in the
first place by 403 bot-walls, TLS failures and JS-only rendering, and the environment this pass
ran in blocks direct outbound HTTP to prospect domains entirely — every fetch returns
`403 CONNECT` at the egress proxy. Chromium was available; the network was not. A browser pass
was therefore impossible.

What was used instead: **web search against the indexed content of each company's own site**,
plus Companies House for row 60. Every finding below is sourced from the company's own pages or
a named third party, not inference.

**What that means field by field:**

| Field | Reliability |
|---|---|
| SITE_MATCH | **High** — business identity is unambiguous from indexed copy |
| CUSTOM_OFFERING | **High** — quoted from the company's own custom/bespoke pages, URLs given |
| **VISUAL_TOOL** | **LOW — this is the weak field.** A configurator is a live interactive element. Search indexes its landing page, not its behaviour. "None" here means *no tool page was found*, which is weaker than *no tool exists*. Four rows are marked unconfirmed |
| HOOK | **High** — direct quotes, but re-check freshness before send; some are press, not site copy |
| CLIENT_PROOF | **Medium** — "Not found" is weaker evidence here than in batches 1–3; named clients found are reliable |

**Honest-proof rule applies.** Nothing in the VISUAL_TOOL column should enter copy as a claim
about a prospect ("I noticed you don't have a visualiser…") until it has been eyeballed on the
live site. The other fields are safe to build on.

Status key: ✅ resolved · ⚠️ resolved with a caveat · 🅿️ parked niche (rugs / stained glass, per §7.4)

---

## Mosaic / Pool — ACTIVE NICHE

### 12. New Ravenna — newravenna.com ✅ **STRONGEST ROW IN BATCH 4**
SITE_MATCH: Match — custom stone and glass mosaics, Exmore VA, team of 100+ artisans
CUSTOM_OFFERING: Yes — fully bespoke projects alongside stock and private-label lines; "Made To Measure" custom-cuts selected patterns to exact project dimensions — /made-to-meaure/
VISUAL_TOOL: None found *(unconfirmed — /design-resources/ exists and was not reachable)*
HOOK: "Made to Measure" — patterns cut to exact dimensions so the design is "properly centered and proportioned, eliminating additional cuts or last-minute adjustments on site". Also live: repeated "New Ravenna Presents N Additions to the Studio Line" press releases — the §7.4 recently-launched-collection signal is firing
CLIENT_PROOF: Not found by name
> **Best-fit row in the entire blocked set.** Their stated custom process is a *human rendering loop*: the client sends "photographs, fabric swatches, drawings, magazine clippings" and the creative team renders it into a mosaic concept. That is the MEC pain verbatim — a manual concept-to-approval wait, staffed by people, at $10–25M revenue with 100+ artisans. Lead the mosaic segment with this one.

### 10. Mosaics Lab — mosaicslab.com ✅ *(= row 56 duplicate; delete row 56)*
SITE_MATCH: Match — contemporary custom mosaic art, artwork and tiles
CUSTOM_OFFERING: Yes — upload a photo or painting and have it recreated in stone; customizable by shape, colour, size and material — /custom-mosaics
VISUAL_TOOL: None found — the customisation path is a **free design consultation** with their interior designers and mosaic artists, i.e. a staffed manual loop *(unconfirmed)*
HOOK: "turn any photograph or design into a mosaic masterpiece" — upload-your-own, then a human renders it — /mosaicists.html
CLIENT_PROOF: Not found
> Keep. Same manual-loop shape as New Ravenna, smaller ($1–5M). The free design consultation is the cost centre a configurator removes.

### 11. Blue Water Pool Mosaics — poolmosaics.com ✅
SITE_MATCH: Match — pool mosaics and tile, 20+ years in the pool/spa industry
CUSTOM_OFFERING: Yes — custom logos, sports mascots, family crests, bespoke designs — /custom-mosaics/
VISUAL_TOOL: None customer-facing — but note their own copy: "combined with the latest in **computer design software**, their experienced ceramic artists work with you step-by-step". The software exists and is **staff-operated**, not customer-facing *(unconfirmed)*
HOOK: "the leader in custom pool mosaic creation"; the step-by-step artist collaboration; also "Bespoke Pool Mosaic Tile Art: What Sets Custom Work Apart" — their own blog post arguing the value of custom work
CLIENT_PROOF: Not found
> Keep. The strongest *stated* version of the pain in batch 4 — they advertise the human step-by-step loop as a feature. Revenue blank in Clay; verify before enrichment.

### 14. Oceanside Glasstile — oceansideglasstile.com ⚠️
SITE_MATCH: Match — luxury glass tile manufacturer, founded 1992, recycled bottle glass
CUSTOM_OFFERING: Yes — Oceanside Glass Special Order Program (customisable mosaic tile, submersible-rated); plus "Uniquely Oceanside", a collaboration with Unique Design Solutions to customise pool tile before it ships
VISUAL_TOOL: None found *(unconfirmed)*
HOOK: "up to 85% recycled bottle glass"; and their combinatorial pitch — all product lines share consistent colours so liners, decos and trim from different lines combine for "unlimited possibilities". That sentence is a configurator use-case described in prose
CLIENT_PROOF: Not found
> **COUNTRY CORRECTION CONFIRMED — third time.** Founded in Oceanside, factory in **Carlsbad, California**. The `GB / Banbury` enrichment is wrong. Fix `Country` to **US** in the file, not just in the notes — this error has now survived two documented corrections (§7.2, §7.5) because it keeps coming back in fresh Clay exports.
> **Caveat:** significant sales run through Daltile special-order and independent distributors. Some of the design conversation may sit with the channel, not with them. Keep, but not lead.

## Decorative / Artisan Tile — ACTIVE NICHE

### 26. North Prairie Tileworks — handmadetile.com ✅
SITE_MATCH: Match — handmade tile since 1992, **St. Paul, MN** (684 Transfer Road)
CUSTOM_OFFERING: Yes — "over 150 custom electric and gas-fired glaze colors, custom decorative relief tiles, original and made-to-order designs"; works directly with designers, architects and homeowners
VISUAL_TOOL: None — the site is a static PHP/HTML build (`/glaze.html`, `/relief_flora.php`) served over plain **http**. Almost certainly no internal design tooling at all
HOOK: restoration and replication credits — Minnesota and Kansas State Capitols, Harvard University, Hoover Dam visitor center, the American Swedish Institute, New Jersey DOT — /restore.html
CLIENT_PROOF: Yes — the named institutions above
> Keep. Passes the restoration-only exclusion: they do original and made-to-order design alongside replication. **Old static site on http is the opening** — same play as US Vinyl (row 57). Note the http-only serving for the sending list; the TLS mismatch that blocked the original pass is real, not transient.

### 27. Sonoma Tilemakers — sonomatilemakers.com ⚠️
SITE_MATCH: Match — handmade tile, Windsor CA, operating since 1994, "over 30 years"
CUSTOM_OFFERING: **Unclear** — extensive *selection* (12 collections, 100+ colours, multiple glaze types, field/deco/trim pieces) but no explicit custom-design programme surfaced. Breadth of catalogue ≠ customer design input
VISUAL_TOOL: None found *(unconfirmed)*
HOOK: sustainability — conscious clay sourcing, a custom water-recycling system, solar energy
CLIENT_PROOF: Not found
> **Boundary case — same shape as Zia Tile (row 51).** Two-tiered dealer distribution (Virginia Tile, Tile X Design, Creative Tile Imports, Ceramic Tile Design all resell them) means the design conversation may sit with dealers, not the manufacturer. **Revenue discrepancy:** Clay says 25M–75M; D&B/Zippia put peak revenue at **$10.6M (2024)**. Clears the $1M gate either way, but the band in the file is inflated — do not use it for prioritisation. Keep, low priority, and decide it with the same rule as row 51.

### 34. RTK Studios — rtkstudios.com ✅
SITE_MATCH: Match — custom tile, Ojai CA; Malibu Potteries, Catalina Tile and Cuerda Seca traditions
CUSTOM_OFFERING: Yes — "decorative tile and murals available in stock as well as **custom design services**, serving clients worldwide". Custom orders start at 100 pieces
VISUAL_TOOL: None — static catalogue and product pages — /catalog
HOOK: hand-glazed cuerda seca revival work; the studio is the hands of two named principals, Richard Keit and Mary Kennedy — "bringing old world traditions alive"
CLIENT_PROOF: Not found (Houzz and gallery presence only)
> Keep, **but verify revenue.** A two-principal studio; Clay's $1–5M band is plausible for this vertical (cf. Tabarka in §7.3) but unverified. The 100-piece custom minimum is a tell: custom work is gated because it is expensive to quote — exactly the friction the tool addresses.

## Murals & Wallpaper — ACTIVE NICHE (in scope per the 24 Aug pivot)

### 4. Fancy Walls — fancywalls.eu ✅ **BEST STRATEGIC FIT FOR THE PIVOT**
SITE_MATCH: Match — premium wallpaper and murals, print-on-demand, founded 2018, printed in the EU
CUSTOM_OFFERING: Yes — "Custom Wallpaper | Your Design, Our Print" (upload your own file, checked for print quality) — /wallpaper/custom/; every piece made to order and custom-sized; 3,400+ designs with colour customisation
VISUAL_TOOL: Basic, possibly more *(unconfirmed — needs eyes)* — their mural flow lets the customer "position the artwork and select the section of the design you want to feature", which is a preview interaction, not a static picker
HOOK: **"Wallpaper Dropshipping | Private Label, 1–2 Day Turnaround"** — /peel-and-stick-wallpaper-wholesale/. They already run a white-label programme for other businesses
CLIENT_PROOF: Not found
> **Keep, and read this one carefully.** §7.4's pivot thesis is selling MEC's engine as an *embeddable/white-label configurator a business offers its own customers*. Fancy Walls **already sells white-label wallpaper to other businesses.** They are a company whose existing business model is licensing their capability onward — the pivot pitch needs no explaining to them. Only in scope at all because of the 24 Aug pivot (pure POD would have been excluded under the old ICP), which makes it the clearest single test of whether the pivot was right.
> Note: EU-based (Latvia) — GDPR applies, so LinkedIn-first per §7.8.

## Custom Rugs — 🅿️ PARKED NICHE

*Audited for completeness. Do not send until Abdullah confirms the engine renders these mediums.*
*Batch 4 changes the picture here substantially — see the correction at the end.*

### 39. The Rug Company — therugcompany.com 🅿️ ⚠️ **\*\*\* ADVANCED TOOL \*\*\***
SITE_MATCH: Match — luxury handmade rugs, designer collaborations, internationally recognised
CUSTOM_OFFERING: Yes — /custom-bespoke/ and /bespoke-rugs/; upload images, references or inspiration and the in-house studio develops an original design; colour, size and shape customisation
VISUAL_TOOL: **Advanced** — the "Custom Rug Designer", a virtual portal launched June, at **us.therugcompany.com/build-your-own/**. 100+ best-selling rugs, customise colour and size, spanning the Kelly Behun, Diane von Furstenberg and Kelly Wearstler collections *(confirmed by third-party coverage in Galerie Magazine, not just their own copy)*
HOOK: designer collaborations — Diane von Furstenberg's Climbing Leopard, Alexander McQueen's Monarch, Alexandra Champalimaud's Stingray
CLIENT_PROOF: The named fashion houses and designers above
> Already has the product. Per the §7.4 signals table this is "proven willingness to buy — a different angle, **not a rejection**." The angle: their tool covers 100+ existing designs but a human design team still handles anything bespoke, at 16–24 weeks for handknotted. The gap is the bespoke path, not the catalogue path.

### 41. Rug Artisan — rugartisan.com 🅿️ **\*\*\* ADVANCED TOOL \*\*\***
SITE_MATCH: Match — custom area rugs in any size, shape, design and colour
CUSTOM_OFFERING: Yes — /bespoke; custom shapes down to "a diamond shape to a random amoeba shape"; "our custom rug designers will create a custom rug design as per your specifications and send it to you **for your approval**"
VISUAL_TOOL: **Advanced** — their own copy calls it "innovative and easy-to-use **customization software**": a custom colour library, ~300 pre-set colour combinations per design, texture selection, shape and size pickers — /personalise.html
HOOK: "around 300 pre-set colour combinations to choose from for each custom rug design"
CLIENT_PROOF: Not found
> **Lowest need in the entire audit.** They have built essentially what MEC sells. Deprioritise even if rugs unpark. Domain note for the sending list: both `rugartisan.com` and `rugartisan.eu` are live, and `/personalise.html` sits on the `.eu` and `new.` subdomains — confirm which domain the decision-maker's email uses.

### 42. The Perfect Rug — theperfectrug.com 🅿️ ✅
SITE_MATCH: Match — custom-sized rugs, founded 2010 "when customers were tired of standard rug sizes"
CUSTOM_OFFERING: Yes — /shop-custom-area-rugs, selecting size, material, colour and border; 1,000+ material options; unusual shapes (oval, octagonal, L-shape)
VISUAL_TOOL: Basic, possibly more *(unconfirmed)* — the custom shop is a structured size/material/colour/border picker, and a separate "PerfectFit" page — /perfectfit — suggests a sizing aid
HOOK: "custom-made rugs at reasonable everyday prices rather than custom prices"; free design consultations; 15-business-day production
CLIENT_PROOF: Not found — Trustpilot reviews and an /our-customers page, no named projects
> Keep (parked). Free design consultations are the manual loop. Middling fit — their pitch is *cheap* custom, so a paid tool licence has to argue margin, not speed.

## Stained Glass — 🅿️ PARKED NICHE

### 45. Willet Studios — willet-studios.com 🅿️ ✅
SITE_MATCH: Match — Willet Hauser Architectural Glass, Winona MN. Design, fabrication, preservation and restoration of leaded and faceted stained glass
CUSTOM_OFFERING: Yes — "bespoke stained glass for religious, public, and commercial environments, uniting craftsmanship with architectural clarity" — /studio-locations/
VISUAL_TOOL: None — static project galleries — /projects
HOOK: "created and/or restored windows in **more than 15,000 buildings**" worldwide; formed by the 1977 merger of Willet (Philadelphia) and Hauser (Winona); one of the largest stained glass studios in North America; four studio locations
CLIENT_PROOF: Contemporary Office Install and the project portfolio; the 15,000-building claim
> Keep (parked). Passes the restoration-only exclusion — new commissions sit alongside restoration, same as Judson (row 44). At $10–25M this is the **largest stained-glass prospect in the file**. If the niche unparks, Willet and Judson lead it together.

## Ceramic Tile — row 60 domain resolution

### 60. Jill Campion Handmade Tile Ltd — jillcampion.com ✅ **DROP**
DOMAIN RESOLVED — and the row does not survive it.
- Companies House **02699570**: status **Active**, incorporated 23 March 1992, SIC "other manufacturing not elsewhere classified". Last accounts to 30 June 2024, next due 31 March 2026
- Registered office: **34 Gough Way, Cambridge CB3 9LN** — a residential address, **not Staffordshire**. A Cylex listing places activity at Ayot St Lawrence, Hertfordshire
- The "Heritage ceramics, handmade in Staffordshire" text in the file's `niche` column is **not corroborated by any primary source** — treat it as Clay filler, not fact
- Live presence appears to be Instagram (@jillcampiontile), not the dead domain
> **DROP on three counts:** revenue band 500K–1M **fails the §7.4 $1M floor**; the website is dead (404 on apex and www, so nothing to audit and no hook to quote); and the company profile is a micro-operation run from a home address. No further work needed — this closes the last open item from batch 3.

---

# ⚠️ CORRECTION TO BATCH 3 — row 43, Jubi Rugs

Batch 3 called Jubi **"the strongest row in batch 3"** and recorded `VISUAL_TOOL: Basic`, building
the case on the premise that "The Rug Plan" is *"a **manual** human design-consult loop — a free
service they staff by hand… exactly the workflow an embeddable configurator replaces."*

**That premise is wrong. Jubi already has the configurator.**

`shop-jubi.com/pages/rug-customizer` is an online customizer: choose a design, customise colours
from **1,200 shades**, set the size, and — their words — "preview and adjust colours and sizes
**in real time**". Any design in the collection can be customised in it; the studio handles only
what exceeds the tool.

**Consequences:**
1. Row 43 `VISUAL_TOOL` changes **Basic → Advanced**. Running total of advanced tools found across the audit goes from 4 to **7** (Instabilelab, Bisazza, Fireclay, Popham, + Jubi, The Rug Company, Rug Artisan).
2. Jubi is **not a drop** — §7.4 treats an existing configurator as proven willingness to buy — but the hook inverts completely. "You're doing this by hand" would have been factually wrong in a first touch, to the best-researched name on the parked list. This is precisely the failure the honest-proof rule exists to prevent.
3. **All three rug rows audited in batch 4 have advanced configurators too** (39, 41, and now 43). That is not a coincidence: **custom rugs is a vertical that has already adopted this tooling.** Rugs looked like the strongest parked niche on batch 3's evidence. On batch 4's evidence it is the **weakest**, because the pain is already solved there.
4. **This changes what Abdullah should be asked.** §7.10 Q3 currently asks only whether the *engine renders* rugs and stained glass. Rendering is no longer the binding constraint for rugs — market saturation is. Stained glass, by contrast, shows **zero** configurators across three audited rows (44 Judson, 46 Franklin, 45 Willet) despite all three doing bespoke commission work. **If a parked niche unparks, the evidence now favours stained glass over rugs.**

---

# Batch 4 summary

| Verdict | Rows |
|---|---|
| **Keep — active niche** | 4 Fancy Walls · 10 Mosaics Lab · 11 Blue Water Pool Mosaics · 12 New Ravenna · 14 Oceanside Glasstile · 26 North Prairie Tileworks · 34 RTK Studios |
| **Keep — active, low priority** | 27 Sonoma Tilemakers (dealer-channel boundary case, same rule as row 51) |
| **Keep — parked niche** | 39 The Rug Company · 42 The Perfect Rug · 45 Willet Studios |
| **Keep — parked, deprioritise** | 41 Rug Artisan (already has an advanced configurator) |
| **Drop** | 60 Jill Campion (fails $1M gate, dead site, micro-operation) |

**Advanced visual tools found in batch 4: 2** — The Rug Company (39), Rug Artisan (41).
**Plus 1 correction:** Jubi (43), Basic → Advanced.
**Running total across all four batches: 7** — Instabilelab (8), Bisazza (18), Fireclay (19),
Popham Design (37), Jubi (43), The Rug Company (39), Rug Artisan (41).

## Data corrections to apply to the CSV

| Row | Field | From | To |
|---|---|---|---|
| 14 | Country | `GB` | `US` (Carlsbad, California) — **third time flagged** |
| 26 | Locality | Minneapolis | St. Paul, MN |
| 27 | Annual Revenue | `25M-75M` | ~`10M-25M` — D&B/Zippia peak $10.6M (2024). Clay band inflated |
| 43 | Use AI Visual Tool | `Basic` | `Advanced` — see correction above |
| 56 | — | — | **Delete** (duplicate of row 10) |
| 60 | verdict | pending | **DROP** |

## Outstanding after batch 4

**Zero blocked rows.** All 60 rows of the warm shortlist are audited.

Remaining open items are judgment calls and re-checks, not missing data:

| # | Item | Owner |
|---|---|---|
| 1 | **VISUAL_TOOL needs an eyeball pass on 4 rows** before any copy references it — 4 Fancy Walls, 12 New Ravenna, 27 Sonoma, 42 The Perfect Rug. Do this from an unrestricted network | Shahwaz |
| 2 | Catalog-only boundary rule — decide **once** for rows 51 (Zia) and 27 (Sonoma) and apply to every future catalog row | Shahwaz |
| 3 | Revenue verification on 11 Blue Water (blank) and 34 RTK (unverified band) | Enrichment |
| 4 | Row 59 Bigmural — re-check ~8 Sept 2026 (site rebuild in progress; the rebuild is itself a buying signal) | Calendar |
| 5 | §7.10 Q3 to Abdullah should be **re-framed** — for rugs the question is no longer rendering but saturation; stained glass is the better unpark candidate | Shahwaz |
