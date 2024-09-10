import allure
# demo website used:OrangeHRM
#pytest
import pytest
#importing POM pages
from pages.LoginPage import LoginPage
from pages.HomePage import HomePage
from Utils import Utils as Utils

#@pytest.mark.use fixtures('test_setup')
class TestLogin:

    def test_login(self):
        try:
            driver=self.driver
            driver.get(Utils.URL)
            login=LoginPage(driver)
            login.enter_username(Utils.USERNAME)
            login.enter_password(Utils.PASSWORD)
            login.click_login()
            assert driver.title =='OrangeHRM'
        except AssertionError as error:
            print(error)
            allure.attach(self.driver.get_screenshot_as_png(),name="screenshot",
                          attachment_type=allure.attachment_type.PNG)

            raise

    def test_homepage(self):
        driver = self.driver
        driver.implicitly_wait(5)
        homepage=HomePage(driver)
        homepage.click_about_dropdown()
        homepage.click_logout_link_test()
        assert driver.title == 'OrangeHRM'





