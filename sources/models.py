from sqlalchemy import BLOB, String, create_engine, MetaData, Table, Column, Integer

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String),
    Column("password", BLOB),
    Column("salt", BLOB),
)

engine = create_engine("sqlite:///./db.sqlite3")
metadata.create_all(engine)
