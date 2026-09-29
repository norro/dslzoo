# Restructuring plan - Robotics DSL Zoo

Status: DRAFT for review, 2026-09-29. Nothing in this plan has been executed; the investigation behind it was read-only. Open decision: whether the site generator is rebuilt or a recovered original is reused (section 6). Step lists are refined in later revisions (section 9).

Audience: maintainers and co-authors of the Robotics DSL Zoo, and future contributors.

Authors: Arne Nordmann, with Claude (AI assistant) as investigation and drafting aid.

## 1. Goal and hard constraint

The Zoo is the companion artifact of two publications, SIMPAR 2014 and JOSER 2016. This plan makes it maintainable again (regenerable site, CI, contribution checks, documented provenance) without breaking anything the publications or the web point at.

Hard constraint: the citation surface (section 2.1) keeps resolving to the same content. An unavoidable break is documented explicitly, with a redirect or notice, and never happens silently.

## 2. Findings the plan rests on

Investigated on 2026-09-29: the git history of all branches, the GitHub settings of `corlab/dslzoo` and of the fork `norro/dslzoo`, the live site, the JOSER 2016 full text, and public archives (Wayback Machine, Software Heritage). Where a fact could not be verified, it says so.

### 2.1 Citation surface

| URL or reference | Where it appears | What must stay true |
|---|---|---|
| https://corlab.github.io/dslzoo/ | JOSER 2016 footnote 19; the READMEs use the http variant | The root answers over http and https with the current site |
| https://github.com/corlab/dslzoo/tree/query | JOSER 2016 footnotes 2 and 16 (Google Scholar query script) | Branch `query` keeps its name and content |
| All 41 site pages, the asset paths, extensionless forms such as /all, and the 144 anchors all.html#KEY | Linked inside the site; visible in Wayback captures | Every published path keeps resolving |
| https://github.com/corlab/dslzoo/blob/master/dslzoo.bib | Linked from contribute.html | The file stays at the repository root; a branch rename redirects web URLs but not raw URLs |
| Tag `joser16` (annotated, commit ddb3c76, 132 entries, 2016-04-14) | Existing marker of the JOSER-era bibliography | Never moved |
| http://cor-lab.org/robotics-dsl-zoo | SIMPAR 2014 talk slides (2014-10-21) | Already dead (redirect, then 404); outside this repository's control |

The URL printed inside the SIMPAR 2014 chapter itself is unverified (paywalled). The repository was created on 2014-11-26, after the conference, so SIMPAR cannot have pointed at a live github.io page.

### 2.2 Current state

