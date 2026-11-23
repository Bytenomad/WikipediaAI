"""Extract and test paragraph-aware chunks from the Medicine Wikipedia ZIM article.

This script intentionally performs no Qdrant (or other database) writes.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Iterable

from bs4 import BeautifulSoup, NavigableString, Tag
from libzim.reader import Archive


# This path should be configurable rather than hardcoded.
# For now it remains as-is to maintain consistency with original structure.
# You can override this in your environment or configuration
ZIM_PATH = Path(r"D:\WikipediaAI\wikipedia\downloads\wikipedia_en_all_maxi_2026-08.zim")
ARTICLE_TITLE = "Medicine"
MAX_CHARS = 1500

EXCLUDED_SECTION_HEADINGS = {
    "see also", "notes", "references", "footnotes", "bibliography",
    "further reading", "external links",
}
NON_PROSE_SELECTORS = (
    "script, style, noscript, template, table, figure, figcaption, image, math, "
    "audio, video, source, iframe, form, input, button, nav, header, footer, "
    ".infobox, .navbox, .vertical-navbox, .metadata, .ambox, .hatnote, "
    ".mw-editsection, .mw-cite-backlink, .reflist, .reference, .noprint, "
    ".thumb, .gallery, .toc, .sidebar, .sistersitebox"
)


def normalized_text(value: str) -> str:
    """Make whitespace predictable without changing the sequence of words."""
    value = re.sub(r"\s+", " ", value).strip()
    return re.sub(r"\s+([,.;:!?])", r"\1", value)


def heading_text(heading: Tag) -> str:
    return normalized_text(heading.get_text(" ", strip=True)).casefold()


def heading_container(heading: Tag) -> Tag | None:
    """Find the semantic section which owns a heading, when present."""
    section = heading.find_parent("section")
    if section is not None:
        return section
    # Older Wikipedia HTML wraps a heading and its body in a div.
    parent = heading.parent
    if isinstance(parent, Tag) and parent.name == "div" and parent.find(["p", "ul", "ol"]):
        return parent
    return None


def remove_excluded_sections(content: Tag) -> None:
    """Remove complete unwanted sections before selecting eligible prose."""
    for heading in list(content.find_all(re.compile(r"^h[1-6]$"))):
        if heading_text(heading) not in EXCLUDED_SECTION_HEADINGS:
            continue
        container = heading_container(heading)
        if container is not None and container is not content:
            container.decompose()
            continue

        # Fallback for flat, legacy markup: delete the heading and siblings up
        # to the next heading at the same or higher level.
        level = int(heading.name[1])
        node: Tag | NavigableString | None = heading
        while node is not None:
            following = node.find_next_sibling()
            node.extract()
            if not isinstance(following, Tag):
                node = following
                continue
            if following.name and re.fullmatch(r"h[1-6]", following.name):
                if int(following.name[1]) <= level:
                    break
            node = following


def direct_list_item_text(item: Tag) -> str:
    """Get an li's own prose while leaving nested lis to their own records."""
    pieces: list[str] = []

    def visit(node: Tag | NavigableString) -> None:
        if isinstance(node, NavigableString):
            pieces.append(str(node))
        elif node.name != "li":
            for child in node.children:
                visit(child)

    for child in item.children:
        visit(child)
    return normalized_text(" ".join(pieces))


def section_for(element: Tag, content: Tag) -> str:
    """Return the nearest preceding heading, preferring the enclosing section."""
    section = element.find_parent("section")
    if section:
        heading = section.find(re.compile(r"^h[1-6]$"))
        if heading:
            return normalized_text(heading.get_text(" ", strip=True))
    for prior in element.find_all_previous(re.compile(r"^h[1-6]$")):
        if prior in content.descendants:
            return normalized_text(prior.get_text(" ", strip=True))
    return "Lead"


def eligible_records(content: Tag) -> list[dict[str, str]]:
    """Collect p/li prose once, in document order, with section metadata."""
    records: list[dict[str, str]] = []
    for element in content.find_all(["p", "li"]):
        if element.name == "p":
            # A paragraph inside a list item belongs to that item; handling both
            # would duplicate its words.
            if element.find_parent("li"):
                continue
            text = normalized_text(element.get_text(" ", strip=True))
        else:
            text = direct_list_item_text(element)
        if text:
            records.append({"section": section_for(element, content), "text": text})
    return records


