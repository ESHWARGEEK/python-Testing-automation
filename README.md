# Python Test Automation Framework (Mini)

A lightweight, data-driven test automation framework written in pure Python. Built for demonstrating core test automation concepts (data separation, dynamic execution, reporting) mirroring tools like Robot Framework.

## Features

- **Data-Driven:** Test cases are defined entirely in `test_cases.json`.
- **Dynamic Resolution:** Automatically executes target Python functions based on JSON definitions.
- **Resilient API Testing:** Includes basic REST API validation with an automatic retry mechanism.
- **Reporting:** Structured logging to the console and a generated HTML summary report.

## File Structure

- **`sample_app.py`**: The core "system under test" with local validation functions.
- **`api_checks.py`**: External REST API validation functions.
- **`retry.py`**: A `@retry` decorator demonstrating network resiliency handling.
- **`test_cases.json`**: The test data containing inputs, expected values, and assertions.
- **`runner.py`**: The execution engine that parses cases, runs them, and evaluates passes/failures.
- **`report.html`**: The HTML summary report generated after a test run.

## How to Run

Run the suite with standard output (only failures and the summary are logged to the console):
```bash
python runner.py
```

Run with verbose output (every test case detail is logged):
```bash
python runner.py --verbose
```

After execution, open `report.html` in your browser to see the results.
