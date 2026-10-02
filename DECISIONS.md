# Decisions

## 2026-10-02 - Cited state pinned with four fork tags and one bundle; no second copy

Step 1 of the restructuring plan was executed on the fork. Four annotated tags pin the states the publications and the live site rest on: `legacy-2020-05-08-site` (1bc823f, last hand-generated site), `legacy-2020-05-08-bib` (3eba7a7, last bibliography state, 144 entries), `legacy-2015-12-22-query` (10d0659, tip of `query`) and `joser16-site` (fd34a51). Tag `joser16` stays as it is (annotated, points at ddb3c76, the 132-entry bibliography state). One git bundle of all corlab refs including the 19 pull-request heads (PR 12 exists only on GitHub) was made, restore-tested and kept outside the repository, with no second copy. The tags are on the fork only; the same tags on corlab wait for the maintainer's go-ahead.

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
