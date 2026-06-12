# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Static site generator for Vincent Delecroix's personal academic webpage (hosted at http://www.labri.fr/perso/vdelecro/). The page is written in French. The source is a small Python script plus Jinja2 templates, Markdown content, and JSON data files; rendering produces HTML into `output/`.

## Build / generate

There is no build system, test suite, or linter — the entire site is rebuilt by running:

```
python generate.py
```

Run from the repo root. It writes everything to `output/` (which is gitignored). Dependencies: `markdown`, `jinja2`, `mdx_math` (Markdown extension for LaTeX math). The `output/` directory must already exist; the script does not create it.

Every run regenerates everything — there is no incremental build. A previous mtime-based skip mechanism was removed because the dependencies were tracked incorrectly (data files, `base.html`, and `generate.py` itself weren't part of the graph).

## Architecture

`generate.py` is the single entry point. It does roughly four things in order:

1. **Static copy.** Files in `webpage/static/` (CSS, images) are mtime-copied into `output/`.
2. **Data load.** JSON files in `webpage/data/` (`journals`, `publications`, `conference_papers`, `news`) and Markdown files (`general_presentation.md`, `research_description.md`) are loaded into a single `data` dict. The Markdown files are pre-rendered to HTML at load time. `publications.json` is a single merged list — `generate.py` then splits it into `data['publications']` (anything with a `journal` or `book-title` field) and `data['prepublications']` (everything else).
3. **Page render.** A hardcoded `pages` list in `generate.py` maps each top-level page (Présentation, Recherche, Enseignement, Programmation, Contact, Misc) to a template in `webpage/templates/`. Each template extends `base.html` and receives `data` as keyword args plus the `pages` list (used to render the nav menu, where the current page has `status='selected'`).
4. **Blog render.** Every `.md` file in `webpage/articles/` becomes a blog post. `article_list()` scans the directory and detects Sage code by looking for the `    :::pycon` marker. Posts go through `webpage.process_article.process_article`, which runs Markdown with `CodeHiliteExtension`, `mdx_math`, and tables. Posts containing Sage code additionally get a `<name>_sage.html` variant rendered through `base_blog_sagecell.html`.

### Article timestamps

The "dernière modification" date shown on the blog index comes from `article_mtime(path)`, which returns the commit time of the last git commit touching the file (so the date survives `git clone`). If the file has uncommitted changes or git is unavailable, it falls back to the filesystem mtime. Blog posts are sorted oldest-first by this same value.

### Adding content

- **A publication / journal item / news entry:** edit the relevant JSON in `webpage/data/`. The templates iterate over these lists directly — match the existing object shape.
- **A new blog post:** drop a `.md` file in `webpage/articles/`. The filename (minus `.md`) becomes the URL slug. The first non-blank, non-`[comment]` line of the file is used as the title.
- **A new top-level page:** add an entry to the `pages` list in `generate.py` *and* create the matching template in `webpage/templates/`.

### Publication entry shape

Each entry in `publications.json` / `conference_papers.json` is a dict. Fields are flat (LaTeX-bibliography style), all optional except as noted. An entry counts as published iff it has either a `journal` *or* a `book-title` field; otherwise `generate.py` routes it to the Prépublications section.

- `title`, `coauthors`, `year` — citation basics.
- `journal` — key into `journals.json` (must exist there or rendering fails).
- `volume`, `number` / `issue`, `pages` — bibliographic details. `pages` is a `[first, last]` array. `pages` is reused as-is by book-chapter entries.
- `book-title`, `editors`, `publisher`, `series`, `series-volume` — book-chapter fields (kept flat, mirroring BibTeX `@incollection`). Rendered by the `publication_book` macro in `research.html`. The presence of `book-title` alone is enough to classify the entry as published.
- `arxiv` — drives the arXiv link.
- `abstract` — when present, a "Voir résumé" toggle expands the abstract inline.

### Sage cell integration

`webpage/sageparser.py` defines a `SageCellExtension` that converts `:::pycon` code blocks into Sage Cell Server `<script type="text/x-sage">` widgets. Note that in `process_article.py` the `celler` extension is currently commented out — only the static (CodeHilite) form is wired up, but the `_sage.html` variant is still generated via `base_blog_sagecell.html` which loads the Sage cell JS client-side.

## Conventions

- Page text is French. Variable/code identifiers stay English.
- Do not edit files in `output/` — they are regenerated and gitignored.
- `webpage/articles/*.md` filenames are URL slugs; renaming breaks links.
