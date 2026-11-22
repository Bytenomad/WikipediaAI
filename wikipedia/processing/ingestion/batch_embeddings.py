"""Batch embedding support for offline Wikipedia ingestion."""

import time
import requests

OLLAMA_URL = "http://127.0.0.1:11434/api/embed"
EMBEDDING_MODEL = "nomic-embed-text"
VECTOR_DIMENSIONS = 768
BATCH_SIZE = 32

MAX_ATTEMPTS = 3
RETRY_DELAY_SECONDS = 2


def embed_batch(texts):
    """Embed a batch of Wikipedia chunks with transient-error retries."""

    if not texts:
        return []

    if len(texts) > BATCH_SIZE:
        raise ValueError(
            f"Batch contains {len(texts)} texts; maximum is {BATCH_SIZE}"
        )

    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": EMBEDDING_MODEL,
                    "input": texts,
                },
                timeout=300,
            )

            response.raise_for_status()

            embeddings = response.json()["embeddings"]

            if len(embeddings) != len(texts):
                raise ValueError(
                    f"Expected {len(texts)} embeddings, "
                    f"received {len(embeddings)}"
                )

            for index, vector in enumerate(embeddings):
                if len(vector) != VECTOR_DIMENSIONS:
                    raise ValueError(
                        f"Embedding {index} has {len(vector)} dimensions; "
                        f"expected {VECTOR_DIMENSIONS}"
                    )

            return embeddings

        except (requests.Timeout, requests.ConnectionError) as error:
            if attempt == MAX_ATTEMPTS:
                raise

            delay = RETRY_DELAY_SECONDS * (2 ** (attempt - 1))

            print(
                f"Ollama connection failed "
                f"(attempt {attempt}/{MAX_ATTEMPTS}): {error}"
            )
            print(f"Retrying in {delay} seconds...")

            time.sleep(delay)

    raise RuntimeError("Embedding retries exhausted")