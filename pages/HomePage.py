from selenium.webdriver.common.by import By


class HomePage:
    def __init__(self, driver):
        self.driver=driver

        self.About_dropdown_xpath="//span[@class='oxd-userdropdown-tab']//i[1]"
        self.logout_linktext="Logout"

    def click_about_dropdown(self):
        self.driver.find_element(By.XPATH, self.About_dropdown_xpath).click()

    def click_logout_link_test(self):
        self.driver.find_element(By.LINK_TEXT, self.logout_linktext).click()