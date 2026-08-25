const fs = require('fs');
const d = require('docx');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  WidthType, ShadingType, BorderStyle, AlignmentType, HeadingLevel,
  LevelFormat, TabStopType, PageBreak
} = d;

const W = 9360;                 // content width, Letter with 1" margins
const INK = '10171A', MUTED = '4C5C63', ACCENT = '0D6E79', CLAY = 'A84C28', GOLD = '7E6120';
const SHADE = 'F2F5F5', SHADE2 = 'FAFAFA', WARN = 'FBEEE8', RULE = 'F6F1E2';

const kids = [];
const P = (o) => kids.push(new Paragraph(o));

// ---- helpers ---------------------------------------------------------------
const run = (text, o = {}) => new TextRun({ text, font: o.font || 'Calibri', size: o.size || 20,
  bold: o.bold, italics: o.italics, color: o.color || INK, allCaps: o.caps, characterSpacing: o.cs });

const body = (text, o = {}) => P({ spacing: { after: 140, line: 276 },
  children: [run(text, o)] });

const h1 = (text) => P({ heading: HeadingLevel.HEADING_1, spacing: { before: 360, after: 160 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: INK, space: 6 } },
  children: [run(text, { font: 'Georgia', size: 30, bold: true })] });

const h2 = (text) => P({ heading: HeadingLevel.HEADING_2, spacing: { before: 280, after: 120 },
  children: [run(text, { font: 'Georgia', size: 24, bold: true })] });

const label = (text) => P({ spacing: { before: 220, after: 90 },
  children: [run(text, { font: 'Consolas', size: 15, bold: true, color: MUTED, caps: true, cs: 12 })] });

const bullet = (text, o = {}) => P({ numbering: { reference: 'dots', level: 0 },
  spacing: { after: 90 }, children: [run(text, o)] });

const step = (text) => P({ numbering: { reference: 'steps', level: 0 },
  spacing: { after: 90 }, children: [run(text)] });

const cell = (children, o = {}) => new TableCell({
  width: { size: o.w, type: WidthType.DXA },
  shading: o.fill ? { type: ShadingType.CLEAR, fill: o.fill, color: 'auto' } : undefined,
  margins: { top: 90, bottom: 90, left: 130, right: 130 },
  children,
});

// generic data table: cols = [w,...], head = [str,...], rows = [[str|{t,b,color},...],...]
function table(cols, head, rows, opts = {}) {
  const trs = [];
  if (head) trs.push(new TableRow({ tableHeader: true, children: head.map((h, i) =>
    cell([new Paragraph({ children: [run(h, { font: 'Consolas', size: 15, bold: true, color: MUTED, caps: true })] })],
      { w: cols[i], fill: SHADE })) }));
  rows.forEach(r => trs.push(new TableRow({ children: r.map((c, i) => {
    const o = typeof c === 'string' ? { t: c } : c;
    return cell([new Paragraph({ children: [run(o.t, { bold: o.b, color: o.color, italics: o.i,
      font: o.mono ? 'Consolas' : 'Calibri', size: o.mono ? 18 : 20, strike: o.strike })] })],
      { w: cols[i], fill: o.fill });
  }) })));
  kids.push(new Table({ columnWidths: cols, width: { size: W, type: WidthType.DXA },
    borders: {
      top:{style:BorderStyle.SINGLE,size:4,color:'D6DCDE'}, bottom:{style:BorderStyle.SINGLE,size:4,color:'D6DCDE'},
      left:{style:BorderStyle.SINGLE,size:4,color:'D6DCDE'}, right:{style:BorderStyle.SINGLE,size:4,color:'D6DCDE'},
      insideHorizontal:{style:BorderStyle.SINGLE,size:2,color:'E8ECED'},
      insideVertical:{style:BorderStyle.SINGLE,size:2,color:'E8ECED'},
    }, rows: trs }));
  if (!opts.tight) P({ spacing: { after: 120 }, children: [] });
}

