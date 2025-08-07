"""
Database connection and configuration management
"""
import logging
from typing import Dict, Any, Optional
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError


logger = logging.getLogger(__name__)


class DatabaseConnection:
    """Manages database connections and metadata"""
    
    def __init__(self, connection_string: str, name: str = ""):
        self.connection_string = connection_string
        self.name = name
        self.engine: Optional[Engine] = None
        self.metadata: Optional[MetaData] = None
    
    def connect(self) -> Engine:
        """Establish database connection"""
        try:
            self.engine = create_engine(self.connection_string)
            self.metadata = MetaData()
            self.metadata.reflect(bind=self.engine)
            logger.info(f"Connected to database: {self.name}")
            return self.engine
        except SQLAlchemyError as e:
            logger.error(f"Failed to connect to database {self.name}: {e}")
            raise
    
    def get_tables(self) -> Dict[str, Table]:
        """Get all tables from the database"""
        if not self.metadata:
            raise RuntimeError("Database not connected")
        return self.metadata.tables
    
    def close(self):
        """Close database connection"""
        if self.engine:
            self.engine.dispose()
            logger.info(f"Closed connection to database: {self.name}")


def parse_connection_string(db_config: Dict[str, Any]) -> str:
    """Parse database configuration to connection string"""
    db_type = db_config.get('type', 'sqlite')
    
    if db_type == 'sqlite':
        path = db_config.get('path', ':memory:')
        if path.startswith('/'):
            return f"sqlite://{path}"
        else:
            return f"sqlite:///{path}"
    
    elif db_type in ['mysql', 'postgresql']:
        host = db_config.get('host', 'localhost')
        port = db_config.get('port', 3306 if db_type == 'mysql' else 5432)
        user = db_config.get('user', '')
        password = db_config.get('password', '')
        database = db_config.get('database', '')
        
        if db_type == 'mysql':
            return f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
        else:  # postgresql
            return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    
    else:
        raise ValueError(f"Unsupported database type: {db_type}")