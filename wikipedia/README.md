# Wikipedia AI Data Directory

This directory contains runtime data and development artifacts for the Wikipedia AI system.

## Structure

- `processing/ingestion/` - Contains ingestion components including:
  - **Active code**: `src/wikipedia_ai/ingestion/` (main implementation)
  - **Historical files**: Moved to dedicated `history/` subdirectory for reference
- `downloads/` - Directory for Wikipedia ZIM archives (if present)

## Important Note

The primary working code of this system is located in `src/wikipedia_ai/ingestion/`. The `processing/ingestion/` directory has been reorganized to separate:
- Current, tested implementation (in the main source)
- Historical development versions (now in `history/` subdirectory)

Always refer to the main package in `src/wikipedia_ai/ingestion/` for current, tested, and recommended implementation.