// callout box
function callout(tag, paras, kind = 'note') {
  const fill = kind === 'warn' ? WARN : kind === 'rule' ? RULE : SHADE;
  const bar  = kind === 'warn' ? CLAY : kind === 'rule' ? GOLD : ACCENT;
  const inner = [new Paragraph({ spacing: { after: 90 },
    children: [run(tag, { font: 'Consolas', size: 15, bold: true, color: bar, caps: true })] })];
  paras.forEach((t, i) => inner.push(new Paragraph({ spacing: { after: i === paras.length - 1 ? 0 : 110 },
    children: typeof t === 'string' ? [run(t)] : t })));
  kids.push(new Table({ columnWidths: [W], width: { size: W, type: WidthType.DXA },
    borders: {
      top:{style:BorderStyle.NONE}, bottom:{style:BorderStyle.NONE}, right:{style:BorderStyle.NONE},
      insideHorizontal:{style:BorderStyle.NONE}, insideVertical:{style:BorderStyle.NONE},
      left:{style:BorderStyle.SINGLE,size:18,color:bar},
    },
    rows: [new TableRow({ children: [cell(inner, { w: W, fill })] })] }));
  P({ spacing: { after: 140 }, children: [] });
}

// message block: rows of [blockLabel, text(may contain blank-line paragraphs)]
function message(head, sub, blocks, count) {
  const hdr = [run(head, { font: 'Consolas', size: 16, bold: true, color: MUTED, caps: true })];
  if (sub) hdr.push(run('   ' + sub, { font: 'Consolas', size: 18, bold: true, color: INK }));
  if (count) hdr.push(run('   ' + count, { font: 'Consolas', size: 15, color: MUTED }));
  const trs = [new TableRow({ children: [
    cell([new Paragraph({ children: hdr })], { w: W, fill: SHADE }),
  ] })];
  const inner = [];
  blocks.forEach(([lab, txt]) => {
    const paras = String(txt).split('\n\n').map((t, i, a) => new Paragraph({
      spacing: { after: i === a.length - 1 ? 0 : 120 },
      children: [run(t, { font: 'Consolas', size: 18 })] }));
    inner.push(new TableRow({ children: [
      cell([new Paragraph({ children: [run(lab, { font: 'Consolas', size: 14, bold: true, color: ACCENT, caps: true })] })],
        { w: 1900, fill: SHADE2 }),
      cell(paras, { w: W - 1900 }),
    ] }));
  });
  kids.push(new Table({ columnWidths: [W], width: { size: W, type: WidthType.DXA },
    borders: { top:{style:BorderStyle.SINGLE,size:4,color:'D6DCDE'}, bottom:{style:BorderStyle.NONE},
      left:{style:BorderStyle.SINGLE,size:4,color:'D6DCDE'}, right:{style:BorderStyle.SINGLE,size:4,color:'D6DCDE'},
      insideHorizontal:{style:BorderStyle.NONE}, insideVertical:{style:BorderStyle.NONE} },
    rows: trs }));
  kids.push(new Table({ columnWidths: [1900, W - 1900], width: { size: W, type: WidthType.DXA },
    borders: { top:{style:BorderStyle.NONE}, bottom:{style:BorderStyle.SINGLE,size:4,color:'D6DCDE'},
      left:{style:BorderStyle.SINGLE,size:4,color:'D6DCDE'}, right:{style:BorderStyle.SINGLE,size:4,color:'D6DCDE'},
      insideHorizontal:{style:BorderStyle.SINGLE,size:2,color:'E8ECED'},
      insideVertical:{style:BorderStyle.SINGLE,size:2,color:'E8ECED'} },
    rows: inner }));
  P({ spacing: { after: 160 }, children: [] });
}

// ============================ CONTENT ======================================

P({ spacing: { after: 60 }, children: [run('MEC ARTWORKS AI  ·  OUTREACH COPY  ·  25 AUGUST 2026',
  { font: 'Consolas', size: 15, bold: true, color: MUTED, caps: true, cs: 20 })] });
P({ spacing: { after: 140 }, children: [run('Concept to Yes', { font: 'Georgia', size: 56, bold: true })] });
P({ spacing: { after: 200 }, border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: 'D6DCDE', space: 10 } },
  children: [run('Test copy for three prospects, written against what the product actually does — which is not what our own master doc says it does.',
    { font: 'Georgia', size: 24, color: MUTED })] });

