import os
import time
import logging

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException


class BasePage:
    """
    This is Parent class where defines common page implementations
    """

    IMG_DIR = os.path.join(os.environ.get(
        "REGRESSION_HOME"), "avxt/screenshot")

    def __init__(self, driver: webdriver):
        self.log = logging.getLogger(__name__)
        self.driver = driver

    def actionchains(self):
        """
        This method is to return ActionChains object
        """
        return (webdriver.ActionChains(self.driver))

    def execute_script(self, cmd, element=None):
        """
        This method is to execute java script
        """
        if element:
            self.driver.execute_script(cmd, element)
        else:
            self.driver.execute_script(cmd)

    def wait_element_clickable(self, loc, timeout=10, frequency=0.5):
        """
        This method is to wait required element to be clickble
        @param loc: locators to locate element(definition is in Locators.py)
        @param timeout: default is 10 secs
        @param frequency: default is 0.5 secs
        """
        ignored_exceptions = (StaleElementReferenceException,)
        try:
            WebDriverWait(self.driver, timeout, frequency, ignored_exceptions=ignored_exceptions).until(
                EC.element_to_be_clickable(loc))
        except Exception:
            self.log.error("wait_element_clickable has error:", exc_info=True)
            raise Exception(f"{loc} is not clickable in {timeout} seconds")

    def wait_element_visible(self, loc, timeout=10, frequency=0.5):
        """
        This method is to wait required element to be visible
        @param loc: locators to locate element(definition is in Locators.py)
        @param timeout: default is 10 secs
        @param frequency: default is 0.5 secs
        """
        ignored_exceptions = (StaleElementReferenceException,)
        try:
            WebDriverWait(self.driver, timeout, frequency, ignored_exceptions=ignored_exceptions).until(
                EC.visibility_of_element_located(loc))
        except Exception:
            self.log.error("wait_element_visible has error:", exc_info=True)
            raise Exception(f"{loc} is not visible in {timeout} seconds")

    def wait_element_present(self, loc, timeout=10, frequency=0.5):
        """
        This method is to wait required element to be presented
        @param loc: locators to locate element(definition is in Locators.py)
        @param timeout: default is 10 secs
        @param frequency: default is 0.5 secs
        """
        try:
            WebDriverWait(self.driver, timeout, frequency).until(
                EC.presence_of_element_located(loc))
        except Exception:
            self.log.error("wait_element_present has error:", exc_info=True)
            raise Exception(f"{loc} is not presented in {timeout} seconds")

    def get_element(self, loc, focus=False):
        """
        This method is to do get action
        @param loc: locators to locate element(definition is in Locators.py)
        @return: element object
        """
        try:
            ele = self.driver.find_element(*loc)
            if focus:
                self.driver.execute_script(
                    "arguments[0].scrollIntoView();", ele)
        except NoSuchElementException:
            raise Exception("Failed to get element: %s" % loc)
        else:
            return ele

    def get_elements(self, loc):
        """
        This method is to do get action
        @param loc: locators to locate element(definition is in Locators.py)
        @return: list of element object
        """
        try:
            eles = self.driver.find_elements(*loc)
        except NoSuchElementException:
            raise Exception("Failed to get elements: %s" % loc)
        else:
            return eles

    def click_element(self, loc, timeout=10, frequency=0.5):
        """
        This method is to do click action
        @param loc: locators to locate element(definition is in Locators.py)
        @param timeout: default is 10 secs
        @param frequency: default is 0.5 secs
        """
        self.wait_element_clickable(loc, timeout, frequency)
        ele = self.get_element(loc)
        try:
            ele.click()
        except NameError as e:
            raise Exception("Failed to click element: %s" % e)

    def input_text(self, loc, value, timeout=10, frequency=0.5):
        """
        This method is to do input text
        @param loc: locators to locate element(definition is in Locators.py)
        @param value: value to be entered
        @param timeout: default is 10 secs
        @param frequency: default is 0.5 secs
        """
        self.wait_element_visible(loc, timeout, frequency)
        ele = self.get_element(loc)
        try:
            ele.send_keys(value)
        except Exception as e:
            raise Exception("Failed to send keys: %s" % e)

    def save_img(self, img_description):
        now = time.strftime("%Y-%m-%d %H-%M-%S ", time.localtime())
        img_path = os.path.join(self.IMG_DIR, now + img_description + ".png")
        try:
            self.driver.save_screenshot(img_path)
        except NameError as e:
            raise Exception("Failed to take screenshot: %s" % e)

    def is_element_visible(self, loc, timeout=3, frequency=0.5):
        """
        This method is to check if required element present or not
        @param loc: locators to locate element(definition is in Locators.py)
        @param timeout: default is 3 secs
        @param frequency: default is 0.5 secs
        @return: True or False
        """
        try:
            WebDriverWait(self.driver, timeout, frequency).until(
                EC.visibility_of_element_located(loc))
            return True
        except Exception:
            return False

    def is_element_present(self, loc, timeout=3, frequency=0.5):
        """
        This method is to check if required element present or not
        @param loc: locators to locate element(definition is in Locators.py)
        @param timeout: default is 3 secs
        @param frequency: default is 0.5 secs
        @return: True or False
        """
        try:
            WebDriverWait(self.driver, timeout, frequency).until(
                EC.presence_of_element_located(loc))
            return True
        except Exception:
            return False

    def current_ipaddr(self):
        """
        This method is to retrieve current page url
        @return: page url
        """
        return self.driver.current_url

    def refresh_page(self):
        """
        This method is to refresh page
        """
        self.driver.refresh()

    def click_darkmode(self):
        """
        This method is to click darkmode function
        """
        svgDarkMode = (By.XPATH, "//*[name()='svg' and @data-testid='DarkModeOutlinedIcon']")
        self.click_element(svgDarkMode)
        time.sleep(3)

    def release_info(self, restore=True, display_time=3):
        """
        This method is to check release info button
        @param restore: True = return to main page. False = do nothing after clicking
        @display_time: secs to display release info content
        """
        btnReleaseInfo = (
            By.XPATH,
            "//button[@aria-label='open drawer']/ancestor::div/div[2]/button[3]"
        )
        btnClose = (By.XPATH, "//button[@aria-label='close']")
        self.click_element(btnReleaseInfo)
        time.sleep(display_time)
        if restore:
            self.click_element(btnClose)

    def about(self, restore=True, display_time=3):
        """
        This method is to check release info button
        @param restore: True = return to main page. False = do nothing after clicking
        @display_time: secs to display about content
        """
        btnAbout = (
            By.XPATH,
            "//button[@aria-label='open drawer']/ancestor::div/div[2]/div[1]/button[1]"
        )
        self.click_element(btnAbout)
        time.sleep(display_time)
        if restore:
            webdriver.ActionChains(self.driver).send_keys(
                Keys.ESCAPE).perform()

    def user_info(self):
        svgProfile = (By.XPATH, "//button[@aria-label='User Profile']")
        self.click_element(svgProfile)
        time.sleep(1)
        txaUserInfo = (By.CSS_SELECTOR, "div.FsPopover-backdrop div div div:nth-child(2) div ul li")
        ele = self.get_element(txaUserInfo)
        return ele.text

    def logout(self, confirm=True):
        """
        This method is to check release info button
        @param confirm: True: click Logout. False: return to main page
        """
        btnLogout = (
            By.XPATH,
            "//button[@aria-label='open drawer']/ancestor::div/div[2]/button[5]"
        )
        mnuLogout = (By.XPATH, "//li[text()='Logout']")
        self.click_element(btnLogout)
        if confirm:
            self.click_element(mnuLogout)
        else:
            webdriver.ActionChains(self.driver).send_keys(
                Keys.ESCAPE).perform()

    def skip_introduciton(self):
        btnSkip = (By.XPATH, "//button[text()='Skip']")
        if self.is_element_visible(btnSkip, timeout=5):
            self.click_element(btnSkip)
