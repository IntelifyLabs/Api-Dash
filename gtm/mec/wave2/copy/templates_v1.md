# MEC / ShowHouse outreach — 3 template variants for review (16 Sept 2026)

Each variant is a **segment**, not a tone. The segmentation is what makes them
non-generic: the opening line is a quote or near-quote from that prospect's own
site, taken from the `Use AI Tool Evidence` column that qualifier 1 produced for
all 439 rows. Nothing here is reusable across segments.

Sender: Haroon. Cold, no LinkedIn touch has happened.

| Variant | Segment | `tool_level` | Reachable rows | Worked example |
|---|---|---|---|---|
| A | The manual loop | MANUAL | 34 | The Rookwood Pottery Co. |
| B | No design step | NONE / BASIC | 99 + 23 | Syzygy Tileworks |
| C | Half the tool | ADVANCED, tryon=yes, prompt=no | 57 | Ceramica Mayor |

---

## VARIANT A — THE MANUAL LOOP
**Who:** companies whose own site describes a human doing the visualising. CAD
drawings, posted sample books, glaze trials, coloured pencils on paper.
**Why it is the strongest cut:** they have already decided the customer needs to
see it before buying. They are paying staff to do it. No need to sell the idea,
only the method.
**Never:** call it automation of their craft. It replaces the drawing, not the kiln.

### Email 1
**Subject:** who draws the install before the order

Katelyn,

Your custom page says your designers use CAD to show a customer how the
installation will look in their home before they commit.

That is one person, a queue and a wait on every job. And your own words for the
catalogue are endless options from combining shapes, glazes and palettes, a
space nobody can draw twice.

We built the design engine behind MEC Artworks. Same picture, from your own
shapes and glazes, while the customer is still interested.

Want me to walk you through it?

### Email 2 (send day 4) — mechanism: do their manual step for them
**Subject:** your CAD step, done in about a minute

Katelyn,

Rather than describe it, I did your step.

I took three glazes and two shapes off your collections page and had the tool lay
out a floor in them. About a minute, and nobody opened CAD.

It is here: [render link]

It is not as good as your designer, and it is not meant to be. It is meant to be
the thing a customer sees on Tuesday instead of the following Monday, so your
designer only draws the jobs that are already sold.

What would you change about it?

### Email 3 (send day 9) — mechanism: hand off, or argue against yourself
**Subject:** possibly the wrong Rookwood person

Katelyn,

Two possibilities and I cannot tell which from out here.

One, this is not your call. If the website and the customer journey sit with
somebody else, say the word and I will send them the render instead of you.

Two, I have read your process wrong. If the CAD drawing is quick, or if it is
the part clients are actually paying for, then I have built an argument on
something that is not a problem, and you would be doing me a favour by saying so.

The render stays up either way. Yours to use if it is any good.

### Slot map
- `{observation}` the exact manual artefact, quoted from their site
- `{combinatorial_fact}` what makes their catalogue impossible to show flat
- `{cost_line}` the consequence in their terms, always time-to-approval
- `{render_inputs}` the named glazes, shapes or collection the render was built
  from. Must come off their own site, never invented
- `{render_link}` their page on `tryshowhouse.com`
- `{their_word_for_the_step}` CAD, sample book, glaze trial, pencils. Touch 3
  reverses on this exact word

### Same template, different prospect (first touch only)
**American Restoration Tile — Erin Oliver, erin@restorationtile.com**
**Subject:** the coloured pencils step

Erin,

Your Design Your Own page asks the customer to colour in blank hexagon and
square templates with pencils, or post you photographs to work from.

For a business that prices by pattern complexity, that is the slowest possible
way to reach a yes, and every extra round costs margin on a job already quoted.

We built the design engine behind MEC Artworks. The customer fills the same
templates on screen, in your real glaze colours, and you get a file instead of a
scan.

Worth a look?

---

