# Round 3 sequence — tryshowhouse, furniture / rugs / wallpaper

Draft for review. Nothing built into a CSV yet.

**Audience:** 259 contacts across 242 companies (`round3_contacts_clean.csv`).
253 from Salone del Mobile 2026, 6 from Heimtextil 2027.
Segment B 251, segment C 8. Studio: furniture 253, rugs 4, wallpaper 2.

**Personalisation available, measured not assumed:**

| field | fill | used for |
|---|---|---|
| `contact_first` | 100% | greeting |
| `products` | 100% | the CTA — their actual product lines from the fair |
| `domain` | 100% | the observation |
| `sells_to` | 100% | which observation applies |
| `site_quote` | 71% | optional opening quote |
| `tool_name` | 3% (7 rows) | segment C only |

**What changed from wave 2, and why**

1. **The CTA on email 1 is now a one-word reply, and carries no link.** Wave 2
   asked them to click a demo *and* send a collection — two asks and a link in a
   cold first touch, which standing rule 9 in §7.9 says not to do. "Reply yes
   and I'll load your products in" is one ask, no link, and the work lands on
   us rather than them.

2. **No timeline claim anywhere.** Wave 2's bodies say "It goes live in weeks"
   and "Live in weeks". The tryshowhouse pricing page says "Live the day you
   sign up" and offers a self-serve Studio plan. Those contradict, it has been
   flagged four times and never resolved, so round 3 makes no claim about
   timing at all rather than repeating one I believe is wrong.

3. **No "AI" in the opening.** Per the §11 competitive check: every competitor
   leads with it. What survives as a differentiator is their own catalogue,
   their own domain, and the lead staying theirs.

---

## Email 1 — day 0

### Variant B-CAT — `sells_to = catalogue only` (66 contacts)

> Hello {first},
>
> {domain} shows the collections properly, and then the visit ends at a catalogue.
>
> What it can't do is put one of your pieces in the room the person is standing in. So they look, they make their mind up alone, and they leave — and you never find out who they were.
>
> Showhouse runs on your own domain, under your branding. A visitor photographs their room and your product appears in it. The image unlocks when they confirm an email, so what you keep is the render, a brief in their own words, and a verified address.
>
> Want to see it with your own {product_phrase}? Reply "yes" and I'll load them in and send it over.
>
> Regards,
>
> Haroon
> Triminage

### Variant B-SHOP — `sells_to = consumer, sells online` (101 contacts)

> Hello {first},
>
> Someone can order a {product_single} from {domain} tonight without ever seeing it in their own room.
>
> That's the gap where most of them stall. They like it, they can't picture it, and they close the tab — no name, no basket, nothing you can follow up.
>
> Showhouse sits on {domain} under your own branding. A visitor photographs their room and your product appears in it. The image unlocks when they confirm an email, so you keep the render, their brief and a verified address together.
>
> Want one built with your own {product_phrase}? Just reply "yes" — I'll put them in and send it to you.
>
> Regards,
>
> Haroon
> Triminage

### Variant B-DEALER — `sells_to = consumer, via dealers` (46 contacts)

> Hello {first},
>
> To see a {product_single} in person, {domain} sends someone to a dealer.
>
> Most never make the trip. The ones who do become the dealer's contact, not yours — so the person who wanted your product is someone you never meet.
>
> Showhouse runs on your own domain, under your branding. A visitor photographs their room and your product appears in it. The image unlocks when they confirm an email, so the name arrives with you first, render and brief attached, before anyone drives anywhere.
>
> Want to see it with your own {product_phrase}? Reply "yes" and I'll load them in for you.
>
> Regards,
>
> Haroon
> Triminage

### Variant B-SOFT — `sells_to = unclear` (40 contacts)

