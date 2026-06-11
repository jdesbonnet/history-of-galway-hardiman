#!/usr/bin/env python3
from __future__ import annotations

import html
import os
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString


ROOT = Path(__file__).resolve().parents[1]

# Book pages and their engravings live in text/; only these stay at the repo root.
TEXT_DIR = "text"
ROOT_FILES = {"index.html", "map/index.html"}

PAGES = [
	{
		"file": "index.html",
		"title": "James Hardiman's History of Galway",
		"nav": "Home",
		"section": "Home",
		"subtitle": "A modern static edition of the 1820 history of Galway.",
		"kind": "home",
	},
	{
		"file": "letter.html",
		"title": "Letter to James Daly, Esq.",
		"nav": "Letter",
		"section": "Front matter",
		"subtitle": "Hardiman's dedication to James Daly of Dunsandle.",
		"kind": "article",
	},
	{
		"file": "preface.html",
		"title": "Preface",
		"nav": "Preface",
		"section": "Front matter",
		"subtitle": "The author's statement of purpose and sources.",
		"kind": "article",
	},
	{
		"file": "c1.html",
		"title": "Chapter 1",
		"nav": "1 · The name, Tribes, and old map",
		"section": "Part I",
		"subtitle": "The name Galway, the Tribes of Galway, and the old map.",
		"kind": "article",
		"notes": "c1fn.html",
	},
	{
		"file": "c1fn.html",
		"title": "Chapter 1 Footnotes",
		"nav": "Chapter 1 notes",
		"section": "Notes",
		"subtitle": "Footnotes associated with Chapter 1.",
		"kind": "article",
	},
	{
		"file": "c2.html",
		"title": "Chapter 2",
		"nav": "2 · Earliest accounts to Henry II",
		"section": "Part I",
		"subtitle": "From the earliest accounts to the invasion of Henry II.",
		"kind": "article",
		"notes": "c2fn.html",
	},
	{
		"file": "c2fn.html",
		"title": "Chapter 2 Footnotes",
		"nav": "Chapter 2 notes",
		"section": "Notes",
		"subtitle": "Footnotes associated with Chapter 2.",
		"kind": "article",
	},
	{
		"file": "c3.html",
		"title": "Chapter 3",
		"nav": "3 · Anglo-Norman invasion to 1484",
		"section": "Part I",
		"subtitle": "From the Anglo-Norman invasion to 1484.",
		"kind": "article",
		"notes": "c3fn.html",
	},
	{
		"file": "c3fn.html",
		"title": "Chapter 3 Footnotes",
		"nav": "Chapter 3 notes",
		"section": "Notes",
		"subtitle": "Footnotes associated with Chapter 3.",
		"kind": "article",
	},
	{
		"file": "c4.html",
		"title": "Chapter 4",
		"nav": "4 · 1484 to the Irish Rebellion of 1641",
		"section": "Part I",
		"subtitle": "From 1484 to the commencement of the Irish Rebellion in 1641.",
		"kind": "article",
	},
	{
		"file": "c5.html",
		"title": "Chapter 5",
		"nav": "5 · 1641 to the Restoration of Charles II",
		"section": "Part I",
		"subtitle": "From 1641 to the Restoration of Charles II in 1660.",
		"kind": "article",
	},
	{
		"file": "c6.html",
		"title": "Chapter 6",
		"nav": "6 · 1660 to the surrender of Galway, 1691",
		"section": "Part I",
		"subtitle": "From 1660 to the surrender of Galway to Williamite forces in 1691.",
		"kind": "article",
	},
	{
		"file": "c7.html",
		"title": "Chapter 7",
		"nav": "7 · 1691 to the present time",
		"section": "Part I",
		"subtitle": "From 1691 to the present time of the 1820 edition.",
		"kind": "article",
	},
	{
		"file": "part3.html",
		"title": "Part III",
		"nav": "Part III",
		"section": "Ecclesiastical history",
		"subtitle": "The ecclesiastical history of Galway to Hardiman's present time.",
		"kind": "article",
	},
	{
		"file": "part4.html",
		"title": "Part IV",
		"nav": "Part IV",
		"section": "Modern state",
		"subtitle": "The modern state and description of the town.",
		"kind": "article",
	},
	{
		"file": "engravings.html",
		"title": "Postscript Concerning the Engravings",
		"nav": "Engravings",
		"section": "Reference",
		"subtitle": "Hardiman's note on the engraved plates.",
		"kind": "article",
	},
	{
		"file": "map/index.html",
		"title": "Map Scans",
		"nav": "Map scans",
		"section": "Reference",
		"subtitle": "Compressed PBM scans of the four panels of the accompanying map.",
		"kind": "map",
	},
]