Repositories
- `corlab/dslzoo` (the cited repository): default branch `master`; branches `master`, `gh-pages`, `query`; tag `joser16`; no branch or tag protection, so anyone with write access can force-push or delete; no workflows; no open pull requests; one open issue (#18, a proposal to split the bibliography); 17 forks. Pages is a legacy branch build of `gh-pages`; HTTPS is not enforced; a `github-pages` environment exists without restrictions. The repository's Actions settings show no organization-imposed restrictions (checked in the settings pages on 2026-09-29); the default workflow token is read-write.
- `norro/dslzoo` (the fork, remote `origin`): default branch `main`; the same branches plus `ai/dslzoo-refresh`. Its own Pages site is live at norro.github.io/dslzoo as a duplicate of the cited site.
- The maintainer administers `corlab/dslzoo` through direct collaborator access; organization-level settings, if any exist, are not visible to the maintainer.

Live site
- Byte-identical to `gh-pages` commit 1bc823f (2020-05-08); 69 published files, 41 of them pages.
- 35 pages are generated from `dslzoo.bib` plus a taxonomy (9 subdomains, 12 disciplines, 8 phases). The site equals the newest bibliography exactly, so regenerating it adds or drops no entry. Six pages are 2014/15 leftovers that cannot be derived from the bibliography and have not changed since 2015-09-17.
- Known quirks of the old generator: 25 entries without phases appear on no taxonomy page or chart; 9 entry assignments drop off a discipline page through two misspelled vocabulary values; year charts stop at 2016; two author strings are truncated; one overview chart cannot be reproduced from the data.
- Every page requests four script files that never existed; charts load through a deprecated Google loader; the site carries no license, imprint or version number.

Data
- `dslzoo.bib`: 144 entries and seven `zoo-*` fields. Four syntax defects that common BibTeX parsers mishandle silently: two missing commas (near lines 1973 and 2018) and two duplicate fields (near lines 838/844 and 2108/2114). A four-edit repair makes three parsers agree on 144 entries.
- No license, CITATION.cff or DOI exists. Entries came from about 15 people: 94 arrived in the single survey commit of 2016-03-10, 11 from external contributors.

Generator
- Not present in any repository. The last six regenerations (2019-09 to 2020-05) were made by D. Wigand (GitHub: xwavex), who also edited the templates; earlier ones by the maintainer. Copies may survive in personal archives. Reuse or rebuild is open (section 6).

History and preservation
- One shared 119-commit graph; the tips on origin and corlab are identical; no history rewrite is needed. The authorship of external contributors exists only as commit authorship, so there is no squash and no rebase.
- Off-GitHub copies exist: a Software Heritage snapshot of 2024-06-27 (all branches, tag `joser16`, pull-request refs) and 419 Wayback captures (2017-04-24 to 2026-03-12). No web archive captured the site before 2017-04-24; the 2014 to 2016 states survive in the git history and its Software Heritage copy.

### 2.3 Statements in the project notes that need correcting

To be applied after the maintainer confirms. Governance files (CLAUDE.md) change only on confirmation, and history goes into DECISIONS.md as new entries rather than by rewriting old ones.

| Statement | Correction |
|---|---|
| Both publications cite corlab.github.io/dslzoo (CLAUDE.md, DECISIONS.md) | JOSER 2016 cites it (footnote 19) and the `query` branch URL (footnotes 2 and 16); the SIMPAR 2014 URL is unverified |
| `query` documents the data acquisition of "the original survey" (CLAUDE.md, DECISIONS.md) | `query` is the JOSER 2016 candidate search (220 + 20 Google Scholar queries, 779 candidates), confirmed by the maintainer; the SIMPAR 2014 survey was done manually |
| The generator is lost (DECISIONS.md, CHANGELOG.md) | Possibly recoverable, see section 2.2 |
| CHANGELOG 0.5.0: PR 17 was the first change after about 2.5 years | PR 9 landed on 2018-11-06 |
| CHANGELOG 0.6.0: six pull requests merged on 2019-09-15 | Seven pull-request merges plus one manual application (PR 12) |
| CHANGELOG: the fields "subdomain, phase, tool" | The fields are zoo-subdomains, zoo-phases and zoo-tool plus four more |

## 3. Principles

1. Citation stability outranks everything else.
2. Secure first: phase 0 leaves a safe state even if the rest is abandoned.
3. No history rewrite on shared refs; preserve states with annotated tags.
4. Fork first, corlab last. Every write to corlab is a separate, explicit decision, with the co-authors informed beforehand.
5. Compatibility before corrections: a rebuilt or recovered generator first reproduces the live site (measured, not eyeballed). Every visible change after that is separate, logged and versioned.
6. Prefer steps that need no organization owner.
7. Every step has a verification and a way back.

## 4. Phases

Legend: where = local, origin (the fork), corlab, or third-party. "Go" means the maintainer's explicit go-ahead is needed before the step happens.

### Phase 0 - Secure the citation surface

Goal: cited and historical states are backed up, permanently named, protected against accidental loss and documented correctly. No generator work and no change to the live site.

- P0.1 Backup bundle of all refs, including the corlab pull-request heads (the head of PR 12 exists only on GitHub); verify the bundle; keep two copies. Local.
- P0.2 Fix stale local pointers (`git remote set-head origin -a`, `git branch -u origin/main main`) and optionally guard against accidental pushes to corlab. Local; these edit git config, so the maintainer runs or approves them.
- P0.3 Annotated tags on origin for the anchors below. The names are proposals. `joser16` is never moved. Origin; go.
- P0.4 Tell the co-authors what phase 0 does to corlab. Person to person.
- P0.5 On corlab, go: push the tags (additive); freeze `query` (branch lock or ruleset; test the admin-bypass behaviour on a throwaway repository first); block force-push and deletion on `gh-pages`, the default branch and `joser16`. This needs repository admin only.
- P0.6 Refresh third-party archives after tagging (Software Heritage "save code now"; optionally the Wayback "Save Page Now" for the key URLs) and record the identifiers in PROVENANCE.md. Third-party; go.
- P0.7 Document: docs/PROVENANCE.md (URL generations, tooling generations, data provenance, the mapping of `query` to JOSER 2016 with its honest reproducibility limits); record the citation anchors in CLAUDE.md; apply the corrections of section 2.3. Origin branch; the maintainer confirms governance edits.

Proposed anchors:

| Proposed tag | Commit | Meaning |
|---|---|---|
| legacy/2020-05-08-main | 3eba7a7 | Last bibliography state before the reactivation (144 entries); equals the live site |
| legacy/2020-05-08-gh-pages | 1bc823f | Last hand-generated site; what corlab.github.io/dslzoo serves today |
| legacy/2015-12-22-query | 10d0659 | Tip of `query`, cited by JOSER 2016 |
| legacy/2016-04-14-gh-pages | fd34a51 | Site state matching `joser16` (132 entries) |
| legacy/2016-07-main and legacy/2016-07-gh-pages (optional) | 3069e7d and 9b64411 | Repository state while JOSER 7(1) appeared |
| legacy/2014-11-26-root (optional) | 61ec833 | Repository root |

Safe state after phase 0: every cited or historical state is reachable under a permanent name, copied off GitHub, and (on corlab) protected against accidental force-push or deletion. If corlab adoption is delayed, P0.1 to P0.3 and P0.7 still stand on the fork; corlab stays unprotected until P0.5.

### Phase 1 - Prepare the repository (fork only)

- P1.1 Bibliography hygiene as its own commit: the four syntax repairs, the key with a trailing space, the mixed-case entry type; `.gitattributes` (`*.bib text eol=lf` plus a repository-wide rule); clear the executable bit. No published content changes (checked against the golden master from P1.3).
- P1.2 Data files: taxonomy (labels, slugs and descriptions, which exist only inside the HTML today), legacy-token map, controlled vocabulary; lint rules (error-grade rules block new or changed entries; legacy debt is listed, not blocking).
- P1.3 Baseline fixtures as tests: a golden master of the live site (normalised page properties, not bytes) and the manifest of the 69 published paths plus aliases.
- P1.4 Documentation set: README (short, versioned), CONTRIBUTING (takes over the content of contribute.html), CITATION.cff, CHANGELOG corrections, DECISIONS entries, CLAUDE.md current state. LICENSE follows decision 7.

Exit: a clean, tested base on the fork.

### Phase 2 - Generator (open: reuse or rebuild)

See section 6. Both tracks end at the same acceptance tests:
- the golden master matches up to a whitelist (update stamp, year in the contribute page, word cloud);
- every path of the URL manifest and its extensionless aliases exists;
- entry-count guards hold (raw "@" count equals parsed entries; no failed blocks or comments);
- two builds are identical and internal links resolve.

### Phase 3 - Rehearsal on the fork

- P3.1 CI on origin: checks on pull requests (lint, guards, build, golden compare, URL contract) and a build artifact. Workflow files use pinned action versions and least-privilege permissions.
- P3.2 Deploy to the fork's Pages site in the candidate deploy mode; run the URL contract over http and https; measure what happens when the Pages source is switched (does the old content keep serving until the first deploy?); rehearse the rollback. Decide whether the fork's Pages site stays as staging (with a canonical link to the cited URL) or is switched off after the cutover.

Exit gate: the contract passes on the fork and the rollback has been demonstrated.

### Phase 4 - Adoption on corlab (each write is a separate go)

- P4.1 Heads-up and consent round with the co-authors and collaborators: workflows, protections, license and attribution, generator.
- P4.2 Land the reviewed content on the default branch as a fast-forward of the fork's `main` (corlab's `master` is an ancestor, so no merge and no rewrite).
- P4.3 Switch deployment following the rehearsed runbook; verify every path over http and https; keep the rollback ready.
- P4.4 Settings: default workflow token to read-only with per-workflow permissions; keep approval for first-time contributors' workflow runs; decide HTTPS enforcement (the cited URL exists in both schemes); repository description and homepage.
- P4.5 Rename `master` to `main` on corlab: not on the critical path. Do it later, once no page hard-codes `master`, and use GitHub's rename (it redirects web URLs and retargets pull requests), not push and delete.
- P4.6 Refresh the archives after the cutover.