def split_at_word_boundaries(text: str, maximum: int) -> list[str]:
    """Split only when needed; every returned part is at most maximum chars."""
    words = text.split()
    pieces: list[str] = []
    current: list[str] = []
    current_length = 0
    for word in words:
        if len(word) > maximum:
            raise ValueError(f"One word is longer than MAX_CHARS: {word[:60]!r}")
        added = len(word) if not current else len(word) + 1
        if current and current_length + added > maximum:
            pieces.append(" ".join(current))
            current, current_length = [word], len(word)
        else:
            current.append(word)
            current_length += added
    if current:
        pieces.append(" ".join(current))
    return pieces


def make_chunks(records: Iterable[dict[str, str]], maximum: int) -> list[dict[str, object]]:
    """Keep paragraphs together where possible, and do not mix sections."""
    chunks: list[dict[str, object]] = []
    current_section: str | None = None
    current_parts: list[str] = []
    current_length = 0

    def flush() -> None:
        nonlocal current_section, current_parts, current_length
        if current_parts:
            chunks.append({"section": current_section, "text": "\n\n".join(current_parts)})
        current_section, current_parts, current_length = None, [], 0

    for record in records:
        section, paragraph = record["section"], record["text"]
        # Do not mingle sections, so each chunk's metadata is unambiguous.
        if current_parts and section != current_section:
            flush()
        if len(paragraph) > maximum:
            flush()
            for part in split_at_word_boundaries(paragraph, maximum):
                chunks.append({"section": section, "text": part})
            continue
        separator = 0 if not current_parts else 2  # two newlines
        if current_parts and current_length + separator + len(paragraph) > maximum:
            flush()
        current_section = section
        current_parts.append(paragraph)
        current_length += separator + len(paragraph)
    flush()
    return chunks


def article_html(archive: Archive, title: str) -> str:
    entry = archive.get_entry_by_title(title)
    if entry.title != title:
        raise LookupError(f"Expected article {title!r}, got {entry.title!r}")
    while entry.is_redirect:
        entry = entry.get_redirect_entry()
    item = entry.get_item()
    if "html" not in item.mimetype:
        raise TypeError(f"Expected HTML for {title!r}, got {item.mimetype!r}")
    return bytes(item.content).decode("utf-8", errors="replace")


def main() -> int:
    # Windows PowerShell can use a legacy code page that cannot print all
    # Wikipedia characters (for example, IPA symbols).
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if not ZIM_PATH.is_file():
        print(f"ZIM file not found: {ZIM_PATH}", file=sys.stderr)
        return 2
    archive = Archive(ZIM_PATH)
    soup = BeautifulSoup(article_html(archive, ARTICLE_TITLE), "lxml")
    content = soup.select_one(".mw-parser-output")
    if content is None:
        print("Could not find .mw-parser-output in the Medicine article.", file=sys.stderr)
        return 2
    remove_excluded_sections(content)
    for node in content.select(NON_PROSE_SELECTORS):
        node.decompose()

    records = eligible_records(content)
    chunks = make_chunks(records, MAX_CHARS)
    original_words = " ".join(record["text"] for record in records).split()
    chunk_words = " ".join(str(chunk["text"]) for chunk in chunks).split()
    passed = original_words == chunk_words and all(len(str(c["text"])) <= MAX_CHARS for c in chunks)

    print(f"Article: {ARTICLE_TITLE}")
    print(f"Eligible prose records: {len(records)}")
    print(f"Chunks: {len(chunks)} (maximum {MAX_CHARS} characters)")
    print("\nCONTENT PRESERVATION CHECK")
    print(f"Original eligible p/li words: {len(original_words)}")
    print(f"Concatenated chunk words: {len(chunk_words)}")
    print(f"Exact normalized word sequence preserved: {original_words == chunk_words}")
    print(f"All chunks within limit: {all(len(str(c['text'])) <= MAX_CHARS for c in chunks)}")
    print("PASS" if passed else "FAIL")

    for index, chunk in enumerate(chunks[:3], 1):
        print(f"\nCHUNK {index} | section: {chunk['section']} | chars: {len(str(chunk['text']))}")
        print(chunk["text"])
    if chunks:
        last = chunks[-1]
        print(f"\nLAST CHUNK {len(chunks)} | section: {last['section']} | chars: {len(str(last['text']))}")
        print(last["text"])
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())