PAGE_BY_FILE = {page["file"]: page for page in PAGES}
READING_ORDER = [
	"letter.html",
	"preface.html",
	"c1.html",
	"c1fn.html",
	"c2.html",
	"c2fn.html",
	"c3.html",
	"c3fn.html",
	"c4.html",
	"c5.html",
	"c6.html",
	"c7.html",
	"part3.html",
	"part4.html",
	"engravings.html",
	"map/index.html",
]

NAV_GROUPS = [
	("Start", ["index.html"]),
	("Front matter", ["letter.html", "preface.html"]),
	("Part I", ["c1.html", "c2.html", "c3.html", "c4.html", "c5.html", "c6.html", "c7.html"]),
	("Notes", ["c1fn.html", "c2fn.html", "c3fn.html"]),
	("Later parts", ["part3.html", "part4.html", "engravings.html", "map/index.html"]),
]


def disk_path(file: str) -> str:
	"""Map a logical page name to its on-disk location (book pages live in text/)."""
	if file in ROOT_FILES:
		return file
	return f"{TEXT_DIR}/{file}"


def _rel(from_file: str, to_path: str) -> str:
	start = (ROOT / from_file).parent
	return os.path.relpath(ROOT / to_path, start=start).replace(os.sep, "/")


def rel_url(current_file: str, target_file: str) -> str:
	return _rel(disk_path(current_file), disk_path(target_file))


def asset_url(current_file: str, asset_path: str) -> str:
	return _rel(disk_path(current_file), asset_path)


def h(value: str) -> str:
	return html.escape(value, quote=True)


