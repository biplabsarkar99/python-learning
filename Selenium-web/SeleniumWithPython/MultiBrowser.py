from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys #what is the use?

def main():
    driver =wd.Chrome()
    #driver = wd.Safari() #check error def
    driver.get("http://newtours.demoaut.com/")
    print ("Title :: %s" %driver.title)
    print("URL :: %s" % driver.current_url)
    print("HTML code source :: %s" % driver.page_source)

if __name__=='__main__':
    main()