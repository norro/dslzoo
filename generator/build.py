"""Build the Robotics DSL Zoo site from dslzoo.bib.

Usage: build.py [OUT_DIR]    (default: site; files are overwritten, nothing is deleted)

Inputs: dslzoo.bib, docs/STABLE-REFERENCES.md, generator/vocabulary.toml,
generator/redirects.toml, generator/templates, generator/static. The build fails if the number of parsed
entries differs from the number of entries in the file, so no publication is
silently dropped. Every other finding about the data is printed as a warning.
"""
import collections
import datetime
import pathlib
import re
import shutil
import sys
import tomllib
import urllib.parse
from dataclasses import dataclass

import markdown
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from pybtex.database import parse_file
from pybtex.exceptions import PybtexError
from pylatexenc.latex2text import LatexNodes2Text

ROOT = pathlib.Path(__file__).resolve().parent.parent
HERE = ROOT / "generator"

# Title words that say nothing about a language; everything else of 4+ letters counts.
STOP_WORDS = set(
    "about also based been between both can does each from have into more most only other "
    "over such than that their them then there these they this through toward towards "
    "unified upon using very were what when where which while will with within without your".split()
)


@dataclass
class Term:
    kind: str
    name: str
    description: str = ""
    note: str = ""
    page: str | None = None  # None: not in the vocabulary, so no page
    count: int = 0


@dataclass
class Kind:
    key: str
    label: str
    noun: str
    nav: str
    heading: str
    field: str
    group_by: str
    page: str
    intro: str
    terms: list[Term]


@dataclass
class Entry:
    key: str
    title: str
    authors: str
    year: int | None
    venue: str
    link: str | None
    website: str | None
    download: str | None
    formalism: str
    tool: str
    terms: dict[str, list[Term]]

    def names(self, kind):
        return [t.name for t in self.terms[kind]]


@dataclass
class Row:
    entry: Entry
    anchor: bool  # carries the #key anchor; only the first occurrence on a page does


@dataclass
class Group:
    term: Term | None  # None: entries without a known term of the grouping kind
    rows: list[Row]


_latex = LatexNodes2Text()
warnings = []


def warn(message):
    warnings.append(message)
    print(f"warning: {message}", file=sys.stderr)


