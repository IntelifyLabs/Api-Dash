# -*- coding: utf-8 -*-
"""Per-prospect outreach copy for the MEC Artworks AI campaign.

Keyed by work email. Each entry: three unique subject lines and three email
bodies (first touch + two follow-ups). Every observation is drawn from that
company's own site copy or their contact's job title, per the honest-proof rule.

Sender: Haroon. Cold — no LinkedIn touch has happened, so no message references one.
Competitor rule: MEC Artworks is a mosaic house. Prospects in mosaic/tile name MEC
up front and are offered a walkthrough instead of a link to a competitor's tool.
"""

COPY = {}

def add(email, s1, e1, s2, e2, s3, e3):
    COPY[email] = dict(s1=s1, e1=e1.strip(), s2=s2, e2=e2.strip(), s3=s3, e3=e3.strip())

# ─────────────────────────── MURALS & WALLPAPER ───────────────────────────

add("stacy@limitlesswalls.com",
 "the customer who has nothing to upload", """
Stacy,

Your "GO CUSTOM!" flow is one of the better ones I've seen — upload, crop, resize, live pricing, done.

It only helps the customer who already has the image. The ones who know they want "something botanical, muted, for a north-facing room" have nothing to drop in the box, so they leave.

We built the AI studio MEC Artworks runs. That customer describes it in words, gets an original design back, then sees it on a photo of their own wall.

Want me to send you a walkthrough?
""",
 "when there's nothing in the box", """
Stacy,

The specific bit: someone types "brushed sage, large-scale botanical, low contrast" and gets an original mural concept — not a stock search result. Then they upload the room and see it hung.

For Limitless that's the top of the funnel your crop tool can't reach: the visitor with an idea and no file.

It's live at ai.mecartworks.com — email code, five previews, no subscription.

Two minutes tells you if it fits.
""",
 "how do you convert the no-image visitor?", """
Stacy,

Last note from me.

If you're already converting the no-image visitor some other way, I'd genuinely like to hear how — that's the hard half of custom.

If not, ai.mecartworks.com is the working example.

Either way, your custom flow is better than most of what's out there.
""")

add("tim@megaprint.com",
 "the step before the 48-inch panels", """
Tim,

MegaPrint prints removable custom wallpaper on 48-inch panels, two to three week turnaround, and the customer supplies the artwork.

That last part is the filter. A business that knows it wants a branded wall but has no file and no designer never reaches your order form.

We built the AI studio MEC Artworks runs. It closes that gap: describe the design in plain words, get an original concept, see it on a photo of the actual space.

Want me to run your own lobby through it and send you the result?
""",
 "before the artwork file exists", """
Tim,

The specific: it isn't stock search. Someone types "industrial, muted teal, hop vines" and gets an original design, then drops it into a photo of their space.

For MegaPrint that's the customer who currently never arrives — the one with an idea and no artwork.

ai.mecartworks.com, five free previews, email code only.

If the output isn't print-grade for your panels, you'll know fast.
""",
 "parking this with you", """
Tim,

I'll leave it here.

If most orders arrive with artwork already sorted, this solves a problem you don't have — and that's a good position to be in.

If you ever want the other half of that market, ai.mecartworks.com is the example.

Good luck either way.
""")

add("jtheopistos@finerworks.com",
 "the commission your artists can't preview", """
James,

FinerWorks is built around artists who already have the file — drag it in, live preview, COA on the way out. That's a clean pipeline.

The gap is the commission. When a buyer asks an artist for "something like this, but for my dining room," there's nothing to drag in, and that conversation runs over email for weeks.

We built the AI studio MEC Artworks runs, for exactly that stage: describe it, get an original concept, place it on a photo of the buyer's room.

Worth showing you?
""",
 "a COA for a piece that doesn't exist yet", """
James,

Concretely: the buyer types what they're after, gets an original concept, then sees it on their own wall before the artist starts.

For FinerWorks that could sit ahead of the upload — the artist closes the commission faster, and the file that eventually gets dragged in is one the buyer already approved.

ai.mecartworks.com — five previews, email code, no subscription.

Curious what you'd make of the output quality.
""",
 "one for the roadmap", """
James,

Last one from me.

You've clearly thought about the artist's workflow more than most print platforms have — the COA tool alone says that.

If the commission stage ever comes up as something to solve, ai.mecartworks.com is the working example.

Either way, good luck with it.
""")

add("jennifer.brethack@photowall.com",
 "your simulator, for designs that don't exist yet", """
Jennifer,

Photowall's "Try Before You Buy" simulator already does the hard half — the customer sees the design on their own wall before buying.

What it can't do is invent the design. If someone wants "muted botanical, wide format, north-facing room" and nothing in the catalogue matches, the simulator has nothing to show them.

We built the AI studio MEC Artworks runs. It generates the design from that sentence, then places it in the room.

Want to see how the two stages fit together?
""",
 "thousands of designs, still no match", """
Jennifer,

The specific: someone describes the design in ordinary words, gets an original back, then previews it in their own room — same last step as yours, different first step.

For Photowall that's the visitor who searches, finds nothing close, and leaves. Right now the simulator never gets a chance with them.

ai.mecartworks.com — free, five previews, email code.

Worth two minutes of a marketing afternoon.
""",
 "does 'no close match' show in your search data?", """
Jennifer,

I'll stop here.

If catalogue depth already covers most searches, this is a smaller problem than I think, and that's fair.

If "no close match" ever shows up in your search data, ai.mecartworks.com is the example to look at.

Thanks for reading.
""")

add("ivars@fancywalls.eu",
 "your private label partners, and their customers", """
Ivars,

Fancy Walls already white-labels — private label, dropship, one to two day turnaround. You sell your capability onward, not just your product.

Which makes the bottleneck clear: your partners' customers still have to decide what they want before any of that speed matters. Printing in two days doesn't help if choosing took three weeks.

We built the AI studio MEC Artworks runs. It compresses the choosing — describe it, get an original design, see it on your own wall.

Want me to show you where it would sit in a private-label flow?
""",
 "two days to print, three weeks to decide", """
Ivars,

More concretely: a shopper types what they want, gets an original design back, and sees it on a photo of their room — no drawing, no designer.

For a dropship partner that's the difference between a browser and an order. Your two-day turnaround only starts once someone decides.

ai.mecartworks.com — five free previews, email code.

Happy to talk through the embed side if it looks relevant.
""",
 "is choosing actually your bottleneck?", """
Ivars,

Last note.

If your private-label partners already convert well without a design step, then this isn't your bottleneck and I'd rather know that.

If it is, ai.mecartworks.com shows what it looks like.

Either way — 3,400 designs and two-day print is a genuinely strong setup.
""")

