import sys
import pytest
import numpy
from qdrant_client import QdrantClient


def test_python_environment():
    assert sys.version_info[:2] == (3, 13)
    assert "ingestion" in sys.prefix.lower()
    assert numpy.__version__ == "2.5.4"
    assert QdrantClient is not None


def test_basic_calculation():
    assert sum([10, 20, 30]) == 60


if __name__ == "__main__":
    print("Python:", sys.version)
    print("Executable:", sys.executable)
    print("pytest:", pytest.__version__)
    print("NumPy:", numpy.__version__)
    print("ENVIRONMENT: PASS")
