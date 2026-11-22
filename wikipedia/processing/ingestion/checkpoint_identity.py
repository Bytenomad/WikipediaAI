"""Deterministic configuration-specific ingestion checkpoint names."""

import re


PREFIX = "wikipedia_staging_v1_gen_"


def checkpoint_name(configuration_id):
    """Return an isolated checkpoint name for a configuration fingerprint."""

    if not isinstance(configuration_id, str):
        raise ValueError("Configuration ID must be a string")

    if not re.fullmatch(r"[0-9a-f]{64}", configuration_id):
        raise ValueError(
            "Configuration ID must be 64 lowercase hexadecimal characters"
        )

    return PREFIX + configuration_id
