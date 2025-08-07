"""
Command line interface for SyncDB
"""
import sys
import logging
import click
from typing import Optional, List
from .config import Config, create_sample_config, setup_logging
from .database import DatabaseConnection
from .syncer import DatabaseSyncer


logger = logging.getLogger(__name__)


@click.group()
@click.option('--config', '-c', help='Configuration file path')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.pass_context
def cli(ctx, config: Optional[str], verbose: bool):
    """SyncDB - Database synchronization tool"""
    ctx.ensure_object(dict)
    ctx.obj['config_file'] = config
    ctx.obj['verbose'] = verbose


@cli.command()
@click.option('--file', '-f', default='syncdb.yaml', help='Output file path')
def init(file: str):
    """Create a sample configuration file"""
    try:
        create_sample_config(file)
        click.echo(f"Created sample configuration file: {file}")
        click.echo("Edit the file to configure your databases and run 'syncdb sync' to start synchronization.")
    except Exception as e:
        click.echo(f"Error creating configuration file: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--source', '-s', help='Source database connection string')
@click.option('--target', '-t', help='Target database connection string')
@click.option('--tables', help='Comma-separated list of tables to sync')
@click.option('--schema-only', is_flag=True, help='Sync schema only')
@click.option('--data-only', is_flag=True, help='Sync data only')
@click.option('--truncate', is_flag=True, help='Truncate target tables before syncing data')
@click.pass_context
def sync(ctx, source: Optional[str], target: Optional[str], tables: Optional[str],
         schema_only: bool, data_only: bool, truncate: bool):
    """Synchronize databases"""
    
    # Load configuration
    config = Config(ctx.obj.get('config_file'))
    setup_logging(config.config)
    
    if ctx.obj.get('verbose'):
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Get database connection strings
        source_conn_str = source or config.get_source_connection_string()
        target_conn_str = target or config.get_target_connection_string()
        
        if not source_conn_str or not target_conn_str:
            click.echo("Error: Source and target database configurations are required", err=True)
            click.echo("Use --source and --target options or provide a configuration file", err=True)
            sys.exit(1)
        
        # Parse tables list
        table_list = None
        if tables:
            table_list = [t.strip() for t in tables.split(',')]
        elif config.get_sync_options().get('tables'):
            table_list = config.get_sync_options()['tables']
        
        # Create database connections
        source_db = DatabaseConnection(source_conn_str, "source")
        target_db = DatabaseConnection(target_conn_str, "target")
        
        # Connect to databases
        click.echo("Connecting to databases...")
        source_db.connect()
        target_db.connect()
        
        # Create syncer and perform synchronization
        syncer = DatabaseSyncer(source_db, target_db)
        
        success = False
        if schema_only:
            click.echo("Synchronizing schema...")
            success = syncer.sync_schema(table_list)
        elif data_only:
            click.echo("Synchronizing data...")
            success = syncer.sync_data(table_list, truncate)
        else:
            click.echo("Synchronizing schema and data...")
            success = syncer.sync_all(table_list, truncate)
        
        if success:
            click.echo("Synchronization completed successfully!")
        else:
            click.echo("Synchronization failed!", err=True)
            sys.exit(1)
        
    except Exception as e:
        logger.error(f"Synchronization failed: {e}")
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    
    finally:
        # Clean up connections
        try:
            source_db.close()
            target_db.close()
        except:
            pass


@cli.command()
@click.option('--source', '-s', help='Source database connection string')
@click.option('--target', '-t', help='Target database connection string')
@click.pass_context
def test(ctx, source: Optional[str], target: Optional[str]):
    """Test database connections"""
    
    config = Config(ctx.obj.get('config_file'))
    setup_logging(config.config)
    
    try:
        # Get database connection strings
        source_conn_str = source or config.get_source_connection_string()
        target_conn_str = target or config.get_target_connection_string()
        
        if not source_conn_str or not target_conn_str:
            click.echo("Error: Source and target database configurations are required", err=True)
            sys.exit(1)
        
        # Test source database
        click.echo("Testing source database connection...")
        source_db = DatabaseConnection(source_conn_str, "source")
        source_db.connect()
        source_tables = source_db.get_tables()
        click.echo(f"✓ Source database connected successfully ({len(source_tables)} tables found)")
        
        # Test target database  
        click.echo("Testing target database connection...")
        target_db = DatabaseConnection(target_conn_str, "target")
        target_db.connect()
        target_tables = target_db.get_tables()
        click.echo(f"✓ Target database connected successfully ({len(target_tables)} tables found)")
        
        click.echo("✓ All database connections are working!")
        
    except Exception as e:
        click.echo(f"✗ Connection test failed: {e}", err=True)
        sys.exit(1)
    
    finally:
        try:
            source_db.close()
            target_db.close()
        except:
            pass


def main():
    """Main entry point"""
    cli()


if __name__ == '__main__':
    main()