> Hello {first},
>
> A visitor finishes on {domain} knowing a good deal about {company}. You finish knowing nothing about them.
>
> They can see the work, but not in the room they're actually standing in — so they decide on their own and leave unnamed.
>
> Showhouse runs on your own domain, under your branding. They photograph their room, your product appears in it, and the image unlocks once they confirm an email. You keep the render, a brief in their words and a verified address.
>
> Want one with your own {product_phrase} in it? Reply "yes" and I'll set it up.
>
> Regards,
>
> Haroon
> Triminage

### Variant B-GATED — `sells_to = trade portal, gated` (6 contacts)

> Hello {first},
>
> Your catalogue on {domain} sits behind a login, so the people browsing it are dealers who already know you.
>
> The homeowner who searched for a {product_single} last night never got that far. They saw a landing page, and you never saw them at all.
>
> Showhouse gives you the consumer-facing half without touching the trade side. On your own domain, under your branding: they photograph a room, your product appears in it, and the image unlocks when they confirm an email.
>
> Want one loaded with your own {product_phrase}? Reply "yes" and I'll send it across.
>
> Regards,
>
> Haroon
> Triminage

### Variant C — segment C, already runs a tool (8 contacts)

> Hello {first},
>
> You already run {tool_name}, so someone can lay your pieces out properly. Most of this category still can't do that.
>
> What it doesn't do is tell you who they were. They plan, they like it, and they leave with no name attached to any of it.
>
> Showhouse adds that half. Same idea, on your own domain under your branding, except the image unlocks when the visitor confirms an email — so you keep the render, their brief and a verified address.
>
> Want to see it running on your own {product_phrase}? Reply "yes" and I'll build one.
>
> Regards,
>
> Haroon
> Triminage

---

## Email 2 — day 4. Show the lead, don't describe it.

> Hello {first},
>
> Easier to show you than to explain.
>
> When somebody finishes, this is the record that arrives on your side:
>
> — a photo of their actual room with your product in it
> — their own words, something like "low oak frame, warm, wide enough for six"
> — the spec: the piece, the finish, the size
> — and an email address they've confirmed
>
> Nobody filled in a contact form. They'd settled the room, the look and the size before anyone on your team said a word.
>
> Still happy to put your own {product_phrase} into one so you can see yours rather than mine — just say the word.
>
> Regards,
>
> Haroon
> Triminage

---

## Email 3 — day 9. One real question, no pitch.

### Variant 3-A (split by row)

> Hello {first},
>
> A genuine question rather than a pitch.
>
> Of everyone who looked at {domain} last month, how many did you get a name for?
>
> Whatever that number is, the rest of them liked something enough to look. You just never found out who.
>
> Regards,
>
> Haroon
> Triminage

### Variant 3-B (split by row)

> Hello {first},
>
> If someone lands on {domain} tonight and falls for one of your {product_single}s, what do you actually know about them tomorrow morning?
>
> If the answer is nothing, that's the whole reason I wrote.
>
> Regards,
>
> Haroon
> Triminage

---

## Token definitions

| token | source | example |
|---|---|---|
| `{first}` | `contact_first` | Federica |
| `{company}` | `company`, title-cased | Cantori |
| `{domain}` | `domain` | cantori.it |
| `{product_phrase}` | first two entries of `products`, lowercased | "wooden dining tables and upholstered beds" |
| `{product_single}` | first entry of `products`, singular | "wooden dining table" |
| `{tool_name}` | `tool_name` | pCon |

## Open before this can ship

1. **The CTA promises work.** "Reply yes and I'll load your products in" means
   somebody builds a branded demo per yes. At 242 companies, even a 15% yes rate
   is ~36 demos. Campaign 1 is blocked right now for exactly this shape — its
   CTA promised a "build breakdown" asset that does not exist (§3 blocker 1,
   §11 item 1). Need to know who builds these, how long one takes, and whether
   the self-serve Studio plan on the pricing page can carry it instead.
2. **Spam audit not yet run.** `wave2/copy/spam_audit.py` should run over every
   variant before any of this is built, as it did for wave 2's 1,560 emails.
3. **Inbox placement unconfirmed** on the sending domain (§10, Campaign 2 item 1).
