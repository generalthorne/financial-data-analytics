import os

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine

from pathlib import Path

from sqlalchemy import text


load_dotenv()


def get_database_engine():
    """Create and return a SQLAlchemy database engine."""

    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    database = os.getenv("DB_NAME", "financial_data")

    if not username or not password:
        raise ValueError("Database credentials not found in .env file.")

    connection_url = URL.create(
        drivername="postgresql+psycopg2",
        username=username,
        password=password,
        host=host,
        port=int(port),
        database=database
    )

    engine = create_engine(connection_url)

    return engine


def initialize_database():
    """Create the database tables using schema.sql."""

    engine = get_database_engine()

    schema_path = Path(__file__).with_name("schema.sql")

    with open(schema_path, "r", encoding="utf-8") as file:
        schema = file.read()

    with engine.begin() as connection:
        connection.execute(text(schema))

    engine.dispose()