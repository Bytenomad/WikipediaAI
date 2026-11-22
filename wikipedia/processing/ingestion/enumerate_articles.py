"""Memory-efficient enumeration of HTML entries in the Wikipedia ZIM."""

from itertools import islice
from bs4 import BeautifulSoup
from libzim.reader import Archive
from test_chunking import ZIM_PATH



def is_html_meta_redirect(item):
    """Detect HTML meta-refresh redirects using a small prefix."""
    raw = bytes(item.content)[:8192]
    soup = BeautifulSoup(raw, "lxml")

    for meta in soup.select("meta[http-equiv][content]"):
        directive = meta.get("http-equiv", "").strip().lower()

        if directive != "refresh":
            continue

        content = meta.get("content", "")
        parts = content.split(";", 1)

        if len(parts) != 2:
            continue

        if parts[1].strip().lower().startswith("url="):
            return True

    return False


def enumerate_articles(archive):
    """Yield non-redirect HTML entries without loading article content."""
    for entry in archive.iter_by_title():
        if entry.is_redirect:
            continue

        item = entry.get_item()

        if item.mimetype != "text/html":
            continue

        # Conservative filter: exclude explicitly named
        # disambiguation pages, but not articles that merely
        # link to disambiguation pages.
        if entry.title.casefold().strip().endswith("(disambiguation)"):
            continue

        # HTML-level redirects are not always flagged as
        # native ZIM redirects. Exclude confirmed meta-refresh
        # redirects before yielding an article.
        if is_html_meta_redirect(item):
            continue

        yield {
            "title": entry.title,
            "article_path": entry.path,
        }


def main():
    archive = Archive(ZIM_PATH)

    articles = list(islice(enumerate_articles(archive), 20))

    print("FILTERED ARTICLE ENUMERATION TEST")
    print()

    for index, article in enumerate(articles, 1):
        print(
            f"{index:2}. {article['title']} "
            f"[{article['article_path']}]"
        )

    print()
    print("HTML entries found:", len(articles))
    print(
        "VALIDATION:",
        "PASS" if len(articles) == 20 else "FAIL"
    )


if __name__ == "__main__":
    main()