## VARIANT B — NO DESIGN STEP
**Who:** the largest cut. Collections, downloads, a PDF catalogue, maybe filters.
The customer journey ends at a sample request or a contact form.
**Why it works:** the promise is already written on their site. They sell choice
and give the buyer no way to see it.
**Never:** say "you have no tool" as a fact. Qualifier 1 records NONE as *none
found*. Open on what they promise, not on what they lack.

### Email 1
**Subject:** any colour on any pattern, and nowhere to see it

Josh,

Your site says a customer can take a colour-way, change it to suit them, and put
it on any tile in any pattern.

That is a large promise to make in text. Nobody signs off on something they are
imagining, so they ask for a sample and the job slows to the speed of the post.

We built the design engine behind MEC Artworks. It renders a maker's own glazes
and shapes on screen, so the choice becomes something you look at.

Fifteen minutes to show you?

### Email 2 (send day 4) — mechanism: give away a fact they can use, then show the work
**Subject:** three of the four sites let them see it

Josh,

One thing worth having whether or not you ever reply to me.

Daltile runs a visualiser. Marazzi runs one. A lot of mid-size makers run Roomvo,
which is white-labelled, so it turns up under the maker's own name and a buyer
never knows it was bought in. When a designer is comparing four tile sites in an
afternoon, three of them let her see it and one asks her to imagine it.

I put four of your colour-ways on a hex layout to see how it reads on a screen:
[render link]

Twenty people hand-brushing glaze is the whole argument. It should not be the
part nobody sees.

### Email 3 (send day 9) — mechanism: no ask at all
**Subject:** the file, no strings

Josh,

I am not asking you for anything in this one.

The render from last week is yours. Put it on the colour-ways page, recrop it,
bin it. No attribution, no catch. It took a minute to make and it is worth more
to you than to me.

If you ever want the thing that made it sitting on syzygytile.com, you know where
I am. If not, that is a fine outcome too.

### Slot map
- `{promise}` the choice they advertise, quoted
- `{friction}` what the buyer does instead today: sample, quote form, PDF
- `{craft_fact}` the thing that must not sound automated
- `{competitor_line}` only where true. Daltile, Marazzi and Roomvo are verified
- `{render_link}` optional here. If no render was made, cut that line and the
  touch-3 giveaway becomes "here is the tool" instead of "here is the file"

### Same template, different prospect (first touch only)
**41zero42 — Frederic Ades, f.ades@41zero42.it**
**Subject:** the collection ends at a download

Frederic,

41zero42 builds collections with named designers and the visitor's last step on
the site is a downloads page.

A PDF is fine for a specifier who already knows the product. It does nothing for
the architect deciding between you and three other brands in the same week, and
that decision is made on a picture.

We built the design engine behind MEC Artworks. Your collections, rendered into
the client's own room photo, on 41zero42.com.

Can I show you?

---

## VARIANT C — HALF THE TOOL
**Who:** the 57 rows with `has_tryon = yes` and `has_prompt = no`. They bought
visualisation already. Budget and intent are proven.
**Why it is the sharpest cut on the list:** they cleared the hard objection
themselves. The missing half is the half that is hard to buy anywhere else.
**Never:** imply they lack a tool. Praise it first, honestly, then find its edge.

### Email 1
**Subject:** the pool that is not in the simulator

Eva,

Your Design Your Pool tool is better than most in this category. Real
combinations, real finishes, a preview that means something.

It answers a customer who wants something you already make. The one who arrives
with a picture in their head and no reference for it gets nothing back, and that
customer had the budget.

We built the design engine behind MEC Artworks. Someone describes the pool in
plain words and gets an original layout drawn from your own tiles.

Want to see it running?

### Email 2 (send day 4) — mechanism: use their own tool, and report where it stopped
**Subject:** I spent ten minutes in Design Your Pool

Eva,

I used your tool before I wrote to you the first time.

I tried to build one specific thing in it: [the exact request that hit the wall].
It will not do that, because it is built to arrange the tiles you already make
rather than invent an arrangement you have not made yet. That is not a fault, it
is what the tool is for.

