# Restructuring plan - Robotics DSL Zoo

Status: DRAFT rev 4 (re-scoped), 2026-10-04. Rev 4 narrows the fixed constraints to what the publications cite and limits scientific rigor to what lands on or is served from corlab (section 1). Done so far: step 1 including corlab and step 2 (rulesets) on corlab (both 2026-10-03), the Actions deploy trial of step 7 on the fork (2026-10-03), step 4 on the fork (2026-10-02, see section 8); the citation note and the Actions deploy are live on corlab (2026-10-04, steps 3 and 7 in their minimal form, see DECISIONS.md); step 5 is being built directly in this repository (plan A, 2026-10-03, see DECISIONS.md); nothing else has been executed. Rev 3 replaced the much larger rev 2, which was judged over-engineered for this artifact. This document lives only on the fork branch `ai/dslzoo-refresh` and is not meant to be landed on `main` or on corlab.

Audience: maintainers and co-authors of the Robotics DSL Zoo, and future contributors.

Authors: Arne Nordmann, with Claude (AI assistant) as investigation and drafting aid.

## 1. Goal and scope

Make the Zoo maintainable again: a bibliography that contributors extend through pull requests, a site that is generated from it in CI, and a documented history. The Zoo is not mission-critical software. The generator runs offline and is never time-critical, so it may be lean and new, may produce different pages and a different structure than the old one, and needs no exhaustive tests.

Scientific rigor applies to two things only, and only to what lands on or is served from corlab (the repository the publications cite). The fork (`origin`) is a working copy, not a reference target, and needs none of it.

1. The references that publications cite and that still exist stay stable (table below).
2. The bibliography stays intact: its history, all publications in it, and their manual classification, made by hand following the process documented in JOSER 2016.

Everything else may change as long as both hold. One added requirement: a prominent notice that these references exist, that they stay stable, and why. It goes into the README, a note shown on every page of the generated site and a versions page (DECISIONS.md, 2026-10-03). The legacy `gh-pages` content is frozen (hand-committed, ruleset-protected), so the notice reaches the site through the Actions deploy of step 7 (live on corlab since 2026-10-04).

The fixed references, because a publication points at them:

| URL or reference | Where it appears | What must stay true |
|---|---|---|
| https://corlab.github.io/dslzoo/ | JOSER 2016 footnote 19; the READMEs | The root keeps answering with the current site |
| https://github.com/corlab/dslzoo/tree/query | JOSER 2016 footnotes 2 and 16 (Google Scholar query script) | Branch `query` keeps its name and content |
| Tag `joser16` (commit ddb3c76, 2016-04-14) | Existing marker of the JOSER-era bibliography | Never moved |
| `dslzoo.bib` at the repository root | Linked from contribute.html, raw use unknown; the data the surveys rest on | Stays at that path; entries, history and manual classification stay intact |

Not fixed any more: page names, `#key` anchors and the 41 pages of the legacy site (JOSER cites only the root; the legacy state stays pinned by tag `legacy-2020-05-08-site`, the Software Heritage snapshot and the Wayback captures). Open: whether `contribute.html` keeps its name, since the READMEs link to it.

History is never rewritten. The SIMPAR 2014 survey process was manual (no script); `query` is the JOSER 2016 candidate search. The SIMPAR 2014 chapter prints only the former address http://cor-lab.org/robotics-dsl-zoo (footnotes 6 and 8; verified 2026-10-03 against the authors' copy, which the maintainer states is content-identical to the published chapter). That address no longer serves the Zoo, so SIMPAR has no working fixed citation URL.

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
| Both publications cite corlab.github.io/dslzoo | JOSER 2016 cites it and the `query` branch URL; SIMPAR 2014 cites only the former address cor-lab.org/robotics-dsl-zoo, which is dead |
| `query` documents the data acquisition of "the original survey" | `query` is the JOSER 2016 candidate search; SIMPAR 2014 was manual |
| The generator is lost | It is in no public repository; recovery is handled in a private repository and the original is only a template for the new one |
| CHANGELOG 0.5.0: PR 17 was the first change after about 2.5 years | PR 9 landed on 2018-11-06 |
| CHANGELOG 0.6.0: six pull requests merged on 2019-09-15 | Seven merges plus one manual application (PR 12) |
| CHANGELOG: fields "subdomain, phase, tool" | The fields are zoo-subdomains, zoo-phases, zoo-tool plus four more |