def normalize_legacy_fragment(source_file: str, raw: str) -> str:
	soup = BeautifulSoup(raw, "html.parser")

	generated_article = soup.find("article", class_="book-article")
	container = generated_article if generated_article and generated_article.get("data-source-preserved") == "true" else (soup.body if soup.body else soup)

	for tag_name in ("head", "title"):
		for tag in container.find_all(tag_name):
			tag.decompose()

	for table in list(container.find_all("table")):
		if "scanned/OCRed" in table.get_text():
			table.decompose()

	source_text = container.get_text()

	for tag in list(container.find_all(True)):
		tag.name = tag.name.lower()

		if tag.name == "center":
			tag.name = "div"
			tag.attrs = {"class": "text-center"}
			continue

		if tag.name == "font":
			tag.unwrap()
			continue

		if tag.name == "b":
			tag.name = "strong"

		if tag.name == "i":
			tag.name = "em"

		if tag.name == "img":
			allowed = {}
			for attr in ("src", "alt", "width", "height"):
				if tag.has_attr(attr):
					allowed[attr] = tag[attr]
			allowed["loading"] = "lazy"
			allowed["decoding"] = "async"
			tag.attrs = allowed

		if tag.name == "a":
			if tag.has_attr("#name") and not tag.has_attr("name"):
				tag["name"] = tag["#name"]
				del tag["#name"]
			if tag.has_attr("href"):
				href = tag["href"]
				if source_file == "c1.html" and href.startswith("#fn-"):
					tag["href"] = "c1fn.html" + href
				if source_file == "part4.html" and href == "#amicablesoceity":
					tag["href"] = "#amicablesociety"
				if source_file == "engravings.html" and href == "#fn1":
					contents = list(tag.contents)
					if contents and isinstance(contents[0], NavigableString):
						first_text = str(contents[0])
						marker = "[[1]]"
						if first_text.startswith(marker) and first_text != marker:
							remainder = first_text[len(marker):]
							for node in reversed(contents[1:]):
								tag.insert_after(node.extract())
							if remainder:
								tag.insert_after(NavigableString(remainder))
							tag.clear()
							tag.append(marker)
			if tag.has_attr("name"):
				anchor_id = tag["name"].lstrip("#")
				if tag.has_attr("href"):
					tag["id"] = anchor_id
					del tag["name"]
				else:
					tag.name = "span"
					tag.attrs = {"id": anchor_id}

		if tag.has_attr("id") and isinstance(tag["id"], str):
			tag["id"] = tag["id"].lstrip("#")

		for attr in list(tag.attrs):
			if attr in {"bgcolor", "cellpadding", "cellspacing", "border", "align", "vspace", "hspace", "size", "color"}:
				del tag[attr]

	normalized = container.decode_contents(formatter="minimal").strip()
	if source_file == "preface.html":
		normalized = normalized.replace('<span id="fn2"></span>\n\n[[1]]', '<span id="fn1"></span>\n\n[[1]]', 1)
	if source_file == "c1fn.html":
		missing_anchors = [
			("fn-08", "\n~ 'l'he chle"),
			("fn-09", "\n  9 s11cL"),
			("fn-10", "\n 10. To open"),
		]
		for anchor_id, marker in missing_anchors:
			if f'id="{anchor_id}"' not in normalized and marker in normalized:
				normalized = normalized.replace(marker, f'\n<span id="{anchor_id}"></span>{marker.lstrip(chr(10))}', 1)
	if "<pre" not in normalized:
		normalized = BeautifulSoup(normalized, "html5lib").body.decode_contents(formatter="minimal").strip()
	normalized_text = BeautifulSoup(normalized, "html.parser").get_text()
	if source_text.strip() != normalized_text.strip():
		raise RuntimeError(f"text preservation check failed for {source_file}")
	return normalized


def extract_article(source_file: str) -> str:
	path = ROOT / disk_path(source_file)
	raw = path.read_text(encoding="utf-8", errors="replace")
	return normalize_legacy_fragment(source_file, raw)


def render_sidebar(current_file: str) -> str:
	groups = []
	for title, files in NAV_GROUPS:
		links = []
		for file_name in files:
			page = PAGE_BY_FILE[file_name]
			active = " active" if file_name == current_file else ""
			links.append(
				f'<li><a class="nav-link{active}" href="{h(rel_url(current_file, file_name))}" title="{h(page["title"])}">'
				f'<span class="bs-sidebar-label">{h(page["nav"])}</span></a></li>'
			)
		groups.append(
			f'<div class="bs-nav-section-title">{h(title)}</div><ul class="nav">{"".join(links)}</ul>'
		)

	return (
		'<div class="bs-sidebar-content">'
		f'<a class="bs-sidebar-brand" href="{h(rel_url(current_file, "index.html"))}" title="Hardiman home">'
		'<span class="brand-mark" aria-hidden="true">H</span>'
		'<span class="brand-text"><span class="brand-title">Hardiman</span>'
		'<span class="brand-subtitle">History of Galway</span></span></a>'
		'<button class="mobile-nav-close" type="button" data-mobile-nav-close aria-label="Close navigation">x</button>'
		f'{"".join(groups)}'
		'<div class="bs-sidebar-actions">'
		'<button type="button" id="strixieSidebarToggle" class="bs-sidebar-toggle" '
		'aria-label="Collapse navigation" aria-pressed="false" title="Collapse navigation"><</button>'
		'</div></div>'
	)


