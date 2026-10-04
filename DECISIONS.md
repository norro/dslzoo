# Decisions

## 2026-10-04 - Machine-readable and LLM access goes on the roadmap as step 9 (semantic web, llms.txt, MCP)

The maintainer wants all information of the zoo to be accessible as well as possible for semantic web tooling and for LLMs: semantic web features, possibly `llms.txt`, possibly an MCP server, and similar. Recorded in `docs/RESTRUCTURING-PLAN.md` as step 9 (9a semantic web layer, 9b `llms.txt` and plain views, 9c MCP server as an uncommitted candidate); "machine-readable exports" is removed from the plan's not-part-of-the-plan list. Nothing is built yet; 9a starts after step 5 has landed on `corlab`.

Constraints carried into the steps: everything is generated from `dslzoo.bib` and `generator/vocabulary.toml` by the same build, the bibliography itself is not changed, so the rigor scope of rev 4 is unaffected; the generated data describes the current edition, the pinned states stay the citable ones. Two points are open and listed in plan section 5, item 8: the IRI scheme for entries and terms (published identifiers are a new stability duty, so fix them before the first release to `corlab`) and the license (plan decision 4; publishing the data as a dataset wants one and needs the co-authors). `llms.txt` is a proposed convention, not a standard. An MCP server cannot run on Pages; the preferred form is a local package that reads the published data files.

**Why:** the maintainer's wish; the zoo is a curated map of robotics DSLs, and linked data plus LLM-readable files make that curation usable by tools without scraping the HTML.
**Alternatives considered:** a plain JSON export only (cheaper, but no linked-data integration and no shared vocabulary); an MCP server first (needs the dataset of 9a anyway); a hosted MCP server (needs a separate host and operation, too heavy for a not-mission-critical artifact).

## 2026-10-04 - The generator exists and deploys the fork; removed pages become redirect stubs; venv and pip instead of uv

The new generator lives in `generator/` (`build.py` with pybtex, pylatexenc, Jinja2 and Markdown; templates, `vocabulary.toml`, `redirects.toml`, static CSS and a small script). It reads `dslzoo.bib` and `docs/STABLE-REFERENCES.md` and writes the site; it fails if the parsed entry count differs from the number of entries in the file, everything else about the data is a warning (40 at this date: entries without phase or subdomain, tokens outside the vocabulary). Names of the 35 legacy pages that continue to exist are kept, the look is new: own CSS with dark mode, no Bootstrap, jQuery, d3 or Google Charts, no external requests, charts rendered at build time as HTML and CSS, an index table with sortable columns and a text filter (`all.html?q=`), the citation note and `versions.html` built in. The vocabulary texts come from the public legacy pages. `pages.yml` now builds with the generator and the fork (`norro.github.io/dslzoo`) deploys on every push to `ai/dslzoo-refresh`; `.github/citation-note.py` is removed, the generator replaces it.

Six legacy pages are gone (five 2015 subdomain pages, four of them empty, and `domain-examples.html`). Each is a redirect stub to a successor (`redirects.toml`: the five to the Architectures and Programming subdomain, the domain example to the subdomain overview). GitHub Pages cannot send HTTP 3xx; a stub has a meta refresh of 0 seconds, a `rel=canonical` and a script fallback that keeps query string and anchor. Both are relative, not absolute, because the host differs between the fork and `corlab`. The build fails if a target is not a generated page. What the six pages were, where the originals are and how to bring one back: `docs/REMOVED-PAGES.md`. Real 3xx would need a host in front of Pages (own domain with a CDN or proxy), which `corlab.github.io` does not have.

Counts differ from the legacy site: the generator counts distinct entries, the old charts counted an entry once per page it appeared on (Capability Building 189 there, 106 now). Entries without a known term of the grouping kind appear in a group "Not assigned to a ..." instead of vanishing from the page.

Not released to `corlab`: this version of `pages.yml` replaces the live site content on `corlab` as soon as it reaches `master` and is therefore the cutover itself; it must not be merged or cherry-picked there without the go-ahead and the before/after check of rev 4. The way back stays the Pages source `gh-pages` plus a legacy build.

