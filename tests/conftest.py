import os
from datetime import datetime

import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from webdriver_manager.firefox import GeckoDriverManager


#instantiate the driver session based on the given browser name
@pytest.fixture(scope="class", autouse=True)
def test_setup(request):
    global driver
    browser=request.config.getoption("--browser")
    if browser =='chrome':
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    elif browser =='firefox':
        driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

    driver.implicitly_wait(5)
    driver.maximize_window()
    request.cls.driver = driver
    print("test_setup done")
    yield
    driver.close()
    driver.quit()
    print("test completed")

def pytest_addoption(parser):
    parser.addoption("--browser",default="chrome", help="Type in browser name")

# https://docs.pytest.org/en/7.1.x/reference/reference.html#pytest.hookspec.pytest_configure
def pytest_configure(config):    #
    config._metadata = None
    config.option.htmlpath = _create_report_path() + '/' + 'Test_Automation_Report_' \
                             + datetime.now().strftime("%d-%m-%Y %H-%M-%S") + ".html"

def _create_report_path():
    # Get the current directory
    current_directory = os.getcwd()
    # Create the full path for the new folder
    print(current_directory)
    new_folder_path = os.path.join(current_directory, 'Test_Automation_Report')
    if not os.path.exists(new_folder_path):
        # Create the new folder
        os.mkdir(new_folder_path)
    return new_folder_path


def pytest_html_report_title(report):
    report.title = 'Test Automation Report'

def _capture_screenshot(file_name):
    screenshot_path = _create_report_path()
    driver.save_screenshot(screenshot_path + '\\' + file_name)
    return screenshot_path

#PyTest Plugin to take and embed screenshot in html report, whenever test fails
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_") + ".png"
            _capture_screenshot(file_name)
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_name
                extra.append(pytest_html.extras.html(html))
        report.extra = extra

