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

# import tests.test_server_class


"""
This file contains the classes handling the tests as described in the file 'run_tests'.

Each test method has the same description regarding the test as presented in 'run_tests'
"""

import unittest
import random
import string

from server import Server


def random_folder(string_length=6):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


class ServerClassTestingStepOne(unittest.TestCase):
    """Handles the test for command and quit response"""

    def test_commands_response(self):
        """
        This test will check whether server responds commands.
        """

        server = Server()

        output = server.print_commands()

        self.assertTrue(output)

    def test_commands_quit(self):
        """
        This test will check quit response.
        """
        expected_results = ["\nLogged out successfully"]
        results = []

        server = Server()

        results.append(server.quit("127.0.0.1"))

        self.assertListEqual(results, expected_results)


class ServerClassTestingStepTwo(unittest.TestCase):
    """Handles the tests for login and listing the files"""

    def test_server_login(self):
        """
        This test will check login.
        Test1 : Wrong password
        Test2 : Wrong username
        Test3 : Proper login
        """
        server = Server()
        server.login_validation = {"127.0.0.1" : None}
        server.login_data = {"users": {"test": "123"}}
        expected_results = ["\nWrong password", "\nUser not registered", "\nLogin successfull"]
        results = []
        tests = [
            ["test", "1234", "127.0.0.1"],
            ["test2", "123", "127.0.0.1"],
            ["test", "123", "127.0.0.1"]
        ]

        for test in tests:
            results.append(server.login(
                test[0], test[1], test[2]))

        self.assertListEqual(results, expected_results)

    def test_server_list(self):
        """
        This test will check list command.
        Test1 : Listing without login.
        Test2 : Listing folder for user test
        """
        results = []
        expected_results = ["\nLogin First", "testfolder1"]
        server = Server()
        server.login_validation = {"127.0.0.1" : None}
        server.login_data = {"users": {"test": "123"}}
        results.append(server.list("127.0.0.1"))
        server.login("test", "123", "127.0.0.1")
        result_folder = server.list("127.0.0.1")
        if expected_results[1] in result_folder:
            results.append(expected_results[1])
        self.assertListEqual(results, expected_results)


class ServerClassTestingStepThree(unittest.TestCase):
    """Handles the tests to check response for change folder and create folder"""

    def test_server_change_folder(self):
        """
        This test will check response for change folder.
        Test1 : Change folder without login.
        Test2 : Wrong directory change.
        Test3 : Proper directory change.
        """
        results = []
        expected_results = ["\nLogin First", "\nUnable to change requested directory", "\nChanged directory successfully"]
        server = Server()
        server.login_validation = {"127.0.0.1" : None}
        server.login_data = {"users": {"test": "123"}}
        results.append(server.change_folder("testfolder1", "127.0.0.1"))
        server.login("test", "123", "127.0.0.1")
        results.append(server.change_folder("testfolder2", "127.0.0.1"))
        results.append(server.change_folder("testfolder1", "127.0.0.1"))

        self.assertListEqual(results, expected_results)

    def test_server_create_folder(self):
        """
        This test will check response for create folder.
        Test1 : Create already present directory.
        Test2 : Proper directory with random name.
        """
        results = []
        expected_results = ["\nDirectory Already Present", "\nSuccessfully made directory"]
        server = Server()
        server.login_validation = {"127.0.0.1" : None}
        server.login_data = {"users": {"test": "123"}}
        server.login("test", "123", "127.0.0.1")
        results.append(server.create_folder("testfolder1", "127.0.0.1"))
        server.change_folder("testfolder1", "127.0.0.1")
        results.append(server.create_folder("test" + random_folder(), "127.0.0.1"))

        self.assertListEqual(results, expected_results)



class ServerClassTestingStepFour(unittest.TestCase):
    """Handles the final part of the tests inculting tests for read and write the files"""

    def test_server_read_file(self):
        """
        This test will check read file.
        Test1 : Read the non existing file.
        Test2 : Proper read file.
        """
        results = []
        expected_results = ["\nNo such file found", "\nContent from characters : 0 - 100\nDontChangeThisContent"]
        server = Server()
        server.login_validation = {"127.0.0.1" : None}
        server.login_data = {"users": {"test": "123"}}
        server.login("test", "123", "127.0.0.1")
        server.change_folder("testfolder1", "127.0.0.1")
        results.append(server.read_file("test_read2.txt", "127.0.0.1"))
        results.append(server.read_file("test_read.txt", "127.0.0.1"))

        self.assertListEqual(results, expected_results)

    def test_server_write_file(self):
        """
        This test will check write file.
        Test1 : Write on non existing file.
        Test2 : Proper write file.
        """
        results = []
        expected_results = ["\nNo such file found\nWritten a new file\n", "\nWritten successfully"]
        server = Server()
        server.login_validation = {"127.0.0.1" : None}
        server.login_data = {"users": {"test": "123"}}
        server.login("test", "123", "127.0.0.1")
        server.change_folder("testfolder1", "127.0.0.1")
        results.append(server.write_file(random_folder() + ".txt", "content", "127.0.0.1"))
        results.append(server.write_file("test_write.txt", "content", "127.0.0.1"))

        self.assertListEqual(results, expected_results)







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
    return is_finished_with_step(ServerClassTestingStepOne)

def is_finished_with_step_two():
    """Run the second batch of tests"""
    print('-'*70 + "\nStarting test suite 2:\n")
    return is_finished_with_step(ServerClassTestingStepTwo)

def is_finished_with_step_three():
    """Run the second batch of tests"""
    print('-'*70 + "\nStarting test suite 3:\n")
    return is_finished_with_step(ServerClassTestingStepThree)

def is_finished_with_step_four():
    """Run the second batch of tests"""
    print('-'*70 + "\nStarting test suite 4:\n")
    return is_finished_with_step(ServerClassTestingStepFour)

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
