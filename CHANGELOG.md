# Changelog

All notable changes to the Robotics DSL Zoo bib source are documented here.
Versioning follows [semver](https://semver.org/).

> **Note on 0.1.0-0.8.0:** the project never used version numbers before this
> file existed. Those entries are reconstructed retroactively from git history
> (`git log`) on 2026-09-28, grouped by the date each change actually landed on
> `master`. They approximate the real history but are not authoritative
> releases - see [DECISIONS.md](DECISIONS.md).

## [Unreleased]

### Added
- Citation tags `joser16-site`, `legacy-2015-12-22-query`,
  `legacy-2020-05-08-bib` and `legacy-2020-05-08-site` pushed to `corlab`
  (step 1 of the plan complete). Identical tag objects on both remotes; no
  branch on `corlab` changed. `v0.8.2` stays on the fork.

### Changed
- Never-move rule for the citation tags scoped to `corlab` (CLAUDE.md,
  DECISIONS.md). The three `legacy-*` tags were re-created on the fork with
  the same targets and a message without the fork-only plan pointer, ahead of
  their push to `corlab`.

## [0.8.2] - 2026-10-02

### Added
- `CLAUDE.md` documenting remote/branch conventions for future sessions.
- `docs/RESTRUCTURING-PLAN.md`: draft lean restructuring plan (rev 3, eight
  steps) from a read-only investigation: fixed citation names, backup and
  tags, provenance docs, bibliography hygiene, a new Python generator, CI
  deploy via Pages.
- Annotated tags on the fork pinning the cited states (step 1 of the plan):
  `legacy-2020-05-08-site`, `legacy-2020-05-08-bib`, `legacy-2015-12-22-query`,
  `joser16-site`. corlab is untouched; `joser16` is unchanged.
- `.gitattributes` (`* text=auto eol=lf`) to keep line endings consistent; the
  index was already LF, so no blob changes.

### Fixed
- `dslzoo.bib`, four syntax defects (step 4 of the plan): missing comma after
  `year` in `Araiza-Illan2016` and after `url` in `Ciccozzi2016Adopting`;
  duplicate `booktitle` in `hochgeschwender2014declarative` (identical value,
  second copy removed); duplicate `keywords` in `Detzner2019Novel` (merged into
  one field). Before: pybtex aborted on the file, bibtexparser silently read
  142 of 144 entries. After: both read all 144 and agree on every field.
- `dslzoo.bib`, vocabulary: `zoo-ap-subdomains` tokens "Error and Exeption
  Handling" (8 entries) and "Control of Handling and Events" (1 entry) now use
  the canonical names "Error and Exception Handling and Fault Tolerance" and
  "Control and Handling of Events". The old site silently left these 9 entries
  off those pages.

### Changed
- `dslzoo.bib` normalised: one blank line between entries, 2-space indent,
  `name = value` spacing, no trailing whitespace, LF, `, ` between vocabulary
  tokens; entry types and field names lower-case; every entry ends its last
  field with a comma. No content change beyond the vocabulary fix above
  (verified with two parsers). The whitespace-only part is its own commit, so
  `git blame --ignore-rev` can skip it.
- Splitting `dslzoo.bib` is on the roadmap as step 5a of the plan.
- `master` renamed to `main`.
- Restructuring plan approved: consolidate bib source, generator, and docs
  into `main`; stop committing generated HTML; build and deploy to
  `gh-pages` via CI instead. Documented as an explicit tooling-generation
  break (2014-2020 vs. 2026) rather than a silent rewrite, since this repo
  is a citable academic artifact - see `DECISIONS.md` and the upcoming
  `PROVENANCE.md`.
- Scope widened from "Arne's own fork" to `corlab/dslzoo` directly, the repo
  the two associated publications actually cite - confirmed admin access.

## [0.8.1] - 2026-09-28

### Changed
- Reactivated the project: fast-forwarded `norro/dslzoo` (this fork) to match
  upstream `corlab/dslzoo` (was 39 commits behind on `master`, 9 on
  `gh-pages`, no unique fork commits).
- Established a feature-branch workflow (`ai/dslzoo-refresh`); `master` stays
  untouched until changes are reviewed and cherry-picked.
- Added this changelog, `DECISIONS.md`, and a versioned README header.

### Known issues
- The site generator (bib -> HTML) is missing entirely - not present in any
  branch, fork, or corlab-org repository. The HTML in `gh-pages` can no
  longer be regenerated from `dslzoo.bib` until a replacement is built.

## [0.8.0] - 2020-05-08

### Added
- Specification Patterns for Robotic Missions reference (Claudio Menghi, PR #20).

### Fixed
- URL on the `menghi2019Specification` entry.

## [0.7.0] - 2020-04-06

### Added
- New bibliography entry (Sergio Garcia Gonzalo, PR #19).

### Fixed
- Typos in bib entries.

## [0.6.1] - 2019-12-04

### Added
- Detzner 2019 "Novel..." entry.

## [0.6.0] - 2019-09-15

### Added
- Six community pull requests merged in one backlog-clearing pass, most of
  which had been open since late 2018:
  - HRI-testing entry (emassey2)
  - Model-driven code-generator-composition entry (Zahid)
  - Model-based-framework entries (Khoi)
  - Saglietti & Meitner entry, plus website/tool field cleanup (Minh Nguyen)
  - A journal entry (kerikon)
  - Gritzner & Greenyer 2018 entry, plus a syntax fix (Debaraj Barua)

### Changed
- Naming-convention cleanup across bib keys (xwavex).

## [0.5.0] - 2019-03-21

### Added
- CoBlox entry (davidcshepherd, PR #17) - first change to land after roughly
  two and a half years of inactivity.

## [0.4.0] - 2016-04-14

### Changed
- Bibliography refreshed against the JOSER "Survey on Domain-Specific
  Languages in Robotics" query results.
- ICRA 2015 entry added.
- Title formatting cleanup (subscript/superscript issues).

## [0.3.2] - 2015-09-11

### Added
- LRP publication (Johan Fabry).

### Fixed
- A BibTeX entry error.

## [0.3.1] - 2015-05-13

### Added
- SIMPAR 2014 "Structured Design and Development of DSLs in Robotics" paper
  (Sebastian Wrede, PR #5).

## [0.3.0] - 2015-03-12

### Added
- IROS 2013 deployment-DSL entry, DSLRob paper details, RPSL/SIMPAR paper
  (nicoh, PRs #3-#4).

## [0.2.1] - 2015-01-14

### Added
- Custom zoo-specific BibTeX fields (subdomain, phase, tool).
- First community entry (Lotz et al. 2014).

### Changed
- Cleanup: use `keywords` field instead of `mendeley-tags`.

## [0.2.0] - 2015-01-08

### Added
- Initial `dslzoo.bib` source file.

## [0.1.0] - 2014-11-26

### Added
- Initial repository scaffold and dummy landing page (swrede, Arne Nordmann).
