#!/usr/bin/env python3
"""Build the static Pinetta Nursery site from the files in content/.

Python 3 standard library only. Run from the repository root:

    python3 build.py
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"

CATEGORIES = {
    "business": "Business",
    "homesteading": "Homesteading",
}

TAGS = {
    "greenhouse": "Greenhouse",
    "infrastructure": "Infrastructure",
    "nursery": "Nursery",
    "propagation": "Propagation",
}

NAV = [
    ("for-sale/", "For Sale"),
    ("about-us/", "About"),
    ("food-forests/", "Food Forests"),
    ("contact-form/", "Contact"),
]

POSTS = [
    {
        "slug": "build-greenhouse",
        "title": "Building a greenhouse",
        "date": "2024-05-16T15:20:24-04:00",
        "display_date": "May 16, 2024",
        "image": "greenhouse1.png",
        "width": 1199,
        "height": 537,
        "categories": ["business", "homesteading"],
        "tags": ["greenhouse", "infrastructure", "nursery"],
    },
    {
        "slug": "irrigation",
        "title": "Irrigation",
        "date": "2024-05-16T15:12:23-04:00",
        "display_date": "May 16, 2024",
        "image": "irrigation-workshop.jpg",
        "width": 2149,
        "height": 1872,
        "categories": ["homesteading"],
        "tags": ["infrastructure"],
    },
    {
        "slug": "how-to-start",
        "title": "How to Start",
        "date": "2024-05-16T13:38:25-04:00",
        "display_date": "May 16, 2024",
        "image": "youtubebanner.jpg",
        "width": 2047,
        "height": 1151,
        "categories": ["business"],
        "tags": ["nursery", "propagation"],
    },
]


def rel_prefix(page_dir: str) -> str:
    parts = [part for part in page_dir.split("/") if part]
    return "../" * len(parts)


def href(page_dir: str, target: str) -> str:
    target = target.strip()
    if target in ("", "/", "index.html"):
        prefix = rel_prefix(page_dir)
        return prefix if prefix else "./"
    return rel_prefix(page_dir) + target.lstrip("/")


def asset(page_dir: str, path: str) -> str:
    return rel_prefix(page_dir) + path.lstrip("/")


def render_fragment(text: str, page_dir: str) -> str:
    text = re.sub(
        r"\{\{img:([^}]+)\}\}",
        lambda match: asset(page_dir, "images/" + match.group(1).strip()),
        text,
    )
    text = re.sub(
        r"\{\{url:([^}]+)\}\}",
        lambda match: href(page_dir, match.group(1).strip()),
        text,
    )
    return text.strip()


def plain_text(fragment: str) -> str:
    text = re.sub(r"<[^>]+>", " ", fragment)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def excerpt(text: str, words: int = 55) -> str:
    parts = text.split()
    if len(parts) <= words:
        return text
    return " ".join(parts[:words]) + "…"


def read_content(name: str, page_dir: str) -> str:
    return render_fragment((CONTENT / name).read_text(encoding="utf-8"), page_dir)


def header(page_dir: str, current: str) -> str:
    links = []
    for path, label in NAV:
        current_attr = ' aria-current="page"' if path.rstrip("/") == current.rstrip("/") else ""
        links.append(
            f'<a href="{html.escape(href(page_dir, path))}"{current_attr}>{html.escape(label)}</a>'
        )
    home = href(page_dir, "")
    home_current = ' aria-current="page"' if current == "" else ""
    logo = asset(page_dir, "images/logo.png")
    return f"""<header class="site-header">
  <div class="brand">
    <a class="logo-link" href="{html.escape(home)}"{home_current}><img src="{html.escape(logo)}" alt="Pinetta Nursery" width="533" height="533"></a>
  </div>
  <div class="brand-text">
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
    <nav id="site-nav" class="site-nav" aria-label="Navigation">
      {''.join(links)}
    </nav>
    <p class="tagline">Fruit, Nuts &amp; Flowers for North Florida</p>
  </div>
</header>
<noscript><style>@media (max-width: 781px) {{ .site-nav {{ display: flex !important; flex-direction: column; align-items: center; }} }}</style></noscript>"""


def footer(page_dir: str) -> str:
    home = href(page_dir, "")
    return f"""<footer class="site-footer">
  <p class="site-title"><a href="{html.escape(home)}">Pinetta Nursery</a></p>
  <p class="footer-note">Fruit, Nuts &amp; Flowers for North Florida</p>
