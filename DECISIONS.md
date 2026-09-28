# Decisions

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

## 2026-09-28 - Rebuild the site generator instead of searching for it further

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

## 2026-09-28 - Work on a feature branch, cherry-pick into master

All reactivation work (this scaffolding, the future generator rebuild, bib
updates) happens on `ai/dslzoo-refresh`. `master` stays untouched until Arne
reviews and cherry-picks specific commits into it.

**Why:** keeps the AI footprint out of `master`'s history by default; Arne
decides what actually lands and when.

**Alternatives considered:** squash-merge the whole branch in one commit once
reviewed (less granular control per change); work directly against
`corlab/master` and open PRs upstream, if the goal turns out to be reviving
the org project rather than just this fork (not chosen - scope for now is
Arne's own fork).

## 2026-09-28 - Fast-forward the fork to match upstream before starting work

`norro/dslzoo` (this fork) had zero unique commits and was purely stale - 39
commits behind `corlab/dslzoo` on `master`, 9 behind on `gh-pages`. Both
branches were fast-forwarded (locally, then pushed to `origin`) before any
new work began.

**Why:** starting from a five-and-a-half-year-old snapshot would mean
re-doing work the upstream community already did; a clean fast-forward carried
no conflict risk since the fork had no divergent history.