add("verena.nava@glamora.it",
 "your Bespoke Design Service, before the first sketch", """
Verena,

Glamora offers a Bespoke Design Service to professionals — an architect brings a project, your studio designs to it.

That process starts with a conversation and a lot of imagination. The client approving the budget usually can't picture the result, which is where bespoke work gets trimmed or delayed.

We built the AI studio MEC Artworks runs. It puts a concept on screen in that first conversation — described in words, then placed on a photo of the actual space.

Would it be useful to see it against one of your collections?
""",
 "turning the first meeting into a decision", """
Verena,

The detail worth adding: no CAD and no drawing. Someone describes the piece — colour, mood, scale — and gets an original concept, then sees it in the room.

For a bespoke service selling into hotels like SILENA and Bellerive, that turns the first meeting into a decision instead of a brief.

ai.mecartworks.com — free, five previews, email verification only.

Two minutes and you'll know if it holds up next to Glamora's work.
""",
 "do you show them anything in meeting one?", """
Verena,

I'll leave this with you.

If your studio already shows clients something visual in that first meeting, you've solved the part most bespoke suppliers haven't.

If not, ai.mecartworks.com is the working example.

Either way, the hospitality work on your diary page is a strong showcase.
""")

add("paolo.amenta@inkiostrobianco.com",
 "progetti su misura, before the render", """
Paolo,

Inkiostro Bianco offers progetti su misura — and with a 3D lead in the room, you're already producing visuals to sell them.

That's the expensive part. Every bespoke enquiry that needs a render costs studio time before anyone has committed to anything.

We built the AI studio MEC Artworks runs. It produces the first-pass version in seconds: describe the piece, get an original concept, place it on a photo of the room.

Not a replacement for your 3D work — a filter in front of it. Worth a look?
""",
 "a 3D lead's read on the output", """
Paolo,

The part I'd want your read on specifically: output quality.

Someone types "warm ochre, botanical, large scale" and gets an original concept, then drops it into a photo of the space. No CAD.

You'd know within a minute whether it's good enough to put in front of a client, or only good enough to narrow a direction internally. Both are useful — I'd like to know which.

ai.mecartworks.com, five free previews.
""",
 "if the 3D queue is never a queue", """
Paolo,

I'll stop here.

If your 3D pipeline already turns bespoke enquiries around fast enough, this solves nothing for you and that's a good place to be.

If it's ever a queue, ai.mecartworks.com is the example.

Either way, the Hotel La Gemma work is a strong reference.
""")

add("g.menin@instabilelab.it",
 "Real Wall and Live Room, one step earlier", """
Giulia,

Real Wall and Live Room put Instabilelab ahead of most of this industry — most wallcovering brands still ship a static gallery.

Both configurators start from your existing collections, though. The visitor who wants something that isn't in them has no path, and a laboratorio di sperimentazione is exactly the brand that customer came looking for.

We built the AI studio MEC Artworks runs. It generates the design first, described in words, then places it in the room.

Would it be useful to see how it sits in front of Real Wall?
""",
 "the visitor your configurators never meet", """
Giulia,

To be concrete: someone types "ochre, oversized botanical, matte" and gets an original design, then sees it on their wall. Your configurators handle everything after that.

For Instabilelab it's a first step, not a replacement — it feeds Real Wall the customers who currently leave.

ai.mecartworks.com — five previews, email code, no subscription.

Two minutes will tell you whether the output is up to your standard.
""",
 "you've built configurators — what did you learn?", """
Giulia,

I'll leave it here.

You've already invested in configurators, so you know what they cost and what they return better than I do. If the gap I'm describing isn't real for you, that's genuinely useful to hear.

ai.mecartworks.com if it ever is.

Either way, the Hotel Feldhof project is a good showcase.
""")

# ─────────────────────────── MOSAIC / POOL ───────────────────────────
# MEC competitors — name MEC up front, offer a walkthrough, never a raw link.

add("mike@aquablumosaics.com",
 "Create a Mosaic, before the drawing", """
Michael,

Your "Create a Mosaic" service is why I'm writing — a homeowner or builder describes what they want in the pool, and your team turns it into a design.

Between that conversation and an approved drawing is where custom pool work slows down, and pool budgets move fast.

Being upfront: we built the AI studio MEC Artworks runs, and they're in mosaics too. It takes a plain-words description and puts the design on a photo of the actual pool.

Happy to walk you through it rather than send a link — worth 15 minutes?
""",
 "selling the finished pool, not the drawing", """
Michael,

The specific mechanic: someone types "deep blue, geometric, Mediterranean" and gets an original mosaic concept back, then it's placed on a photo of the real pool.

At a Ritz-Carlton level of spec, that's the difference between selling a drawing and selling a picture of the finished pool.

I'd rather show you than have you register on a competitor's site — 15 minutes, screen share, no deck.

Want me to send a couple of times?
""",
 "if custom pools already close fast", """
Michael,

I'll stop here.

If your team already gets clients to a yes quickly on custom pools, that's the whole game and you've got it.

If concept-to-approval is ever the slow part, the offer to walk you through it stands.

Either way, good luck with the season.
""")

add("chad.k@mosaicslab.com",
 "the free design consultation", """
Chad,

Mosaics Lab offers a free design consultation on custom work — a customer sends a photo or a painting, and your team turns it into a mosaic concept.

That's real staff time on every enquiry, spent before anyone has committed to buying.

Straight with you: we built the AI studio MEC Artworks runs, and they're in your industry. It does the first pass — a description or an uploaded image in, concept out, placed on a photo of the space.

Rather than point you at a competitor's site, can I walk you through it?
""",
 "how many consultations turn into orders?", """
Chad,

The number I'd be curious about: how many free consultations turn into paid mosaics?

If it's high, ignore me. If it's the usual, the consultation is doing sales work a first-pass visual could do in seconds — leaving your artists for the customers who are serious.

Fifteen minutes on a screen share and you'd know whether it fits.

Want a couple of times?
""",
 "owners know where the time leaks", """
Chad,

Last one from me.

Owner-run studios usually know exactly where their time leaks, so if the consultation isn't one of them, I'll take your word for it.

The walkthrough offer stands if it ever is.

Good luck with the year.
""")

