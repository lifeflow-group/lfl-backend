import os
import sys
import argparse
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy.engine.url import make_url

# Add project root to sys.path to import app.*
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from app.models import *

# 1. Drop the entire database
# python scripts/drop_database.py --admin-user postgres --admin-password your_password --drop-type database

# 2. Only drop all tables (schema)
# python scripts/drop_database.py --admin-user postgres --admin-password your_password --drop-type tables

# Add project root to sys.path to import app.*
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from app.database import engine
from app.database import Base  # if you want to drop using Base.metadata.drop_all()

# DATABASE_URL: Should be aligned with your setup
DATABASE_URL = os.getenv("DATABASE_URL")
print("Loaded DATABASE_URL:", DATABASE_URL)


def parse_args():
    parser = argparse.ArgumentParser(description="Drop database or tables.")
    parser.add_argument("--admin-user", required=True, help="PostgreSQL admin username")
    parser.add_argument(
        "--admin-password", required=True, help="PostgreSQL admin password"
    )
    parser.add_argument(
        "--host", default="localhost", help="Database host (default: localhost)"
    )
    parser.add_argument("--port", default="5432", help="Database port (default: 5432)")
    parser.add_argument(
        "--drop-type",
        choices=["database", "tables"],
        required=True,
        help="Choose to drop the entire 'database' or just all 'tables'.",
    )
    return parser.parse_args()


def drop_database(admin_user, admin_password, host, port):
    """Drop the entire PostgreSQL database."""
    url = make_url(DATABASE_URL)
    db_name = url.database

    try:
        print(
            f"🔗 Connecting to PostgreSQL {host}:{port} as admin '{admin_user}' to drop database '{db_name}'..."
        )
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=admin_user,
            password=admin_password,
            database="postgres",
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # Terminate active connections
        print(f"⚠️ Terminating all connections to '{db_name}'...")
        cursor.execute(
            f"""
            SELECT pg_terminate_backend(pid)
            FROM pg_stat_activity
            WHERE datname = %s;
        """,
            (db_name,),
        )

        # Drop database
        cursor.execute(f"DROP DATABASE IF EXISTS {db_name};")
        print(f"✅ Successfully dropped database '{db_name}'.")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"❌ Error when dropping database: {e}")
        sys.exit(1)


def drop_all_tables():
    """Drop all tables in the current database schema."""
    try:
        print("🔗 Connecting to database to drop all tables...")
        # Drop all tables using metadata (SQLAlchemy approach)
        Base.metadata.drop_all(bind=engine)
        print("✅ Successfully dropped all tables.")

    except Exception as e:
        print(f"❌ Error when dropping tables: {e}")
        sys.exit(1)


def main():
    args = parse_args()

    if args.drop_type == "database":
        drop_database(
            admin_user=args.admin_user,
            admin_password=args.admin_password,
            host=args.host,
            port=args.port,
        )
    elif args.drop_type == "tables":
        drop_all_tables()

    print("🎉 Drop operation completed!")


if __name__ == "__main__":
    main()
