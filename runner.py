import json
import time
import logging
import argparse
import sample_app
import api_checks

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Map module names to module objects for dynamic resolution
MODULE_MAP = {
    "sample_app": sample_app,
    "api_checks": api_checks
}

def load_test_cases(filepath: str) -> list:
    """Loads and parses the JSON file containing test cases."""
    with open(filepath, 'r') as file:
        return json.load(file)

def run_test(case: dict, verbose: bool) -> tuple[bool, str]:
    """Executes a single test case and returns (passed, detail_message)."""
    test_id = case.get("id")
    func_name = case.get("function")
    module_name = case.get("module", "sample_app")
    inputs = case.get("input")
    expected = case.get("expected")
    expect_exception = case.get("expect_exception", False)
    
    # Resolve the target function dynamically
    module_obj = MODULE_MAP.get(module_name)
    if not module_obj:
        return False, f"{test_id} [{func_name}]: FAIL (Module '{module_name}' not found)"
        
    func = getattr(module_obj, func_name, None)
    if not func:
        return False, f"{test_id} [{func_name}]: FAIL (Function '{func_name}' not found)"

    actual = None
    exception_occurred = False
    actual_exception = None

    try:
        # Handle list-style (*args) vs dict-style (**kwargs) inputs
        if isinstance(inputs, list):
            actual = func(*inputs)
        elif isinstance(inputs, dict):
            actual = func(**inputs)
        else:
            actual = func(inputs)
    except Exception as e:
        exception_occurred = True
        actual_exception = type(e).__name__

    if expect_exception:
        if exception_occurred:
            return True, f"{test_id} [{func_name}]: PASS (Exception raised as expected)"
        else:
            return False, f"{test_id} [{func_name}]: FAIL (Expected exception, but none was raised. Actual: {actual})"
    else:
        if exception_occurred:
            return False, f"{test_id} [{func_name}]: FAIL (Unexpected exception: {actual_exception})"
        
        if actual == expected:
            msg = f"{test_id} [{func_name}]: PASS"
            if verbose:
                msg += f" (Input: {inputs}, Expected: {expected}, Actual: {actual})"
            return True, msg
        else:
            return False, f"{test_id} [{func_name}]: FAIL (Expected: {expected}, Actual: {actual})"

def generate_html_report(results: list, filepath: str):
    """Generates a simple HTML report from test results without any templating libraries."""
    html = """
    <html>
    <head>
        <title>Test Execution Report</title>
        <style>
            body { font-family: sans-serif; margin: 20px; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            .pass { color: green; font-weight: bold; }
            .fail { color: red; font-weight: bold; }
        </style>
    </head>
    <body>
        <h2>Test Execution Report</h2>
        <table>
            <tr>
                <th>Test ID</th>
                <th>Function</th>
                <th>Status</th>
                <th>Details</th>
            </tr>
    """
    for res in results:
        case = res['case']
        passed = res['passed']
        details = res['details']
        status_class = "pass" if passed else "fail"
        status_text = "PASS" if passed else "FAIL"
        
        html += f"""
            <tr>
                <td>{case.get('id')}</td>
                <td>{case.get('function')}</td>
                <td class="{status_class}">{status_text}</td>
                <td>{details}</td>
            </tr>
        """
        
    html += """
        </table>
    </body>
    </html>
    """
    with open(filepath, 'w') as file:
        file.write(html)

def main():
    parser = argparse.ArgumentParser(description="Python Test Automation Framework (Mini)")
    parser.add_argument("--verbose", action="store_true", help="Print detailed output for all tests")
    args = parser.parse_args()

    logger.info("Starting test execution...")
    start_time = time.time()
    
    try:
        test_cases = load_test_cases("test_cases.json")
    except Exception as e:
        logger.error(f"Failed to load test cases: {e}")
        return

    passed_count = 0
    failed_count = 0
    results = []

    for case in test_cases:
        passed, msg = run_test(case, args.verbose)
        results.append({"case": case, "passed": passed, "details": msg})
        
        if passed:
            passed_count += 1
            if args.verbose:
                logger.info(msg)
        else:
            failed_count += 1
            logger.error(msg)

    time_taken = time.time() - start_time

    # Console Summary
    print("\\n============================")
    print("TEST SUMMARY")
    print(f"Total: {len(test_cases)} | Passed: {passed_count} | Failed: {failed_count}")
    print(f"Time: {time_taken:.2f}s")
    print("============================\\n")

    # Generate HTML Report
    report_path = "report.html"
    generate_html_report(results, report_path)
    print(f"HTML Report generated at: {report_path}")

if __name__ == "__main__":
    main()
