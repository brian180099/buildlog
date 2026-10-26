from app.core.config import normalize_database_url


def test_supabase_postgresql_url_uses_psycopg_driver() -> None:
    assert (
        normalize_database_url("postgresql://user:password@example.com:5432/postgres")
        == "postgresql+psycopg://user:password@example.com:5432/postgres"
    )


def test_sqlite_url_is_unchanged() -> None:
    assert normalize_database_url("sqlite:///:memory:") == "sqlite:///:memory:"


def test_relative_sqlite_file_is_resolved_from_project_root() -> None:
    normalized = normalize_database_url("sqlite:///./backend/buildlog.db")

    assert normalized.endswith("/backend/buildlog.db")
    assert normalized.startswith("sqlite:///")