**Why:** the plan's step 5 and the maintainer's wish for a slim generator with a modern look; the Pages limits decide the form of the redirects; uv is not installed on this machine (MACHINE.md lists the tools) and the existing workflow already used venv and pip, so the plan's uv became requirements.txt.
**Alternatives considered:** keeping the six pages as static pages (carries dead 2015 structure); a custom 404 page only (loses the successor hint); real 301 behind a proxy (not available for the cited host); uv (can replace the venv step later without changing the build).

## 2026-10-04 - Citation note and Actions deploy released to corlab; the cited root URL is now served by Actions

With the maintainer's go-ahead, two commits (the note and the Pages workflow; then the more prominent note with a thick black frame and the essential phrases in bold) were pushed to `corlab` `master` (fast-forward `3eba7a7..b584809`, no force) and to `origin` `main`, and the `corlab` Pages source was switched from branch `gh-pages` to GitHub Actions. What is served now is a copy of `gh-pages` (`1bc823f`) with the note above the navigation on every page, a nav entry `Versions` and `versions.html`, rendered from `docs/STABLE-REFERENCES.md` by `.github/citation-note.py`, a stand-in for the generator. The workflow runs on pushes to `master` that touch it, the script or the text, and on manual dispatch; it publishes with read-only permissions.

Checks at the cutover, the rigor of rev 4: before, all 69 files of the live site were byte-identical to `gh-pages`; after, all 70 files (41 pages with the note, 28 files unchanged, `versions.html` new) matched the output expected from the same script, the root answered 200 on http and https, the 404 page was byte-identical to before, and a poller (about one request per second, 74 samples across the switch) saw no non-200 answer from the root. `query`, `gh-pages` and the five cited tags were not touched (heads and tag objects compared after the push). Way back: set the Pages source to `gh-pages` (`PUT /repos/corlab/dslzoo/pages` with `build_type=legacy`, source branch `gh-pages`, path `/`) and trigger a legacy build (`POST /repos/corlab/dslzoo/pages/builds`); measured on the fork on 2026-10-03.

Not released to `corlab`, deliberately: the bibliography cleanup commits (open points 6a and 6b of the plan), `.gitattributes`, `CLAUDE.md`, `DECISIONS.md`, `CHANGELOG.md` and the plan (the plan states it is not meant for `corlab`). The editions paragraph of the versions page and the commitment on it were confirmed by the maintainer. The default workflow token of `corlab` is still read-write (the workflow declares read-only permissions itself); the Pages setting "enforce HTTPS" is off, as before, and both http and https answer. `main` on `origin` equals `master` on `corlab`; the working branch merged `main`, so the files of the workflow, script and text are identical on all three.

**Why:** the maintainer wants the note live on the cited address, and the legacy `gh-pages` content is frozen, so the note can only reach the site through a deploy that builds on top of it. A copy-and-inject step keeps `gh-pages` untouched as the way back and needs no generator.
**Alternatives considered:** committing the note into `gh-pages` (breaks the frozen fallback and the intent of the ruleset); waiting for the generator (leaves the cited address without the note for the whole of step 5).

## 2026-10-04 - Scientific rigor re-scoped to corlab and the cited references; plan rev 4

The maintainer re-scoped the plan (rev 4). Scientific rigor applies to two things only, and only to what lands on or is served from `corlab`: (1) the references that publications cite and that still exist (root URL, branch `query`, tag `joser16`, per JOSER 2016) stay stable, and a prominent notice says that they exist, that they stay stable and why; (2) the bibliography stays intact (history, all publications, the manual classification made by hand following the process documented in JOSER 2016). Everything else may change: the new generator is lean, may produce different pages and a different structure, and needs no exhaustive tests. Page names, `#key` anchors and the 41 pages of the legacy site are no longer fixed constraints, and the six 2015 leftover pages need not be carried over. This supersedes the 2026-10-03 points that all 41 page names stay and that the six 2015 pages are carried over as static pages; plan A (generator written in this repository) and the note on every page with a versions page (2026-10-03) stand. The fork (`origin`) is a working copy, not a reference target, and needs none of this rigor.

