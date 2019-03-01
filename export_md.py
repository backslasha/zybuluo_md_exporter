# -*- coding: utf-8 -*-
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

import custom_ec


class AppDynamicsJob:

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.katalon.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

        # logging for debug
        logging.basicConfig(level=logging.INFO)

    def test_app_dynamics_job(self):
        # mock login
        driver = self.driver
        driver.get("https://www.zybuluo.com/mdeditor#")
        driver.find_element_by_id("login").click()
        driver.find_element_by_id("inputEmail").clear()
        driver.find_element_by_id("inputEmail").send_keys("*******")
        driver.find_element_by_id("inputPassword").clear()
        driver.find_element_by_id("inputPassword").send_keys("*******")
        driver.find_element_by_name("form.submit").click()
        logging.info("login success.")

        # wait for articles id returned
        wait = WebDriverWait(driver, 10)
        element_ids = wait.until(custom_ec.elements_id_returned(
            locator=(By.XPATH, "//*[@class='file-item item']/a/span"),
            threshold=5
        ))
        logging.info("catch id list #" + str(element_ids))

        # for every articles id, reload the page, and mock click the 'export to file' button
        for element_id in element_ids:
            # reload the page, use javascript rather simple 'driver.refresh()'
            # because the latter seems don't contains the 'reload' action
            driver.execute_script("location='https://www.zybuluo.com/mdeditor#%s'" % element_id)
            driver.execute_script("location.reload()")
            logging.info("opening url -> " + "https://www.zybuluo.com/mdeditor#%s'" % element_id)
            logging.info("waiting for specific id span(#%s) show." % element_id)

            # waiting for a specific id span, which means the page's reloading finish
            wait.until(custom_ec.element_has_css_class(
                (By.ID, element_id), "whiter-on-black"
            ))
            logging.info("specific id span show.")

            # mock click 'export to file' button
            driver.find_element_by_xpath("//*[@id='preview-settings-button']/span").click()
            driver.find_element_by_id("download-markdown-submenu").click()
            logging.info("perform click setting menu, download submenu.")


if __name__ == "__main__":
    AppDynamicsJob().test_app_dynamics_job()