Then I described the same pool in one sentence to ours: [render link]

Same tiles. A different question being answered. Yours answers which of these.
The other answers what if.

### Email 3 (send day 9) — mechanism: one line
**Subject:** one question

Eva,

Where does a customer go when Design Your Pool does not have what they came for?

That is the whole email.

### Slot map
- `{their_tool_name}` always the exact name: Design Your Pool, Roomviewer, Virtual Viewer, Stylizer
- `{honest_praise}` one true thing it does well
- `{edge}` the request it cannot serve
- `{domain}` used in email 2 to make the "stays on your site" point land
- `{the_wall}` **the single highest-value and highest-risk slot in the whole
  document.** The specific thing somebody tried to build in their tool and could
  not. It has to be real. Whoever fills it opens the tool, attempts one concrete
  request, and writes down where it stopped. If that has not happened, the row
  does not get this email

### Same template, different prospect (first touch only)
**Cotto d'Este — Matteo Iseppi, matteo.iseppi@cottodeste.it**
**Subject:** Roomviewer, and the request it cannot take

Matteo,

Roomviewer does the hard part well. Photograph the room, choose the surface, see
the result straight away.

It works from the collection. A specifier who wants a surface you have not made
yet, for a project that has to look unlike everyone else's, has nowhere to put
that request except an email to your team.

We built the design engine behind MEC Artworks for that request. Described in
words, rendered in your finishes.

Worth twenty minutes?

---

## Why the follow-ups are built this way

A follow-up that explains the product again is a bump wearing a hat. The reader
has already heard the argument. What they have not had is something arrive.

So every follow-up here is a **move**, not a paragraph. No message in this
document opens with "just checking in", "circling back", "bumping this" or "last
one from me". The breakup email is deliberately absent from all three variants,
because every prospect on this list has received forty of them.

| | Touch 2 move | Touch 3 move |
|---|---|---|
| A | Perform their manual step and send the result | Offer to hand off to the right person, or argue against your own case |
| B | Give away a competitive fact they can use, then show the render | Give the file away with no ask attached |
| C | Use their tool, hit its wall, report exactly where | One sentence, one question |

**The four moves worth keeping in the bank**, in order of how hard they are to
ignore:

1. **Do the work.** Arrive with the artefact instead of the offer. Only possible
   because the tool exists and their catalogue is public.
2. **Use their own tool and tell them what it would not do.** Requires ten real
   minutes and cannot be faked. This is the single least generic email available
   to this campaign.
3. **Remove the ask.** A message with nothing in it for the sender is the one
   people answer. It also costs nothing, because the artefact already exists
   from touch 2.
4. **Question your own premise.** "I may have read you wrong, tell me if I did"
   gets a correction, and a correction is a reply.

## What this costs to produce, honestly

These follow-ups are not free, and pretending otherwise would put the campaign
back where campaign 2 was.

- **Touch 2 for A and B needs one render per prospect.** Collection names, glaze
  names and shapes are on their site and already partly captured in
  `Use AI Tool Evidence`, so the input is cheap. The render is not zero.
- **Touch 2 for C needs somebody to actually open their tool.** Ten minutes a
  prospect. **Never invent the limitation.** If the wall in that email is made
  up and the reader knows their own product, the whole sequence is dead and so
  is the sender reputation. If nobody has time to open the tool, use a different
  touch 2.
- **Do not attach the render as a file.** Image attachments from a low
  reputation TLD are a filter pattern. Host each render on its own page and link
  it, as a per-prospect page under `tryshowhouse.com`.

**Tiering that makes this affordable:** run the artefact version on variant A
(34 reachable) and variant C (57), which is about 90 prospects and the two
highest-intent cuts on the list. For the long tail in variant B, keep move 3 and
move 4, which need no render at all, and drop the render line from touch 2.

## Rules these obey

1. **Four-block structure** (standing rule 13): verifiable observation from
   their own site, consequence in their terms, proof, low-commitment CTA.
