# CLAUDE.md - Robotics DSL Zoo

Companion artifact to two publications (full citations in README.md /
PROVENANCE.md once it exists): SIMPAR 2014 and JOSER 2016 surveys on DSLs in
robotics, both authored by Arne. Both cite the live
`corlab.github.io/dslzoo` URL. **Any change that could break that citable
URL needs to be called out explicitly, never silently.**

**Rigor scope:** scientific rigor (stable cited references, bibliography
intact with history and manual classification) binds what lands on or is
served from `corlab`. `origin` is a working copy, not a reference target;
no such rigor needed there. Detail: DECISIONS.md, 2026-10-04.

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

## Tags - scientific reference, never move

`joser16*` and `legacy-*` pin the states the publications and the live site
rest on (list and rationale: DECISIONS.md, 2026-10-02). **On `corlab`, never
move, delete or re-create them; a new state gets a new tag.** Why: `corlab` is
the only target of scientific references, and a published citation must
resolve to exactly the cited state years later - a moved tag silently changes
what the citation refers to, and readers cannot detect it. The rule binds only
once a tag is on `corlab`; before that, a tag on `origin` may still be fixed
(re-created), after which the identical object goes to `corlab`. Pushing to
`corlab` only with explicit go-ahead, always by explicit refspec per tag,
never `--tags` or `--follow-tags`. Version tags (`vX.Y.Z`) go to `corlab` only
when their commit is on a `corlab` branch, never pointing into fork-only
history.

## Generator (private, separate repo)

Generator recovery, reconstruction and its docs live in the private repo
`norro/dslzoo-gen` (read its CLAUDE.md there).
**Nothing from it - code, docs, history, file names, findings - goes into this
public repo.** A revamped generator moves here only as a clean, reviewed
import by Arne's explicit go-ahead, never by copying the private history.

## Contributors

Past contributors (GitHub handles vs. real identities, several still in
contact with Arne) are not derivable from this repo alone - see Arne's
memory entry `dslzoo-contributors` if attribution matters for new docs.

## Docs

- `README.md` - short overview, versioned H1 (semver).
- `CHANGELOG.md` - release history; 0.1.0-0.8.0 is a retroactive
  reconstruction from git log, flagged as such.
- `DECISIONS.md` - why behind every non-obvious choice above.
