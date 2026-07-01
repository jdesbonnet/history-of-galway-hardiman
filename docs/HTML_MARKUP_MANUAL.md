# HTML Markup Manual

This manual describes the HTML conventions used for the book edition in this repository. It is intended for editors who need to reconcile OCR, repair markup, or add missing content while keeping the page structure stable.

## Scope

- The book pages live in `text/`.
- The home page is `index.html`.
- The map scans live under `map/`.
- Edit the existing HTML pages in place unless there is a clear reason to add a new page.

## Core Principles

- Preserve Hardiman's historical spelling, punctuation, capitalization, and lineation unless the OCR has clearly damaged the text.
- Correct OCR errors, but do not modernize prose.
- Keep any optional reader-facing modernisation separate from the canonical transcription. See [Text Modernisation Layer Proposal](MODERNISATION_LAYER_PROPOSAL.md).
- Keep the existing page shell, navigation, and overall structure consistent across pages.
- Prefer semantic HTML5 elements over generic `<div>` wrappers when the content has a clear role.
- Keep changes local to the smallest page or section that needs them.

## Document Shell

Each book page should follow the same basic shell:

- `<!doctype html>`
- `<html lang="en">`
- `<head>` with charset, viewport, title, stylesheet, and script
- `<body class="bs-shell">`
- Skip link to `#main-content`
- Navigation backdrop button
- `.site-layout`
- Primary sidebar navigation
- `.site-content`
- Sticky top bar
- `<main id="main-content" class="container-fluid">`
- Footer

The shell is already present in the generated pages. Do not replace it with a different layout.

## Page Structure

Book pages usually use this sequence:

1. `section.page-hero.card`
2. `nav.page-nav`
3. `section[aria-label="OCR notice"].notice`
4. `section.reading-card.card`
5. `nav.page-nav`

Inside `section.reading-card.card`, the actual content sits in:

- `<article class="book-article" data-transcription="2026-ocr">`

The `data-transcription` value marks the OCR-backed transcription source. Keep it consistent with the current edition unless there is a deliberate migration.

## Headings

- Use the existing heading hierarchy already implied by the source.
- Keep chapter titles, section titles, and internal subheads as written in the book.
- Avoid inventing new headings unless you are restoring content that clearly belongs there.

## Paragraphs And Lists

- Use `<p>` for prose paragraphs.
- Use `<h2>` and `<h3>` only when the source has a true structural heading.
- Use `<ul>` or `<ol>` only when the source is explicitly list-like.
- Preserve blank-line separations only when they represent meaningful structure.

## Footnotes

Footnotes must be explicit and navigable.

### Required semantics

- The note reference in the body should be an anchor with:
  - `role="doc-noteref"`
  - a stable `id` such as `fnref-c1-1`
  - an `href` pointing to the matching note, such as `#fn-c1-1`
- The note itself should be an `<aside>` with:
  - `role="doc-footnote"`
  - a stable `id` such as `fn-c1-1`
  - an accessible `aria-label`
- Each note should end with a backlink anchor using:
  - `role="doc-backlink"`
  - `href` pointing back to the reference anchor

### Placement

- Keep the note reference immediately after the sentence or clause it supports.
- If a note is embedded at the end of a chapter page, place the note section after the chapter text and before the closing page navigation.
- If a dedicated notes page is still used, it should remain a compatibility or navigation page only when the note text has been moved into the chapter page.

### Chapter 1 convention

- Chapter 1 notes are embedded in `text/c1.html` at the end of the chapter.
- `text/c1fn.html` exists as a compatibility stub and should not duplicate the note text.

## Figures And Images

- Use `<figure>` for embedded illustrations or scanned plates.
- Use `<img>` with descriptive `alt` text.
- Use `<figcaption>` when the image needs a source note or explanatory caption.
- Keep image markup close to the related text.

## OCR Notices

Use the OCR notice section to explain transcription provenance:

- Keep it short.
- State that the text was reconciled against the scan.
- Do not overclaim manual verification unless it was actually performed.

## Links And Navigation

- Use relative links.
- Keep chapter-to-chapter navigation consistent.
- If a page has a note section, make sure the chapter page and the notes entry point agree.
- Avoid dead links when you move footnotes into the main chapter text.

## Editing Checklist

Before finishing a markup change, check:

- The page renders with valid HTML structure.
- Footnote references and backlinks resolve correctly.
- Historical text is preserved where it should be.
- OCR fixes are limited to real transcription errors.
- Navigation still points to the correct pages.
- If the chapter notes move, any compatibility page or landing-page shortcut is updated.

## Project Notes

- `assets/site.css` contains the supporting styles for semantic footnotes, figures, cards, and navigation.
- `tools/reconcile_ocr.py` is the automation used to reconcile OCR against the scanned edition.
- If you add new HTML conventions, update this manual first so the next edit follows the same pattern.
