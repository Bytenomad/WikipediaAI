@echo off
REM Batch script to run Wikipedia AI ingestion with proper environment

echo Setting up Wikipedia AI ingestion environment...

REM Set Qdrant connection if needed (modify this as appropriate for your setup)
REM set QDRANT_HOST=your-qdrant-host
REM set QDRANT_PORT=6333

REM Navigate to the project directory
cd /d C:\WikipediaAI

echo Installing/Updating package...
pip install -e .

echo Running ingestion verification test...
python wikipedia\processing\ingestion\final_verification.py

echo If verification passed, you can now run:
echo python wikipedia\processing\ingestion\ingest_article.py "Article Title"

pause