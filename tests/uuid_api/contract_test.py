import pathlib

import pytest
from specmatic.core.specmatic import Specmatic

from tests import ROOT_DIR
from uuid_api import app

SPECMATIC_CONFIG = str(pathlib.Path(__file__).parent / "specmatic.yaml")
DB_FILE = ROOT_DIR.parent / "uuid.db"


@pytest.fixture(scope="session", autouse=True)
def cleanup_db():
    DB_FILE.unlink(missing_ok=True)
    yield
    DB_FILE.unlink(missing_ok=True)


class TestUuidApiContract:
    pass


Specmatic().with_specmatic_config_file_path(SPECMATIC_CONFIG).with_asgi_app(
    "uuid_api:app",
).test_with_api_coverage_for_fastapi_app(TestUuidApiContract, app).run()

if __name__ == "__main__":
    pytest.main()