add("sal@poolmosaics.com",
 "your artists, working step-by-step", """
Sal,

Blue Water's own copy says your ceramic artists work with the customer step-by-step to create the custom piece — logos, mascots, family crests.

That's a person on every enquiry. The design software sits with your team, so the customer only sees a result after someone has already spent the hours.

Being direct: we built the AI studio MEC Artworks runs — same industry as you. It puts a first version on screen from a description, on a photo of the actual pool.

Happy to walk you through it. Worth 15 minutes?
""",
 "software for your artists vs software for your customer", """
Sal,

The difference in one line: your software is a tool for your artists. This one is a tool for your customer.

They type "navy, school mascot, six feet across", see a version on the pool photo, and arrive at your artists already knowing what they want.

Same step-by-step outcome, minus the hours spent before the customer is serious.

Screen share, 15 minutes, no deck. Want me to send times?
""",
 "wrapping this up", """
Sal,

I'll close this off.

Twenty years in the pool industry means you've seen a lot of tools promise this. Fair to be sceptical.

The walkthrough offer stands if it's ever worth an afternoon.

Good luck with the season.
""")

add("swilkins@newravenna.com",
 "your concept board team", """
Stephenie,

New Ravenna's bespoke route starts with photographs, fabric swatches, sometimes a magazine clipping — and your team turning that into a mosaic concept before anything is cut.

You have a manager for that step, which tells me it carries real weight and real hours.

Being upfront: we built the AI studio MEC Artworks runs, and they're in mosaics too. It produces a first-pass concept from a description and places it on a photo of the room.

I'd rather show you than send a competitor's link. Worth 15 minutes?
""",
 "photographs, swatches, clippings", """
Stephenie,

The mechanic specifically: someone types "warm terracotta, geometric, Moorish influence" and gets an original concept back, then sees it on a photo of the actual wall.

It doesn't replace a concept board. It gets the client to a direction before the board is worth making — which is where your team's hours go.

Fifteen minutes on a screen share and you'd know.

Want me to send a couple of times?
""",
 "how does the first pass work now?", """
Stephenie,

I'll leave this alone now.

If your first pass is already fast enough at the volume you run, that's a good place to be and I'm glad I asked.

If it's ever the bottleneck — usually when volume climbs, not when the work changes — the walkthrough offer stands.

Thanks for reading this far.
""")

add("christina@hakatai.com",
 "custom mosaic murals, before the layout", """
Christina,

Hakatai does custom designed glass tile installations — mosaic murals and uncut custom patterns, not just stock series.

That work asks the client to picture a whole wall from a sample board and a photo of somebody else's project. Some of them shrink the scope rather than commit.

Being straight: we built the AI studio MEC Artworks runs — same industry. It generates a concept from a description and places it on a photo of the actual space.

Happy to walk you through it — worth 15 minutes?
""",
 "clients who can see it approve the bigger piece", """
Christina,

The commercial version of this: clients who can see the finished wall approve the bigger piece, and they approve it sooner.

Someone types "sea glass blues, organic, twelve feet" and sees it on the real wall — before the layout work starts.

I'd rather demo it than send you to a competitor's site. Fifteen minutes, screen share.

Want a couple of times?
""",
 "one last note", """
Christina,

Closing this out.

As CEO you'll have a clearer view than I do on whether custom enquiries convert well enough already. If they do, ignore me entirely.

The offer to walk through it stands.

Good luck with the year.
""")

add("sgildea@oceansideglasstile.com",
 "the Special Order Program", """
Sean,

Oceanside's Special Order Program and the Uniquely Oceanside collaboration both let a client customise before the tile ships.

Both still ask them to commit to a combination they've only seen as separate samples. Your own site makes the point — liners, decos and trim combine for "unlimited possibilities", which is a lot to hold in your head.

Being upfront: we built the AI studio MEC Artworks runs, same industry. It puts the combination on a photo of the real space.

Worth 15 minutes to walk through?
""",
 "unlimited possibilities, one decision", """
Sean,

Where it fits Oceanside specifically: unlimited combinations is a selling point right up until the client has to choose one.

Someone describes what they're after, sees it rendered on the actual pool or wall, and the special order gets placed instead of postponed.

I'd rather show you directly than send a competitor's link. Fifteen minutes on a screen share.

Want me to send times?
""",
 "thirty years of recycled glass", """
Sean,

Last one from me.

Thirty-plus years and a recycled-glass process that predates everyone else doing it — you've built something durable, and you don't need a tool to prove it.

The walkthrough offer stands if the special order flow ever needs help.

Good luck with it.
""")

add("colleenbellingeri@artistictile.com",
 "what Tailored To asks of a client", """
Colleen,

"Tailored To" is a proper bespoke programme — custom cutting and finishing, not just a size option.

The client approving it is looking at slabs and gallery photos and imagining the result. At Artistic Tile's price point, imagination is doing a lot of expensive work.

Being upfront: we built the AI studio MEC Artworks runs — they're in tile and mosaic too. It renders a described design onto a photo of the actual room.

I'd rather walk you through it than send a competitor's link. Worth 15 minutes?
""",
 "a better lead than a sample request", """
Colleen,

From a marketing angle: this is content as much as it is a tool.

A visitor describes what they want, sees it on their own wall, and hands you their intent — which is a better lead than a sample request.

Fifteen minutes on a screen share and you'd know if it's worth a conversation internally.

Want me to send a couple of times?
""",
 "not adding to your inbox", """
Colleen,

I'll stop here.

If Tailored To is already converting the way you want, this is noise and I'd rather not add to your inbox.

The offer to walk through it stands.

Either way, good luck with the season's launches.
""")

