# CLAUDE.md - Robotics DSL Zoo

Companion artifact to two publications (full citations in README.md /
PROVENANCE.md once it exists): SIMPAR 2014 and JOSER 2016 surveys on DSLs in
robotics, both authored by Arne. Both cite the live
`corlab.github.io/dslzoo` URL. **Any change that could break that citable
URL needs to be called out explicitly, never silently.**

## Remotes - do not conflate

- `origin` = `norro/dslzoo` (Arne's personal GitHub account) - **the only
  remote to push to by default.**
- `corlab` = `corlab/dslzoo` (upstream org repo, the one the publications
  actually cite; Arne has admin there). **Never push here without an
  explicit go-ahead** - timing needs coordination with the other
  contributors first (see below). Fetch/compare freely.

## Branches

- `main` - default branch on `origin`. Source of truth once reviewed;
  currently just README.md + dslzoo.bib (renamed from `master` 2026-09-28).
- `ai/dslzoo-refresh` - active working branch for the reactivation. New work
  happens here first; reviewed pieces get cherry-picked into `main`, not
  pushed there directly.
- `gh-pages` - built site output. Currently hand-committed HTML from a
  generator tool that no longer exists (see DECISIONS.md); plan is to stop
  committing generated HTML here and deploy via CI instead.
- `query` - frozen. Documents the Python2/Google Scholar methodology used to
  gather the original survey data. Historical record, not meant to be
  extended or modernized as part of this reactivation.

## Contributors

Past contributors (GitHub handles vs. real identities, several still in
contact with Arne) are not derivable from this repo alone - see Arne's
memory entry `dslzoo-contributors` if attribution matters for new docs.

## Docs

- `README.md` - short overview, versioned H1 (semver).
- `CHANGELOG.md` - release history; 0.1.0-0.8.0 is a retroactive
  reconstruction from git log, flagged as such.
- `DECISIONS.md` - why behind every non-obvious choice above.
