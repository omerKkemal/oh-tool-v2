"""Configuration and app initialization tests."""

from pathlib import Path

from utility.setting import Setting

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_setting_initialization_creates_expected_values():
    """The application settings object should expose key runtime values."""
    config = Setting()

    assert config.SECRAT_KEY
    assert config.DB_DIR == "db"
    assert config.LOG_DIR == "logs"
    assert config.DB_URI.startswith("sqlite:///")
    assert config.LOG_FILE_PATH.endswith("log.txt")
    assert config.JSON_FILE_PATH.endswith("info.json")


def test_flask_app_can_be_imported_and_configured():
    """The Flask app should instantiate with registered blueprints."""
    from app import app

    assert app is not None
    assert hasattr(app, "config")
    assert app.secret_key
    assert len(app.blueprints) >= 7
    assert "view" in app.blueprints
    assert "public" in app.blueprints