table([2340, 2340, 2340, 2340],
  ['Channels', 'Sendable list', 'Frameworks', 'Status'],
  [[ 'LinkedIn (Shahwaz) → Email (Haroon)', '42 KEEP rows', 'House 4-block · BAB', 'Touches 1–2 launch-ready' ]]);

// ---- 1
h1('1.  What the product actually is');
body('I could not reach the Triminage portfolio page from the drafting environment, so I read MEC’s own published pages about the tool instead. What they describe does not match §7 of the master doc.');

table([4680, 4680],
  ['What CLAUDE.md §7 says', 'What AI Mosaic Studio does'],
  [[
    { t: '“User sets palette, pattern style, tile density and scale → renders mosaic visualisations in real time via canvas-based rendering.”  A parametric configurator: you move sliders, it redraws.', color: MUTED },
    { t: 'IMAGINE FROM SCRATCH — describe a mosaic in everyday words; the AI generates an original concept from your colour, subject, mood and material. “You don’t need to draw. You don’t need CAD experience.”  CUSTOMIZE YOUR SPACE — upload a photo of the actual room, choose the surface, generate a preview of the mosaic in place.' },
  ]]);

callout('Why this matters', [
  'The copy drafted earlier pitched a slider-based configurator. It would have described the wrong product to a prospect who then clicked through and saw something else — the fastest way to lose a technical buyer’s trust.',
  [run('Someone should reconcile §7 of the master doc against the live app.', { bold: true }),
   run(' Either the product moved from canvas rendering to generative AI, or the doc recorded the build stack and not the user experience. Until that is settled, treat the copy below as authoritative and §7 as stale.')],
], 'warn');

h2('The real pitch, in one line');
body('A client describes what they want in ordinary language and sees it on a photograph of their own wall — before anyone quotes, samples or fabricates.');

label('Access terms — these are the CTA');
bullet('Free. Five high-resolution previews.');
bullet('Email verification only — a one-time code. No password to create, no subscription to manage.');
bullet('Uploads accept JPEG, PNG and WebP up to 10 MB.');
body('“No password, no subscription” is worth saying out loud. It removes the objection the reader forms while reading the sentence.');

// ---- 2
h1('2.  The problem nobody has raised yet');
P({ spacing: { after: 140, line: 276 }, children: [
  run('ai.mecartworks.com is MEC Artworks’ own lead-generation asset.', { bold: true }),
  run(' It is their brand, it captures emails, and it feeds their custom mosaic business. MEC Artworks is a mosaic company — and §7.2 lists five of our prospects as direct MEC competitors: New Ravenna, Artistic Tile, Aqua Blu Mosaics, Hakatai, Blue Water Pool Mosaics.'),
] });

callout('Open question for Abdullah — new', [
  'Abdullah dropped the competitor concern, but that answer was about whether we may target MEC’s competitors. This is the opposite direction: are we comfortable sending a rival mosaic firm to a competitor’s branded, email-gated tool and asking them to register?',
  'They will recognise MEC within seconds. Handled badly it reads as careless. Handled deliberately it is a strong pitch — “a mosaic house your size built this; we built it for them” — but it has to be a choice, not an accident.',
], 'warn');

h2('How the copy below handles it');
table([2400, 2000, 4960],
  ['Segment', 'MEC competitor?', 'CTA used'],
  [
    ['Mosaic / pool / artisan tile', { t: 'Yes — direct', color: CLAY, b: true }, 'No raw link. Offer a walkthrough. Name MEC openly as our client rather than letting them discover it'],
    ['Murals & wallcoverings', 'No — different product', 'Send the link. “Free, five previews, no signup wall”'],
    ['Ceramic tile (catalogue-led)', 'Partly', 'Judgement per row. Default to the walkthrough'],
  ]);