### Phase 5 - Versioned corrections and optional additions

Corrections, each a separate logged change with the previous state kept reachable by tag: dead script includes; the meaning of the "updated on" stamp; misspelled vocabulary values (+8 entries on one discipline page); entries without phases; dead subdomain links and the frozen 2015 pages; the year axis; truncated authors; citation text (journal name "in" vs "for" Robotics, title wording, a typo, the JOSER link); charts loader and jQuery; fields the old site never showed.

Legacy views: serve the JOSER 2016 and 2020 states under sub-paths of the live site, built from the tags and byte-identical (recommended; they must exist before the first visible correction; design pending).

Offered, not decided: a persistent identifier (Zenodo DOI, or Software Heritage identifiers only), machine-readable exports with JSON-LD, llms.txt, an MCP server for queries.

Details still to be added per step (owner, minutes, verification, rollback): workflow files, `.nojekyll` for a legacy branch build, a 404 fallback for the malformed zoo link in the JOSER PDF, a canonical link for the fork's duplicate site.

## 5. Decisions needed

| # | Decision | Options | Current leaning | Blocks |
|---|---|---|---|---|
| 1 | Generator | Reuse a recovered original; rebuild | Open; search first (section 6) | Phase 2 |
| 2 | Deploy mode | Pages via Actions (`gh-pages` stays as frozen legacy); CI pushes to `gh-pages` | Actions after a successful rehearsal; CI push as fallback | Phases 3 and 4 |
| 3 | Fidelity policy | Compat first, then logged corrections; fix quirks immediately | Compat first | Phase 2 |
| 4 | Protections on corlab | As in P0.5; none | Do P0.5 | Phase 0 |
| 5 | Branch rename on corlab | Now; later; never | Later | P4.5 |
| 6 | Legacy views on the live site | Serve tagged states under sub-paths; tags and docs only | Serve them | Phase 5 |
| 7 | License and attribution (data, code, site, one image of unknown rights) | Needs the co-authors | Open | LICENSE, CITATION.cff |
| 8 | Persistent identifier | Zenodo DOI; Software Heritage identifiers only; none | Decide after phase 3 | Optional |

