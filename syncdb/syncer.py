"""
Core synchronization logic for database schemas and data
"""
import logging
from typing import List, Dict, Any, Set, Optional
from sqlalchemy import MetaData, Table, Column, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from .database import DatabaseConnection


logger = logging.getLogger(__name__)


class DatabaseSyncer:
    """Handles synchronization between two databases"""
    
    def __init__(self, source_db: DatabaseConnection, target_db: DatabaseConnection):
        self.source_db = source_db
        self.target_db = target_db
    
    def sync_schema(self, tables: Optional[List[str]] = None) -> bool:
        """
        Synchronize database schema from source to target
        
        Args:
            tables: List of table names to sync. If None, sync all tables.
            
        Returns:
            True if successful, False otherwise
        """
        try:
            source_tables = self.source_db.get_tables()
            target_tables = self.target_db.get_tables()
            
            if tables:
                # Filter to only specified tables
                source_tables = {name: table for name, table in source_tables.items() 
                               if name in tables}
            
            # Create missing tables in target
            for table_name, source_table in source_tables.items():
                if table_name not in target_tables:
                    logger.info(f"Creating table {table_name} in target database")
                    self._create_table(source_table, self.target_db.engine)
                else:
                    logger.info(f"Table {table_name} already exists in target database")
                    # Could add column comparison and alteration here
            
            # Refresh target metadata after creating tables
            self.target_db.metadata.reflect(bind=self.target_db.engine)
            
            return True
            
        except Exception as e:
            logger.error(f"Schema synchronization failed: {e}")
            return False
    
    def sync_data(self, tables: Optional[List[str]] = None, 
                  truncate_target: bool = False) -> bool:
        """
        Synchronize data from source to target database
        
        Args:
            tables: List of table names to sync. If None, sync all tables.
            truncate_target: Whether to truncate target tables before sync
            
        Returns:
            True if successful, False otherwise
        """
        try:
            source_tables = self.source_db.get_tables()
            # Refresh target metadata to get latest schema
            self.target_db.metadata.reflect(bind=self.target_db.engine)
            target_tables = self.target_db.get_tables()
            
            if tables:
                source_tables = {name: table for name, table in source_tables.items() 
                               if name in tables}
            
            for table_name, source_table in source_tables.items():
                if table_name not in target_tables:
                    logger.warning(f"Table {table_name} does not exist in target database")
                    continue
                
                logger.info(f"Syncing data for table {table_name}")
                self._sync_table_data(source_table, target_tables[table_name], 
                                    truncate_target)
            
            return True
            
        except Exception as e:
            logger.error(f"Data synchronization failed: {e}")
            return False
    
    def sync_all(self, tables: Optional[List[str]] = None, 
                 truncate_target: bool = False) -> bool:
        """
        Synchronize both schema and data
        
        Args:
            tables: List of table names to sync. If None, sync all tables.
            truncate_target: Whether to truncate target tables before data sync
            
        Returns:
            True if successful, False otherwise
        """
        logger.info("Starting full database synchronization")
        
        # First sync schema
        if not self.sync_schema(tables):
            logger.error("Schema synchronization failed, aborting")
            return False
        
        # Then sync data
        if not self.sync_data(tables, truncate_target):
            logger.error("Data synchronization failed")
            return False
        
        logger.info("Database synchronization completed successfully")
        return True
    
    def _create_table(self, source_table: Table, target_engine: Engine):
        """Create a table in the target database based on source table schema"""
        try:
            # Create table with same schema
            target_metadata = MetaData()
            new_table = Table(source_table.name, target_metadata)
            
            # Copy columns
            for column in source_table.columns:
                new_column = Column(
                    column.name,
                    column.type,
                    primary_key=column.primary_key,
                    nullable=column.nullable,
                    default=column.default
                )
                new_table.append_column(new_column)
            
            # Create the table
            target_metadata.create_all(target_engine)
            logger.info(f"Successfully created table {source_table.name}")
            
        except SQLAlchemyError as e:
            logger.error(f"Failed to create table {source_table.name}: {e}")
            raise
    
    def _sync_table_data(self, source_table: Table, target_table: Table, 
                        truncate_target: bool = False):
        """Sync data between two tables"""
        try:
            # Truncate target table if requested
            if truncate_target:
                with self.target_db.engine.connect() as conn:
                    conn.execute(text(f"DELETE FROM {target_table.name}"))
                    conn.commit()
                logger.info(f"Truncated target table {target_table.name}")
            
            # Read data from source
            with self.source_db.engine.connect() as source_conn:
                result = source_conn.execute(source_table.select())
                rows = result.fetchall()
                
                if not rows:
                    logger.info(f"No data to sync for table {source_table.name}")
                    return
                
                # Insert data into target
                with self.target_db.engine.connect() as target_conn:
                    # Convert rows to dictionaries for insert
                    data_to_insert = []
                    for row in rows:
                        row_dict = {}
                        for i, column in enumerate(source_table.columns):
                            row_dict[column.name] = row[i]
                        data_to_insert.append(row_dict)
                    
                    target_conn.execute(target_table.insert(), data_to_insert)
                    target_conn.commit()
                    
                    logger.info(f"Synced {len(data_to_insert)} rows for table {source_table.name}")
        
        except SQLAlchemyError as e:
            logger.error(f"Failed to sync data for table {source_table.name}: {e}")
            raise