def render_topbar(page: dict[str, str], current_file: str) -> str:
	return (
		'<header class="bs-topbar">'
		'<div class="topbar-inner">'
		'<button class="mobile-nav-toggle" type="button" data-mobile-nav-open aria-label="Open navigation">Menu</button>'
		'<div>'
		f'<h1 class="topbar-title">{h(page["title"])}</h1>'
		f'<p class="bs-topbar-subtitle">{h(page["section"])}</p>'
		'</div>'
		'<div class="topbar-actions">'
		f'<a class="btn btn-sm" href="{h(rel_url(current_file, "index.html"))}">Contents</a>'
		'<a class="btn btn-sm" href="https://github.com/jdesbonnet/history-of-galway-hardiman">GitHub</a>'
		'</div>'
		'</div>'
		'</header>'
	)


def render_shell(page: dict[str, str], current_file: str, main_html: str) -> str:
	title = page["title"]
	if current_file != "index.html":
		title = f"{title} | Hardiman's History of Galway"

	return (
		"<!doctype html>\n"
		'<html lang="en">\n'
		"<head>\n"
		'\t<meta charset="utf-8">\n'
		'\t<meta name="viewport" content="width=device-width, initial-scale=1">\n'
		f"\t<title>{h(title)}</title>\n"
		f'\t<link rel="stylesheet" href="{h(asset_url(current_file, "assets/site.css"))}">\n'
		f'\t<script src="{h(asset_url(current_file, "assets/site.js"))}" defer></script>\n'
		"</head>\n"
		'<body class="bs-shell">\n'
		'\t<a class="skip-link" href="#main-content">Skip to main content</a>\n'
		'\t<button class="nav-backdrop" type="button" data-nav-backdrop aria-label="Close navigation"></button>\n'
		'\t<div class="site-layout">\n'
		f'\t\t<aside class="bs-sidebar" id="primary-nav" aria-label="Primary navigation">{render_sidebar(current_file)}</aside>\n'
		'\t\t<div class="site-content">\n'
		f'\t\t\t{render_topbar(page, current_file)}\n'
		f'\t\t\t<main id="main-content" class="container-fluid">{main_html}</main>\n'
		'\t\t\t<footer class="site-footer">HTML markup of <em>Hardiman\'s History of Galway</em>, &copy;1995 Wombat Research. Modern static shell generated for GitHub Pages.</footer>\n'
		"\t\t</div>\n"
		"\t</div>\n"
		"</body>\n"
		"</html>\n"
	)


def adjacent_links(current_file: str) -> str:
	if current_file not in READING_ORDER:
		return ""
	index = READING_ORDER.index(current_file)
	prev_file = READING_ORDER[index - 1] if index > 0 else None
	next_file = READING_ORDER[index + 1] if index + 1 < len(READING_ORDER) else None
	parts = ['<nav class="page-nav" aria-label="Previous and next pages">']
	if prev_file:
		prev_page = PAGE_BY_FILE[prev_file]
		parts.append(
			f'<a href="{h(rel_url(current_file, prev_file))}"><span>Previous</span>{h(prev_page["title"])}</a>'
		)
	else:
		parts.append("<div></div>")
	if next_file:
		next_page = PAGE_BY_FILE[next_file]
		parts.append(
			f'<a href="{h(rel_url(current_file, next_file))}"><span>Next</span>{h(next_page["title"])}</a>'
		)
	else:
		parts.append("<div></div>")
	parts.append("</nav>")
	return "".join(parts)


def render_article_page(page: dict[str, str]) -> str:
	current_file = page["file"]
	article = extract_article(current_file)
	notes_link = ""
	if "notes" in page:
		notes = page["notes"]
		notes_link = f'<a class="btn" href="{h(rel_url(current_file, notes))}">Chapter footnotes</a>'

	main = (
		'<section class="page-hero card">'
		f'<p class="eyebrow">{h(page["section"])}</p>'
		f'<h1>{h(page["title"])}</h1>'
		f'<p class="page-summary">{h(page["subtitle"])}</p>'
		'<div class="page-actions">'
		f'<a class="btn btn-primary" href="{h(rel_url(current_file, "index.html"))}">Contents</a>'
		f'{notes_link}'
		'</div>'
		'</section>'
		f'{adjacent_links(current_file)}'
		'<section class="notice" aria-label="OCR notice"><span class="notice-mark" aria-hidden="true">!</span>'
		'<p><strong>OCR text preserved.</strong> This transcription has not been proofed; spelling and recognition errors remain as found in the source files.</p></section>'
		'<section class="reading-card card">'
		f'<article class="book-article" data-source-preserved="true">{article}</article>'
		'</section>'
		f'{adjacent_links(current_file)}'
	)
	return render_shell(page, current_file, main)


