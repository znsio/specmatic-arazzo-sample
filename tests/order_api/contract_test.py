import pathlib

import pytest
from specmatic.core.specmatic import Specmatic

from order_api import app
from tests import ROOT_DIR

SPECMATIC_CONFIG = str(pathlib.Path(__file__).parent / "specmatic.yaml")
DB_FILE = ROOT_DIR.parent / "order.db"


@pytest.fixture(scope="session", autouse=True)
def cleanup_db():
    DB_FILE.unlink(missing_ok=True)
    yield
    DB_FILE.unlink(missing_ok=True)


class TestOrderApiContract:
    pass


Specmatic().with_specmatic_config_file_path(SPECMATIC_CONFIG).with_asgi_app(
    "order_api:app",
).test_with_api_coverage_for_fastapi_app(TestOrderApiContract, app).run()

if __name__ == "__main__":
    pytest.main()