add("andrea.f@sicis.com",
 "your design service for architects", """
Andrea,

Sicis runs a design service for architects — soluzioni su misura across mosaic, glass and interiors.

An architect specifying that has to sell it onward to their own client, usually from a sample and a portfolio of someone else's project. Work like Paradis Latin or the Benetti yacht is hard to translate into a different room.

We built the AI studio MEC Artworks runs — same industry. It renders a described design onto a photo of the actual space.

Worth walking you through?
""",
 "an image that works as a proposal and as content", """
Andrea,

For your side of the business specifically: this makes shareable content as easily as it makes proposals.

Someone describes a space, sees a Sicis-style treatment placed in it, and that image is both a sales asset and a social one.

Fifteen minutes on a screen share and you'd see whether the output is up to the brand.

Want me to send a couple of times?
""",
 "Sicis may not need generated imagery", """
Andrea,

I'll leave it here.

Sicis has a stronger visual archive than almost anyone in this category, so you may simply not need generated imagery.

If it's ever useful, the walkthrough offer stands.

Either way, the Flora Springs project is a great piece of work.
""")

add("paolo.rinaldi@bisazza.com",
 "the Bisazza App, and the consultation behind it", """
Paolo,

Bisazza already runs a space configurator and a free Design Studio consultation for custom mosaic work — further along than most of this industry.

The consultation is the interesting part. It's staffed, it's free, and it exists because the app configures existing products rather than generating new ones.

We built the AI studio MEC Artworks runs. It takes a plain-words brief and returns an original design, placed on a photo of the real space.

Worth a look as a front end to the Design Studio?
""",
 "where the Design Studio hours go", """
Paolo,

Framing it for your side: the app handles configuration, the studio handles creation, and the gap between them is human hours.

Someone types "Novembre-scale geometry, warm metallics" and gets an original concept placed in the room. The consultation then starts from something instead of nothing.

I'd rather show you than send a link — 15 minutes on a screen share.

Want a couple of times?
""",
 "have you looked at generative tooling already?", """
Paolo,

Closing this off.

At Bisazza's scale you'll have looked at generative tooling already, and possibly built some. If so, I'd genuinely like to know what you concluded.

The walkthrough offer stands either way.

Good luck with the season.
""")

# ─────────────────────────── DECORATIVE / ARTISAN TILE ───────────────────────────

add("samantha@fireclaytile.com",
 "your Mosaic Visualizer, one step earlier", """
Samantha,

Fireclay's Mosaic Visualizer is one of the few real ones in this industry — most tile brands still ship a photo gallery and call it a tool.

It visualises patterns you've already designed, though. The customer who wants something that isn't in the system still ends up in a custom enquiry queue.

We built the AI studio MEC Artworks runs: describe a design in plain words, get an original back, see it on a photo of the actual room.

Would it be useful to see how it sits in front of the Visualizer?
""",
 "the Foundry launch and the 'like that, but…' requests", """
Samantha,

The Foundry Collection is a good example of the gap. A launch creates demand for a look, and the requests that follow are always "like that, but…".

This handles the "but" — original concept from a description, placed in the customer's own space, before it reaches your custom team.

ai.mecartworks.com, five free previews, email code.

Two minutes will tell you whether the output clears Fireclay's bar.
""",
 "one for the roadmap file", """
Samantha,

I'll stop here.

You've already built visualisation tooling in-house, so you know the cost and the payoff better than I can argue it.

If the generative step is ever on the roadmap, ai.mecartworks.com is a working reference.

Either way, the Foundry launch looks great.
""")

add("randi@mercurymosaics.com",
 "your consultants, and the first ten minutes", """
Randi,

"Create Your Blend" lets a customer pick colours for diamond tiles — and you have a director of design consultants, which suggests plenty of custom work starts as a conversation rather than a selector.

Those first conversations are where the hours go: translating "something warm, sort of organic" into an actual layout.

We built the AI studio MEC Artworks runs. It turns that sentence into an original concept and puts it on a photo of the customer's room.

Would it help your consultants to see it?
""",
 "refining instead of interpreting", """
Randi,

Specifically for a consulting team: it changes what the first call starts from.

Instead of describing options, your consultant opens with a concept already placed in the customer's room, and spends the call refining rather than interpreting.

ai.mecartworks.com — free, five previews, email code only.

Two minutes and you'd know whether it's useful to the team or just to the marketing page.
""",
 "closing the loop", """
Randi,

Last note.

If your consultants already get customers to a clear direction quickly, then this solves something you don't have.

If the first ten minutes are ever the slow part, ai.mecartworks.com is the example.

Either way — the Whitney commission is a remarkable credit.
""")

add("justinb@motawi.com",
 "Project Tile, and what comes before it", """
Justin,

Project Tile is a smart piece of work — customers planning a backsplash or fireplace with your patterns instead of guessing.

It starts once they've chosen the pattern, though. The customer who knows the room but not the tile has nothing to plan with, and that's usually where an art director's time gets spent.

We built the AI studio MEC Artworks runs. It generates an original design from a description and places it on a photo of the actual room.

Worth seeing how it sits in front of Project Tile?
""",
 "an art director's verdict in two minutes", """
Justin,

As an art director you'd judge this faster than anyone: does the generated output look like something you'd let out under your name?

Someone types "arts and crafts, muted green, botanical" and gets an original concept, placed in the room. Two minutes will answer it.

ai.mecartworks.com — five free previews, email code.

Genuinely interested in your verdict either way.
""",
 "generated design might be exactly wrong for Motawi", """
Justin,

I'll leave this here.

Motawi's patterns are distinctive enough that generated design may be exactly the wrong fit — that's a legitimate answer and I'd rather hear it than not.

ai.mecartworks.com if you're curious.

Either way, Project Tile is better than most of what this industry ships.
""")

add("susanne@prattandlarson.com",
 "serendipity, minus the shipping time", """
Susanne,

Your InLine Design Cards are a genuinely good idea — physical cards so someone can experiment and let serendipity do its work.

They also require shipping, handling, and a customer patient enough to play. Plenty of people who'd have bought after experimenting never start.

We built the AI studio MEC Artworks runs. Same experimentation, on screen: describe a direction, get an original concept, see it on a photo of the actual room.

Worth showing you the parallel?
""",
 "customers who experiment specify bigger", """
Susanne,

The commercial version: customers who experiment buy more confidently and specify bigger. Your cards prove you already believe that — this just removes the postage and the wait.

Describe it, see it on the wall, adjust, decide.

ai.mecartworks.com — five previews, free, email code only.

Two minutes will tell you whether it belongs next to the cards or nowhere near them.
""",
 "if the cards are working, ignore me", """
Susanne,

I'll stop here.

If the cards are converting the way you hoped, that's a better result than most digital tools produce and I'd leave well alone.

ai.mecartworks.com if the digital version is ever interesting.

Either way, the Cedar & Moss collaboration is lovely work.
""")

