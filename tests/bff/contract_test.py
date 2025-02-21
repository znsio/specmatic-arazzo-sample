import pathlib

import pytest
from specmatic.core.specmatic import Specmatic

from bff import app

SPECMATIC_CONFIG = str(pathlib.Path(__file__).parent / "specmatic.yaml")
EXAMPLES_DIR = pathlib.Path(__file__).parent / "stub_examples"


class TestBffContract:
    pass


Specmatic().with_specmatic_config_file_path(SPECMATIC_CONFIG).with_asgi_app(
    "bff:app",
).with_stub(stub_port=8080, stub_host="localhost", expectations=list(EXAMPLES_DIR.iterdir())).test_with_api_coverage_for_fastapi_app(
    TestBffContract,
    app,
).run()

if __name__ == "__main__":
    pytest.main()
