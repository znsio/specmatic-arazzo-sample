import pathlib
import signal
import subprocess
import sys
from time import sleep

from sqlmodel import Session, SQLModel, create_engine

from schemas.product import Product, ProductType

BASE_DIR = pathlib.Path(__file__).parent
ORDER_DB_PATH = BASE_DIR / "order.db"
UUID_DB_PATH = BASE_DIR / "uuid.db"
engine = create_engine(f"sqlite:///{ORDER_DB_PATH}", connect_args={"check_same_thread": False})


def initialize_database():
    SQLModel.metadata.create_all(engine)
    products = [
        Product(name="Phone", type=ProductType.GADGET, inventory=100),
        Product(name="Pizza", type=ProductType.FOOD, inventory=50),
    ]

    with Session(engine) as session:
        session.add_all(products)
        session.commit()


def remove_databases():
    engine.dispose()
    for db_path in [ORDER_DB_PATH, UUID_DB_PATH]:
        db_path.unlink(missing_ok=True)


def terminate_processes(processes):
    for process in processes:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()

    sleep(1)
    remove_databases()


def handle_shutdown(signum, frame):
    terminate_processes(active_processes)
    sys.exit(0)


if __name__ == "__main__":
    remove_databases()
    initialize_database()

    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)

    services = {
        "UUID Service": ["uvicorn", "uuid_api:app", "--host", "127.0.0.1", "--port", "9000"],
        "Order Service": ["uvicorn", "order_api:app", "--host", "127.0.0.1", "--port", "5000"],
        "BFF Service": ["uvicorn", "bff:app", "--host", "127.0.0.1", "--port", "3000"],
    }

    active_processes = [subprocess.Popen(command, cwd=BASE_DIR) for command in services.values()]
    try:
        for process in active_processes:
            process.wait()
    except KeyboardInterrupt:
        handle_shutdown(None, None)
