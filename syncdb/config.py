"""
Configuration management for SyncDB
"""
import os
import yaml
import logging
from typing import Dict, Any, Optional
from .database import parse_connection_string


logger = logging.getLogger(__name__)


class Config:
    """Configuration manager for SyncDB"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file
        self.config: Dict[str, Any] = {}
        self._load_config()
    
    def _load_config(self):
        """Load configuration from file or environment"""
        if self.config_file and os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self.config = yaml.safe_load(f) or {}
                logger.info(f"Loaded configuration from {self.config_file}")
            except Exception as e:
                logger.error(f"Failed to load config file {self.config_file}: {e}")
                raise
        else:
            # Use default empty config
            self.config = {}
    
    def get_source_db_config(self) -> Dict[str, Any]:
        """Get source database configuration"""
        return self.config.get('source_db', {})
    
    def get_target_db_config(self) -> Dict[str, Any]:
        """Get target database configuration"""
        return self.config.get('target_db', {})
    
    def get_sync_options(self) -> Dict[str, Any]:
        """Get synchronization options"""
        return self.config.get('sync_options', {})
    
    def get_source_connection_string(self) -> str:
        """Get source database connection string"""
        return parse_connection_string(self.get_source_db_config())
    
    def get_target_connection_string(self) -> str:
        """Get target database connection string"""
        return parse_connection_string(self.get_target_db_config())


def create_sample_config(file_path: str):
    """Create a sample configuration file"""
    sample_config = {
        'source_db': {
            'type': 'sqlite',
            'path': 'source.db'
        },
        'target_db': {
            'type': 'sqlite', 
            'path': 'target.db'
        },
        'sync_options': {
            'tables': [],  # Empty list means sync all tables
            'truncate_target': False,
            'schema_only': False,
            'data_only': False
        },
        'logging': {
            'level': 'INFO',
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    }
    
    try:
        with open(file_path, 'w') as f:
            yaml.dump(sample_config, f, default_flow_style=False, indent=2)
        logger.info(f"Created sample configuration file: {file_path}")
    except Exception as e:
        logger.error(f"Failed to create sample config file: {e}")
        raise


def setup_logging(config: Dict[str, Any]):
    """Setup logging based on configuration"""
    log_config = config.get('logging', {})
    level = getattr(logging, log_config.get('level', 'INFO').upper())
    format_str = log_config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    logging.basicConfig(
        level=level,
        format=format_str,
        handlers=[logging.StreamHandler()]
    )