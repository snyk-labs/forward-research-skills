# Card production

## Format

- **Size:** 1200×675 (16:9), saved at 2× for sharpness. It suits LinkedIn, X and slides.
- **Background:** the project's visual system (light or dark), with one accent rule across the top.
- **Text, top to bottom:**
  - eyebrow: monospace, uppercase, accent colour;
  - headline: about 34 pt semibold, with the number in it, at the paper's wording ceiling;
  - sub-line: one or two lines, about 16 pt;
  - one chart;
  - caveat line: monospace, about 10.5 pt, faint;
  - footer: study name and site, right-aligned.
- **System colours:** keep each system's colour from the paper's figures. No system, the authors' own product included, gets a highlight colour, bolder label or prime position that the others on the card don't get. Order bars by the paper's stated rule.

## Chart shapes that read at a glance

- Horizontal bars with the value at the bar's end.
- A stacked bar for "A plus what B adds", next to the best alternative combination.
- Grouped bars for a strictness ladder (looser to stricter matching).
- A log scale for time or cost ranges that span more than about 10×. Say so in the caveat.
- Small multiples for repeated runs, only where repeats were run for every system shown.

## Defects to look for

- **Overlaps:** the caveat overlapping the footer, or a chart overlapping the sub-line. Fix positions (for example the caveat at 8.5% of the height and the footer at 3.5%) and move the chart up rather than shrinking the text.
- **Mathtext:** matplotlib treats paired `$` signs as math, so a label with two dollar amounts loses its dollar signs and sets the text between them as a formula. Escape them as `\$` in every string and tick label (the skeleton's `money()` does).
- **Wording that sounds right but isn't:** a time interval, run count or basis described more loosely than the paper states it. Every sub-line and caveat goes through the copy review, like the posts.
- **Headline drift:** the card's headline is copy too, so it keeps the paper's ceiling and names the right basis.
- **Unscoped caveats:** a caveat for a card from the main runs starts "Main runs.", so it isn't read as covering supplementary results.
- **Hand-typed numbers:** any number in a label that doesn't come from a table or claim. Corpus sizes that appear on every card can be constants, declared once at the top of the script.
- **Uneven treatment:** one system's bar annotated or explained and the others not, or a cropped axis that exaggerates one gap.

## Check

Render all the cards into one contact sheet and look at it. Then open each card at its full size, check every number against `manifest.csv`, and read every word.
