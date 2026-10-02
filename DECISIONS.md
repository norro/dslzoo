# Decisions

## 2026-10-02 - Version 0.8.2 cut on the working branch without a git tag

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