2. **Honest-proof rule.** The only figures used are the two published for MEC:
   seven weeks, three people. No invented performance numbers, because the case
   study has none.
3. **"AI" is never the opening.** Daltile and Marazzi give a visualiser away
   free and Mozaico already ships text-to-mosaic. The feature is not the
   differentiator. What is: their own glazes, their own domain, and removing
   their specific manual artefact.
4. **No em dashes, no signature block, plain words, first touch under 90 words.**
5. **Competitor rule.** MEC Artworks is a mosaic house. No tile or mosaic
   prospect gets a link to `ai.mecartworks.com`. They get a walkthrough offer, or
   `tryshowhouse.com`, which carries no competitor's name.
6. **Links.** See the link policy below.

## Link policy: tryshowhouse.com

**Default: the link goes in touch 2, never touch 1, and never as the ask.**

**The touch-2 link is now a per-prospect page, not the homepage.** Every
follow-up above carries `[render link]`, which should resolve to something like
`tryshowhouse.com/r/rookwood`: their render on the page, and a button under it
that opens the tool with their palette already loaded. That is strictly better
than a bare homepage link. The reader lands on their own tile, not on a pitch,
and the domain is still the neutral one. `tryshowhouse.com` on its own stays as
the fallback wherever no render was produced.

Three reasons it belongs in touch 2 and not touch 1:

- A cold first email from `triminage.space` or `triminage.site` carrying a link
  to a third, unrelated domain is a textbook filter pattern. Those TLDs are
  already the campaign's known deliverability risk. Touch 2 goes to someone who
  received touch 1, so the first message has already proved placement.
- **The link cannot be the CTA.** The north star is replies and booked calls. A
  click is not a reply, and with open and click tracking off (correctly) it is
  not even measurable. So the link is evidence sitting next to the question, not
  a replacement for it. One ask per message still holds.
- Touch 1 is under 90 words and every word is doing work. The link buys nothing
  there that the observation does not already buy.

**Why tryshowhouse.com and not ai.mecartworks.com:** it carries no competitor's
name. MEC Artworks is a mosaic house, and most of this list is tile and mosaic.
ShowHouse is the only asset that can be sent to them safely. That is the single
biggest argument for attaching a link at all.

**Mechanics, all of which matter more than the copy:**
- Plain URL, no anchor text, no shortener, no UTM string.
- **Click tracking off in Instantly.** A tracking-domain redirect on a low
  reputation TLD is a far worse signal than the naked link.
- One link per email. No signature block, no social icons, no unsubscribe image.

**The one A/B worth running** (this is the open test in section 11): put the
link in touch 1 for **variant C only**. Variant C already makes a comparison
claim, and a comparison claim is only credible if the reader can check it. Those
prospects also own a visualiser, so they are the cohort most likely to click a
rival one. Variants A and B get no touch-1 link in either arm.

Touch-1 link arm for variant C, last two lines only:

> We built the design engine behind MEC Artworks. Someone describes the pool in
> plain words and gets an original layout drawn from your own tiles.
>
> It is running here if you want to try it: tryshowhouse.com
>
> Worth twenty minutes either way?

**Blocking check before any of this sends.** I still cannot load
tryshowhouse.com from here, so three things need eyes: that the page shows the
prompt half and not just the try-on half, that nothing behind it demands a
sign-up or a credit card, and that it loads on a phone. A dead or gated link in
touch 2 is worse than no link at all.

## Two things to decide before these scale

- **The offer is still unconfirmed** (section 7.10 Q2, open since August). These
  are written for licensed, embeddable tool access on the prospect's own domain,
  per the 24 Aug pivot. If it is a custom build at agency rates instead, the
  "seven weeks with three people" line becomes the pitch rather than a
  reassurance, and every CTA changes from "see it running" to "scope it".
- **`tryshowhouse.com` is quoted in variant C and I have not been able to load
  it.** Egress is blocked from here and it has no indexed pages. Before that line
  sends, someone needs to confirm the page actually shows the prompt half.
