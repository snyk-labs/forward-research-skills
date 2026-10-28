# Figure rules

Rules for paper figures, each with a short reason and a generic example. Apply them before the first render. Record a new correction for this paper as a dated rule in the project's `review-rounds.md`, not here: this file belongs to the shared skill and changes only by a deliberate edit to the plugin.

## Contents

1. Pipeline and provenance
2. What every chart must show
3. Axes, scales and values that don't fit
4. Labels, legends and layout
5. Wording on figures
6. Colour, naming and accessibility
7. Captions
8. Paper versus web variants
9. The visual check

## 1. Pipeline and provenance

- **One script, tables in, figures out.** The script reads only the pipeline's `tables/` and the claims registry. No raw data, no typed numbers. Why: a figure that disagrees with the text is the hardest error for a reader to forgive, and the cheapest way to prevent it is to give both one source.
- **Every printed value is a claim.** If a figure prints a ratio, a per-unit cost or a difference, a pipeline step computes it and registers a claim. The figure script only formats. Table rows may set geometry (bar lengths, interval ends); printed labels are looked up in the registry, by claim ID or by the claim's `table` and `query` fields (`claim_where()` in the skeleton), never by a hand-typed system-to-ID map. The script merges each figure's claim IDs into `figures/manifest.json`; `check_claims.py --manifest` verifies them.
- **Re-render everything from a clean run** before each review round. A figure from an earlier run silently disagrees with a re-run ledger.
- **A `--only` filter and an output-directory flag.** Iteration is per figure, and paper PDFs are copied into `paper/figures/` by the script, never by hand.

## 2. What every chart must show

- **Show the ‹reference tool› explicitly** in every comparison, as its own labelled row or marker. Never leave it as an assumed baseline that readers must infer from the caption. Why: readers who skim figures will not read the caption that explains an implicit baseline.
- **Show every system the text compares**, in the same order everywhere, ordered by a stated rule (the headline metric, or a fixed order chosen before the figures). A system that appears in the text but not in the figure invites the question of what is hidden.
- **Give no system emphasis the question doesn't need.** No highlight colour, bold label, annotation or prime position for the authors' product or the reference tool that the other systems don't get. An annotation that explains one system's bar is offered for every bar in the same situation.
- **Keep supplementary or control runs distinct:** a different marker or outline, labelled in the legend, never merged into the main bars or into a union.
- **Don't plot unlike metrics on one axis.** If one system family is scored differently, give it its own panel or axis, labelled with its metric.
- **Split crowded figures.** If a figure has more than about three panels or needs a long caption to decode, split it. One figure, one point.

## 3. Axes, scales and values that don't fit

- **Use off-axis markers for values that don't fit the axis.** Example: a system with no recorded cost gets its own narrow column beside the cost axis, labelled "no per-run cost", joined to the axis with a break mark. Never put it at zero or at an arbitrary value: zero is a value, unavailable is not.
- **Use log scales when ratios span orders of magnitude.** Say "log scale" on the axis label.
- **Share axes when panels are compared directly.** Use the same row order and the same scale where the reader is meant to compare across panels.
- **Make axis titles say what is counted and out of what:** "‹items› matched (of ‹N›)", not "score".

## 4. Labels, legends and layout

- **No overlapping text.** Rotated column labels anchor at the tick: rotation about 35°, left-aligned, anchored at the tick. Otherwise neighbouring labels collide. Leave enough top margin.
- **Keep legends off the data.** Put the legend below the axis, beside the panel, or inline next to the series it names. A legend that sits on a bar makes the bar read as the legend's value.
- **Place annotations inside the axes.** Arrows and direction labels that reach the frame get clipped in the PDF.
- **Separate point labels in dense scatter plots.** Use per-label offsets chosen by looking at the render, not an automatic placer that moves labels between runs.
- **Use one panel-letter style everywhere,** matching between figure titles, captions and text ("(A)" in the figure means "Figure 3A" in the text).
- **Use grouped rows with white separators** for heatmaps that mix rule families. Don't use rotated side labels that collide with row labels.

## 5. Wording on figures

- **Use plain words, not pipeline jargon.** Write "rule used for all results", not "registered" (which implies pre-registration). Write "alternative class names", not an internal field name. Write "items the default settings skip", not the internal name of a setting.
- **Use full system names** the first time and in legends, short forms only where space forces it. The paper says once what the short forms mean.
- **No internal IDs, codenames or file paths** on any figure.
- **Explain statistic labels.** If a column prints "tau ‹value›", the caption says what tau is (rank agreement with the outlined row).

## 6. Colour, naming and accessibility

- **One colour per system, fixed across every figure,** and one name per system across text and figures. Start from a colour-blind-safe palette (Okabe-Ito in the skeleton). If family members share a hue, separate them by hatch, marker or outline as well, never by lightness alone.
- **Keep the ‹reference tool›'s colour neutral and distinct,** not the brand accent, so the figures don't read as promotional, and check it stays visible on every theme, with interval lines in a colour that contrasts with every fill.
- **Make the print canvas white and readable in greyscale.** Hatch or outline the series that matter. Dark variants are for the web.
- **Apply the project's visual system inside these rules.** Fonts, palette and footer can follow the brand; where they conflict with print readability, colour-blind safety or neutral treatment of every system, these rules win.
- **No text below 7 pt at final size** (tick labels, annotations, notes included). Check by viewing the figure at the width it prints in the PDF.
- **Write alt text** for every figure: one or two sentences giving the takeaway and the key values. arXiv's HTML rendering and screen readers use it; keep it in the claim inventory's figure table next to the claim IDs.

## 7. Captions

- **Say what an interval represents:** "95% interval from resampling the ‹units›; it shows how much the score depends on which ‹units› are in the corpus, not run-to-run variation."
- **Say what was not run** when the design limits a reading: for example, with one run per configuration every ratio is a single observation. Skip this when the design has repetitions, and say how many instead.
- **Say what a marker or tick means** if it shows a sensitivity view, and which rows carry it.
- **Use one sentence per panel,** in panel order, letters matching the figure.
- **Keep captions consistent with the final figure.** When a figure gains or loses a panel, update its caption and every in-text reference to its panels.

## 8. Paper versus web variants

- The paper gets vector PDFs on a white canvas, with no explanatory notes inside the image (the caption does that job).
- Web and social variants come from the same code, with a theme switch (light and dark), notes rendered inside the image (they travel without a caption), and a footer with the benchmark name. Social sizes are a separate layout pass, never a resized paper figure.
- **Review the in-image notes too.** They never appear in the paper PDF, so a paper review round does not see them: give the reviewer the web PNGs and check each note against the registry and the final paper wording (counts, timing, terms). Stale notes are the usual failure: an old timing, an internal label, or a claim the paper has since corrected.

## 9. The visual check

After every render, open the PNG and look at it. Check for:

- overlapping or clipped labels;
- legends covering data;
- arrows clipped at the frame;
- panels that look like separate charts when they should read as one;
- inconsistent row order between panels;
- values that cannot be read at print size.

Then compile the paper and look at the page the figure lands on. Check that the float doesn't split a paragraph and that the caption stays on the same page.