def render_home(page: dict[str, str]) -> str:
	current_file = page["file"]
	cards = []
	for item in PAGES:
		if item["file"] == "index.html":
			continue
		search_text = " ".join([item["title"], item["nav"], item["section"], item["subtitle"]])
		cards.append(
			f'<a class="content-card card" href="{h(rel_url(current_file, item["file"]))}" data-filter-item="{h(search_text)}">'
			f'<span class="badge">{h(item["section"])}</span>'
			f'<h3>{h(item["title"])}</h3>'
			f'<p>{h(item["subtitle"])}</p>'
			'<span class="meta">Open</span>'
			'</a>'
		)

	main = (
		'<section class="landing-hero">'
		'<div class="hero-copy card">'
		'<p class="eyebrow">1820 static edition</p>'
		"<h1>James Hardiman's History of Galway</h1>"
		'<p class="lead">A cleaner, navigable GitHub Pages edition of Hardiman\'s out-of-copyright history of Galway, preserving the OCR text from the 1995 Wombat Research HTML markup.</p>'
		'<div class="hero-actions">'
		f'<a class="btn btn-primary" href="{h(rel_url(current_file, "letter.html"))}">Start reading</a>'
		f'<a class="btn" href="{h(rel_url(current_file, "c1.html"))}">Go to Chapter 1</a>'
		'</div>'
		'</div>'
		'<figure class="hero-engraving card">'
		f'<img src="{h(asset_url(current_file, "text/lynchcastle.jpg"))}" alt="Lynch\'s Castle, Galway" loading="eager" decoding="async">'
		"<figcaption>Lynch's Castle, Galway, one of the engravings included with the text.</figcaption>"
		'</figure>'
		'</section>'
		'<section class="section-header">'
		'<div><p class="eyebrow">Contents</p><h2>Read the book</h2></div>'
		'<input class="filter-input" type="search" placeholder="Filter chapters and sections" data-filter-input aria-label="Filter contents">'
		'</section>'
		f'<section class="content-grid" data-filter-list>{"".join(cards)}</section>'
	)
	return render_shell(page, current_file, main)


def render_map_page(page: dict[str, str]) -> str:
	current_file = page["file"]
	map_files = ["scan1.pbm.gz", "scan2.pbm.gz", "scan3.pbm.gz", "scan4.pbm.gz"]
	items = []
	for index, file_name in enumerate(map_files, start=1):
		items.append(f'<li><a href="{h(file_name)}"><strong>Panel {index}</strong><br><span>{h(file_name)}</span></a></li>')
	main = (
		'<section class="page-hero card">'
		f'<p class="eyebrow">{h(page["section"])}</p>'
		f'<h1>{h(page["title"])}</h1>'
		f'<p class="page-summary">{h(page["subtitle"])}</p>'
		'</section>'
		f'{adjacent_links(current_file)}'
		'<section class="reading-card card">'
		'<article class="book-article" data-source-preserved="true">'
		'<p>Scans of the four panels of the accompanying map.</p>'
		f'<ul class="map-list">{"".join(items)}</ul>'
		'</article>'
		'</section>'
	)
	return render_shell(page, current_file, main)


def main() -> None:
	for page in PAGES:
		if page["kind"] == "home":
			output = render_home(page)
		elif page["kind"] == "map":
			output = render_map_page(page)
		else:
			output = render_article_page(page)

		path = ROOT / disk_path(page["file"])
		path.parent.mkdir(parents=True, exist_ok=True)
		path.write_text(output, encoding="utf-8")
		print(f"wrote {page['file']}")


if __name__ == "__main__":
	main()