// ---- 3
h1('3.  Which frameworks, and why');
table([2400, 1500, 5460],
  ['Framework', 'Verdict', 'Reasoning'],
  [
    [{ t: 'House 4-block\nObservation → Consequence → Proof → CTA', b: true }, { t: 'VARIANT A', b: true, color: ACCENT }, 'Standing rule 13, and the designed fix for Campaign 2’s failure. Still unproven, so it has to be the primary'],
    [{ t: 'BAB\nBefore → After → Bridge', b: true }, { t: 'VARIANT B', b: true, color: ACCENT }, 'The only framework whose middle step is satisfied by a working link. “After” is a thing we can show instead of claim'],
    ['AIDA', { t: 'Reject', color: CLAY }, '“Desire” needs a claim that makes them want it. MEC has no published performance figures — manufacturing desire means inventing proof'],
    ['PAS', { t: 'Reject', color: CLAY }, '“Agitate” means telling a stranger their pain is worse than they think. We did that with Jubi and were wrong'],
    ['QVC · SPIN · sniper', { t: 'Hold', color: MUTED }, 'A cold question invites “no”; SPIN needs dialogue; sniper is for the 200+ headcount rows'],
  ]);

callout('Standing rule 13 needs a MEC carve-out', [
  [run('Rule 13 sets block 3 as “CureMD proof.” Correct for the healthcare campaigns. Wrong here — quoting 98% note accuracy from a medical-scribe build to a tile studio reads like a stock agency deck. '),
   run('For MEC, block 3 is the tool itself.', { bold: true })],
], 'rule');

h2('What we may and may not say');
table([4680, 4680],
  ['Safe — publicly verifiable', 'Never'],
  [
    ['Describe a mosaic in plain words, get an original concept', 'Any percentage, hours saved, or conversion figure'],
    ['Upload a room photo, choose a surface, preview in place', 'Any named MEC customer'],
    ['Five free previews · email code · no password or subscription', 'CureMD’s figures — wrong client, wrong campaign'],
    ['Built by Triminage in 7 weeks with a team of 3 (per §0; not re-verified)', 'That we know their internal process — we know their website'],
  ]);

callout('The Jubi rule', [
  'Never assert a prospect does something by hand or lacks a tool. We were wrong once, on the best-researched name in the file. Every observation below comes from their own site copy or their contact’s job title — never from what we assume happens inside.',
]);

// ---- 4 New Ravenna
kids.push(new Paragraph({ children: [new PageBreak()] }));
h1('4.  New Ravenna');
table([2600, 6760], null, [
  [{ t: 'Contact', fill: SHADE, mono: true }, { t: 'Stephenie Wilkins — Concept Board Team Manager — swilkins@newravenna.com', b: true }],
  [{ t: 'Profile', fill: SHADE, mono: true }, 'Row 12 · Mosaic / Pool · $10–25M · Exmore, VA · Priority 1 · DIRECT MEC COMPETITOR'],
  [{ t: 'Why', fill: SHADE, mono: true }, 'They employ a manager whose job title is the approval step we sell into. Not an inference — it is her title. Strongest observation in the file.'],
]);

callout('CTA changed for this row', [
  'No raw link. New Ravenna is a $10–25M mosaic house; MEC is a mosaic house. Asking them to hand an email to a competitor’s tool is the wrong ask. We name MEC as our client up front and offer to walk them through it instead.',
], 'warn');

label('Subject lines');
table([1100, 4000, 4260], ['Touch', 'Subject', 'Rationale'], [
  ['1', { t: 'your concept board team', mono: true }, 'Names her actual team. Cannot be mistaken for a blast'],
  ['2', { t: 'describing it in plain words', mono: true }, 'The new specific thing — how the tool actually works'],
  ['3', { t: 'closing this out', mono: true }, 'Honest breakup, no manufactured urgency'],
]);

message('Touch 1 · Variant A', 'your concept board team', [
  ['Persona bridge', 'Stephenie — my colleague Shahwaz reached out on LinkedIn recently, so I’ll keep this short.'],
  ['1 · Observation', 'New Ravenna turns client photographs and fabric swatches into mosaic concepts before anything is cut. You have a team manager for that step, which says it carries real weight.'],
  ['2 · Consequence', 'That first pass is usually where custom work stalls — not fabrication.'],
  ['3 · Proof', 'We built the AI studio MEC Artworks runs. A client types what they want in plain words, uploads a photo of the room, and sees the mosaic on their own wall.'],
  ['4 · CTA', 'Happy to walk you through it — worth a look?'],
], '86 words');

