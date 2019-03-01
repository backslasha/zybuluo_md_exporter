from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By


class elements_id_returned(object):
    """ An expectation for checking that all element ids that I need is returned
    """

    def __init__(self, locator, threshold):
        self.threshold = threshold
        self.locator = locator

    def __call__(self, driver):
        try:
            elements = driver.find_elements(
                by=self.locator[0] or By.ID,
                value=self.locator[1] or None
            )
            if elements.__len__() < self.threshold:
                return None
            elements_id = list(map(
                lambda we: we.get_attribute('id'),
                elements
            ))
            return elements_id
        except StaleElementReferenceException:
            return None


class element_has_css_class(object):
    """An expectation for checking that an element has a particular css class.

    locator - used to find the element
    returns the WebElement once it has the particular css class
    """

    def __init__(self, locator, css_class):
        self.locator = locator
        self.css_class = css_class

    def __call__(self, driver):
        try:
            element = driver.find_element(*self.locator)  # Finding the referenced element
            if self.css_class in element.get_attribute("class"):
                return element
            else:
                return False
        except StaleElementReferenceException:
            return False
