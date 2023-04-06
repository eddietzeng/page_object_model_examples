from ..basepage import BasePage
from .locators import DashboardLocator


class DashboardPage(BasePage):
    """
    This is Dashboard Page class which inherits from BasePage
    Dashboard implementations are defined here
    """
    locator = DashboardLocator

    def click_main_page(self):
        """
        This method is to click and check Dashboard page
        """
        try:
            self.click_element(self.locator.btnDashboard)
        except RuntimeError as e:
            raise Exception("Faield to click Dashboad page: %s" % e)