message('Touch 1 · Variant B · BAB', 'before the client says yes', [
  ['Persona bridge', 'Stephenie — Shahwaz messaged you on LinkedIn recently; short version here.'],
  ['Before', 'A concept board goes out, then there’s a wait — feedback, a revision, another board, and a client who can still change direction.'],
  ['After', 'Now imagine they describe the change in a sentence and see it on a photo of their own wall while you’re still talking.'],
  ['Bridge', 'That’s what we built for MEC Artworks. I can show you the working version — want me to?'],
], '84 words');

message('Touch 2 · +3–4 days', 'describing it in plain words', [
  ['New specific', 'Stephenie — the part I should have led with.\n\nThere’s no drawing and no CAD in it. Someone types “warm terracotta, geometric, Moorish influence” and gets an original concept back. Then they upload a photo of the wall and see it in place.\n\nThe reason I think it’s relevant to a concept board team: it doesn’t replace the board, it gets the client to a direction before the board is worth making.\n\nFifteen minutes on a call and you’ll know whether that’s useful or not.'],
]);

message('Touch 3 · +4–5 days', 'closing this out', [
  ['Soft breakup', 'Stephenie — I’ll leave this alone now.\n\nIf the concept stage is already as fast as you want it, that’s a good place to be and I’m glad I asked.\n\nIf it ever becomes the bottleneck — usually when volume climbs rather than when the work itself changes — we’re easy to find.\n\nThanks for reading this far.'],
]);

label('LinkedIn — Shahwaz');
message('Invite note', null, [
  ['Note', 'Hi Stephenie — your title caught my eye. Having a manager dedicated to concept boards says a lot about how much of New Ravenna’s work happens before a client says yes. That step is what I spend my time on. Would like to follow what your team puts out.'],
], '251 / 280 chars');

message('DM on accept', null, [
  ['Message', 'Thanks for connecting, Stephenie.\n\nI’ll be straight about who I am: we’re the studio that built the AI mosaic tool MEC Artworks runs. They’re in your industry, so I’d rather say that up front than have you find it.\n\nWhat it does: a client describes a mosaic in ordinary words — colour, mood, subject — and gets an original concept. Then they upload a photo of the actual room and see it on the wall.\n\nIt’s aimed at the stage before a concept board is worth making. Given your team owns exactly that step, I’d value your read on it more than most people’s.\n\nWant me to walk you through it?'],
]);

// ---- 5 Area Environments
kids.push(new Paragraph({ children: [new PageBreak()] }));
h1('5.  Area Environments');
table([2600, 6760], null, [
  [{ t: 'Contact', fill: SHADE, mono: true }, { t: 'Heather Neurer — Design Manager — hneurer@areaenvironments.com', b: true }],
  [{ t: 'Profile', fill: SHADE, mono: true }, 'Row 54 · Murals & wallcoverings · $1–5M · Priority 1 · Trade-only · Not a competitor'],
  [{ t: 'Why', fill: SHADE, mono: true }, 'Highest tool-gap-to-need ratio in the file. Trade-only — §7.4’s strongest free signal — plus an explicit upload-your-own-artwork offer. Direct site visit, so findings are solid.'],
]);

label('Subject lines');
table([1100, 4000, 4260], ['Touch', 'Subject', 'Rationale'], [
  ['1', { t: 'bring your own artwork', mono: true }, 'Their own FAQ language, quoted back'],
  ['2', { t: 'five previews, no signup wall', mono: true }, 'States the exact cost of acting'],
  ['3', { t: 'last note from me', mono: true }, 'Clean exit'],
]);

