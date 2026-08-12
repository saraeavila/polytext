from app.db.session import DATABASE_URL


def test_database_url_uses_postgresql():
    assert DATABASE_URL.startswith("postgresql+psycopg://")