</footer>"""


def page_shell(page_dir: str, current: str, title: str, body: str, h1: str = "", center_h1: bool = False, extra_js: str = "") -> str:
    h1_html = ""
    if h1:
        klass = ' class="center"' if center_h1 else ""
        h1_html = f"<h1{klass}>{html.escape(h1)}</h1>\n"
    extra = f'<script src="{html.escape(extra_js)}"></script>\n' if extra_js else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="Fruit, Nuts and Flowers for North Florida. Pinetta Nursery.">
<link rel="icon" href="{html.escape(asset(page_dir, "images/logo.png"))}" type="image/png">
<link rel="apple-touch-icon" href="{html.escape(asset(page_dir, "images/logo.png"))}">
<link rel="stylesheet" href="{html.escape(asset(page_dir, "css/style.css"))}">
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
{header(page_dir, current)}
<main id="main">
{h1_html}{body}
</main>
{footer(page_dir)}
{extra}<script src="{html.escape(asset(page_dir, "js/site.js"))}"></script>
</body>
</html>
"""


def post_by_slug(slug: str) -> dict:
    for post in POSTS:
        if post["slug"] == slug:
            return post
    raise KeyError(slug)


def term_links(page_dir: str, slugs: list[str], mapping: dict[str, str], kind: str) -> str:
    parts = []
    for slug in slugs:
        url = href(page_dir, f"{kind}/{slug}/")
        parts.append(f'<a href="{html.escape(url)}">{html.escape(mapping[slug])}</a>')
    return ", ".join(parts)


def home_cards(page_dir: str) -> str:
    items = []
    for post in POSTS:
        url = href(page_dir, post["slug"] + "/")
        image = asset(page_dir, "images/" + post["image"])
        text = excerpt(plain_text(read_content(post["slug"] + ".html", page_dir)))
        tags = term_links(page_dir, post["tags"], TAGS, "tag")
        items.append(
            f"""<li class="post-card">
  <a href="{html.escape(url)}"><img src="{html.escape(image)}" alt="{html.escape(post["title"])}" width="{post["width"]}" height="{post["height"]}"></a>
  <h2><a href="{html.escape(url)}">{html.escape(post["title"])}</a></h2>
  <p class="excerpt">{html.escape(text)}</p>
  <p class="more"><a href="{html.escape(url)}">read more</a></p>
  <p class="tags">{tags}</p>
</li>"""
        )
    return '<ul class="post-grid">\n' + "\n".join(items) + "\n</ul>"


def archive_cards(page_dir: str, posts: list[dict]) -> str:
    items = []
    for post in posts:
        url = href(page_dir, post["slug"] + "/")
        image = asset(page_dir, "images/" + post["image"])
        text = excerpt(plain_text((CONTENT / f"{post['slug']}.html").read_text(encoding="utf-8")))
        items.append(
            f"""<li class="archive-card">
  <a href="{html.escape(url)}"><img src="{html.escape(image)}" alt="{html.escape(post["title"])}" width="{post["width"]}" height="{post["height"]}"></a>
  <h2><a href="{html.escape(url)}">{html.escape(post["title"])}</a></h2>
  <p class="excerpt">{html.escape(text)}</p>
  <p class="post-date"><a href="{html.escape(url)}"><time datetime="{html.escape(post["date"])}">{html.escape(post["display_date"])}</time></a></p>
</li>"""
        )
    return '<ul class="archive-list">\n' + "\n".join(items) + "\n</ul>"


def post_meta(page_dir: str, post: dict) -> str:
    categories = term_links(page_dir, post["categories"], CATEGORIES, "category")
    tags = term_links(page_dir, post["tags"], TAGS, "tag")
    author = href(page_dir, "author/joe-moraca/")
    return f"""<p class="post-meta">
  <span>Posted</span>
  <time datetime="{html.escape(post["date"])}">{html.escape(post["display_date"])}</time>
  <span>in</span>
  <span>{categories}</span>
  <span>by</span>
  <a href="{html.escape(author)}">Joe Moraca</a>
  <span>Tags: {tags}</span>
</p>"""


def write_page(page_dir: str, html_text: str) -> None:
    if page_dir in ("", "."):
        path = ROOT / "index.html"
    else:
        path = ROOT / page_dir / "index.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html_text, encoding="utf-8")
    print("wrote", path.relative_to(ROOT))


