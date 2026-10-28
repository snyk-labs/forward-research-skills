---
name: social-packet
description: "Turn a published benchmark paper's findings into public launch material: a working doc, one shareable launch page (what the study is, plain-language terms, findings with evidence cards, draft quotes, LinkedIn and X posts, say / don't-say guardrails and answers to likely questions), and an image pack rendered from the paper's own figure script. A builder refuses to write the page if a number doesn't trace to the claims registry, a card is missing, an X post runs over, a quote isn't marked as a draft or the disclosure is missing. Use when the user says \"social assets\", \"launch kit\", \"launch page\", \"charts for social\", \"launch posts for the benchmark\", \"LinkedIn and X posts for the paper\", \"highlights from the paper\", \"image pack for marketing\", \"messaging for the launch\", \"what can we post\", \"turn this reply into a chart\", or \"site update with the results\". Only after the paper is public, or with the release gate held. Not for the paper's own figures (paper-authorship) or a single post in a personal voice (the user's voice skill, with these rules)."
---

# Social packet: public launch material from the published paper

**Inputs** (ask for anything missing):

- the public paper and repository (the only sources of numbers), the claims registry (`tables/claims.csv`), the claim inventory, the paper's figure script and tables;
- the narrative guideline's "claims never to make" and wording guardrails;
- the project's visual system and channels, and any audience questions worth answering (replies, comments).

**Outputs** (in the project's `social/` folder):

- the working doc, from `assets/social-assets-template.md`: release gate, audiences, channels, disclosure line, people who may be quoted, the findings list with its balance check, copy rules, the copy-review log, decisions;
- `cards/` with `manifest.csv`, from a card script started from `assets/card-script-skeleton.py`;
- `page_content.py`, from `assets/page-content-template.py`: all copy as data, every item tagged with its claim IDs;
- `page.html`, built by `scripts/build_page.py` from `assets/page-template.html`.

**Human checkpoints:** the working doc's findings list (before any copy); the rendered cards; the finished page; every hand-off to another team. Every quote needs approval from the person it is attributed to. Owners of evaluated systems get the same sign-off chance on material about their system that they had for the paper, offered to every owner on the same terms. Nothing is posted, scheduled, sent or shared by this skill.

**Hand-off:** the human, and through them whoever distributes it; a personal-voice skill, if the user has one, for posts in their own voice, with these rules still applying.

Why a separate step: paper figures are built for readers who check the method; launch material is for people scrolling past, so each piece makes one point in plain words. Short form is where the paper's guardrails are easiest to break, and where one cropped chart or one favourable basis can misrepresent a careful result.

## Objectivity

The plugin's rules (`benchmark:workflow`, "Objectivity comes first") hold here unchanged; launch material is where they are most tested.

- **The set represents the paper.** Findings follow the paper's order of weight, including the ones unfavourable to the authors' product. Leaving a finding out for clarity is fine; leaving it out because of where it points is not.
- **Every system the same.** Each card shows every system in its comparison, in the paper's order and colours; no system gets a highlight, bolder label or annotation the others don't. Comparable results get the same verbs and caveats.
- **The paper's ceiling and basis.** No number is rounded or re-based; a count that depends on which systems, metric or runs it covers names that basis.
- **Disclosure.** The page and at least one post per channel say who ran the study and any tie to an evaluated system.
- **Likely questions get factual answers.** Questions a reader will ask (about limitations, a system's weak result, the authors' tie to a system) get answers that state the facts with the paper's numbers and point to where the paper covers them.

Each finding in the content file declares which systems it reflects well and badly on; the build prints the balance across the set so the human can check it against the paper.

## Order of work

1. **Working doc** with the human: release gate, audiences, channels and counts, disclosure line, who may be quoted (verified roles only), visual system.
2. **Findings list:** each with its message at the paper's ceiling, proof points with claim IDs, the basis behind every count, the caveat that keeps it true, the systems it reflects on, the audience, its card. Fill the balance check. **Checkpoint.**
3. **Cards** (`references/card-production.md`): drawn from the paper's figure script and tables, never by editing images; render them all and look at each at its real size. **Checkpoint.**
4. **Copy as data** in `page_content.py`: one-liner and context, a fact strip, plain-language terms (one term per concept, used everywhere), findings, quotes (drafts, only facts the paper states), posts per `references/channel-rules.md`, guardrails and likely questions. Any number the copy needs that the paper doesn't print gets a pipeline claim first.
5. **Build** with the checks:

   ```
   python3 ‹skill›/scripts/build_page.py --content social/page_content.py --template social/page-template.html \
       --claims analysis/tables/claims.csv --cards social/cards --out social/page.html [--standalone]
   ```

   It refuses to write the page unless every claim ID exists, every card exists, every number traces to its claims (or to the declared `STRUCTURAL` list, with a reason), every X post fits in 280 characters with the paper link, every quote says "draft", every finding declares its balance, and the disclosure is present. Use `--standalone` for a static HTML file; without it the output is a page body for a host that adds the document skeleton, such as a published Claude artifact.
6. **Copy review** by a fresh reviewer (`references/copy-review.md`), then fixes and a rebuild; log the round in the working doc.
7. **Publish privately or deliver the file,** persist everything in the project, and tell the human: the page is private until they share it, which quotes need approval, where the link placeholder is, and which counts depend on a basis. **Checkpoint.** Later changes go through `page_content.py` and a rebuild.

Short-form wording rules are in `references/short-form-rules.md`; restate them in the working doc with the study's own names and metrics.

## Do not

Do not post, schedule, send or share anything. Do not use a number that is not in the public paper or repository. Do not turn adjudicated or supplementary results into headline claims the paper itself keeps separate. Do not present a draft quote as approved.