def slugify(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def clean(text):
    return " ".join(_latex.latex_to_text(text or "").split())


def url_field(key, field, value):
    """Return value as an http(s) URL, or None (with a warning) for anything else."""
    value = re.sub(r"\\([_%&#$])", r"\1", value.strip().strip("{}")).strip()
    if not value:
        return None
    if urllib.parse.urlparse(value).scheme not in ("http", "https"):
        warn(f"{key}: {field} is not an http(s) URL and is not linked: {value!r}")
        return None
    return value


def load_vocabulary():
    data = tomllib.loads((HERE / "vocabulary.toml").read_text(encoding="utf-8"))
    kinds = {}
    for key, spec in data.items():
        terms = [
            Term(key, t["name"], t["description"], t.get("note", ""), page=f"{slugify(t['name'])}-{key}.html")
            for t in spec["terms"]
        ]
        kinds[key] = Kind(
            key, spec["label"], spec["noun"], spec["nav"], spec["heading"], spec["field"],
            spec["group_by"], spec["page"], spec["intro"], terms,
        )
    return kinds


def load_entries(path, kinds):
    text = path.read_text(encoding="utf-8")
    expected = len(re.findall(r"^\s*@(?!(?:comment|string|preamble)\b)\w+\s*[{(]", text, re.I | re.M))
    try:
        bib = parse_file(str(path), bib_format="bibtex", encoding="utf-8")
    except PybtexError as error:
        sys.exit(f"{path.name}: {error}")
    if len(bib.entries) != expected:
        sys.exit(f"entry count mismatch: {expected} entries in {path.name}, {len(bib.entries)} parsed")

    by_name = {k: {t.name: t for t in kind.terms} for k, kind in kinds.items()}
    entries = []
    for key, raw in bib.entries.items():
        f = raw.fields
        people = raw.persons.get("author") or raw.persons.get("editor") or []
        names = [
            clean(" ".join(p.first_names + p.middle_names + p.prelast_names + p.last_names + p.lineage_names))
            for p in people
        ]
        names = ["et al." if n == "others" else n for n in names]
        title = clean(f.get("title", ""))
        year = int(f["year"]) if f.get("year", "").strip().isdigit() else None
        if not title or not names or year is None:
            warn(f"{key}: title, author or year missing or unreadable")

        doi = f.get("doi", "").strip()
        link = f"https://doi.org/{urllib.parse.quote(doi, safe='/:()')}" if doi else url_field(key, "url", f.get("url", ""))

        terms = {}
        for kind in kinds.values():
            tokens = [" ".join(t.split()) for t in f.get(kind.field, "").split(",")]
            terms[kind.key] = [by_name[kind.key].get(t) or Term(kind.key, t) for t in tokens if t]
            for t in terms[kind.key]:
                if t.page is None:
                    warn(f"{key}: {t.name!r} in {kind.field} is not in the vocabulary, so it has no page")
        if not terms["phase"]:
            warn(f"{key}: no development phase, so it is on no phase page")
        if not terms["subdomain"]:
            warn(f"{key}: no subdomain, so it is on no subdomain page")

        entries.append(Entry(
            key=key,
            title=title,
            authors=", ".join(names),
            year=year,
            venue=clean(f.get("journal") or f.get("booktitle") or f.get("howpublished") or ""),
            link=link,
            website=url_field(key, "zoo-website", f.get("zoo-website", "")),
            download=url_field(key, "zoo-download", f.get("zoo-download", "")),
            formalism=clean(f.get("zoo-formalism", "")),
            tool=clean(f.get("zoo-tool", "")),
            terms=terms,
        ))
    entries.sort(key=lambda e: e.key.lower())

    for kind in kinds.values():
        for term in kind.terms:
            term.count = sum(term.name in e.names(kind.key) for e in entries)
    return entries


def chart(title, items):
    """items: (label, href, count, tick); share is relative to the largest count."""
    top = max((count for _, _, count, _ in items), default=0) or 1
    return {
        "title": title,
        "items": [{"label": l, "href": h, "count": c, "tick": t, "share": c / top} for l, h, c, t in items],
    }


def year_chart(entries, years):
    counts = collections.Counter(e.year for e in entries)
    return chart("Publications per year", [(str(y), None, counts[y], y % 5 == 0) for y in years])


def term_chart(kind, entries):
    counts = collections.Counter(n for e in entries for n in e.names(kind.key))
    return chart(f"Publications per {kind.noun}", [(t.name, t.page, counts[t.name], False) for t in kind.terms])


def groups(kind, term, entries, kinds):
    """The entries of a term, grouped by the kind named in kind.group_by."""
    by = kinds[kind.group_by]
    members = [e for e in entries if term.name in e.names(kind.key)]
    seen = set()

    def rows(items):
        out = []
        for e in items:
            out.append(Row(e, e.key not in seen))
            seen.add(e.key)
        return out

    result = [Group(g, rows(items)) for g in by.terms if (items := [e for e in members if g.name in e.names(by.key)])]
    rest = [e for e in members if not any(t.page for t in e.terms[by.key])]
    if rest:
        result.append(Group(None, rows(rest)))
    return members, result


def word_cloud(entries, limit=40):
    counts = collections.Counter(
        w for e in entries for w in set(re.findall(r"[a-z]{4,}", e.title.lower())) if w not in STOP_WORDS
    )
    top = counts.most_common(limit)
    low, high = top[-1][1], top[0][1]
    return [(w, c, (c - low) / (high - low or 1)) for w, c in sorted(top)]


def main(out_dir):
    out = pathlib.Path(out_dir).resolve()
    kinds = load_vocabulary()
    entries = load_entries(ROOT / "dslzoo.bib", kinds)
    years = [e.year for e in entries if e.year]
    year_range = range(min(years), max(years) + 1)

    env = Environment(
        loader=FileSystemLoader(HERE / "templates"), autoescape=True,
        undefined=StrictUndefined, trim_blocks=True, lstrip_blocks=True,
    )
    nav = (
        [("Home", "index.html")]
        + [(k.nav, k.page) for k in kinds.values()]
        + [("Index", "all.html"), ("Contribute", "contribute.html"), ("Versions", "versions.html")]
    )
    env.globals.update(
        kinds=kinds, nav=nav, count=len(entries), built=datetime.datetime.now(datetime.timezone.utc).date().isoformat(),
        first_year=year_range.start, last_year=year_range.stop - 1,
    )

    out.mkdir(parents=True, exist_ok=True)
    shutil.copytree(HERE / "static", out, dirs_exist_ok=True)
    written = []

    def render(page, template, **context):
        context.setdefault("active", page)
        context.setdefault("title", None)
        (out / page).write_text(env.get_template(template).render(page=page, **context), encoding="utf-8")
        written.append(page)

    render("index.html", "home.html", cloud=word_cloud(entries))
    render("all.html", "all.html", title="Index", rows=[Row(e, True) for e in entries])
    render("contribute.html", "contribute.html", title="Contribute")
    versions = markdown.markdown(
        (ROOT / "docs" / "STABLE-REFERENCES.md").read_text(encoding="utf-8"), extensions=["tables", "fenced_code"]
    )
    render("versions.html", "versions.html", title="Versions", body=versions)

    for kind in kinds.values():
        render(
            kind.page, "overview.html", title=kind.nav, kind=kind,
            charts=[term_chart(kind, entries), year_chart(entries, year_range)],
        )
        by = kinds[kind.group_by]
        for term in kind.terms:
            members, grouped = groups(kind, term, entries, kinds)
            render(
                term.page, "category.html", title=f"{term.name} ({kind.label.lower()})", active=kind.page,
                kind=kind, term=term, by=by, groups=grouped,
                charts=[term_chart(by, members), year_chart(members, year_range)],
            )

    redirects = tomllib.loads((HERE / "redirects.toml").read_text(encoding="utf-8"))
    for old, new in redirects.items():
        if old in written:
            sys.exit(f"redirects.toml: {old} is a generated page and cannot be a redirect")
        if new not in written:
            sys.exit(f"redirects.toml: target {new} of {old} is not a generated page")
    for old, new in redirects.items():
        render(old, "redirect.html", title="Moved", target=f"./{new}")

    print(f"{len(entries)} entries, {len(written) - len(redirects)} pages and {len(redirects)} redirects in {out}, {len(warnings)} warnings")


if __name__ == "__main__":
    if len(sys.argv) > 2:
        sys.exit(__doc__)
    main(sys.argv[1] if len(sys.argv) == 2 else ROOT / "site")
