import os
import sys
import argparse
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy.engine.url import make_url

# Add project root to sys.path to import app.*
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

# Import app modules
from app.database import engine, Base
from app.models.user import User
from app.models.habit_category import HabitCategory
from sqlalchemy.orm import sessionmaker

# DATABASE_URL: retrieved from env or settings.py if available, hardcoded for demo
DATABASE_URL = os.getenv("DATABASE_URL")


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Setup PostgreSQL database and initialize tables."
    )
    parser.add_argument("--admin-user", required=True, help="PostgreSQL admin username")
    parser.add_argument(
        "--admin-password", required=True, help="PostgreSQL admin password"
    )
    parser.add_argument(
        "--host", default="localhost", help="Database host (default: localhost)"
    )
    parser.add_argument("--port", default="5432", help="Database port (default: 5432)")
    return parser.parse_args()


def setup_database_and_user(admin_user, admin_password, host, port):
    """Create PostgreSQL user and database if they don't exist."""
    url = make_url(DATABASE_URL)

    db_user = url.username
    db_password = url.password
    db_name = url.database

    try:
        print(f"🔗 Connecting to PostgreSQL {host}:{port} with user '{admin_user}'...")
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=admin_user,
            password=admin_password,
            database="postgres",  # Connect to default postgres database
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # Create user if it doesn't exist
        cursor.execute("SELECT 1 FROM pg_roles WHERE rolname=%s", (db_user,))
        if not cursor.fetchone():
            cursor.execute(f"CREATE USER {db_user} WITH PASSWORD %s", (db_password,))
            print(f"✅ Created user '{db_user}'.")
        else:
            print(f"ℹ️  User '{db_user}' already exists.")

        # Create database if it doesn't exist
        cursor.execute("SELECT 1 FROM pg_database WHERE datname=%s", (db_name,))
        if not cursor.fetchone():
            cursor.execute(f"CREATE DATABASE {db_name} OWNER {db_user}")
            print(f"✅ Created database '{db_name}'.")
        else:
            print(f"ℹ️  Database '{db_name}' already exists.")

        # Grant privileges to user
        cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user}")
        print(f"✅ Granted privileges to user '{db_user}' on database '{db_name}'.")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"❌ Error when creating database/user: {e}")
        sys.exit(1)


def init_db():
    """Create tables in database using SQLAlchemy."""
    print("🚀 Initializing tables with SQLAlchemy...")
    try:
        # Must import all models so Base.metadata knows about them!
        Base.metadata.create_all(bind=engine)
        print("✅ Successfully created tables.")
    except Exception as e:
        print(f"❌ Error when creating tables: {e}")


def add_sample_data():
    """Add sample user data to the database."""
    print("📊 Adding sample data to the database...")

    try:
        # Create a session
        Session = sessionmaker(bind=engine)
        session = Session()

        # Check if users already exist
        if session.query(User).count() > 0:
            print("ℹ️  Sample user data already exists. Skipping.")
        else:
            # Sample users
            users = [
                User(id="hoan", name="Nguyen Van Hoan"),
                User(
                    id="jane_smith",
                    name="Jane Smith",
                ),
            ]

            # Add users to the session
            for user in users:
                session.add(user)

            # Commit the changes
            session.commit()
            print(f"✅ Successfully added {len(users)} sample users.")

        # Add sample categories
        add_sample_categories(session)

        session.close()

    except Exception as e:
        print(f"❌ Error when adding sample data: {e}")


def add_sample_categories(session):
    """Add sample categories to the database."""
    # Check if categories already exist
    if session.query(HabitCategory).count() > 0:
        print("ℹ️  Sample category data already exists. Skipping.")
        return

    # Sample categories
    categories = [
        HabitCategory(
            id="health",
            name="Health",
            icon_path="assets/icons/health.png",
            color_hex="#FF5733",
        ),
        HabitCategory(
            id="work",
            name="Work",
            icon_path="assets/icons/work.png",
            color_hex="#3498DB",
        ),
        HabitCategory(
            id="personal_growth",
            name="Personal Growth",
            icon_path="assets/icons/personal_growth.png",
            color_hex="#9B59B6",
        ),
        HabitCategory(
            id="hobby",
            name="Hobby",
            icon_path="assets/icons/hobby.png",
            color_hex="#F1C40F",
        ),
        HabitCategory(
            id="fitness",
            name="Fitness",
            icon_path="assets/icons/fitness.png",
            color_hex="#2ECC71",
        ),
        HabitCategory(
            id="education",
            name="Education",
            icon_path="assets/icons/education.png",
            color_hex="#E67E22",
        ),
        HabitCategory(
            id="finance",
            name="Finance",
            icon_path="assets/icons/finance.png",
            color_hex="#27AE60",
        ),
        HabitCategory(
            id="social",
            name="Social",
            icon_path="assets/icons/social.png",
            color_hex="#E74C3C",
        ),
        HabitCategory(
            id="spiritual",
            name="Spiritual",
            icon_path="assets/icons/spiritual.png",
            color_hex="#8E44AD",
        ),
    ]

    # Add categories to the session
    for category in categories:
        session.add(category)

    # Commit the changes
    session.commit()
    print(f"✅ Successfully added {len(categories)} sample categories.")


def main():
    args = parse_args()

    # Step 1: Initialize user/database (if needed)
    setup_database_and_user(
        admin_user=args.admin_user,
        admin_password=args.admin_password,
        host=args.host,
        port=args.port,
    )

    # Step 2: Create tables in database
    init_db()

    # Step 3: Add sample data
    add_sample_data()

    print("🎉 Database setup completed!")


if __name__ == "__main__":
    main()
