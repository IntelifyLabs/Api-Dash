# Round 3 sources: closed, 6 Oct 2026

Two of the four verticals that round 2 set out to cover. Closed on
Shahwaz's call, not because the other two were exhausted.

| Vertical | Source | Outcome |
|---|---|---|
| Furniture & joinery | Salone del Mobile 2026 | **846 companies** |
| Wallpaper & murals | Heimtextil 2027 | **468 rows**, 45 into `/wallpaper` and `/rugs` |
| Countertops & surfaces | Marmomac 2026 | **failed**, see `marmomac/DECISION.md` |
| Gardens & landscaping | spoga+gafa | **not attempted** |

**1,314 companies assembled. 844 take, 272 review, 198 excluded.**

## What closing here costs

Two studios have no campaign behind them and will not get one in this round:

- `/countertops` — 4 companies. Marmomac was the obvious source and it is a
  supply-chain fair: quarries, processors, tool and machinery builders selling
  to each other, almost nobody with a consumer website for a visualiser to sit
  on. Six halls read, 562 companies, zero prospects. Natural Stone Institute
  membership or KBIS would be the next places to look.
- `/gardens` — 2 companies. spoga+gafa is the source and it was never
  attempted. It also needs its own copy first: the bodies open on "your site
  shows the collections well, and then the visit ends at a catalogue", which
  fits an outdoor furniture brand and does not fit a landscaper, who quotes
  jobs rather than selling from a catalogue.

Both are reopenable. Neither blocks the round.

## What it simplifies

Copy work for round 3 is three studios, not seven: `/furniture` for 799 rows,
`/rugs` for 30, `/wallpaper` for 15.

## Order from here

1. **Classifier rewrite.** Free, and it blocks everything. `R_3D` currently
   reads "furniture or 3D ceramics. Engine renders flat patterns only" and
   would cut all 799 furniture rows. Running enrichment before this means
   paying for rows the classifier then discards.
2. **Copy** for furniture, rugs, wallpaper.
3. **Enrichment**, last, so credits only land on rows that survived. Domains
   and company emails came free from both APIs, so this is person-level only.
