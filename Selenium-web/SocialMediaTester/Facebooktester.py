from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

def main():

    # Step 1) Open Chrome
    browser = webdriver.Chrome()
    # Step 2) Navigate to Facebook
    browser.get("http://www.facebook.com")
    # Step 3) Search & Enter the Email or Phone field & Enter Password
    username = browser.find_element_by_id("email")
    password = browser.find_element_by_id("pass")
    submit = browser.find_element_by_id("loginbutton")
    username.send_keys("biplab.sarkar99@gmail.com")
    password.send_keys("pass123")
    # Step 4) Click Login
    submit.click()
    wait = WebDriverWait(browser, 5)
    page_title = browser.title
    print("Page title :: %s" %page_title)
    assert page_title == "Facebook – log in or sign up"

if __name__ == '__main__':
    main()