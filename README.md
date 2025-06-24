# Arazzo Sample Project

This project consists of three microservices:
- **Order API**
- **BFF (Backend for Frontend)**
- **UUID API**

All services are developed using **FastAPI**, **SQLModel**, and **SQLite** as the database system.

## Cloning the Repository

1. Clone the repository
```shell
git clone https://github.com/znsio/specmatic-arazzo-sample.git
```

2. Initialize and update the specmatic-order-contracts submodule
```shell
git submodule update --init --recursive --remote
```

3. Enable automatic submodule updating when executing git pull
```shell
git config submodule.recurse true
```

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

## Workflow Specification

The `workflow/` directory contains a minimal Arazzo specification. The following instructions assume that you have the Specmatic Arazzo JAR file available and have aliased it as `specmatic-arazzo`.

### Navigate to the `workflow/` Directory

```shell
cd workflow/
```

### Extrapolating the Specification

Specmatic Arazzo can extrapolate a complete specification from the minimal one by filling in missing parameters, request bodies, and defining success and failure actions and outputs. To perform the extrapolation, execute:

```shell
specmatic-arazzo extrapolate --spec-file=uuid_order_workflow.arazzo.yaml -o .
```
After executing this command, you should see two new files generated in the `workflow/` directory:

1.  **Extrapolated Specification:** `uuid_order_workflow.arazzo_extrapolated.arazzo.yaml`
2.  **Generated Inputs File:** `uuid_order_workflow.arazzo_extrapolated.arazzo_input.json`

### Validating the Specification

Once the specification is extrapolated, validate it to ensure that all parameters, request bodies, schemas, outputs, and actions are correctly defined. Run the following command to validate the extrapolated specification:

```shell
specmatic-arazzo validate --spec-file=uuid_order_workflow.arazzo_extrapolated.arazzo.yaml
```

**Tip:** For testing purposes, consider modifying the `email` field in the workflow inputs by removing its format specification. This alteration should trigger a validation failure, demonstrating the effectiveness of the validation process.

### Running the Workflow

Before executing the workflow tests, verify that the input values in the Arazzo inputs file correspond with the seed data specified in `run.py`.
The `productId` in `PlaceOrder` and the `id` in `RetrieveProductDetails` should be set to either 1 or 2.

#### Initialize Services and Populate Data
Execute the `run.py` script from the root directory to initialize the required services and populate the database with product data:

```shell
python run.py
```

#### Execute Workflow Tests
After initializing the services, run the workflow tests using `Specmatic Arazzo`. From within the `/workflow` directory, execute:

```shell
specmatic-arazzo test
```

Upon completion of the tests, a detailed HTML report will be generated in the `workflow/build/reports/specmatic/html/index.html` directory. 
This report provides a comprehensive overview of the test outcomes, including a workflow diagram and additional information.

### Generating Examples
To generate examples from the extrapolated specification, run the following command:

```shell
specmatic-arazzo examples --spec=uuid_order_workflow.arazzo_extrapolated.arazzo.yaml
```

The generated examples will be placed in the parent directory of the specifications, specifically in the `central-repo` submodule folder.
