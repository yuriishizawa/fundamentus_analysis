"""
    This module contains the FundamentusData class, which
    is used to retrieve data from the Fundamentus website.
    The FundamentusData class uses Selenium to interact with the Fundamentus
    website and retrieve data from it.
Example:
    To retrieve data from the Fundamentus website, you can use
    the FundamentusData class as follows:

    ```python
    data = FundamentusData()
    df = data.get_df()
    ```
"""

import pandas as pd
from selenium import webdriver

from fundamentus_analysis import logger


class FundamentusData:
    """
    A class for retrieving data from the Fundamentus website.

    Attributes:
        driver (WebDriver): The Selenium WebDriver instance.
    """

    def __init__(self):
        self.driver = self.get_driver()

    def get_driver(self):
        """
        Initializes and returns a Selenium WebDriver instance.

        Returns:
            WebDriver: The Selenium WebDriver instance.
        """
        logger.info("Starting Selenium driver")
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(5)
        driver.get("https://www.fundamentus.com.br/buscaavancada.php")
        logger.info("Driver started")
        return driver

    def close_driver(self):
        """
        Closes the Selenium WebDriver instance.
        """
        logger.info("Closing Selenium driver")
        self.driver.quit()
        logger.info("Driver closed")

    def click_params(self):
        """
        Sets the search parameters on the Fundamentus website.
        """
        logger.info("Setting search parameters")
        buttons = {
            "pl_min": 0,
            "pl_max": 20,
            "divy_min": 0,
            "firma_ebit_min": 0,
            "margemebit_min": 0,
            "patrim_min": 1e8,
            "liq_min": 1e7,
        }
        for button, limit in buttons.items():
            field = self.driver.find_element(by="name", value=button)
            field.click()
            field.send_keys(limit)
        search_button = self.driver.find_element(
            by="xpath", value="/html/body/div[1]/div[2]/form/input"
        )
        search_button.click()
        logger.info("Search parameters set")

    def get_df(self):
        """
        Retrieves data from the Fundamentus website and returns it as a DataFrame.

        Returns:
            DataFrame: The retrieved data.
        """
        logger.info("Getting data")
        self.click_params()
        self.driver.find_element(by="xpath", value="/html/body/div[1]/div[2]/table")
        div_yield = "Div.Yield"
        mrg_liq = "Mrg. Líq."
        columns = [
            "Papel",
            "EV/EBIT",
            "EV/EBITDA",
            "P/L",
            "P/VP",
            div_yield,
            mrg_liq,
            "Liq.2meses",
            "Patrim. Líq",
        ]
        df_new = pd.read_html(self.driver.page_source.replace(",", "."))[0][columns]
        df_new[[div_yield, mrg_liq]] = (
            df_new[[div_yield, mrg_liq]]
            .replace("%", "", regex=True)
            .astype(float)
            .div(100)
        )
        logger.info("Data retrieved")
        self.close_driver()
        return df_new


if __name__ == "__main__":
    data = FundamentusData()
    df = data.get_df()
    logger.info("\n" + df.head().to_string(index=False, float_format="{:.2f}".format))
    logger.info("Data saved to results.csv")
    df.to_csv("results.csv", index=False)
