# Channel rules

## All channels

- **One point per post.** Each post is paired with one card, and the card's headline and the post's opening line make the same point.
- **Plain words.** Use the page's terms list, the same words everywhere, for example "answer key" rather than "reference set" or "found" rather than "matched", if those are the page's terms.
- **Name systems as the paper does,** in the shortest unambiguous form, with the setting where a number is attached. Every system gets the same naming treatment.
- **Keep the paper's ceiling.** A post never says more than the paper's wording allows: no "beats" for results the paper calls close, no "because" where it says "consistent with".
- **End on the public data:** the study's site, and the paper's link once it exists.
- **No padding:** avoid "delve", "game-changer", "in today's fast-paced world", "unlock" and similar.
- **Emoji and hashtags:** one or two at most, and only where the publisher's channels use them.
- **Disclosure:** at least one post per channel says who ran the study and any tie to an evaluated system (`discloses=True` in the content file; the build checks it).

## Opening lines (vary them across a set)

| Pattern | Shape |
|---|---|
| Question | "Do ‹systems› find the same ‹items›? We checked ‹n›." |
| Number first | "‹n› of ‹N› ‹items›: ‹what the number means›." |
| Contrast | "‹System A›: ‹value›. ‹System B›: ‹value›. Same ‹units›, same rule." |
| What surprised us | "We expected ‹x›. The data said ‹y›." (only if the prediction was recorded before the results) |
| Lessons list | "What we learned running ‹study›: 1. … 2. … 3. …" |
| Announcement | "We just published ‹study›: …" (carries the disclosure) |
| Open question | "What ‹study› couldn't answer yet: …" (from the paper's future work) |

## LinkedIn

- **Length:** 600–1,300 characters. The first two lines must work on their own, because they show above "see more".
- **Structure:**
  1. opening line;
  2. what was tested, in one sentence;
  3. two or three numbered or bulleted points with their numbers, each with the comparison it needs;
  4. why it matters to this post's audience;
  5. the link to the data.
- **Coverage:** one or more posts per audience in the working doc, and at least one announcement post with the disclosure.

## X

- **Hard limit:** 280 characters, counted as X counts them: every URL is 23 characters, whatever its length. Include the paper's link in the count before it exists (the build appends a stand-in URL). Emoji and some scripts count double; keep a margin.
- **Shape:** lead with the number, use line breaks for rhythm, keep one claim per post.
- **Caveats:** if a post's claim needs one and it doesn't fit, the card carries it. If the card can't carry it either, drop the post.

## Audiences

Write each post for one audience, from the working doc. Typical ones: practitioners who use systems like these, decision makers who choose between them, researchers who build or evaluate them, and the builders of the evaluated systems themselves. Lead with what that audience can act on, from the same findings and with the same caveats.
