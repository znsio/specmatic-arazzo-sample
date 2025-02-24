# Arazzo Sample Project

This project consists of three microservices:
- **Order API**
- **BFF (Backend for Frontend)**
- **UUID API**

All services are developed using **FastAPI**, **SQLModel**, and **SQLite** as the database system.

## Setup Instructions

### Setting Up Virtual Environment
#### On Unix/macOS:
```shell
python3 -m venv venv
source venv/bin/activate
```

#### On Windows (Command Prompt):
```shell
python -m venv venv
venv\Scripts\activate
```

### Installing Dependencies
```shell
pip install -r requirements.txt
```

## Running the Services
Execute the `run.py` script located in the root directory to initialize all three services, which will also populate the database with product data.
```shell
python run.py
```

## Service Interactions
The **BFF** service sends a request to the **UUID API** to retrieve a UUID for a customer based on the request payload. It subsequently uses this UUID to make a request to the **Order API**.

## Running Tests
This project uses `pytest` and `Specmatic` for contract testing.

### Running Unit Tests

- To run all tests:
  ```shell
  pytest -v -s
  ```
- To run tests for an individual service execute:
  ```shell
  pytest tests/<service_folder> -v -s
  ```

### Workflow Specification
The `workflow/` directory includes a **minimal Arazzo specification**. Execute the extrapolate command on this minimal specification with `specmatic arazzo`, then validate it using the same tool. After that, you can run the tests and generate examples as well as an HTML report.

## Note
Ensure that input values in arrazo inputs file match the **seed data** from `run.py` to get accurate results.