message('Touch 1 · Variant A', 'bring your own artwork', [
  ['Persona bridge', 'Heather — my colleague Shahwaz reached out on LinkedIn recently, so I’ll keep this short.'],
  ['1 · Observation', 'Your FAQ says if someone brings a piece or a photograph, Area will build the wallcovering around it. That’s a real offer, and trade-only — so a designer specifies it to a client waiting on the other side.'],
  ['2 · Consequence', 'Right now that client approves from a sample and their imagination.'],
  ['3 · Proof', 'We built a tool for MEC Artworks where you upload a photo of the room and see the design on the actual wall. It’s free and live.'],
  ['4 · CTA', 'Want the link?'],
], '89 words');

message('Touch 1 · Variant B · BAB', 'approving from a sample', [
  ['Persona bridge', 'Heather — Shahwaz messaged you on LinkedIn recently; short version.'],
  ['Before', 'A designer brings artwork to Area, you build the wallcovering around it, and their client signs off from a sample and a lot of trust.'],
  ['After', 'With a preview, that client sees it on their own wall before anyone commits to a print run.'],
  ['Bridge', 'We built one for MEC Artworks — free, five previews, no subscription. Send it over?'],
], '82 words');

message('Touch 2 · +3–4 days', 'five previews, no signup wall', [
  ['New specific', 'Heather — should have included this first time.\n\nIt’s at ai.mecartworks.com. An email code gets you five high-resolution previews. No password to create, no subscription.\n\nUpload a photo, describe what you want, pick the surface. Given every Area piece starts with a specific artist’s work, the honest test is whether the result looks like something you’d put in front of a designer.\n\nIf it doesn’t, that’s a fair answer and I’ll stop here.'],
]);

message('Touch 3 · +4–5 days', 'last note from me', [
  ['Soft breakup', 'Heather — I’ll stop here.\n\nSelling to the trade only means your approval cycle runs through someone else’s client, which is the hardest version of this to fix from the inside. If Area ever wants to hand designers something they can show live, ai.mecartworks.com is the example.\n\nEither way — paying artists a royalty on every wallcovering sold in their name is a genuinely good thing to see in this industry.'],
]);

label('LinkedIn — Shahwaz');
message('Invite note', null, [
  ['Note', 'Hi Heather — I read that Area builds a wallcovering around a client’s own piece or photograph, and that every artist earns a royalty on what sells in their name. That’s a rare way to run it. I work on the design-approval side of this world and would like to connect.'],
], '266 / 280 chars');

message('DM on accept', null, [
  ['Message', 'Thanks for connecting, Heather.\n\nTwo things stood out: Area sells to the trade only, and your FAQ says if someone brings a piece, a photograph or a concept, you’ll build the wallcovering around it.\n\nSo a designer is specifying your work to a client who has to picture the result before approving it.\n\nWe built a tool for MEC Artworks that closes that gap — you upload a photo of the room, describe the design in plain words, and see it on the wall. Free, five previews, no subscription.\n\nWorth two minutes on one of your artist collections. Want the link?'],
]);

// ---- 6 US Vinyl
kids.push(new Paragraph({ children: [new PageBreak()] }));
h1('6.  US Vinyl Manufacturing');
table([2600, 6760], null, [
  [{ t: 'Contact', fill: SHADE, mono: true }, { t: 'Susan Steinicke — Creative Director — susansteinicke@usvinyl.com', b: true }],
  [{ t: 'Profile', fill: SHADE, mono: true }, 'Row 57 · Wallcovering / hospitality · $5–10M · La Fayette, GA · Priority 1 · Live rebrand'],
  [{ t: 'Why', fill: SHADE, mono: true }, 'A dated reason to write now: mid-rebrand into “USV Wallcovering Murals Graphics”, a stated move beyond hotel standards into art-led work.'],
]);

callout('Do not mention', [
  'Their site runs Joomla over plain HTTP. That is useful context for us and an insult if said aloud. It never appears in copy.',
], 'warn');

label('Subject lines');
table([1100, 4000, 4260], ['Touch', 'Subject', 'Rationale'], [
  ['1', { t: 'USV Murals & Graphics', mono: true }, 'Their own new line name'],
  ['2', { t: 'a new line has no install photos yet', mono: true }, 'A real insight about launching'],
  ['3', { t: 'wrapping up', mono: true }, 'Clean exit'],
]);