add("cmcdougal@senecatiles.com",
 "the Handmold Mini Panels", """
Connie,

Seneca brought back the Handmold Mini Panels by popular demand — which tells me your specifiers respond to seeing the real thing in front of them.

That's the whole difficulty with tile: panels and samples travel slowly, and the architect's client is usually the one who needs convincing.

We built the AI studio MEC Artworks runs. It puts a described design onto a photo of the actual space, in seconds.

I couldn't tell from your site how much custom work Seneca takes on — worth a short conversation?
""",
 "a straight question about how Seneca sells", """
Connie,

Being honest about why I'm asking: your site is clear on collections but not on how far you'll go on a custom request.

If the answer is "quite far", this is relevant — it shortens the distance between an enquiry and an approved design.

If the answer is "we're a manufacturer, not a design studio", tell me and I'll stop.

Either way, ai.mecartworks.com shows what I mean in two minutes.
""",
 "the Mini Panels run", """
Connie,

Last note from me.

A general manager's time is the wrong thing to spend on a cold email, so I'll leave it.

If Seneca does take custom design work and it ever slows things down, ai.mecartworks.com is the example.

Good luck with the Mini Panels run.
""")

add("mark@derbypottery.com",
 "the New Orleans street tiles", """
Mark,

Making the New Orleans letter and number tiles for the city since 2003 is a hard credential to argue with.

The rest of the range is where I'm curious — Victorian patterns with traditional and specialty glazing, ordered by people who've only seen a photo of somebody else's floor.

We built the AI studio MEC Artworks runs. Someone describes what they want and sees it laid into a photo of their own room.

Worth two minutes of an owner's time?
""",
 "specialty glazing, undecided customers", """
Mark,

More useful detail: no drawing, no software to learn. A customer types "Victorian, deep green, geometric border" and sees it on their own floor.

For a studio your size that's the difference between answering the same questions by email for a week and getting to a yes.

ai.mecartworks.com — five free previews, email code.

If it doesn't do your glazes justice, I'd want to know that too.
""",
 "one more tool to evaluate", """
Mark,

I'll leave it here.

Running a studio means the last thing you need is another tool to evaluate. Fair enough.

ai.mecartworks.com if it's ever a slow week.

Either way, twenty-plus years making the city's own tiles is a good thing to have built.
""")

add("nmerkowitz@mooremerkowitztile.com",
 "19 collections, one decision", """
Neil,

Nineteen design collections in the Molding & Trim series is a lot of choice — and choice is exactly what stalls a tile decision.

A customer looking at stunning patterns and rich glazes across nineteen options usually needs someone to narrow it for them. That someone is you.

We built the AI studio MEC Artworks runs. They describe the room, see a combination placed on a photo of it, and arrive at you already decided.

Worth a couple of minutes?
""",
 "let the customer do the narrowing", """
Neil,

The practical version: the customer does the narrowing themselves, on screen, before they contact you.

They type what they're after, see it on their own wall, and the conversation you get is about ordering rather than choosing.

ai.mecartworks.com — free, five previews, email code only.

Two minutes will tell you whether it handles your glazes properly.
""",
 "when choosing eats a week", """
Neil,

Last one from me.

Owner-run means your time is the scarce thing, so I won't keep asking for it.

ai.mecartworks.com if the choosing stage ever eats a week.

Good luck with the season.
""")

add("carli@kibaktile.com",
 "before the meeting gets booked", """
Carli,

Kibak offers custom tile and custom murals, and the site invites people to book a meeting to talk the project through.

That meeting is doing a lot of work — the customer arrives with a vague idea and you turn it into something concrete, one conversation at a time.

We built the AI studio MEC Artworks runs. Someone describes the mural in plain words, gets an original concept, and sees it on a photo of the actual wall.

Would that be useful before the meeting rather than during it?
""",
 "refining, not interpreting", """
Carli,

Concretely: the customer books the meeting already holding a picture of what they want, placed in their own space.

You spend the call refining instead of interpreting — and the ones who were never serious don't book at all.

ai.mecartworks.com — five free previews, email code.

Two minutes and you'd know whether it fits how Kibak works.
""",
 "a solution looking for a problem?", """
Carli,

I'll leave this with you.

If your booked meetings already convert well, this is a solution looking for a problem and I'd rather admit that.

ai.mecartworks.com if the vague-idea stage is ever the slow one.

Good luck with the year.
""")

# ─────────────────────────── CUSTOM RUGS (PARKED) ───────────────────────────

add("emma.geiszler@therugcompany.com",
 "your Custom Rug Designer, and the bespoke queue", """
Emma,

The Custom Rug Designer put you ahead of the category — a hundred designs, colour and size, all self-serve.

Bespoke still goes to the studio though. When someone wants a design that isn't in the portal, a person picks it up, and that's before a sixteen to twenty-four week weave even starts.

We built the AI studio MEC Artworks runs. It generates an original design from a plain-words brief and places it in a photo of the room.

Worth seeing as a front end to the bespoke route?
""",
 "the portal configures, the studio creates", """
Emma,

To be specific about where it fits: your portal configures, your studio creates, and the gap between them is people.

A client types "Wearstler-scale geometry, bone and rust" and sees it on their own floor. The studio conversation then starts from an image instead of a description.

Happy to walk you through it — 20 minutes, screen share.

Want a couple of times?
""",
 "is the bespoke gap worth closing?", """
Emma,

I'll leave it here.

You've built a configurator already, so you know exactly what these tools cost and return — if the bespoke gap isn't worth closing, that's genuinely useful for me to hear.

The walkthrough offer stands.

Either way, the DvF collaboration is great brand work.
""")

add("kayla@modernrugs.com",
 "any size, any shape, any colour", """
Kayla,

"Any size, any shape, any colour — we'll bring your vision to life" is a strong promise, and your pickers cover size, material and weave well.

The vision part is the gap. A customer with a specific idea can't see it until someone in production makes it visible, which puts you in the middle of every custom enquiry.

We built the AI studio MEC Artworks runs. Describe it in words, get an original design, see it in a photo of the room.

Worth two minutes?
""",
 "fewer rounds before production", """
Kayla,

From a production side specifically: fewer rounds.

If the customer approves a visual before anything is sampled, the brief that reaches production is settled rather than still moving.

ai.mecartworks.com — free, five previews, email code only.

Two minutes will tell you whether the output is precise enough to work from.
""",
 "do custom briefs arrive clear?", """
Kayla,

Last note.

If custom briefs already arrive clear, this fixes something that isn't broken and I'd rather leave you to it.

ai.mecartworks.com if the back-and-forth ever gets long.

Good luck with the season.
""")

