from selenium.webdriver.common.by import By


class LoginLocator():
    """
    Locators related to login are defined here
    """
    txaUsername = (By.NAME, "Username")
    txaPassword = (By.NAME, "Password")

    btnLogin = (By.XPATH, "//button[@tabindex='0']")

    txaControllerIP = (By.NAME, "controllerIp")
    prgProgressbar = (By.CSS_SELECTOR, "div[role='progressbar']")

    txaServiceAccount = (By.NAME, "Service Account")
    txaServicePassword = (By.NAME, "Password")

    btnSubmit = (By.XPATH, "//button[text()='Submit']")

    txaCustomerID = (By.NAME, "CoPilot Customer ID")

    # Alert message locators
    dlgAlert = (
        By.CSS_SELECTOR, "div[role='alert']"
    )

    chkDiskOption = (By.ID, "enhanced-table-checkbox-0")
    btnStart = (By.XPATH, "//span[text()='Start']")
    btnFinish = (By.XPATH, "//span[text()='Finish']")

    btnOpen = (By.XPATH, "//button[@title='Open']")

