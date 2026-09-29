# Decisions

## 2026-09-29 - Generator: reuse vs rebuild left open until the original has been searched for

The 2026-09-28 decision to rebuild the site generator without searching further is suspended. The last six site regenerations (2019-09 to 2020-05) were made by D. Wigand, who also edited the templates, and the maintainer may still hold a copy in old personal archives; both are checked first. The plan (docs/RESTRUCTURING-PLAN.md) keeps two generator tracks, reuse and rebuild, that end at the same acceptance tests. Nothing else in the plan waits for this.

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

**Why:** the original was local tooling (commits authored from
`anordman@cor-lab.uni-bielefeld.de`, an institute address Arne no longer has
access to) - low odds of recovery, and a small rebuild (e.g. Python +
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