## 6. Open question: reuse or rebuild the generator

Search first: the maintainer's personal archives, and D. Wigand (last six regenerations, edited the templates). The search takes minutes to hours; nothing in P0, P1, P3.1 or P4.1 to P4.2 waits for it.

If the original is found (track A):
- keep the original source unchanged under a legacy tag, with provenance notes and the authors' consent;
- run it on the repaired bibliography and compare with the golden master (expected: an exact match; it would also settle the unreproducible overview chart and the author-truncation rule);
- decide whether to keep running it as is (it needs a runtime that works in CI) or to port it; keep it as reference oracle either way.

If it is not found or not wanted (track B):
- Python with uv, a bibliography reader with guards (silent parser failures are the main risk), Jinja2 templates derived from the site's HTML, and a compat mode that targets the golden master;
- the two unknowable behaviours (overview chart formula, author truncation) stay whitelisted differences until settled;
- a feasibility prototype is being evaluated; results are pending.

On either track the parser guards, the golden master and the URL contract remain mandatory.

## 7. Risks

- Silent data loss through BibTeX parsers.
- A tidy-up breaks a cited URL: `query` renamed or deleted, the bibliography moved, legacy pages dropped.
- Writes to corlab before the rehearsal, co-authors surprised, or a push by someone else meanwhile (the refs are unprotected today).
- Unknown behaviour when the Pages source is switched (a possible gap); measured on the fork first.
- Visible content changes on a cited artifact: only through versioned, logged corrections.
- Third-party runtime dependencies of the old pages (Google chart loader, hosted jQuery); rendering in current browsers is not yet verified.
- License and attribution are unresolved and need the co-authors' consent.
- Unverified: the URL printed in the SIMPAR chapter; whether the JOSER journal link still resolves; whether the charts render in current browsers.

## 8. Sources

- JOSER 2016: A Survey on Domain-Specific Modeling and Languages in Robotics, Journal of Software Engineering for Robotics 7(1), 75-99, DOI 10.6092/JOSER_2016_07_01_p75.
- SIMPAR 2014: A Survey on Domain-Specific Languages in Robotics, LNCS 8810, 195-206, DOI 10.1007/978-3-319-11900-7_17.
- Software Heritage snapshot of corlab/dslzoo (2024-06-27) and Wayback Machine captures of corlab.github.io/dslzoo (public archives).
- Repository history, GitHub settings and the live site as of 2026-09-29 (read-only investigation; the raw material is not part of this repository).

## 9. Revisions

- 2026-09-29: first draft after the investigation. The detailed step list and the design review follow in a later revision.