add("kruthika@rugartisan.com",
 "300 colourways, and the design nobody's drawn", """
Kruthika,

Rug Artisan's customisation software with 300 preset colourways per design is further than most of this industry has got.

Your own process describes what happens after: for a fully bespoke request, your designers create the design and send it for approval. That's a person, and a round trip.

We built the AI studio MEC Artworks runs. It generates an original design from a plain-words brief and places it in the room.

Worth seeing where it sits before your designers pick it up?
""",
 "variation vs designs that don't exist yet", """
Kruthika,

Put simply: your software handles variation on existing designs. This handles designs that don't exist yet.

The client arrives at your design team having already seen and approved a direction, so the round trip becomes confirmation rather than discovery.

Happy to walk you through it — 20 minutes.

Want a couple of times?
""",
 "is the round trip a cost, or just the work?", """
Kruthika,

I'll stop here.

As design manager you'll know whether the bespoke round trip is actually a cost or just how the work goes. If it's the latter, fair enough.

The walkthrough offer stands.

Either way, the personalise tool is well built.
""")

add("hope@theperfectrug.com",
 "custom prices vs everyday prices", """
Hope,

The Perfect Rug's whole positioning is custom at everyday prices rather than custom prices — and you back it with free design consultations.

Free consultations are the expensive part of that promise. They're staff hours attached to every undecided customer, which is exactly what a value position can't afford to scale.

We built the AI studio MEC Artworks runs. A customer describes the rug, sees it on a photo of their own floor, and decides before a consultation is needed.

Worth two minutes?
""",
 "content your customers make for you", """
Hope,

For a content and partnerships role there's a second angle: the output is shareable.

Someone describes a room, gets an image of their own space with the rug in it, and that's content your customers make for you.

ai.mecartworks.com — free, five previews, email code.

Two minutes and you'd know if it fits the brand.
""",
 "do the consultations still scale?", """
Hope,

I'll leave it here.

If the consultations are converting well enough to justify themselves, that's the answer and it's a good one.

ai.mecartworks.com if they ever stop scaling.

Either way, good luck with the partnerships work.
""")

add("cassie@shop-jubi.com",
 "The Rug Plan, and the customizer", """
Cassie,

Jubi runs both a real-time customizer with 1,200 shades and The Rug Plan, where your studio replies by hand with rugs chosen for someone's room.

That you staff the second one despite having the first is the interesting bit — it says plenty of customers arrive without a starting point, and a colour picker can't give them one.

We built the AI studio MEC Artworks runs. It generates the starting point from a sentence, then places it in the room.

Worth a look as a front end to The Rug Plan?
""",
 "what does The Rug Plan cost per enquiry?", """
Cassie,

As a founder you'll price this instantly: what does The Rug Plan cost you per enquiry, and what share convert?

If someone arrives having already described their room and seen a design in it, your studio's reply becomes a shorter, better-qualified conversation.

ai.mecartworks.com — free, five previews, email code.

Two minutes will tell you whether it clears Jubi's bar.
""",
 "what did you learn building yours?", """
Cassie,

Last one from me.

You've already built the tooling most of this industry hasn't, so you're the wrong person to sell a visualiser to — I'd rather ask what you learned building yours.

ai.mecartworks.com if you're curious.

Either way, The Rug Plan is lovely service design.
""")

# ─────────────────────────── STAINED GLASS (PARKED) ───────────────────────────

add("djudson@judsonstudios.com",
 "the renaissance piece", """
David,

The piece calling stained glass a renaissance and naming Judson as the studio fuelling it is a good problem to have — more enquiries from people who've never commissioned glass before.

Those clients approve a window they cannot picture, from drawings, and at Judson's scale that's a long, careful conversation every time.

We built the AI studio MEC Artworks runs. It renders a described design into a photo of the actual opening.

Worth a short conversation?
""",
 "triage as much as sales", """
David,

To be clear about what it is and isn't: it won't design a Judson window. It gets a client to a direction — palette, subject, density — before your designers invest hours.

For a studio doing both new commissions and restoration, that's triage as much as sales.

ai.mecartworks.com — five free previews, email code.

Two minutes and you'd know.
""",
 "Unity Temple doesn't need my help", """
David,

I'll leave this with you.

A studio that's worked on Unity Temple doesn't need a generative tool to sell its work, and I'm aware of that.

ai.mecartworks.com if enquiry volume ever outpaces the design team.

Either way, good luck with the renaissance.
""")

add("kathy.jordan@willet-studios.com",
 "15,000 buildings", """
Kathy,

Windows in more than 15,000 buildings is a number very few studios can put on a page.

Most of those commissions get approved by a committee — a church board, a hospital board — and committees approve what they can see. Drawings ask each member to imagine the same thing, which is where these decisions stall for months.

We built the AI studio MEC Artworks runs. It puts a described design into a photo of the actual window opening.

Worth 15 minutes?
""",
 "the committee that has to agree", """
Kathy,

The committee point is the one I'd stand behind commercially: when everyone in the room sees the same image, the decision happens in that meeting instead of the next one.

Describe the design, place it in the real opening, discuss the actual thing.

ai.mecartworks.com — free, five previews, email code only.

Two minutes will tell you whether it's usable at your standard.
""",
 "no is a reasonable answer here", """
Kathy,

Last note from me.

As creative director you'd be the one deciding whether generated imagery belongs anywhere near Willet's work — and no is a perfectly reasonable answer for a studio with your history.

ai.mecartworks.com if it's ever worth a look.

Good luck with the current commissions.
""")

