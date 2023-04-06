import time

from selenium.webdriver.common.keys import Keys

from ..basepage import BasePage
from .locators import LoginLocator


class LoginPage(BasePage):
    """
    This is Login Page class which inherits from BasePage
    Login implementations are defined here
    """
    locator = LoginLocator

    def input_username(self, user):
        """
        This method is to input username
        @param user: user name for Copilot
        """
        try:
            self.input_text(self.locator.txaUsername, user)
        except RuntimeError as e:
            raise Exception("Failed to input username: %s" % e)

    def input_password(self, pwd):
        """
        This method is to input password
        @param pwd: password for Copilot
        """
        try:
            self.input_text(self.locator.txaPassword, pwd)
        except RuntimeError as e:
            raise Exception("Failed to input password: %s" % e)

    def click_login_button(self):
        """
        This method is to click login button
        """
        try:
            self.click_element(self.locator.btnLogin)
        except RuntimeError as e:
            raise Exception("Failed to click login button: %s" % e)

    def capture_alert(self, timeout=3):
        """
        This method is to catpturing alert
        """
        if self.is_element_visible(self.locator.dlgAlert, timeout=timeout):
            err = self.get_element(self.locator.dlgAlert).text
            if "Succesfully setup dynamic disk storage" in err:
                pass
            else:
                raise ValueError(err)

    def handle_initial_login(self, user, pwd, controller_ip, customer_id):
        """
        This method is to handle possible login scenarios
        @param user: user name for Copilot
        @param pwd: password for Copilot
        @param controller_ip: controller ip
        """
        is_ctrlip_checked = False
        is_custid_checked = False
        is_service_checked = False

        start_time = time.time()
        while ("dashboard" not in self.current_ipaddr()) and (time.time() - start_time < int(360)):
            # handle controllerip input
            if not is_ctrlip_checked and self.is_element_visible(self.locator.txaControllerIP, timeout=1):
                is_ctrlip_checked = True
                self.log.info("Entering Controller IP ...")
                self.input_text(self.locator.txaControllerIP, controller_ip)
                self.click_element(self.locator.btnLogin)
                time.sleep(5)
                if self.is_element_visible(self.locator.prgProgressbar, timeout=1):
                    raise RuntimeError(
                        "Failed to connect Controller, please check Controller %s" % controller_ip)
            # handle customer id input
            elif not is_custid_checked and self.is_element_visible(self.locator.txaCustomerID, timeout=1):
                is_custid_checked = True
                self.log.info("Entering Customer ID ...")
                self.input_text(self.locator.txaCustomerID, customer_id)
                self.click_element(self.locator.btnSubmit)
                # time.sleep(3)
            # handle service account input
            elif not is_service_checked and self.is_element_visible(self.locator.txaServiceAccount, timeout=1):
                is_service_checked = True
                self.log.info("Entering Service Account/Password ...")
                self.input_text(self.locator.txaServiceAccount, user)
                self.input_text(self.locator.txaServicePassword, pwd)
                self.click_element(self.locator.btnSubmit)
                # time.sleep(3)

            # handle Disk Setup
            elif "initialdisk" in self.current_ipaddr():
                self.log.info("Handling Disk Setup ...")
                # self.click_element(self.locator.chkDiskOption)
                self.click_element(self.locator.btnOpen)
                self.actionchains().send_keys(
                    Keys.PAGE_DOWN).send_keys(Keys.ENTER).send_keys(Keys.ESCAPE).perform()
                self.click_element(self.locator.btnStart)
                self.click_element(self.locator.btnFinish, timeout=300)
                time.sleep(3)
        self.capture_alert()
