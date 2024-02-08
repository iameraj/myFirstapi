from django.test.runner import DiscoverRunner
from termcolor import colored
from unittest import TestResult


class CustomTestRunner(DiscoverRunner):
    def run_suite(self, suite, **kwargs):
        # Get the number of tests in the suite
        num_tests = suite.countTestCases()

        result = TestResult()

        # Print a header
        print(colored(f"Running {num_tests} Tests", "cyan"))
        print("=" * 30)

        # Iterate through each test and run them
        for index, test in enumerate(suite):
            # Print the title of the test
            print(f"Test {index + 1}: {test._testMethodName}", end=": ")

            # Run the test
            test(result)

            # Print the result
            if not result.errors and not result.failures:
                print(colored("Passed", "green"))
            else:
                print(colored("Failed", "red"))

        return result
