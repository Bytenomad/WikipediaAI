import unittest
from unittest.mock import MagicMock

from wikipedia_ai.ingestion.category_utils import (
    extract_category_article_titles,
    get_articles_from_category,
)


class TestCategoryUtils(unittest.TestCase):
    def test_extracts_only_direct_article_members_from_zim_links(self):
        html = """
        <div id="mw-subcategories">
          <a href="Category%3AHistory_of_the_United_States">History</a>
        </div>
        <div id="mw-pages">
          <a href="American_Civil_War">American Civil War</a>
          <a href="History%2C_or_The_Style_of_Too_Late_Capitalism">History</a>
          <a href="Category%3AExample">A category, not an article</a>
          <a href="https://en.wikipedia.org/wiki/External">External</a>
          <a href="American_Civil_War">Duplicate</a>
        </div>
        """

        self.assertEqual(
            extract_category_article_titles(html),
            ["American Civil War", "History, or The Style of Too Late Capitalism"],
        )

    def test_category_lookup_accepts_names_without_namespace_prefix(self):
        archive = MagicMock()
        item = MagicMock()
        item.mimetype = "text/html"
        item.content = b'<div id="mw-pages"><a href="Sample_Article">Sample</a></div>'
        entry = MagicMock()
        entry.get_item.return_value = item
        archive.get_entry_by_title.return_value = entry

        self.assertEqual(get_articles_from_category(archive, "History"), ["Sample Article"])
        archive.get_entry_by_title.assert_called_once_with("Category:History")


if __name__ == "__main__":
    unittest.main()
