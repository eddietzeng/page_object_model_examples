import time

from selenium.webdriver.common.keys import Keys

from .dashboard_page import DashboardPage


class DashboardOverviewPage(DashboardPage):
    """
    Dashboard -> Overview
    This is Overview Page class which inherits from DashboardPage
    Overview implementations are defined here
    """

    def click_tab(self):
        """
        This method is to click Overview tag
        """
        try:
            self.click_element(self.locator.tabOverview)
        except RuntimeError as e:
            raise Exception("Failed to click Overview tag: %s" % e)

    def click_aviatrix_gateways_and_retrieve_gws(self):
        """This method is to click Aviatrix Gateways and return gateways
        :return: gateways information
        """
        try:
            self.click_element(self.locator.txtGateways)
            time.sleep(5)
            eles = self.get_elements(self.locator.txaGWs)
            gw_info = [e.text for e in eles]
            return gw_info

        except RuntimeError as e:
            raise Exception("Failed to Aviatrix Gateways: %s" % e)

        finally:
            self.actionchains().send_keys(Keys.ESCAPE).perform()