add("garyh@franklinartglass.com",
 "four generations, one slow step", """
Gary,

A hundred and one years and four generations — Franklin has outlasted most of the industry it started in.

The custom side is what I'm writing about: working directly with homeowners, architects and designers on one-of-a-kind projects. Those clients approve from sketches, and sketches take your people's time before anyone has committed.

We built the AI studio MEC Artworks runs. It renders a described design into a photo of the actual window.

Worth a short conversation?
""",
 "making custom cheaper to quote", """
Gary,

Being realistic about your business: most of Franklin's revenue is supply, and custom sits alongside it.

Which is precisely why a faster first pass might matter — it makes custom work cheaper to quote without pulling more people onto it.

ai.mecartworks.com — five free previews, email code.

Two minutes is all it takes to judge.
""",
 "since 1924, without my advice", """
Gary,

I'll stop here.

A business that's lasted since 1924 doesn't need advice from a cold email, and I won't pretend otherwise.

ai.mecartworks.com if the custom side ever needs a faster front end.

Good luck with the next generation of it.
""")

# ─────────────────────────── CERAMIC TILE ───────────────────────────

add("anna@heathceramics.com",
 "a set builder for dinnerware, not for tile", """
Anna,

Heath built a set builder for dinnerware — start building, save 10%, see it come together.

Tile doesn't have one. It has over a hundred glazes and an inquiry form, which means the customer choosing between them is doing it in their head while the dinnerware customer gets a tool.

We built the AI studio MEC Artworks runs. Someone describes a room, sees a tile treatment placed in a photo of it, and chooses with their eyes.

Worth seeing the parallel?
""",
 "Seeds of Summer, on someone's actual wall", """
Anna,

Seeds of Summer is the case in point — moodier pinks and reds, launched in April, and the hard part is getting someone to imagine a whole wall of it.

Described in words, rendered into their own room, decided in a minute.

ai.mecartworks.com — free, five previews, email code only.

Two minutes will tell you whether the glazes survive the translation.
""",
 "one for the list", """
Anna,

I'll leave this here.

Heath's design standards are the reason to say no to a tool like this, and I'd take that answer seriously.

ai.mecartworks.com if the tile side ever wants what the dinnerware side has.

Either way, Seeds of Summer is a beautiful collection.
""")

add("jamie@ziatile.com",
 "designed in LA, crafted everywhere", """
Jamie,

Zia's line — designed in Los Angeles, crafted by artisans around the globe — is a curated position rather than a made-to-order one, and the filters on the site reflect that.

Which makes the customer's job harder in one specific way: zellige varies, and a swatch photo doesn't tell you what a whole wall of it looks like.

We built the AI studio MEC Artworks runs. Someone describes their room and sees a treatment placed in a photo of it.

Worth two minutes of a marketing director's time?
""",
 "a discovery tool, not a design service", """
Jamie,

To be clear, I'm not suggesting Zia move into custom — the curated position is the brand.

This sits before the filters: someone who knows the room but not the collection sees a direction, then lands on the product that matches. Discovery, not a design service.

ai.mecartworks.com — free, five previews.

Two minutes and you'd know if it's on-brand.
""",
 "maybe the filters already do this", """
Jamie,

Last note.

If site search and the collection filters already do this job, then I've misread it and I'd rather know.

ai.mecartworks.com if discovery is ever the drop-off point.

Either way, good luck with the season.
""")

# ─────────────────────────── WALLCOVERING (US) ───────────────────────────

add("lindsay@lookwalls.com",
 "the Gilded print in Reflections", """
Lindsay,

The Gilded print technology in the Reflections Collection — fine gold accents, reflective detail — is the kind of thing that has to be seen rather than described.

Which is the whole difficulty. Your process is deliberately collaborative, concept through production, and each round of that collaboration is your team's time before a job is confirmed.

We built the AI studio MEC Artworks runs. A designer describes the piece and sees it in a photo of the actual space.

Worth 15 minutes?
""",
 "for a 15-person studio, rounds are margin", """
Lindsay,

The commercial angle for a fifteen-person studio: rounds are your margin.

If the designer and their client agree a direction from a rendered image before your team starts, you spend production time on confirmed work instead of exploration.

ai.mecartworks.com — five free previews, email code only.

Two minutes will tell you whether it does the Gilded finish justice. I suspect that's the real test.
""",
 "every tool has to earn its place", """
Lindsay,

I'll leave it here.

Founder-run and fifteen people means every tool has to earn its place, so no is a completely reasonable answer.

ai.mecartworks.com if the concept rounds ever get long.

Either way, building a print operation alongside a design studio is a genuinely smart structure.
""")

add("hneurer@areaenvironments.com",
 "approving a wall they've never seen", """
Heather,

Area sells to the trade only, and your FAQ says if someone brings a piece or a photograph, you'll build the wallcovering around it.

So the person who signs off — the designer's client — is approving from a sample and their imagination. That's where custom work shrinks: a smaller wall, a safer colourway, a "let's revisit next quarter."

Show them the finished piece on their own wall and they stop hedging. Bigger yes, sooner.

We built the AI studio MEC Artworks runs.

Want me to run one of your collections through it and send you the result?
""",
 "the feature wall that became an accent", """
Heather,

One thing I'd guess at: how often does a custom project come back smaller than it started?

Not lost — just trimmed. A feature wall becomes an accent panel. That trim is almost always uncertainty, not budget.

The tool is at ai.mecartworks.com. Email code, five free previews, no subscription. Upload a room, describe the piece, see it in place.

Ninety seconds will tell you whether it holds up next to your artists' work.
""",
 "how do your designers show it now?", """
Heather,

I'll stop here.

If your designers already have a way to show a client the finished wall before it's printed, you've solved the hard part — and I'd genuinely like to know how.

If not: ai.mecartworks.com, five previews, free.

Either way, paying artists a royalty on every piece sold in their name is a good thing to see in this industry.
""")

add("susansteinicke@usvinyl.com",
 "Murals & Graphics, before the first install", """
Susan,

USV Murals & Graphics is a different sell from hotel standards. Marriott and Hilton buy to spec — they know exactly what arrives. Art-led work gets bought on how it looks in the room.

And a new line has no installed photography yet, so there's nothing to point at.

We built the AI studio MEC Artworks runs. It fills that gap: upload a photo of the space, describe the mural, see it on the wall before it's printed.

Would it help to see one of your new pieces mocked into a real hotel corridor? I'll send it over.
""",
 "brushed gold, botanical, low contrast", """
Susan,

Worth adding — it isn't a rendering job. Someone types "brushed gold, botanical, low contrast" and gets an original concept back, then drops it into a photo of the actual space.

For a line without a back catalogue, that does the job reference images usually do.

ai.mecartworks.com — email code, five previews, no subscription.

If it's not up to your print standards you'll know in two minutes, and I'll take the hint.
""",
 "parking this until your launch", """
Susan,

Closing this off.

Forty years of combined print experience on your team means you've solved harder problems than showing a mural before it exists.

If the Murals & Graphics launch ever needs that, ai.mecartworks.com is the working example.

Good luck with it either way.
""")

