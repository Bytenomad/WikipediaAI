"""
Ingestion package for Wikipedia AI system.
"""

# Import core components for easy access
from .article_ingestion import ingest_article, ConfirmedUnsupportedArticle
from .batch_embeddings import embed_batch
from .chunking import make_chunks, eligible_records
from .qdrant_batch import upload_batch
from .progress_tracking import (
    register_article, get_article, start_article, 
    complete_article, fail_article, is_completed, 
    exclude_article, is_excluded
)
from .config import configuration_id, configuration_details
from .enumeration import enumerate_articles
from .cleanup import remove_stale_chunks, remove_article_chunks

# Export constants
from .target import ACTIVE_COLLECTION, TEST_COLLECTION