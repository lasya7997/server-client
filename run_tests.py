"""
This file contains the tests given for assignment 2.
Each of these tests must pass for your assignment to be assessed.

The following unit tests are conducted on the class Snake:
    1. test_commands_response
            This test will check whether server responds commands.

    2. test_server_login
            This test will check login.


"""

import unittest
import sys

import tests.test_server_class


def is_finished_with_step(test_case_class_to_use):
    """Helper function to initialize, load, and run tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(
        loader.loadTestsFromTestCase(
            test_case_class_to_use
        )
    )

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if result.skipped:
        return False

    return result.wasSuccessful()


def is_finished_with_step_one():
    """Run the first batch of tests"""
    print('-'*70 + "\nStarting test suite 1:\n")
    return is_finished_with_step(tests.test_server_class.ServerClassTestingStepOne)

def is_finished_with_step_two():
    """Run the second batch of tests"""
    print('-'*70 + "\nStarting test suite 2:\n")
    return is_finished_with_step(tests.test_server_class.ServerClassTestingStepTwo)

def is_finished_with_step_three():
    """Run the second batch of tests"""
    print('-'*70 + "\nStarting test suite 3:\n")
    return is_finished_with_step(tests.test_server_class.ServerClassTestingStepThree)

def is_finished_with_step_four():
    """Run the second batch of tests"""
    print('-'*70 + "\nStarting test suite 4:\n")
    return is_finished_with_step(tests.test_server_class.ServerClassTestingStepFour)

if __name__ == "__main__":
    if is_finished_with_step_one() is not True:
        print("\n\tThe first testing step did not pass," +
              "either because of a failed or a skipped test.")
        print("\tFurther testing will not continue until these tests pass.")
        sys.exit(1)

    elif is_finished_with_step_two() is not True:
        print("\n\tThe second testing step did not pass," +
              "either because of a failed or a skipped test.")
        print("\tFurther testing will not continue until these tests pass.")
        sys.exit(1)

    elif is_finished_with_step_three() is not True:
        print("\n\tThe third testing step did not pass," +
              "either because of a failed or a skipped test.")
        print("\tFurther testing will not continue until these tests pass.")
        sys.exit(1)

    elif is_finished_with_step_four() is not True:
        print("\n\tThe fourth testing step did not pass," +
              "either because of a failed or a skipped test.")
        print("\tFurther testing will not continue until these tests pass.")
        sys.exit(1)

    sys.exit(0)