Consequences in the plan: step 3 becomes the stability notice (README section, a note on every page, the versions page) plus a short PROVENANCE.md; step 5 is lean and free in structure; step 5a (bibliography split) is deferred because it would split the history of `dslzoo.bib`; step 6 shrinks to a build test and the entry-count guard; step 7 carries a before/after check of the root at the `corlab` cutover. The notice reaches the site only through a deploy built on top of the frozen legacy `gh-pages` content (entry above). Open, due when the bibliography commits are cherry-picked to `corlab`: whether to keep the new spelling of nine classification tokens changed on 2026-10-02 (8x `Error and Exeption Handling`, 1x `Control of Handling and Events`; the tag `legacy-2020-05-08-bib` keeps the original), and whether the whitespace-only commit goes to `corlab` with a `.git-blame-ignore-revs` entry. Also open: whether `contribute.html` keeps its name. `CLAUDE.md` states the rigor scope.

Wording of the notice (maintainer's line, same day): the zoo is a dynamic, live robotics DSL and model zoo, on `corlab` as well as on the fork; the citable truth for the SIMPAR 2014 and JOSER 2016 surveys lies on `corlab` in pinned states, with a pointer to how and where to find the old state. The SIMPAR half is open: the chapter prints only the dead former address (entry above), and the repository starts on 2014-11-26 with the bibliography first committed on 2015-01-08, after that survey, so there is no pinned state from its time; the notice says exactly this and points at the Internet Archive capture and the first generated site of 2014-12-10 (plan, section 5, item 6). The notice follows the design of the entry above (a note on every page, a versions page `versions.html`); `docs/STABLE-REFERENCES.md` is the source text of that page.

**Why:** the Zoo is not mission-critical, and two requirements carry the scientific weight: a published citation must keep resolving, and the data the surveys rest on must stay intact. Rev 3 still froze everything the legacy site did (page names, anchors, leftovers), which no publication asks for and which would tie the new generator to a structure nobody cites. The fork is cited nowhere, so rigor there only costs time.
**Alternatives considered:** keeping all 41 page names stable (the earlier recommendation: cheap, but it fixes a structure nobody cites); applying the rigor to both remotes (over-strict for a working copy).

## 2026-10-03 - Every page carries a citation note and links a versions page; SIMPAR 2014 prints only a dead address

The generated site shows a note above the navigation on every page (not dismissible) and has a page `versions.html`. The note names the fixed, absolute addresses for scientific citation: for JOSER 2016 `https://corlab.github.io/dslzoo/` and `https://github.com/corlab/dslzoo/tree/query` (article footnotes 19, 2 and 16). For SIMPAR 2014 it names the address the chapter prints, `http://cor-lab.org/robotics-dsl-zoo` (footnotes 6 and 8, verified on 2026-10-03 against the authors' copy, which the maintainer states is content-identical to the published chapter), as no longer reachable. The only preserved state around the conference is the Internet Archive capture `20141009225401` of that address (shows "updated on August 13th 2014"); the closest git states are the repository start of 2014-11-26 and the first generated site of 2014-12-10 (commit 6ffcb65). The versions page explains where the cited states are (tags, tag archives, Internet Archive, Software Heritage), that the modernization of the website started on 2026-09-28, and that the hand-curated edition (2014-2020) is succeeded by a generated edition that is curated less by hand but stays current. The addresses are literal and never derived from the deployment host, because the preview is served from `norro.github.io/dslzoo`. The wording about the transition between editions stays marked as a draft until the maintainer confirms it.

**Why:** the address printed in SIMPAR is dead and readers arrive on any page through the cited trees and tags; they must learn at once which edition they see and how to reach the cited state.
**Alternatives considered:** a note on the home page only (does not reach deep links); leaving the SIMPAR address out or inventing a working one (neither is verifiable); relative links (break on the preview host).

## 2026-10-03 - The peculiarities of the old site are not requirements of the new generator (page-name part superseded by 2026-10-04)

Structure comes from the controlled vocabulary (9 subdomains, 8 phases, 12 disciplines of Architectures and Programming): one page per vocabulary item; an entry appears on every page whose category it carries and always in the index. Entries without a phase, with an empty subdomain or with an unknown token are neither hidden nor patched by the generator; a lint names them. A value outside the vocabulary (for example a lower-case `components`) creates no page. Broken accents of the old pages are decoded correctly instead of being reproduced. The comparison with branch `gh-pages` is a one-off plausibility check of page names and anchors, not a conformance test. The six 2015 pages that cannot be derived from the bibliography stay as static pages in the new layout with a notice (decision 3 of the plan: all 41 page names stay; superseded by 2026-10-04: page names are free and the six pages need not be carried over); redirect stubs remain an option.

**Why:** the maintainer's judgement: peculiarities and exceptions of the old pages are likely errors, not the goal of the generator. Reproducing them would carry defects such as misspelled disciplines that silently dropped entries into the new site and would make generator and specification several times larger.
**Alternatives considered:** byte- or number-identical reproduction (rev 2 of the plan, dropped); redirect stubs for the six 2015 pages (cleaner, loses their content).

## 2026-10-03 - The new generator is written directly in this repository (plan A); supersedes "build in the private repository first"

The generator (Python with uv, pybtex, Jinja2; built and published by a GitHub Actions workflow to GitHub Pages) is written from scratch in `norro/dslzoo` on `ai/dslzoo-refresh`. Its only inputs are public: `dslzoo.bib` and the HTML of branch `gh-pages`. The private generator repository is not read and nothing from it is used. This replaces the step "build privately, then import cleanly" of the plan and is the maintainer's go-ahead for a generator in this repository. First target is the fork site `norro.github.io/dslzoo`; `corlab` is not touched. `dslzoo.bib` stays one file for now; the loader is isolated, so the split of the bibliography (step 5a) changes only that part.

**Why:** the Actions pipeline needs the code in this repository, and a fresh implementation from public sources carries nothing private, so an import step would only copy files.
**Alternatives considered:** build privately, then import (more effort, same result); CI that fetches the private repository (needs credentials in CI).

## 2026-10-03 - corlab refs protected by rulesets; Pages deploy via Actions tried on the fork, fallback to gh-pages verified

Two rulesets without bypass list went live on `corlab` (maintainer's go-ahead): `protect-cited-branches` (deletion, non-fast-forward) for `query` and `gh-pages`, `protect-cited-tags` (deletion, non-fast-forward, update) for `joser16*` and `legacy-*`. `master` is deliberately not covered. The throwaway-repository trial of the plan was skipped: rulesets are unavailable on private repositories without GitHub Pro, and the maintainer chose to apply them directly; the rulesets were only read back, never attacked. Deployment via Actions (upload-pages-artifact plus deploy-pages, Pages source "GitHub Actions") was tried on the fork with a test workflow publishing the unchanged `gh-pages` content: all 69 files, root, `/index` and the 404 page were byte-identical to the legacy site, and a marker file (`deploy-check.txt`, carrying the run id and commit SHA) proved that Actions, not the legacy build, served it. The fork was then switched back: setting the source back to `gh-pages` alone changes nothing visible (the Actions artifact keeps being served); a manual legacy build (`POST /repos/{repo}/pages/builds`) is required, after which the marker returned 404 and the site matched the baseline again (about 40 s). The first comparison right after the 404 still showed two stale files and was identical on re-measurement, so a rollback check must wait for the CDN to settle. The fork's `github-pages` environment only allowed `gh-pages`; a branch policy for `ai/dslzoo-refresh` was added for the test (`corlab` has no policy). The gap between switching to Actions and the first deploy was at most about 35 s on the fork, not polled. The fork is back on the legacy source; the test workflow stays in the branch and is not meant for `corlab`.

**Why:** the rulesets guard the cited refs against accidental deletion or force-push (an agreement alone is not enforced, `corlab` had no protection). The Actions trial measures the Pages switch semantics on the fork before touching `corlab`, as the plan requires, and the rollback test proves the way back that makes `gh-pages` worth keeping.
**Alternatives considered:** rulesets for the tags and `query` only, without `gh-pages` (the assistant's recommended minimum; the maintainer chose to include `gh-pages` as the fallback source); CI pushing to `gh-pages` instead of the Actions artifact (keeps generated HTML in history and loses the frozen fallback).

## 2026-10-02 - Never-move rule for citation tags binds on corlab only; three fork tags re-created before they go there

The never-move rule for `joser16*` and `legacy-*` (entry of 2026-10-02 below, CLAUDE.md) is scoped: it is strict on `corlab`, the only target of scientific references, and binds for a tag from the moment it is on `corlab`. Until then a tag on the fork may be fixed. Applied right away: `legacy-2020-05-08-site`, `legacy-2020-05-08-bib` and `legacy-2015-12-22-query` are re-created on the fork with the same targets but without the "see docs/RESTRUCTURING-PLAN.md" pointer in their messages, because that file exists only on the fork branch and would dangle on `corlab`. `joser16-site` has no such pointer and stays. The plan for `corlab` (executed 2026-10-03 with the maintainer's go-ahead, identical tag objects on both remotes verified): push these four tags by explicit refspec; they add only tag objects, since all four targets are already heads or ancestors on `corlab` (gh-pages, master, query). `v0.8.2` stays on the fork: its commit is on `ai/dslzoo-refresh` and would drag fork-only history, including this file and the plan, into `corlab`.

**Why:** re-creating the fork tags now gives `corlab` and the fork the identical tag object under each name, which is cheap to verify later; re-creating after the `corlab` push would be the silent change the rule exists to prevent. The fork tags are hours old and cited nowhere, so nothing depends on their old object ids.
**Alternatives considered:** push the tags with the dangling pointer and explain it in PROVENANCE.md (the assistant's first proposal; rejected by the maintainer, who scoped the rule instead); apply the rule to both remotes from day one (over-strict for a fork that is a working copy).

## 2026-10-02 - Version 0.8.2 tagged on the fork's working branch

`v0.8.2` is an annotated tag on `norro/dslzoo`, on the commit that records this decision. The maintainer asked for it after the consequence was stated: the tag names a branch commit, not the hash the version will have once its pieces are cherry-picked into `main`. Consequence for later: tags are never moved or re-created, so when the version reaches `main` it gets the next free number (or another tag name), not a second `v0.8.2`. The tag is on the fork only; corlab is untouched.

**Why:** the maintainer wants the released state addressable on the fork now. A new version tag is a new name; it does not touch the never-move rule for `joser16*` and `legacy-*`.
**Alternatives considered:** wait with the tag until the version exists on `main` (the decision below, now superseded).

## 2026-10-02 - Version 0.8.2 cut on the working branch without a git tag (superseded by the entry above)

The backlog since 0.8.1 (bibliography fixes and cleanup, `.gitattributes`, plan, tags) was released as 0.8.2 (PATCH: fixes and tooling, no new capability) in CHANGELOG and README. No `v0.8.2` git tag was created or pushed.

**Why:** the release commit sits on `ai/dslzoo-refresh`, whose reviewed pieces are cherry-picked into `main` with new hashes; a tag on the branch commit would point at a state that never lands on `main`. In this repo tags double as scientific references that are never moved (CLAUDE.md), so a tag that has to be deleted or re-created later is worse than no tag. Tag the version once it exists on `main`.
**Alternatives considered:** tag now on the branch (the generic push ritual; rejected for the reason above); no version bump until the work lands on `main` (leaves the backlog uncut, which the generic ritual exists to prevent).

## 2026-10-02 - Bibliography cleaned in two separate commits; split goes on the roadmap, form open

`dslzoo.bib` was cleaned up in two commits so each can be checked on its own. Commit one is whitespace only (blank lines, indent, `name = value`, trailing whitespace, LF, `, ` between vocabulary tokens); its check is strict: the file with all whitespace removed is identical before and after, and both parsers read identical entries. Commit two changes content only where it is mechanical: lower-case entry types and field names, a trailing comma after every entry's last field, and two vocabulary typos in `zoo-ap-subdomains` mapped to the names of the discipline pages on the pinned site (`legacy-2020-05-08-site`). The entry order was left alone.

Deliberately not changed, because it needs the maintainer: the 25 entries without `zoo-phases`, the empty or missing `zoo-subdomains`, the lowercase subdomain tokens, the free-text `zoo-formalism` values (listed in the plan, section 6). Not done either: sorting entries or reordering fields.

The maintainer wants the single file split because it is unwieldy; this is on the plan as step 5a. Preferred form: one file per entry in `bib/`, with `dslzoo.bib` kept at the root as a generated aggregate. Split by year is not recommended.

**Why:** a whitespace reformat mixed with content edits cannot be verified and ruins `git blame`; separate commits let a mechanical check carry the first one. The 9 re-tokenised entries will now appear on their discipline pages after regeneration, which is the intended behaviour the old site missed. The split waits for step 5 because the new generator decides what it reads, and `dslzoo.bib` at the root is a fixed constraint (linked from contribute.html).
**Alternatives considered:** one combined cleanup commit (unverifiable); sorting entries by key now (a huge diff for no gain if the split follows); mapping the lowercase subdomain tokens or filling the missing phases (guessing at the maintainer's classification); a split by year (uneven: 21 entries in 2012, 2 in the 1980s together, 31 distinct years).

## 2026-10-02 - Bibliography syntax fixed; duplicate keywords merged, not dropped

Step 4 of the restructuring plan: the four syntax defects in `dslzoo.bib` were fixed in a commit of their own (so it can be cherry-picked on its own); `.gitattributes` (`* text=auto eol=lf`) follows with the docs. Two missing commas were added (`Araiza-Illan2016`, `Ciccozzi2016Adopting`). In `hochgeschwender2014declarative` the second `booktitle` was removed; it was identical to the first. In `Detzner2019Novel` the two `keywords` fields (the publisher's semicolon list and the zoo's `dsl-zoo` list) were merged into one comma-separated field: `dsl-zoo` first, then the publisher's keywords, case-insensitive duplicates dropped (the zoo's own four extra keywords were already in the publisher list). Verification: pybtex and bibtexparser 1.x both read 144 of 144 entries and agree on every field (names compared as parsed persons, month macros normalized). Before the fix pybtex aborted with a duplicate-field error and bibtexparser silently read only 142 entries (the two it lost are exactly the two with a missing comma).

**Why:** with a duplicate `keywords` field the outcome depended on the parser: bibtexparser 1.x keeps the first (here the publisher list, so the `dsl-zoo` marker is lost), pybtex rejects the whole file. A merge is the only fix that is parser-independent and loses nothing. The `.gitattributes` rule matches what the index already holds (LF), so it changes no blob; it only stops CRLF from reaching commits on Windows checkouts.
**Alternatives considered:** keeping only the zoo's `keywords` (loses the publisher's keywords); keeping only the publisher's (loses the marker); leaving the entry and relying on one parser's behaviour (the failure mode this step exists to remove).

## 2026-10-02 - Cited state pinned with four fork tags and one bundle; no second copy

Step 1 of the restructuring plan was executed on the fork. Four annotated tags pin the states the publications and the live site rest on: `legacy-2020-05-08-site` (1bc823f, last hand-generated site), `legacy-2020-05-08-bib` (3eba7a7, last bibliography state, 144 entries), `legacy-2015-12-22-query` (10d0659, tip of `query`) and `joser16-site` (fd34a51). Tag `joser16` stays as it is (annotated, points at ddb3c76, the 132-entry bibliography state). One git bundle of all corlab refs including the 19 pull-request heads (PR 12 exists only on GitHub) was made, restore-tested and kept outside the repository, with no second copy. The tags are on the fork only; the same tags on corlab wait for the maintainer's go-ahead. The rule that these tags are never moved, deleted or re-created is recorded in CLAUDE.md (scientific reference: a published citation must keep resolving to exactly the cited state).

`joser16-site` is the last `gh-pages` commit before the tag `joser16` was created (13:52 CEST against 13:58 CEST on 2016-04-14; the next site commit followed at 14:11). The `joser16` commit itself is a bibliography state, not a site state, so the site state needed its own tag.

**Why:** the generated site and the bibliography are about to be restructured; the cited states need names that cannot be mistaken and a way back that does not depend on one hosting service. No second copy: the maintainer judged the existing public copies sufficient (corlab itself, the Software Heritage snapshot of 2024-06-27, Wayback captures); the bundle adds the pull-request heads and a local pin.
**Alternatives considered:** a second copy in a second cloud account, as a release asset on the fork or in a private GitLab project (the plan's original "two places"; not pursued); tagging corlab right away (held back, every write to corlab needs the maintainer's go-ahead).

## 2026-10-01 - Lean, pragmatic scope; the old generator is only a template

The restructuring plan is cut to a lean eight-step plan (docs/RESTRUCTURING-PLAN.md rev 3). The Zoo is not mission-critical, generation runs offline and is never time-critical, so: no byte-identical reproduction of the old pages (the generated artifacts are to be modernized), pragmatic instead of exhaustive testing, and no ceremony around hypothetical failure cases. The old generator is used only to understand the historical approach and goal; the new generator is written fresh, most likely in Python, in the private generator repository and imported cleanly. Fixed are only the cited names: the Pages URL with its page names, branch `query`, tag `joser16`, and no history rewrite.

**Why:** the earlier plan (rev 2, 52 core steps, about 53 hours) protected against failures that matter little for this artifact and fixed byte-identity, which contradicts modernizing the output.
**Alternatives considered:** keep rev 2 (rejected as over-engineered); drop all protection of the cited names (rejected: two publications point at them and the protection is cheap).

## 2026-09-29 - Generator: reuse vs rebuild left open until the original has been searched for (superseded in part 2026-10-01)

The 2026-09-28 decision to rebuild the site generator without searching further is suspended. The last six site regenerations (2019-09 to 2020-05) were made by a co-author, who also edited the templates, and the maintainer may still hold a copy in old personal archives; both are checked first. The plan (docs/RESTRUCTURING-PLAN.md) keeps two generator tracks, reuse and rebuild, that end at the same acceptance tests. Nothing else in the plan waits for this.

**Why:** the generator ran in at least two environments after 2016, so it plausibly survives. Recovering it would give byte-exact reference output and settle two behaviours (an overview chart formula, the truncation of two author strings) that a rebuild cannot derive from the data.
**Alternatives considered:** rebuild immediately (the 2026-09-28 decision: cheap, but discards a possibly available reference); delay everything until the search is done (unnecessary, because the securing and preparation phases are independent of the generator).

## 2026-09-28 - Corlab/dslzoo confirmed as legitimate restructuring target, not just the personal fork

Verified via `gh api repos/corlab/dslzoo --jq .permissions` that Arne has
admin rights directly on `corlab/dslzoo` (the org repo the two publications
cite), not just push access via a PR-based fork workflow. This supersedes the
"scope for now is Arne's own fork" alternative noted in the feature-branch
decision below.

**Why:** the two publications' citations point at `corlab.github.io/dslzoo`,
not the personal fork - so keeping the reactivation confined to
`norro/dslzoo` indefinitely would not actually update the cited artifact.
Admin access means there's no procedural reason (PR review, org membership)
to avoid working directly against `corlab/dslzoo` once changes are reviewed.

**Alternatives considered:** keep `norro/dslzoo` as the sole target and
eventually open a PR to `corlab/dslzoo` like an external contributor would -
unnecessary friction given direct admin access.

## 2026-09-28 - Full restructuring authorized; scientific-citation stability is the one hard constraint

Arne explicitly authorized redesigning branch structure, file layout, and
tooling from scratch - nothing about the current shape (`master`/`gh-pages`/
`query`) needs to be preserved for its own sake. The one non-negotiable: the
two publications citing `corlab.github.io/dslzoo` must keep resolving, or any
break in that gets an explicit, documented redirect/notice.

**Why:** dslzoo is a citable academic artifact, not just a personal repo -
restructuring is free, breaking a published citation silently is not.

## 2026-09-28 - Rename `master` to `main`; document the 2014-2020 vs. 2026 tooling generations as an explicit break

Renamed the local `master` branch to `main` (modern default, matches this
machine's `init.defaultBranch` convention). Approved the "clean break"
restructuring: consolidate bib source, generator, and docs into `main`; stop
committing generated HTML at all; build and deploy to `gh-pages` via CI
instead. A new `PROVENANCE.md` will document this as an explicit
methodological generation change (tooling X, 2014-2020, hand-maintained vs.
tooling Y, 2026, automated) in the same spirit as the `query` branch's
existing documentation of the survey's data-acquisition methodology - not
hidden or silently rewritten, since readers of the two publications may land
on this repo years later and need to understand what changed and why.

**Why:** Arne asked explicitly for scientifically clean documentation of any
break, matching the rigor already applied to the `query` branch.

**Alternatives considered:** evolutionary option (keep `gh-pages` as a
hand/CI-updated branch but otherwise unchanged structure); split into
separate bib/generator/site repos (more overhead than warranted here).

## 2026-09-28 - Reconstruct CHANGELOG.md retroactively from git history

Versions 0.1.0-0.8.0 in `CHANGELOG.md` were generated from `git log` on
`master`, grouping commits by the date they actually landed there. They
approximate the real history but are a best-effort reconstruction, not
authoritative dated releases (author-local commit dates and merge/landing
dates sometimes differ by months, e.g. several 2018 entries only landed on
`master` in a September 2019 backlog-clearing merge).

**Why:** the project never used semver or a changelog before. Needed a
starting point that satisfies "README H1 shows current version" without
pretending the granularity is more precise than the source history allows.

## 2026-09-28 - Rebuild the site generator instead of searching for it further (superseded 2026-09-29)

The tool that turned `dslzoo.bib` into the `gh-pages` HTML is not present in
any branch, fork, or corlab-org repository - only the bib source and the
generated HTML output were ever committed. Decided to write a new generator
rather than keep searching for the original.

**Why:** the original was local tooling (commits authored from an institute
address Arne no longer has access to) - low odds of recovery, and a small
rebuild (e.g. Python +
bibtexparser + a templating library) is cheap compared to more searching.

**Alternatives considered:** dig through old backups/institute mail for the
original script first; postpone regeneration and only maintain the bib file
for now.

## 2026-09-28 - Work on a feature branch, cherry-pick into master (superseded in part 2026-09-28)

All reactivation work (this scaffolding, the future generator rebuild, bib
updates) happens on `ai/dslzoo-refresh`. `master` stays untouched until Arne
reviews and cherry-picks specific commits into it.

**Why:** keeps the AI footprint out of `master`'s history by default; Arne
decides what actually lands and when. The branch-then-review mechanic still
stands; only the "scope for now is Arne's own fork" alternative below was
superseded the same day once admin access to `corlab/dslzoo` was confirmed
(see the entry above) and `master` was renamed to `main`.

**Alternatives considered:** squash-merge the whole branch in one commit once
reviewed (less granular control per change); work directly against
`corlab/master` and open PRs upstream, if the goal turns out to be reviving
the org project rather than just this fork (not chosen at the time - scope
was Arne's own fork only).

## 2026-09-28 - Fast-forward the fork to match upstream before starting work

`norro/dslzoo` (this fork) had zero unique commits and was purely stale - 39
commits behind `corlab/dslzoo` on `master`, 9 behind on `gh-pages`. Both
branches were fast-forwarded (locally, then pushed to `origin`) before any
new work began.

**Why:** starting from a five-and-a-half-year-old snapshot would mean
re-doing work the upstream community already did; a clean fast-forward carried
no conflict risk since the fork had no divergent history.
