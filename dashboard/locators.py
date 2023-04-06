from selenium.webdriver.common.by import By


class DashboardLocator():
    """
    Locators related to Dashboard page are defined here
    """
    btnDashboard = (By.XPATH, "//a[@data-testid='/dashboard']")
    # btnDashboard = (By.XPATH, "//span[text()='']")

    # tabOverview = (By.XPATH, "//a[@data-testid='fsnavtab-Overview']")
    tabTraffic = (By.XPATH, "//span[text()='Traffic']")

    txtGateways = (By.ID, "Aviatrix Gateways")
    txaGWs = (
        By.XPATH, "//div[@data-testid='dashChipTableRow']/div[1]/descendant::h6")
    # txaGWs = (
    #     By.XPATH, "//div[@id='root']/following-sibling::div/div[3]/div[2]/div[1]/descendant::h6")