## 3. Approach

1. Pragmatic over watertight: no byte-identical output, no exhaustive failure testing, no ceremony around hypothetical failures.
2. Keep the cited names, never rewrite history, keep a way back (the old `gh-pages` branch stays as it is).
3. Try on the fork first (its Pages site is live and configured like corlab; a rehearsal, not a reference target, so no rigor needed there), then corlab.
4. Every write to corlab needs the maintainer's explicit go-ahead; the assistant never edits git config and never posts messages for the maintainer.
5. The new generator is written from scratch directly in this repository (plan A, 2026-10-03), from public sources only (`dslzoo.bib` and the HTML of branch `gh-pages`); nothing from the private generator repository described in CLAUDE.md is read or used.
6. Public documents carry no secrets, e-mail addresses, local paths or names of individuals attached to roles.
7. Rigor sits at three transitions to corlab: the Pages cutover (before and after, the root answers 200 with the Zoo), every bibliography commit that goes to corlab (entry-count guard, classification unchanged unless the maintainer decided otherwise), and the protected refs (`query`, `gh-pages`, `joser16*`, `legacy-*`), which are not touched.

## 4. Plan

| # | Step | Who and where | Effort (rough) |
|---|---|---|---|
| 1 | Backup and pins: a git bundle of all corlab refs including pull-request heads (the head of PR 12 exists only on GitHub), kept in one place outside the repository (the maintainer decided against a second copy); annotated tags on the fork for the key states: `legacy-2020-05-08-site` (1bc823f, last hand-generated site), `legacy-2020-05-08-bib` (3eba7a7, last bibliography state), `legacy-2015-12-22-query` (10d0659, tip of `query`), `joser16-site` (fd34a51, site state matching `joser16`); later the same tags on corlab. `joser16` is never moved. **Status 2026-10-03: done.** Bundle (19 pull-request heads included, restore-tested), the four fork tags, and the same four tags on corlab (identical tag objects on both remotes, pushed by explicit refspec with the maintainer's go-ahead). | Claude and maintainer, fork first, then corlab with go-ahead | 1 h |
| 2 | Optional guard on corlab: one repository ruleset that blocks deletion and force-push for `query`, `gh-pages`, `joser16*` and `legacy-*`, with no bypass list; any admin can switch it off. Try it on a throwaway repository first. **Status 2026-10-03: done on corlab** (branches `query` and `gh-pages`, tags `joser16*` and `legacy-*`); the throwaway trial was skipped because private repositories have no rulesets without GitHub Pro. | Maintainer-approved, corlab | 0.5 h |
| 3 | Stability notice and documentation: README section "Stable references" (what is cited, that it stays stable, why: tags, rulesets, public archives); the text of the note shown on every page and of the versions page, handed to the generator (step 5); a short `docs/PROVENANCE.md` (URL generations, `query` = JOSER search, SIMPAR manual, tags, what is and is not preserved) and the corrections of section 2. **Status 2026-10-04:** the note on every page, the versions page (`docs/STABLE-REFERENCES.md`) and the README section are live on corlab (see DECISIONS.md); `docs/PROVENANCE.md` and the corrections of section 2 follow after the maintainer's confirmation. | Claude drafts, maintainer confirms governance files | 1 h |
| 4 | Bibliography hygiene as its own small commit: the four syntax fixes, `.gitattributes` for line endings, check that two parsers agree on all entries. **Status 2026-10-02:** done on the fork (pybtex and bibtexparser 1.x agree on all 144 entries; duplicate `keywords` merged, see DECISIONS.md); not yet on corlab (open points before the cherry-pick: section 5). The vocabulary typos and the 25 entries without a phase are not part of this step; they belong to the lint in step 6. | Claude, fork | 1 h |
| 5 | New generator in Python (uv, a BibTeX parser plus a guard that the entry count equals the parsed count, Jinja2). Lean and free: new or different pages and structure are fine, only the root must answer with the Zoo; page names and anchors of the legacy site are not fixed and the six 2015 leftover pages need not be carried over. The structure comes from the controlled vocabulary and the peculiarities of the old site are not requirements (DECISIONS.md). The old generator is read only for approach and goals. Written directly in this repository (plan A, 2026-10-03). Every page carries a note with the fixed citation addresses that links a versions page. **Status 2026-10-04:** first version in `generator/`, deployed to the fork by `pages.yml`; removed pages are redirect stubs; not on corlab, the release is the cutover of step 7 (see DECISIONS.md). | Claude with maintainer review | 3 to 5 h |
| 5a | Deferred, not required (maintainer wish 2026-10-02: the single file is unwieldy). It touches the bibliography, whose history and classification are fixed by section 1: one file per entry would split the history of `dslzoo.bib`. Revisit only after the generator runs. Preferred form then: one file per entry in `bib/` (file name = key), with `dslzoo.bib` kept at the repository root as a generated aggregate, checked for sync in CI. | Maintainer decides if and when, Claude implements | 2 to 3 h, if ever |
| 6 | Minimal CI: the build succeeds and the entry-count guard holds (parsed entries = entries in the bibliography), so no publication is silently dropped. Everything else (required fields, vocabulary tokens, internal links, markup characters) is optional and runs as warnings, not as gates. | Claude | 0.5 h |
| 7 | CI deploy: one GitHub Actions workflow builds the site and publishes it with Pages (Pages source set to GitHub Actions); the `gh-pages` branch stays untouched as the way back (switching the Pages source back restores the old site). Trial on the fork first, then corlab with go-ahead; set the default workflow token to read-only. Cutover check on corlab: before and after the switch the root answers 200 with the Zoo (after: with the stability notice); the way back is verified. **Status 2026-10-03:** trial done on the fork with a test workflow that publishes the unchanged `gh-pages` content; byte-identical, proved served by Actions via a marker file, rollback verified (source back to `gh-pages` plus a manual legacy build); fork is back on the legacy source. **Status 2026-10-04:** corlab is served by Actions (a copy of `gh-pages` plus the citation note, a stand-in until the generator exists); checked before and after, way back documented, see DECISIONS.md. | Claude, then maintainer flips the setting | 1 to 2 h |
| 8 | Contributor path: README and CONTRIBUTING updated, PR template. | Claude | 0.5 h |
| 9a | Semantic web layer (maintainer wish 2026-10-04: all information of the zoo accessible for semantic web tooling and for LLMs; step 9 is 9a to 9c). The generator additionally emits the bibliography and the controlled vocabulary as linked data, from the same build and without touching `dslzoo.bib`: JSON-LD (and Turtle) with one resource per entry, the classification axes as a SKOS concept scheme built from `vocabulary.toml`, a dataset description, and JSON-LD embedded in the generated pages for crawlers. Pages has no content negotiation, so the files sit at fixed paths. The data describes the current edition; the pinned states stay the citable ones (versions page). Open before the first release to corlab: the IRI scheme for entries and terms (host and pattern; minting identifiers creates a new stability duty, so derive them from the bibliography key and decide once) and the license (decision 4; publishing the data as a dataset wants one, and it needs the co-authors). Starts after step 5 has landed on corlab. | Claude with maintainer review; maintainer decides the IRI scheme | 3 to 5 h |
| 9b | LLM-facing files: `llms.txt` at the site root (a proposed convention, not a standard; adoption by crawlers is unclear, so keep it cheap), plain Markdown or JSON views of entries and categories, `sitemap.xml` and `robots.txt` (the site has neither today). Links the data files of 9a. | Claude | 1 h |
| 9c | Candidate, not committed: MCP server for the zoo (search and filter entries by subdomain, phase and tool, return an entry as BibTeX or JSON-LD). Static Pages cannot host a server. Preferred form then: a small local (stdio) package that reads the published data files of 9a, with no hosting; a remote server needs a separate host and operation, which does not fit a not-mission-critical artifact. Decide after 9a and 9b, since it needs the dataset anyway. | Maintainer decides if and when, Claude implements | 3 to 5 h, if ever |

Total (rev 4): roughly 6 to 9 hours of Claude work (rev 3: 12 to 17) and 2 to 3 hours for the maintainer (reviews, go-aheads, one message to the co-author who ran the last regenerations, checks in a browser). These are rough estimates (plus or minus 50 percent). Steps 9a to 9c (added 2026-10-04) are not included.

Not part of the plan unless wanted later: byte-identical reproduction, fixed page names and anchors, three legacy views under `/versions/`, a rulesets-and-notice ceremony for every change, a Zenodo record or license track (needs the co-authors' agreement), renaming `master` on corlab, modernization beyond the new generator's own output.

## 5. Decisions needed

1. Decided, done 2026-10-03: tags and rulesets on corlab (steps 1 and 2).
2. Decided, trialled on the fork: Pages via Actions with `gh-pages` kept as fallback (step 7).
3. Decided (rev 4, supersedes the plan A point that all 41 page names stay): only the references that publications cite stay fixed; page names and anchors are free. Open: does `contribute.html` keep its name?
4. Later, not now: license and citation file (CITATION.cff), which need the co-authors.
5. Deferred (rev 4): the bibliography split (step 5a).
6. Open: the citable state for SIMPAR 2014. The chapter prints only the dead former address (section 1), so the zoo has no pinned state from that time: the repository starts on 2014-11-26 and the bibliography was first committed on 2015-01-08, after the survey. The closest preserved states are the Internet Archive capture `20141009225401` of the former address and, in git, the first generated site of 2014-12-10 (commit 6ffcb65). Options: say exactly this in the notice and on the versions page (current text); additionally tag the first generated site on corlab as a new tag (needs the maintainer's go-ahead).
7. Open, due when the bibliography commits are cherry-picked to corlab: (a) keep or revert the new spelling of nine classification tokens changed on 2026-10-02 (`Error and Exeption Handling` to `Error and Exception Handling and Fault Tolerance` in eight entries, `Control of Handling and Events` to `Control and Handling of Events` in one; tag `legacy-2020-05-08-bib` keeps the original); reverting means the generator maps the old spellings; (b) whether the whitespace-only commit goes to corlab, with a `.git-blame-ignore-revs` entry to keep `git blame` useful.

8. Open (2026-10-04), for step 9a: the IRI scheme for entries and vocabulary terms (host and pattern), to be fixed before the first machine-readable release to corlab because published identifiers become a stability duty; and whether to publish the data before a license exists (item 4).

## 6. Risks and open items

- Pages semantics when switching the source (a short gap, extensionless URLs, custom 404) are measured on the fork before corlab. The way back is a settings change.
- Silent BibTeX parser failures: covered by the entry-count guard and the syntax fixes.
- Markup characters inside entries would render raw: a lint warning (step 6, optional).
- Unverified: whether the old charts render in current browsers; organization-level policy beyond the repository settings.
- Rights (license, contributor consent, one image of unknown provenance) are unresolved and deliberately left out.
- Content gaps in `dslzoo.bib` that need the maintainer, not a mechanical fix (left as they are): 25 entries without `zoo-phases` (the old site silently left them off the phase pages); 6 entries with an empty `zoo-subdomains` and 1 without the field; 6 entries with lowercase subdomain tokens (`components`, `transformation`, `perception`, `robot-structure`, `manipulation-and-grasping`), of which only `components` has a page on the old site; free-text `zoo-formalism` values such as `CFG?`. Step 6 may report these as warnings.

## 7. Sources

- JOSER 2016: A Survey on Domain-Specific Modeling and Languages in Robotics, Journal of Software Engineering for Robotics 7(1), 75-99, DOI 10.6092/JOSER_2016_07_01_p75.
- SIMPAR 2014: A Survey on Domain-Specific Languages in Robotics, LNCS 8810, 195-206, DOI 10.1007/978-3-319-11900-7_17.
- Software Heritage snapshot of corlab/dslzoo (2024-06-27) and Wayback Machine captures of corlab.github.io/dslzoo (public archives).
- Repository history, GitHub settings and the live site as of 2026-09-29 (read-only investigation).

## 8. Revisions

- Rev 1, 2026-09-29: first draft after the investigation.
- Rev 2, 2026-09-29: design round and a seven-lens review; 52 core steps, byte-identical cutover, rulesets, notice waves. Judged over-engineered.
- Rev 3, 2026-10-01: lean plan of 8 steps. Dropped: byte-identical reproduction, the drill, soak and notice machinery, legacy views, the rights and DOI track, the extensive test tiers. Rev 2 remains visible in the history of this branch.
- Progress, 2026-10-02: step 1 executed on the fork. A bundle of all corlab refs (`gh-pages`, `master`, `query`, `joser16`, 19 pull-request heads including PR 12) was made from a mirror clone, restored into an empty repository and checked (`git fsck`, all ref SHAs identical). Annotated tags `legacy-2020-05-08-site`, `legacy-2020-05-08-bib`, `legacy-2015-12-22-query` and `joser16-site` were pushed to the fork; corlab was not touched. No second copy of the bundle, by decision of the maintainer.
- Progress, 2026-10-02: step 4 executed on the fork. Four syntax defects in `dslzoo.bib` fixed, `.gitattributes` added; pybtex and bibtexparser 1.x now both read 144 of 144 entries and agree on every field (before: pybtex aborted, bibtexparser read 142). Details in DECISIONS.md.
- Progress, 2026-10-02 (later): `dslzoo.bib` cleaned up on the fork in two verified commits (whitespace only; then vocabulary typos, field-name case, trailing commas). The split of the bibliography is on the roadmap as step 5a.
- Progress, 2026-10-03: step 1 completed on corlab. The three `legacy-*` tags were first re-created on the fork with messages that do not point at this fork-only document (the never-move rule binds on corlab only, see DECISIONS.md), then `joser16-site`, `legacy-2015-12-22-query`, `legacy-2020-05-08-bib` and `legacy-2020-05-08-site` were pushed to corlab by explicit refspec. Verified afterwards: identical tag objects on origin and corlab, corlab branch heads unchanged, `v0.8.2` not on corlab. Only tag objects were added; all four targets were already heads or ancestors on corlab.
- Progress, 2026-10-03 (later): step 2 applied on corlab (two rulesets, no bypass list, read back only). Step 7 trialled on the fork: Actions deploy identical to the legacy site, marker file proves it is served by Actions, rollback needs the Pages source switched back and a manual legacy build. Details in DECISIONS.md.
- Progress, 2026-10-03 (later): plan A chosen for step 5. The generator is written directly in this repository from public sources, replacing the private-first route; the page names stay (decision 3), deployment via Actions (decision 2), the six 2015 pages stay as static pages in the new layout, the split of the bibliography (decision 5) is postponed and the generator reads the single file through an isolated loader. The address printed in the SIMPAR chapter is verified as a dead former address (section 1). Details in DECISIONS.md.
- Rev 4, 2026-10-04: re-scope by the maintainer. Scientific rigor limited to corlab and to two things: the references the publications cite (root URL, branch `query`, tag `joser16`) plus a prominent stability notice, and the intact bibliography (history, entries, manual classification). Page names, anchors and the 41 legacy pages are no longer fixed; step 3 became the notice, step 5 lean and free in structure, step 5a deferred, step 6 reduced to a build test and the entry-count guard, step 7 got a cutover check. The fork is a working copy without that rigor. Details in DECISIONS.md. It supersedes the plan A points that keep all 41 page names and the six 2015 pages as static pages; plan A itself (generator written in this repository) stands.
- Progress, 2026-10-04: step 3 (notice) and the Actions deploy of step 7 released to corlab in their minimal form: `master` fast-forwarded by two commits, Pages source switched to GitHub Actions, root and 69 legacy files verified before and after, `query`, `gh-pages` and the cited tags untouched. Not released: the bibliography commits, `CLAUDE.md`, `DECISIONS.md`, `CHANGELOG.md` and this plan. Details in DECISIONS.md.
- Addition, 2026-10-04: step 9 (9a semantic web layer, 9b `llms.txt` and plain views, 9c MCP server as a candidate) added on the maintainer's wish that all information of the zoo be accessible for semantic web tooling and LLMs; "machine-readable exports" removed from the not-part-of-the-plan list. Not started. Rigor of rev 4 unaffected: everything is generated from `dslzoo.bib`, which stays untouched. Details in DECISIONS.md.