def search_entries() -> list[dict]:
    entries = []
    home_text = plain_text((CONTENT / "home.html").read_text(encoding="utf-8"))
    entries.append({"title": "Pinetta Nursery", "url": "./", "text": home_text})
    for path, label in NAV:
        text = plain_text((CONTENT / f"{path.strip('/')}.html").read_text(encoding="utf-8"))
        entries.append({"title": label, "url": path, "text": text})
    for post in POSTS:
        text = plain_text((CONTENT / f"{post['slug']}.html").read_text(encoding="utf-8"))
        entries.append({"title": post["title"], "url": post["slug"] + "/", "text": text})
    return entries


def build() -> None:
    home_body = read_content("home.html", "") + "\n" + home_cards("")
    write_page(
        "",
        page_shell("", "", "Pinetta Nursery – Fruit, Nuts & Flowers for North Florida", home_body),
    )

    pages = [
        ("for-sale", "For Sale – Pinetta Nursery", "For Sale", True),
        ("about-us", "About Us Page – Pinetta Nursery", "About Us Page", True),
        ("food-forests", "Food Forests – Pinetta Nursery", "Food Forests", True),
        ("contact-form", "Contact Form – Pinetta Nursery", "Contact Form", True),
    ]
    for slug, title, h1, center in pages:
        body = read_content(slug + ".html", slug)
        write_page(slug, page_shell(slug, slug, title, body, h1=h1, center_h1=center))

    for post in POSTS:
        slug = post["slug"]
        body = read_content(slug + ".html", slug) + "\n" + post_meta(slug, post)
        write_page(
            slug,
            page_shell(slug, slug, f"{post['title']} – Pinetta Nursery", body, h1=post["title"]),
        )

    groups = [("category", CATEGORIES, "categories"), ("tag", TAGS, "tags")]
    for kind, mapping, field in groups:
        for slug, label in mapping.items():
            page_dir = f"{kind}/{slug}"
            matched = [post for post in POSTS if slug in post[field]]
            heading = f"{'Category' if kind == 'category' else 'Tag'}: {label}"
            body = archive_cards(page_dir, matched)
            title_prefix = label
            write_page(
                page_dir,
                page_shell(page_dir, "", f"{title_prefix} – Pinetta Nursery", body, h1=heading),
            )

    author_dir = "author/joe-moraca"
    write_page(
        author_dir,
        page_shell(
            author_dir,
            "",
            "Joe Moraca – Pinetta Nursery",
            archive_cards(author_dir, POSTS),
            h1="Author: Joe Moraca",
        ),
    )

    missing = """<h1>404 Page – not the droid you are looking for</h1>
<p>This page could not be found.</p>
<form id="site-search" class="search-form" role="search">
  <label for="search-input">Search</label>
  <input id="search-input" type="search" name="s" placeholder="Search..." required>
  <button type="submit" aria-label="Search">Search</button>
</form>
<ul id="search-results" class="search-results"></ul>
<p><a href="./">Back to the home page</a></p>"""
    not_found = page_shell("", "", "Page not found – Pinetta Nursery", missing, extra_js="js/search-index.js")
    (ROOT / "404.html").write_text(not_found, encoding="utf-8")
    print("wrote 404.html")

    index = search_entries()
    payload = "window.SITE_PAGES = " + json.dumps(index, ensure_ascii=False) + ";\n"
    (ROOT / "js" / "search-index.js").write_text(payload, encoding="utf-8")
    print("wrote js/search-index.js")


def check_local_links() -> None:
    missing = []
    html_files = [ROOT / "index.html", ROOT / "404.html"]
    html_files.extend(ROOT.glob("*/index.html"))
    html_files.extend(ROOT.glob("*/*/index.html"))
    for path in html_files:
        text = path.read_text(encoding="utf-8")
        page_dir = "" if path.name == "404.html" or path.parent == ROOT else str(path.parent.relative_to(ROOT))
        base = ROOT if path.parent == ROOT or path.name == "404.html" else path.parent
        if path.name == "404.html":
            base = ROOT
        for match in re.findall(r'(?:href|src)="([^"]+)"', text):
            if match.startswith(("http://", "https://", "tel:", "mailto:", "#")):
                continue
            target = (base / match).resolve()
            if not target.exists():
                missing.append(f"{path.relative_to(ROOT)} -> {match}")
    if missing:
        raise SystemExit("Missing local files:\n" + "\n".join(missing))
    hotlinks = []
    for path in html_files:
        text = path.read_text(encoding="utf-8")
        if "pinettanursery.com/wp-content" in text or "wp-json" in text:
            hotlinks.append(str(path))
    if hotlinks:
        raise SystemExit("WordPress asset hotlinks remain in " + ", ".join(hotlinks))
    print(f"checked {len(html_files)} pages")


if __name__ == "__main__":
    build()
    check_local_links()
