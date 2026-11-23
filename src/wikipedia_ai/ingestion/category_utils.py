"""Helpers for extracting direct article members from Wikipedia ZIM categories."""

from __future__ import annotations

import logging
from urllib.parse import unquote, urlsplit

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

_NON_ARTICLE_NAMESPACES = {
    "category", "file", "help", "media", "mediawiki", "module",
    "portal", "special", "talk", "template", "user", "wikipedia",
}


def extract_category_article_titles(category_html: str) -> list[str]:
    """Return direct article-member titles from a rendered ZIM category page.

    ZIM-rendered Wikipedia links use relative paths (for example,
    ``American_Civil_War``), unlike the ``/wiki/...`` URLs used on Wikipedia.
    Restrict extraction to ``#mw-pages`` so subcategory links aren't imported
    as articles.
    """
    soup = BeautifulSoup(category_html, "lxml")
    page_list = soup.select_one("#mw-pages")
    if page_list is None:
        logger.warning("Category HTML has no #mw-pages article listing")
        return []

    titles: list[str] = []
    seen: set[str] = set()
    for link in page_list.find_all("a", href=True):
        parsed = urlsplit(link["href"].strip())
        if parsed.scheme or parsed.netloc:
            continue

        path = parsed.path
        if path.startswith("/wiki/"):
            path = path[len("/wiki/"):]
        elif path.startswith("./"):
            path = path[2:]
        path = path.strip("/")
        if not path:
            continue

        title = unquote(path).replace("_", " ").strip()
        namespace, separator, _ = title.partition(":")
        if separator and namespace.casefold() in _NON_ARTICLE_NAMESPACES:
            continue
        if title and title not in seen:
            titles.append(title)
            seen.add(title)

    return titles


def get_articles_from_category(zim_archive, category_name: str) -> list[str]:
    """Look up a category entry and return its direct article members."""
    formatted_category = (
        category_name
        if category_name.startswith("Category:")
        else f"Category:{category_name}"
    )
    try:
        category_entry = zim_archive.get_entry_by_title(formatted_category)
        item = category_entry.get_item()
        if "html" not in item.mimetype:
            logger.warning("Category %r is not HTML (%s)", formatted_category, item.mimetype)
            return []

        html = bytes(item.content).decode("utf-8", errors="replace")
        articles = extract_category_article_titles(html)
        logger.info("Found %d direct articles in category %r", len(articles), formatted_category)
        return articles
    except Exception as exc:
        logger.warning("Could not retrieve category %r: %s", formatted_category, exc)
        return []
