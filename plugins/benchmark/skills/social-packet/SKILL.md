---
name: social-packet
description: "Turn a published benchmark paper's findings into public chart and highlight assets for a website and social channels: a release gate, short-form copy rules derived from the paper's guardrails, one spec per asset (takeaway, chart, numbers, paper figure and claim, caveat line), an image pack rendered from the paper's own figure script, and a sourced copy bank. Use when the user says \"social assets\", \"charts for social\", \"launch posts for the benchmark\", \"highlights from the paper\", \"image pack for marketing\", \"what can we post\", \"turn this reply into a chart\", or \"site update with the results\". Only after the paper is public. Not for the paper's own figures (paper-authorship) or for a personal-voice post on its own (use the user's voice skill, with these rules)."
---

# Social packet: public assets derived from the published paper

> Scaffold (v0). Built from one release's plan before that release ran end to end; refine it after the first full use.

**Inputs:** the public paper and repository (the only sources of numbers), the paper's figure script and tables, the narrative guideline (its "claims never to make" and wording guardrails), the claim inventory, the project's brand or visual system, and any audience questions worth answering (replies, comments). **Outputs:** one working doc from `assets/social-assets-template.md` (release gate, copy rules, production notes, asset specs, copy bank, decisions), then an image pack: one file per asset, each paired with its copy line and alt text. **Human checkpoints:** the human approves the asset list, each rendered asset and its copy, and every hand-off to another team; owners of evaluated systems get the same sign-off chance on assets about their system that they got for the paper. Nothing is posted by this skill. **Hand-off:** the human (or a marketing team) for distribution; a personal-voice skill, if the user has one, for posts in their own voice, with these rules still applying.

Why a separate step: paper figures are built for readers who check the method; social assets are for people scrolling past, so each makes one point in plain words. Short form is where the paper's guardrails are easiest to break, and where a single cropped chart can misrepresent a careful result.

## 1. Release gate

Nothing goes out before the paper is public. After that, every number on an asset comes from the paper or the public repository, and each asset spec names the paper figure and the claim it comes from, so the check is mechanical. Statements about any evaluated system go through the same owner sign-off as the paper, offered to every owner on the same terms.

## 2. Copy rules

Restate the guideline's guardrails for short form in the working doc (`references/short-form-rules.md` has the generic set): lead with what the study found, not "who won"; name the full configuration; keep metric families apart; keep the paper's wording ceiling; carry the one caveat that keeps each asset honest.

## 3. Choose the assets

- Start from the paper's findings in its own order of weight, then add assets that answer real audience questions.
- When a question asks for a framing that would break a rule (for example a metric that labels unmatched outputs as false), keep the idea and change the framing; record that in the asset's "Origin" line.
- **Objectivity:** the set as a whole must represent the paper, including findings unfavourable to the authors' product. An asset shows every system in its comparison, not a favourable subset. Emphasis (highlighting, ordering) follows the paper's stated rule. A competitor's result gets the same full name, wording and caveat the authors' product would. Leaving out an asset is fine for clarity; leaving it out because of where it points is not.
- Before rendering, any number an asset needs that the paper doesn't print (a difference, a subset count) gets a pipeline claim first, never a hand subtraction.

## 4. Produce

- Render from the paper's figure script with a social layout pass (sizes per channel), never by editing images. Numbers stay tied to the tables.
- Apply the brand or visual system through the project's brand skill, if one exists, inside the figure rules (readability, accessibility, neutral treatment).
- Every asset carries a footer (study name and link) and its caveat line. Use short configuration names on the image and the full names in the alt text.
- Look at every rendered asset at its real size before handing it over.

## 5. Copy bank and site

Keep one-line highlights in the working doc, each traceable to the paper. Interactive site versions are planned there too; building them is separate work.

## Do not

Do not post, schedule or send anything. Do not use numbers that are not in the public paper or repository. Do not turn adjudicated or supplementary results into headline claims the paper itself keeps separate.
