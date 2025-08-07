# SyncDB

A simple and powerful database synchronization tool that allows you to sync schema and data between different database systems.

## Features

- **Multi-database support**: SQLite, MySQL, PostgreSQL
- **Schema synchronization**: Create missing tables in target database
- **Data synchronization**: Copy data from source to target database
- **Selective sync**: Choose specific tables to synchronize
- **Flexible configuration**: YAML configuration files or command-line options
- **Safe operations**: Options to truncate target tables or sync schema-only

## Installation

### From source
```bash
git clone https://github.com/ObjectOriented0/SyncDB.git
cd SyncDB
pip install -r requirements.txt
pip install -e .
```

### Using pip (when published)
```bash
pip install syncdb
```

## Quick Start

### 1. Initialize configuration
```bash
syncdb init
```

This creates a `syncdb.yaml` configuration file with sample settings.

### 2. Configure your databases

Edit `syncdb.yaml` to configure your source and target databases:

```yaml
source_db:
  type: sqlite
  path: source.db

target_db:
  type: mysql
  host: localhost
  port: 3306
  user: username
  password: password
  database: target_db
```

### 3. Test connections
```bash
syncdb test
```

### 4. Synchronize databases
```bash
# Sync everything (schema + data)
syncdb sync

# Sync only schema
syncdb sync --schema-only

# Sync only data
syncdb sync --data-only

# Sync specific tables
syncdb sync --tables "users,products,orders"

# Truncate target tables before syncing
syncdb sync --truncate
```

## Configuration

### Database Types

#### SQLite
```yaml
source_db:
  type: sqlite
  path: /path/to/database.db
```

#### MySQL
```yaml
source_db:
  type: mysql
  host: localhost
  port: 3306
  user: username
  password: password
  database: database_name
```

#### PostgreSQL
```yaml
source_db:
  type: postgresql
  host: localhost
  port: 5432
  user: username
  password: password
  database: database_name
```

### Sync Options
```yaml
sync_options:
  tables: ["users", "products"]    # Specific tables (empty = all tables)
  truncate_target: false           # Truncate target before sync
  schema_only: false               # Sync only schema
  data_only: false                 # Sync only data
```

## Command Line Usage

### Basic Commands

```bash
# Initialize configuration
syncdb init

# Test database connections
syncdb test

# Sync databases using config file
syncdb sync

# Sync with custom config file
syncdb sync --config /path/to/config.yaml

# Sync with connection strings (no config file needed)
syncdb sync --source "sqlite:///source.db" --target "mysql://user:pass@localhost/db"
```

### Advanced Options

```bash
# Sync specific tables only
syncdb sync --tables "users,orders,products"

# Sync schema only (no data)
syncdb sync --schema-only

# Sync data only (no schema changes)
syncdb sync --data-only

# Truncate target tables before syncing data
syncdb sync --truncate

# Enable verbose logging
syncdb sync --verbose
```

## Examples

### Example 1: SQLite to MySQL
```bash
# Initialize config
syncdb init

# Edit syncdb.yaml:
# source_db:
#   type: sqlite
#   path: myapp.db
# target_db:
#   type: mysql
#   host: localhost
#   user: root
#   password: secret
#   database: myapp_backup

# Sync
syncdb sync
```

### Example 2: PostgreSQL to SQLite (backup)
```bash
syncdb sync \
  --source "postgresql://user:pass@localhost:5432/production" \
  --target "sqlite:///backup.db"
```

### Example 3: Selective table sync
```bash
syncdb sync --tables "users,sessions" --truncate
```

## API Usage

You can also use SyncDB programmatically:

```python
from syncdb.database import DatabaseConnection
from syncdb.syncer import DatabaseSyncer

# Create database connections
source_db = DatabaseConnection("sqlite:///source.db", "source")
target_db = DatabaseConnection("mysql://user:pass@localhost/target", "target")

# Connect
source_db.connect()
target_db.connect()

# Create syncer and sync
syncer = DatabaseSyncer(source_db, target_db)
success = syncer.sync_all()

# Clean up
source_db.close()
target_db.close()
```

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Development Installation
```bash
git clone https://github.com/ObjectOriented0/SyncDB.git
cd SyncDB
pip install -e .
```

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## Support

For issues and questions, please use the GitHub issue tracker.