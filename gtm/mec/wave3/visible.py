"""Reduce a fetched page to the text a human actually reads.

Why this exists. Gate 4 and gate 5 both matched their signal regexes against
raw HTML, and both were wrong in the same way, because raw HTML is not page
copy -- it also contains inline JavaScript, CSS, JSON config blobs and the
class and attribute names of every element. Three of the errors this caused,
all found by measurement rather than by reading the code:

  * gate 5 reported 213 companies running the configurator brand Configura.
    Nearly all were the minified-JS tokens `configuration` and `configurable`,
    and Shopify's `webPixelsConfigList`. Matching visible text with a word
    boundary leaves 17.

  * gate 5 labelled 121 companies DISTRIBUTOR. The commonest match was
    `"import-export-customization":true` -- a feature flag in the Elementor
    WordPress page builder's config JSON. 79 of them were that string.

  * gate 4 read a `module-configurator` CSS class as a product configurator,
    and `area riservata` in a footer as a dealer portal.

The pattern in all of them is the same: a token in the chrome or the code taken
for a fact about the business. Stripping scripts, styles and tags does not make
the regexes smarter, but it makes them answer the question they were written to
answer -- what does this page tell a visitor? -- instead of a question nobody
asked.

What is deliberately lost: alt text, title attributes and meta tags go too.
That costs a few true positives (a visualiser whose only mention is an image
alt) and is worth it, because attribute text is where machine-generated
boilerplate concentrates.
"""
import html as _html
import re

# Non-greedy with DOTALL. The obvious "cleverer" form,
#   <(?:script|style)\b[^>]*>[^<]*(?:<(?!/script)[^<]*)*</script>
# nests quantifiers and backtracks catastrophically on minified bundles; it ran
# for over ten minutes on 839 pages before being abandoned. Keep this one.
_CODE = re.compile(r'<(script|style|noscript|template|svg)\b[^>]*>.*?</\1>', re.I | re.S)
_COMMENT = re.compile(r'<!--.*?-->', re.S)
_TAG = re.compile(r'<[^>]+>')
_WS = re.compile(r'\s+')

def visible_text(body):
    """HTML -> one line of the words a visitor sees."""
    if not body:
        return ''
    b = _CODE.sub(' ', body)
    b = _COMMENT.sub(' ', b)
    b = _TAG.sub(' ', b)
    return _WS.sub(' ', _html.unescape(b)).strip()
