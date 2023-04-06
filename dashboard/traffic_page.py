from .dashboard_page import DashboardPage


class TrafficPage(DashboardPage):
    """
    Dashboard -> Traffic
    This is Traffice Page class which inherits from DashboardPage
    Traffice implementations are defined here
    """

    def click_tab(self):
        """
        This method is to clicl Traffic tab
        """
        try:
            self.click_element(self.locator.tabTraffic)
        except RuntimeError as e:
            raise Exception("Failed to click Traffic tab: %s" % e)
