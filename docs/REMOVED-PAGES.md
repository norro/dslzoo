# Removed legacy pages and how to bring them back

The generator (`generator/`) does not build six pages of the legacy site; each is a
redirect stub instead (`generator/redirects.toml`). Why: DECISIONS.md, 2026-10-04. This
file records what the pages were, where the originals are, and what restoring one
involves, so the step can be taken later without redoing the investigation.

## The six pages

| Legacy page | What it showed | Redirects to |
|---|---|---|
| `components-subdomain.html` | heading and an empty table | `architectures-and-programming-subdomain.html` |
| `composition-subdomain.html` | heading and an empty table | same |
| `computation-subdomain.html` | heading and an empty table | same |
| `communication-subdomain.html` | heading and an empty table | same |
| `coordination-subdomain.html` | heading and a flat table of six entries | same |
| `domain-examples.html` | a narrative that derives subdomains from the RoboCup@Work Precision Placement Test, with the image `images/pptPlatform.jpg` | `subdomains.html` |

The redirect targets are the maintainers' to change; they are a proposal.

## Where the originals are

All six pages and the image are in the tags `legacy-2020-05-08-site` (`1bc823f`, tip of
`gh-pages`) and `joser16-site` (`fd34a51`), on both remotes:

```
git show legacy-2020-05-08-site:coordination-subdomain.html
git show legacy-2020-05-08-site:domain-examples.html
git show legacy-2020-05-08-site:images/pptPlatform.jpg > pptPlatform.jpg
```

## What the pages rested on

They are leftovers of 2014 and 2015, not output of the 2020 generator: `components`,
`coordination` and `domain-examples` date from the first generated site (2014-12-10,
`6ffcb65`), the other three from 2015-09-16 (`9b05fa3`), and none changed after
2015-09-17 (`5c78537`). Consequences, checked against `legacy-2020-05-08-bib`:

- The five subdomain pages belong to the 2015 classification (a different set of subdomains
  than the nine of the 2020 overview). Four tables are empty. The `coordination` table lists
  `de2012scripting`, `dai2002specifying`, `dantam2011motion`, `loetzsch2006xabsl`,
  `Angerer2012` and `Buchmann2013`; in the 2020 bibliography none of them carries the term
  `Coordination` (five have `Architectures and Programming`, `Buchmann2013` has an empty
  `zoo-subdomains`). So restoring the page from the bibliography would not reproduce it.
- Today's bibliography still holds terms of that classification that have no page in the
  generated site (the build warns for each): `components` (`Akim2010`, `Romero2011`),
  `Coordination` (`garcia2019high`), `transformation` (`Frigerio2011`, `Laet2012`),
  `robot-structure` (`Frigerio2011`), `perception` (`Hochgeschwender2013`),
  `manipulation-and-grasping` (`Schneider2014`). The legacy index linked `components` and
  `coordination` to the stale pages.
- `domain-examples.html` links nine targets, six of which never existed among the 41
  pages of the last legacy site (404 there already): `architecture`, `perception`,
  `reasoning-and-planning`, `robot-structure`, `transformation` and
  `manipulation-and-grasping`, each as `-subdomain.html`.

## Inbound links

Only three legacy pages linked to the six: `all.html` (the two subdomain pages above),
`domain-examples.html` (to `components` and `coordination`) and `contribute.html` (twice to
`domain-examples.html`, in its "Content-wise" requirement). The main navigation linked none.
The generated `contribute.html` keeps that requirement verbatim and still links
`./domain-examples.html`, which is the redirect stub today; a restored page makes that link
work again without an edit.

## Restoring a subdomain page

1. Add a term to the `subdomain` kind in `generator/vocabulary.toml`
   (`[[subdomain.terms]]`, with `name` and `description`; the legacy pages had no
   description). The page name is the slug of the name plus `-subdomain.html`, so
   `Components`, `Composition`, `Computation`, `Communication` and `Coordination`
   re-create the legacy file names.
2. Delete its line in `generator/redirects.toml`; the build fails if a name is both a
   generated page and a redirect.
3. Make the bibliography spell the term exactly as the vocabulary does (matching is
   exact and case-sensitive): `components` would have to become `Components`. Classification
   is manual work of the maintainers and a spelling change touches `dslzoo.bib` (see the
   token spelling decisions of 2026-10-02 in DECISIONS.md).
4. Everything else follows from the vocabulary: the subdomain overview and its chart, the
   counts on the start page, the term list in the BibTeX template on `contribute.html`, the
   page itself (entries grouped by phase, entries without a phase in a separate group).

A new subdomain is a change to the classification the surveys use, not only to the site.

## Restoring the domain example

1. Take the body text from `legacy-2020-05-08-site:domain-examples.html` into a new
   `generator/templates/domain-examples.html` that extends `base.html`; copy
   `images/pptPlatform.jpg` (950 KB, shown at 25 percent width) to
   `generator/static/images/`.
2. Render it in `build.py` (one `render(...)` call) and link it, for example from the
   subdomain overview or the navigation.
3. Repoint the six dead links and the `#key` anchors to current pages (`all.html#<key>`
   carries every key as an anchor); the text describes the 2015 subdomains and needs a
   decision: keep as history or rewrite for the nine current ones.
4. Delete its line in `generator/redirects.toml`.
5. Rights: the plan (docs/RESTRUCTURING-PLAN.md, section 6) lists one image of unknown
   provenance as unresolved; this is the only picture of the legacy site besides the icons,
   check whether it is the one before publishing it again.

## After restoring any page

Build (`generator/build.py`), look at the page, add a DECISIONS.md entry. A restored page
replaces its stub; copies of the redirect that search engines or browsers cached may linger
for a while.