add("bardia@thekimiatile.com",
 "no two tiles alike", """
Bardia,

Kimia's line about no two tiles being exactly alike — subtle variation in colour and texture — is the honest way to sell handmade tile.

It's also the hardest thing to sell from a sample. One tile shows the variation; it doesn't show what a whole wall of it looks like, and the wall is what the client is actually buying.

We built the AI studio MEC Artworks runs. Someone describes the space and sees the treatment across a photo of the real wall.

Worth two minutes?
""",
 "character across a wall, inconsistency on a sample", """
Bardia,

The specific gap for handmade: variation reads as character across a wall and as inconsistency on a single sample.

Showing the whole surface before the order is placed removes the objection you probably answer most often.

ai.mecartworks.com — free, five previews, email code.

Two minutes and you'd know whether it renders the variation honestly.
""",
 "the sample-to-wall gap", """
Bardia,

Last note from me.

Building a tile company in the UAE market means you're closer to how your clients decide than I could be from here.

ai.mecartworks.com if the sample-to-wall gap is ever a problem.

Good luck with the growth.
""")

# ───────── HOLD-REVENUE rows: copy written, sending gated on the $1M check ─────────

add("geoffrey@eazywallz.com",
 "Watercolor Forest, and the mural nobody's made", """
Geoffrey,

Eazywallz has the upload path solved — crop tool, live strip preview, pricing as you go. Most of this industry still can't do that.

It assumes the customer arrives with an image though. Someone browsing Wall Mural of the Month because they like Watercolor Forest but want it warmer, or wider, or with different foliage has nowhere to go but the contact form.

We built the AI studio MEC Artworks runs. They describe that variation in words, get an original design, and see it on a photo of their own wall.

Want me to send you a walkthrough?
""",
 "'like that, but warmer'", """
Geoffrey,

The specific: someone types "watercolour forest, warmer, less contrast, twelve feet wide" and gets an original design back — then previews it in their room.

For Eazywallz that's the browser who likes a collection piece but not quite. Right now they either compromise or leave, and your customizer never sees them.

ai.mecartworks.com — email code, five previews, no subscription.

Two minutes tells you whether it's worth more of your time.
""",
 "you already built the hard half", """
Geoffrey,

Last note from me.

You've already built the harder half of this — a working customizer with live pricing is not a small thing, and plenty of bigger companies haven't managed it.

If the design-generation step is ever interesting, ai.mecartworks.com is the working example.

Either way, good luck with the next Mural of the Month.
""")

add("tony@wallsauce.com",
 "Try Before You Buy, without the email round trip", """
Tony,

Wallsauce offers a free wall preview — the customer emails a product code and a photo, and someone sends back a visual.

That's a person in the loop on every one, and a wait in the middle of a buying decision. You built it because it works, which is the interesting part.

We built the AI studio MEC Artworks runs. It does the same thing instantly, and it also generates the design when the customer doesn't have one.

Want me to show you where it would fit?
""",
 "the same service, minus the person", """
Tony,

To be concrete about the difference: your preview service needs a product code, so the customer has already chosen. This one starts a step earlier — they describe what they want, get an original design, then see it on their wall.

Same outcome as Try Before You Buy, without the email round trip or your team's time.

ai.mecartworks.com — five free previews, email code only.

Two minutes and you'd know.
""",
 "you clearly already believe in previews", """
Tony,

I'll stop here.

Running a manual preview service says you already believe seeing it converts people — so this is a question of automation, not of principle.

ai.mecartworks.com if it's ever worth an afternoon.

Either way, the RHG hotel lobby work is a good reference to have.
""")

add("josh@claysquared.com",
 "the Cosmic Collection, on someone's actual wall", """
Josh,

Clay Squared runs three distinct directions at once — the Cosmic Collection, Medieval Floral, and the 1920s–50s mid-century reproductions. That's a lot of range for one studio.

It also means a customer has to work out which one belongs in their room, from photos of other people's rooms. Most of them ask you instead, and that's an artist's afternoon.

We built the AI studio MEC Artworks runs. They describe the space, see a treatment placed in a photo of it, and arrive already decided.

Worth a couple of minutes of an owner's time?
""",
 "an artist's afternoon, back", """
Josh,

The practical version: they type "mid-century, warm rust, geometric" and see it on their own wall before they email you.

For a studio where the owner is also the artist, that afternoon is the whole point.

ai.mecartworks.com — free, five previews, email code.

If it doesn't do your glazes justice, that's worth knowing too.
""",
 "three collections, one decision", """
Josh,

Last one from me.

If customers already find their way between the three collections without much help, then I've invented a problem you don't have.

ai.mecartworks.com if the choosing ever eats your studio time.

Either way, the David Heide collaboration is a good credit to have.
""")

add("caitlin@pophamdesign.com",
 "your simulators, and the pattern that isn't in them", """
Caitlin,

Popham runs two live simulators — concrete and zellige — which puts you further ahead than almost anyone in tile. BACKGAMMON, BRASILIA, KELLY Relief: a customer can play with all of them.

They can only play with patterns you've already drawn, though. The one who wants something adjacent has to describe it to a person and wait.

We built the AI studio MEC Artworks runs. It generates the pattern from a description, then places it in a photo of the actual room.

Worth seeing how it sits in front of the simulators?
""",
 "generating the pattern, not just colouring it", """
Caitlin,

The distinction: your simulators handle colour and layout on existing patterns. This generates the pattern itself, from a sentence, then puts it in the room.

Feeding your simulators customers who arrive knowing what they want seems more useful than replacing anything.

ai.mecartworks.com — five free previews, email code.

You'd judge the output quality faster than I could explain it.
""",
 "what did building the simulators teach you?", """
Caitlin,

I'll leave it here.

You've built two of these already, so you know the cost and the return better than any pitch of mine — and I'd genuinely rather hear what you learned than argue the case.

ai.mecartworks.com if you're curious.

Either way, the simulators are the best thing in this category.
""")
