# Wikipedia AI Ingestion Development History

This directory contains historical development files, experimental implementations, and backup versions of the ingestion components.

## Purpose

This directory serves as a development history repository containing:
- Alternative implementation approaches
- Backup copies of previous versions  
- Experimental code variants
- Debugging scripts and test programs

## Structure

**Active Code**: `src/wikipedia_ai/ingestion/`
The actual working code and current implementation lives in the main source package.

**Historical Files**: `wikipedia/processing/ingestion/history/`
All files in this subdirectory represent historical versions, alternative approaches, or backup implementations that should not be used as the active system. These files are preserved for reference during development and debugging.

Files in this directory are **NOT** part of the active system:
- `*_before_*` files: Versions before certain features or fixes 
- `*_backup*` or `*_v2*` files: Alternative implementation paths
- Test and debugging scripts with historical implementations

## Note for Developers

When examining this directory, always refer to the corresponding files in `src/wikipedia_ai/ingestion/` for the current, tested, and recommended implementation.