message('Touch 1 · Variant A', 'USV Murals & Graphics', [
  ['Persona bridge', 'Susan — my colleague Shahwaz reached out on LinkedIn recently, so I’ll keep this brief.'],
  ['1 · Observation', 'USV Murals & Graphics is a different sell from hotel standards. Marriott and Hilton buy to spec. Art-led work gets bought on how it looks in the room.'],
  ['2 · Consequence', 'That’s the harder thing to show from a sample book.'],
  ['3 · Proof', 'We built a tool for MEC Artworks where a client uploads a photo of the space, describes what they want, and sees it on the wall. Free to try.'],
  ['4 · CTA', 'For a line that sells on look, might be two minutes well spent.'],
], '88 words');

message('Touch 1 · Variant B · BAB', 'spec work vs art-led work', [
  ['Persona bridge', 'Susan — Shahwaz messaged you on LinkedIn recently; here’s the short version.'],
  ['Before', 'A hotel client picks from a standard and knows exactly what arrives. An art-led mural is the opposite — they’re approving something they’ve never seen at scale.'],
  ['After', 'With a preview they see it at scale, in their own space, before the print run is committed.'],
  ['Bridge', 'We built one for MEC Artworks and it’s free to try. Want the link?'],
], '85 words');

message('Touch 2 · +3–4 days', 'a new line has no install photos yet', [
  ['New specific', 'Susan — one more thought, then I’ll leave it.\n\nThe reason I think this is relevant to the Murals & Graphics launch specifically: a new creative direction has no back catalogue of installed photography to point at. Showing it live does the job reference images usually do.\n\nIt’s at ai.mecartworks.com — email code, five previews, no subscription. Upload a space, describe the mural, see it in place.\n\nTwo minutes will tell you whether I’m right.'],
]);

message('Touch 3 · +4–5 days', 'wrapping up', [
  ['Soft breakup', 'Susan — last one from me.\n\nForty years of combined print experience and a client list like yours means you’ve solved harder problems than this one. If the new line ends up needing a way to show work before it exists, ai.mecartworks.com is the example to look at.\n\nGood luck with the launch either way.'],
]);

label('LinkedIn — Shahwaz');
message('Invite note', null, [
  ['Note', 'Hi Susan — I saw USV is moving into Murals & Graphics as a new creative direction, beyond the hotel-standard lines. Art-led wallcovering is a different sell from spec work, and that shift is the part I find interesting. Would like to connect and follow it.'],
], '256 / 280 chars');

message('DM on accept', null, [
  ['Message', 'Thanks for connecting, Susan.\n\nThe Murals & Graphics direction is what caught my attention. Supplying Marriott, Hilton and IHG to spec is one business. Art-led work is a different one — it gets bought on how it looks in the room, and that’s much harder to show on a sample board.\n\nWe built a tool for MEC Artworks that handles exactly that: upload a photo of the space, describe the mural in plain words, see it on the wall. Free, five previews.\n\nFor a line that sells on look rather than spec, might be worth two minutes. Want the link?'],
]);

// ---- 7
kids.push(new Paragraph({ children: [new PageBreak()] }));
h1('7.  Scaling to the other 39');
message('Variant A template', null, [
  ['Persona bridge', '{first_name} — my colleague Shahwaz reached out on LinkedIn recently, so I’ll keep this short.'],
  ['1 · Observation', '{One true, specific thing — quote their CUSTOM_OFFERING or HOOK column, or their contact’s job title. Must be checkable on their own site.}'],
  ['2 · Consequence', '{One sentence on what that costs them, in their language.}'],
  ['3 · Proof', 'We built a tool for MEC Artworks where a client describes what they want in plain words, uploads a photo of the space, and sees it on the wall.'],
  ['4 · CTA', '{Rotate — never the same closing twice in one batch.}'],
]);

label('CTA rotation pool');
bullet('“Want the link?” — non-competitors only');
bullet('“Open to seeing it?”');
bullet('“Happy to walk you through it — worth a look?” — competitor segment');
bullet('“Might be two minutes well spent.”');

