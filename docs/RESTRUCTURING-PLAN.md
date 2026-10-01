# Restructuring plan - Robotics DSL Zoo

Status: DRAFT rev 3 (lean), 2026-10-01. Nothing in this plan has been executed. It replaces the much larger rev 2, which was judged over-engineered for this artifact. This document lives only on the fork branch `ai/dslzoo-refresh` and is not meant to be landed on `main` or on corlab.

Audience: maintainers and co-authors of the Robotics DSL Zoo, and future contributors.

Authors: Arne Nordmann, with Claude (AI assistant) as investigation and drafting aid.

## 1. Goal and scope

Make the Zoo maintainable again: a bibliography that contributors extend through pull requests, a site that is generated from it in CI, and a documented history. The Zoo is not mission-critical software. The generator runs offline and is never time-critical, generated pages are free to be modernized, and testing stays pragmatic rather than exhaustive.

The few fixed constraints, because two publications point at them:

| URL or reference | Where it appears | What must stay true |
|---|---|---|
| https://corlab.github.io/dslzoo/ | JOSER 2016 footnote 19; the READMEs | The root keeps answering with the current site |
| https://github.com/corlab/dslzoo/tree/query | JOSER 2016 footnotes 2 and 16 (Google Scholar query script) | Branch `query` keeps its name and content |
| Tag `joser16` (commit ddb3c76, 2016-04-14) | Existing marker of the JOSER-era bibliography | Never moved |
| Page names and `#key` anchors of the generated pages | Linked inside the site and in the wild | Keep the names; a removed page gets a redirect stub |
| `dslzoo.bib` at the repository root | Linked from contribute.html, raw use unknown | Stays at that path |

History is never rewritten. The SIMPAR 2014 survey process was manual (no script); `query` is the JOSER 2016 candidate search. The URL printed in the SIMPAR chapter itself is unverified.

## 2. What the investigation found (short)

- The live site is byte-identical to `gh-pages` commit 1bc823f (2020-05-08), 41 pages. It equals the newest bibliography (144 entries), so regenerating adds or drops nothing. Six pages are 2014/15 leftovers that cannot be derived from the bibliography.
- The old generator is in no public repository. The last regenerations were made by a co-author. It serves only as a template for the historical approach and goal; the new generator is written fresh, most likely in Python.
- `dslzoo.bib` has four syntax defects (two missing commas, two duplicate fields) that common BibTeX parsers handle silently wrongly, and a few vocabulary typos and 25 entries without a phase that the old site silently left off the category pages.
- The old pages request four files that never existed, load charts through a deprecated Google loader and carry no license, imprint or version number.
- Corlab: no workflows, no branch or tag protection, Pages is a legacy build of `gh-pages`, the Actions settings show no organization restrictions, the default workflow token is read-write, a `github-pages` environment exists without protection rules. The maintainer has repository admin there. The fork has the same Pages configuration and is a safe place to try things.
- Off-GitHub copies exist: a Software Heritage snapshot (2024-06-27, all live corlab refs and `joser16`) and about 420 Wayback captures (2017-2026).

Statements in the project notes that need correcting (after the maintainer confirms; history goes into DECISIONS.md as new entries):

| Statement | Correction |
|---|---|
| Both publications cite corlab.github.io/dslzoo | JOSER 2016 cites it and the `query` branch URL; the SIMPAR 2014 URL is unverified |
| `query` documents the data acquisition of "the original survey" | `query` is the JOSER 2016 candidate search; SIMPAR 2014 was manual |
| The generator is lost | It is in no public repository; recovery is handled in a private repository and the original is only a template for the new one |
| CHANGELOG 0.5.0: PR 17 was the first change after about 2.5 years | PR 9 landed on 2018-11-06 |
| CHANGELOG 0.6.0: six pull requests merged on 2019-09-15 | Seven merges plus one manual application (PR 12) |
| CHANGELOG: fields "subdomain, phase, tool" | The fields are zoo-subdomains, zoo-phases, zoo-tool plus four more |

## 3. Approach

1. Pragmatic over watertight: no byte-identical output, no exhaustive failure testing, no ceremony around hypothetical failures.
2. Keep the cited names, never rewrite history, keep a way back (the old `gh-pages` branch stays as it is).
3. Try on the fork first (its Pages site is live and configured like corlab), then corlab.
4. Every write to corlab needs the maintainer's explicit go-ahead; the assistant never edits git config and never posts messages for the maintainer.
5. Generator work happens in the private generator repository described in CLAUDE.md; code reaches this public repository only as a clean, reviewed import after the maintainer's go-ahead.
6. Public documents carry no secrets, e-mail addresses, local paths or names of individuals attached to roles.

## 4. Plan

