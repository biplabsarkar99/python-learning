from selenium import webdriver
import time
import unittest as ut
from POMProjectDemo.Pages.loginPage import LoginPage
from POMProjectDemo.Pages.homePage import HomePage
import os
import sys
#Below step is an alternative for making package references
#Alternate make every folder as package
#sys.path.append(os.path.join(os.path.dirname(__file__),"...","..."))
import HtmlTestRunner as HTR
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Simple test example
=====================

driver = webdriver.Chrome(executable_path="/Users/tuna/Downloads/WebDriver/chromedriver")
driver.implicitly_wait(10)
driver.maximize_window()

#Temp HRM url
driver.get("https://opensource-demo.orangehrmlive.com/")

#Locating username/password fields
driver.find_element_by_id("txtUsername").send_keys("Admin")
driver.find_element_by_id("txtPassword").send_keys("admin123")

#Click Login button
driver.find_element_by_id("btnLogin").click()
#In home page click welcome link (having About us and Logout dropdown)
driver.find_element_by_id("welcome").click()

#Click Logout link
driver.find_element_by_link_text("Logout").click()
time.sleep(2)

driver.close()
driver.quit()
print ("Test completed")
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

"""
Implementing as a UnitTest case object
To Run: Create new run configuration , andselect the module LoginTest UT.
To Run from command line:
To Run from script add call to ut.()
"""

report_folder = '/Users/tuna/Documents/WellsFargo/Learning/python-learning/Selenium-web/POMProjectDemo/reports/'

class LoginTest(ut.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.driver = webdriver.Chrome(
            executable_path="/Users/tuna/Downloads/WebDriver/chromedriver")
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()

    def test_login_valid(self):
        '''
        Valid Login test case scenario
        :return:
        '''

        """
        # This is standalone execution.
        # Locating username/password fields
        self.driver.find_element_by_id("txtUsername").send_keys("Admin")
        self.driver.find_element_by_id("txtPassword").send_keys("admin123")
        # Click Login button
        self.driver.find_element_by_id("btnLogin").click()
        # In home page click welcome link (having About us and Logout dropdown)
        self.driver.find_element_by_id("welcome").click()
        # Click Logout link
        self.driver.find_element_by_link_text("Logout").click()
        time.sleep(2)
        """
        #Execution using POM
        driver = self.driver
        driver.get("https://opensource-demo.orangehrmlive.com/")
        login = LoginPage(driver)

        #Login test
        login.enter_username("Admin")
        login.enter_password("admin123")
        login.click_login()

        #Home Page test
        home = HomePage(driver)
        home.click_welcome()
        home.click_logout()

        time.sleep(2)

    def test_invalid_login(self):
        # Execution using POM
        driver = self.driver
        driver.get("https://opensource-demo.orangehrmlive.com/")
        login = LoginPage(driver)

        # Login test
        login.enter_username("Admin")
        login.enter_password("admin123")
        login.click_login()

        # Home Page test
        home = HomePage(driver)
        home.click_welcome()
        home.click_logout()

        time.sleep(2)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.driver.close()
        cls.driver.quit()
        print("Test completed")

if __name__=='__main__':
    ut.main(testRunner=HTR.HTMLTestRunner(output=report_folder))
    #print ("checkpoint")