label('Column → copy mapping');
table([3200, 6160], ['Copy slot', 'Source column'], [
  ['Observation', { t: 'Use AI Custom Offering  /  Use AI Hook', mono: true }],
  ['Greeting', { t: 'Combined First Names', mono: true }],
  ['CTA choice', { t: 'niche — mosaic/tile → walkthrough, murals → link', mono: true }],
  [{ t: 'Never cite', b: true, color: CLAY }, { t: 'Use AI Visual Tool on rows 4, 12, 27, 42 — unverified', mono: true }],
]);

label('Instantly headers — collision-proof only');
body('msg_subject_line · msg_first_touch · msg_linkedin_dm · dm_first_name · company_name · segment', { font: 'Consolas', size: 18 });
body('Never name a variable email_subject or email_body — they collide with Instantly system fields and cost us a campaign rebuild once already.');

// ---- 8
h1('8.  Reading the results');
callout('Do not run this as an A/B', [
  [run('42 rows split two ways is 21 per arm. At a realistic 5–10% reply rate each arm returns one or two replies. '),
   run('Two replies against one is not a result — it is noise.', { bold: true }),
   run(' No split of a list this size can tell you which framework is better.')],
  'This is the same trap as Campaign 2’s open rates: a number that looks like evidence and is not.',
], 'warn');

label('Do this instead');
step('Run Variant A across all 42. It is the standing rule and the unproven Campaign 2 fix — the thing you actually need an answer about.');
step('Read replies qualitatively. At this volume what people say carries far more than the rate. “Wrong person”, “not interested” and “we already have one” are three different findings.');
step('Hold Variant B in reserve. If A returns near-zero after roughly 20 sends, switch rather than split. A sequential switch beats an underpowered split.');
step('If you must split, split the CTA — walkthrough versus raw link. That changes behaviour far more than sentence structure, and doubles as the competitor test.');

label('Measure');
table([3200, 6160], ['Metric', 'Use'], [
  ['Reply rate', 'Primary'],
  ['Positive-reply rate', 'The real one'],
  ['Previews generated', 'Ask MEC — anyone who uploads a room has self-qualified hard'],
  [{ t: 'Open rate', strike: true, color: MUTED }, { t: 'Ignore. Machine opens make it noise', color: MUTED }],
]);

// ---- 9
h1('9.  Before anything sends');
bullet('Reconcile §7 of the master doc against the live app — canvas renderer or generative AI?');
bullet('Abdullah: are we comfortable pointing MEC’s direct competitors at MEC’s own lead-capture tool?');
bullet('Abdullah: tool access or custom build, and at what price. Touches 1–2 are safe without it; reply handling is not.');
bullet('Sending domain + 3-week warm-up — still not started, still the only uncompressible item on the critical path.');
bullet('Eyeball the tool question on rows 4, 12, 27 and 42 before their copy goes out.');
bullet('LinkedIn first, email second. 12–15 invites/day, weekdays. Never follow up inside 48 hours.');

P({ spacing: { before: 320 }, border: { top: { style: BorderStyle.SINGLE, size: 4, color: 'D6DCDE', space: 10 } },
  children: [run('Copy written 25 August 2026 against MEC’s published product pages. The Triminage portfolio page was unreachable from the drafting environment — figures attributed to §0 are carried from the master doc, not re-verified.',
    { size: 17, color: MUTED, italics: true })] });

// ============================ DOCUMENT =====================================
const doc = new Document({
  numbering: { config: [
    { reference: 'dots', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•',
      alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 360, hanging: 220 } } } }] },
    { reference: 'steps', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.',
      alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 400, hanging: 260 } } } }] },
  ] },
  styles: { default: { document: { run: { font: 'Calibri', size: 20, color: INK } } } },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
    children: kids,
  }],
});

Packer.toBuffer(doc).then(b => {
  fs.writeFileSync('MEC_Copy_Deck.docx', b);
  console.log('wrote MEC_Copy_Deck.docx', b.length, 'bytes');
});