| # | Step | Who and where | Effort (rough) |
|---|---|---|---|
| 1 | Backup and pins: a git bundle of all corlab refs including pull-request heads (the head of PR 12 exists only on GitHub), kept in two places; annotated tags on the fork for the key states: `legacy-2020-05-08-site` (1bc823f, last hand-generated site), `legacy-2020-05-08-bib` (3eba7a7, last bibliography state), `legacy-2015-12-22-query` (10d0659, tip of `query`), `joser16-site` (fd34a51, site state matching `joser16`); later the same tags on corlab. `joser16` is never moved. | Claude and maintainer, fork first, then corlab with go-ahead | 1 h |
| 2 | Optional guard on corlab: one repository ruleset that blocks deletion and force-push for `query`, `gh-pages`, `joser16*` and `legacy-*`, with no bypass list; any admin can switch it off. Try it on a throwaway repository first. | Maintainer-approved, corlab | 0.5 h |
| 3 | Documentation: `docs/PROVENANCE.md` (URL generations, `query` = JOSER search, SIMPAR manual, tags, what is and is not preserved) and the corrections of section 2. | Claude drafts, maintainer confirms governance files | 2 h |
| 4 | Bibliography hygiene as its own small commit: the four syntax fixes, `.gitattributes` for line endings, check that two parsers agree on all entries. | Claude, fork | 1 h |
| 5 | New generator in Python (uv, a BibTeX parser plus a guard that the entry count equals the parsed count, Jinja2). Modernized output; page names and `#key` anchors of the cited pages stay; the six 2015 leftover pages are copied as they are. The old generator is read only for approach and goals. Built in the private generator repository, then imported cleanly. | Claude with maintainer review, private repo then public import with go-ahead | 5 to 8 h |
| 6 | Pragmatic tests and lint in CI: parse, entry count, all expected pages generated, internal links resolve, simple checks for required fields and exact vocabulary tokens, markup characters in entries rejected. | Claude | 1 to 2 h |
| 7 | CI deploy: one GitHub Actions workflow builds the site and publishes it with Pages (Pages source set to GitHub Actions); the `gh-pages` branch stays untouched as the way back (switching the Pages source back restores the old site). Trial on the fork first, then corlab with go-ahead; set the default workflow token to read-only. | Claude, then maintainer flips the setting | 1 to 2 h |
| 8 | Contributor path: README and CONTRIBUTING updated, PR template. | Claude | 1 h |

Total: roughly 12 to 17 hours of Claude work and 2 to 3 hours for the maintainer (reviews, go-aheads, one message to the co-author who ran the last regenerations, checks in a browser). These are rough estimates (plus or minus 50 percent).

Not part of the plan unless wanted later: byte-identical reproduction, three legacy views under `/versions/`, a rulesets-and-notice ceremony for every change, a Zenodo record or license track (needs the co-authors' agreement), renaming `master` on corlab, machine-readable exports, modernization beyond the new generator's own output.

## 5. Decisions needed

1. Tags and the optional ruleset (steps 1 and 2): yes, only tags, or nothing on corlab.
2. Pages via Actions with `gh-pages` kept as fallback (step 7), or CI pushing to `gh-pages`. Recommended: Actions.
3. Which old URLs must stay exactly: all 41 page names (recommended, cheap) or only the root and a few key pages.
4. Later, not now: license and citation file (CITATION.cff), which need the co-authors.

## 6. Risks and open items

- Pages semantics when switching the source (a short gap, extensionless URLs, custom 404) are measured on the fork before corlab. The way back is a settings change.
- Silent BibTeX parser failures: covered by the entry-count guard and the syntax fixes.
- Markup characters inside entries would render raw: rejected by the lint.
- Unverified: the URL printed in the SIMPAR chapter; whether the old charts render in current browsers; organization-level policy beyond the repository settings.
- Rights (license, contributor consent, one image of unknown provenance) are unresolved and deliberately left out.

## 7. Sources

- JOSER 2016: A Survey on Domain-Specific Modeling and Languages in Robotics, Journal of Software Engineering for Robotics 7(1), 75-99, DOI 10.6092/JOSER_2016_07_01_p75.
- SIMPAR 2014: A Survey on Domain-Specific Languages in Robotics, LNCS 8810, 195-206, DOI 10.1007/978-3-319-11900-7_17.
- Software Heritage snapshot of corlab/dslzoo (2024-06-27) and Wayback Machine captures of corlab.github.io/dslzoo (public archives).
- Repository history, GitHub settings and the live site as of 2026-09-29 (read-only investigation).

## 8. Revisions

- Rev 1, 2026-09-29: first draft after the investigation.
- Rev 2, 2026-09-29: design round and a seven-lens review; 52 core steps, byte-identical cutover, rulesets, notice waves. Judged over-engineered.
- Rev 3, 2026-10-01: lean plan of 8 steps. Dropped: byte-identical reproduction, the drill, soak and notice machinery, legacy views, the rights and DOI track, the extensive test tiers. Rev 2 remains visible in the history of this branch.
