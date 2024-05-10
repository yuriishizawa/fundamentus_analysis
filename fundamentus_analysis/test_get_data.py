"""
This module contains the test cases for the get_data module.

The test cases are implemented using the unittest module.
The test cases are used to verify the functionality of the FundamentusData class.

Example:
    To run the test cases, you can use the following command:
    ```bash
    python -m unittest test_get_data.py
    ```
"""

import unittest

from .get_data import FundamentusData


class TestFundamentusData(unittest.TestCase):
    """
    A test case class for testing the functionality of the FundamentusData class.
    """

    def setUp(self):
        """
        Set up the test case by creating an instance of FundamentusData.
        """
        self.data = FundamentusData()

    def tearDown(self):
        """
        Clean up the test case by closing the driver.
        """
        self.data.close_driver()

    def test_get_driver(self):
        """
        Test case for the get_driver method.

        This test verifies that the get_driver method returns a
        non-None value and that the title of the driver's page is
        "FUNDAMENTUS - Invista consciente".
        """
        driver = self.data.get_driver()
        self.assertIsNotNone(driver)
        self.assertEqual(driver.title, "FUNDAMENTUS - Invista consciente")

    def test_click_params(self):
        """
        Test case to verify the functionality of clicking on parameters page.

        This method tests whether the parameters page is loaded correctly
        after clicking on it.
        It calls the `get_driver` method to initialize the driver and then calls
        the `click_params` method
        to simulate clicking on the parameters page. Assertions can be added
        to verify that the parameters
        page is loaded correctly.
        """
        self.data.get_driver()
        self.data.click_params()

    def test_get_df(self):
        """
        Test case for the get_df method of the Data class.

        This method verifies that the DataFrame is retrieved correctly by calling
        the get_df method
        of the Data class and adding assertions to validate the expected behavior.
        """
        self.data.get_driver()
        df = self.data.get_df()
        self.assertIsNotNone(df)
        self.assertGreater(df.shape[0], 0)
        self.assertGreater(df.shape[1], 0)
        self.assertEqual(df.columns[0], "Papel")


if __name__ == "__main__":
    unittest.main()
