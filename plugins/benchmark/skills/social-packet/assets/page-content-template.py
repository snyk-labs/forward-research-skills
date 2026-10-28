"""Launch page content: all copy as data. Copy to <project>/social/page_content.py and replace every ‹placeholder›.

Every item that states a number lists the claim IDs it comes from; build_page.py checks each number against those
claims. Numbers that are structure rather than findings (a version in the study's name, a channel limit) go in
STRUCTURAL with a reason. Terms and the "say" / "avoid" lines should carry no numbers.
"""

SITE = "‹study site, e.g. example-bench.org›"

META = dict(
    title="‹Study› Launch Page",                   # page <title>: a 2-4 word name
    study="‹Study name and version›",
    publisher="‹Who ran the study›",
    disclosure="‹Study› is research by ‹publisher›‹, which makes ‹system›, one of the evaluated systems›. All code and data are public.",
    site=SITE,
    footer="‹Study› · ‹site› · built from the published paper's claims registry",
    paper_link_label="[paper link]",               # shown in posts until the paper's URL exists
    paper_link_stub="https://example.org/abs/0000.00000",  # stand-in URL, counted as 23 characters in X posts
    release_gate="Nothing here goes out before the paper is public. Replace [paper link] with the paper's URL when it exists.",
)

# Numbers that are not findings, each with the reason it needs no claim.
STRUCTURAL = {
    # "2": "version number in the study's name",
}

CARDS = {
    # card file stem -> its headline (used as alt text)
    "card01-‹slug›": "‹headline on the card›",
}

STAGE = dict(
    one_liner="‹What the study is, in one sentence. The rule that makes it strict, in a second.›",
    one_liner_claims=["‹C-…›"],
    why=[  # three cards: (heading, text, claims)
        ("‹Why the question matters now.›", "‹One or two sentences.›", []),
        ("‹Why existing comparisons fall short.›", "‹What this study does differently.›", []),
        ("‹What the study found.›", "‹The paper's own one-sentence answer.›", ["‹C-…›"]),
    ],
    facts=[  # (big number, label, claims)
        ("‹n›", "‹units, e.g. open-source projects›", ["‹C-…›"]),
    ],
)

TERMS = [  # (term, plain-language definition): every term a reader meets on the page
    ("‹Term›", "‹Plain definition, no jargon. Say which paper term it replaces if they differ.›"),
]

FINDINGS = [  # in the paper's order of weight; include the findings unfavourable to any system, the authors' included
    dict(id="‹slug›", card="card01-‹slug›", extra_card=None, audience="‹Audience A, Audience B›",
         title="‹Finding title›",
         message="‹One-line message, at the paper's wording ceiling.›",
         proof=["‹Proof point with its number, on a named basis.›",
                "‹The comparison number for every system the claim concerns.›"],
         caveat="‹The caveat that keeps it true, said plainly.›",
         favours=["‹systems this finding reflects well on›"], against=["‹systems it reflects badly on›"],
         claims=["‹C-…›"]),
]

QUOTES = [  # attributions must say "draft"; only facts the paper states
    dict(who="‹Name›, ‹role from the brief› (draft, needs approval)", text="‹Quote.›", claims=[]),
]

LINKEDIN = [  # one point, one card, one audience each; first two lines work on their own
    dict(card="card01-‹slug›", audience="‹Audience›", claims=["‹C-…›"], discloses=True, text=f"""‹Opening line.›

‹What was tested, one sentence.›

• ‹number›
• ‹number›

‹Why it matters to this audience.›

‹Study› is research by ‹publisher›. Data: {SITE}"""),
]

X = [  # <= 280 characters with the paper link appended; each URL counts as 23
    dict(card="card01-‹slug›", claims=["‹C-…›"], discloses=True,
         text=f"‹Number-led line.›\n\n‹The caveat or comparison.›\n\nResearch by ‹publisher›. {SITE}"),
]

GUARDRAILS = dict(
    say=["‹Permitted wording, with its condition.›"],
    avoid=["‹Forbidden wording, and why.›"],
    questions=[  # (likely question, answer that states the facts with the paper's numbers, claims)
        ("‹\"Likely question?\"›", "‹State the fact exactly, with the paper's numbers and where in the paper it is.›", []),
    ],
)
