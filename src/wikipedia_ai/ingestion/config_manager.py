"""
Configuration management for Wikipedia AI ingestion system.

This module centralizes configuration handling with validation and 
environment awareness.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict


logger = logging.getLogger(__name__)


@dataclass
class WikipediaConfig:
    """Data class representing the main configuration for Wikipedia ingestion."""
    
    # ZIM file settings
    zim_path: str
    zim_filename: str
    
    # Embedding settings  
    embedding_model: str
    vector_dimensions: int
    
    # Qdrant settings
    collection_name: str
    qdrant_host: str
    qdrant_port: int
    
    # Processing settings
    batch_size: int
    chunk_max_chars: int
    chunking_source_hash: str
    
    # Source hashes for tracking changes  
    embedding_source_hash: str
    qdrant_upload_source_hash: str
    enumeration_source_hash: str
    
    # Other settings
    vector_schema_version: str
    enumeration_method: str


class ConfigManager:
    """Centralized configuration manager with validation."""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize the configuration manager.
        
        Args:
            config_file: Optional path to a configuration file (JSON format)
        """
        self._config_file = config_file
        self._config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from environment variables and/or file."""
        # Default values
        config = {
            'zim_path': os.environ.get('ZIM_PATH', ''),
            'zim_filename': '',
            'embedding_model': os.environ.get('EMBEDDING_MODEL', 'nomic-embed-text'),
            'vector_dimensions': int(os.environ.get('VECTOR_DIMENSIONS', '768')),
            'collection_name': os.environ.get('COLLECTION_NAME', 'wikipedia_articles'),
            'qdrant_host': os.environ.get('QDRANT_HOST', 'localhost'),
            'qdrant_port': int(os.environ.get('QDRANT_PORT', '6333')),
            'batch_size': int(os.environ.get('BATCH_SIZE', '10')),
            'chunk_max_chars': int(os.environ.get('CHUNK_MAX_CHARS', '1500')),
            'chunking_source_hash': '',
            'embedding_source_hash': '',
            'qdrant_upload_source_hash': '', 
            'enumeration_source_hash': '',
            'vector_schema_version': os.environ.get('VECTOR_SCHEMA_VERSION', 'wikipedia-v4'),
            'enumeration_method': os.environ.get('ENUMERATION_METHOD', 'iter_by_title')
        }
        
        # Try to load from config file if provided
        if self._config_file and os.path.exists(self._config_file):
            try:
                with open(self._config_file, 'r') as f:
                    file_config = json.load(f)
                    config.update(file_config)
                logger.info(f"Loaded configuration from {self._config_file}")
            except Exception as e:
                logger.warning(f"Failed to load config from {self._config_file}: {e}")
        
        # Validate required settings  
        self._validate_config(config)
        
        return config
        
    def _validate_config(self, config: Dict[str, Any]) -> None:
        """Validate configuration values."""
        required_fields = ['zim_path', 'collection_name']
        
        for field in required_fields:
            if not config.get(field):
                raise ValueError(f"Required configuration field '{field}' is missing")
                
        # Validate that ZIM path exists
        zim_path = config.get('zim_path')
        if zim_path and not os.path.exists(zim_path):
            raise ValueError(f"ZIM file path does not exist: {zim_path}")
            
        logger.debug("Configuration validation passed")
    
    def get_config(self) -> WikipediaConfig:
        """Get the configuration as a WikipediaConfig object."""
        # Create the configuration object using available data
        config_dict = self._config.copy()
        
        # Handle some special cases
        if not config_dict['zim_filename'] and config_dict['zim_path']:
            config_dict['zim_filename'] = Path(config_dict['zim_path']).name
            
        return WikipediaConfig(**config_dict)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self._config.get(key, default)
        
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        self._config[key] = value
        
    def save_config(self, config_file: Optional[str] = None) -> None:
        """Save current configuration to file."""
        save_path = config_file or self._config_file
        if save_path:
            with open(save_path, 'w') as f:
                json.dump(self._config, f, indent=2)
            logger.info(f"Configuration saved to {save_path}")

    def update_from_dict(self, updates: Dict[str, Any]) -> None:
        """Update configuration from a dictionary."""
        self._config.update(updates)
        self._validate_config(self._config)