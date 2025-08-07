"""
Tests for SyncDB functionality
"""
import unittest
import tempfile
import os
import sqlite3
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, text
from syncdb.database import DatabaseConnection, parse_connection_string
from syncdb.syncer import DatabaseSyncer
from syncdb.config import Config, create_sample_config


class TestDatabaseConnection(unittest.TestCase):
    """Test database connection functionality"""
    
    def setUp(self):
        """Set up test databases"""
        self.temp_dir = tempfile.mkdtemp()
        self.source_db_path = os.path.join(self.temp_dir, 'source.db')
        self.target_db_path = os.path.join(self.temp_dir, 'target.db')
    
    def test_sqlite_connection(self):
        """Test SQLite database connection"""
        conn_str = f"sqlite:///{self.source_db_path}"
        db_conn = DatabaseConnection(conn_str, "test")
        
        engine = db_conn.connect()
        self.assertIsNotNone(engine)
        self.assertIsNotNone(db_conn.metadata)
        
        db_conn.close()
    
    def test_parse_connection_string(self):
        """Test connection string parsing"""
        # SQLite
        config = {'type': 'sqlite', 'path': '/tmp/test.db'}
        conn_str = parse_connection_string(config)
        self.assertEqual(conn_str, 'sqlite:///tmp/test.db')
        
        # MySQL
        config = {
            'type': 'mysql',
            'host': 'localhost',
            'port': 3306,
            'user': 'user',
            'password': 'pass',
            'database': 'testdb'
        }
        conn_str = parse_connection_string(config)
        self.assertEqual(conn_str, 'mysql+mysqlconnector://user:pass@localhost:3306/testdb')


class TestDatabaseSyncer(unittest.TestCase):
    """Test database synchronization functionality"""
    
    def setUp(self):
        """Set up test databases with sample data"""
        self.temp_dir = tempfile.mkdtemp()
        self.source_db_path = os.path.join(self.temp_dir, 'source.db')
        self.target_db_path = os.path.join(self.temp_dir, 'target.db')
        
        # Create source database with sample table and data
        source_conn_str = f"sqlite:///{self.source_db_path}"
        self.source_db = DatabaseConnection(source_conn_str, "source")
        self.source_db.connect()
        
        # Create target database (empty)
        target_conn_str = f"sqlite:///{self.target_db_path}"
        self.target_db = DatabaseConnection(target_conn_str, "target")
        self.target_db.connect()
        
        # Create sample table in source database
        self._create_sample_table()
    
    def _create_sample_table(self):
        """Create a sample table with data in source database"""
        with self.source_db.engine.connect() as conn:
            conn.execute(text("""
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT
                )
            """))
            
            conn.execute(text("""
                INSERT INTO users (id, name, email) VALUES 
                (1, 'John Doe', 'john@example.com'),
                (2, 'Jane Smith', 'jane@example.com')
            """))
            conn.commit()
        
        # Refresh metadata
        self.source_db.metadata.reflect(bind=self.source_db.engine)
    
    def test_schema_sync(self):
        """Test schema synchronization"""
        syncer = DatabaseSyncer(self.source_db, self.target_db)
        
        # Sync schema
        success = syncer.sync_schema()
        self.assertTrue(success)
        
        # Check if table was created in target
        self.target_db.metadata.reflect(bind=self.target_db.engine)
        self.assertIn('users', self.target_db.get_tables())
    
    def test_data_sync(self):
        """Test data synchronization"""
        syncer = DatabaseSyncer(self.source_db, self.target_db)
        
        # First sync schema
        syncer.sync_schema()
        
        # Then sync data
        success = syncer.sync_data()
        self.assertTrue(success)
        
        # Verify data was copied
        with self.target_db.engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM users"))
            count = result.scalar()
            self.assertEqual(count, 2)
    
    def test_full_sync(self):
        """Test full synchronization (schema + data)"""
        syncer = DatabaseSyncer(self.source_db, self.target_db)
        
        success = syncer.sync_all()
        self.assertTrue(success)
        
        # Verify both schema and data
        self.target_db.metadata.reflect(bind=self.target_db.engine)
        self.assertIn('users', self.target_db.get_tables())
        
        with self.target_db.engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM users"))
            count = result.scalar()
            self.assertEqual(count, 2)
    
    def tearDown(self):
        """Clean up test databases"""
        self.source_db.close()
        self.target_db.close()


class TestConfig(unittest.TestCase):
    """Test configuration functionality"""
    
    def test_sample_config_creation(self):
        """Test sample configuration file creation"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.yaml') as f:
            config_path = f.name
        
        try:
            create_sample_config(config_path)
            self.assertTrue(os.path.exists(config_path))
            
            # Test loading the config
            config = Config(config_path)
            self.assertIsInstance(config.get_source_db_config(), dict)
            self.assertIsInstance(config.get_target_db_config(), dict)
            
        finally:
            if os.path.exists(config_path):
                os.unlink(config_path)


if __name__ == '__main__':
    unittest.main()