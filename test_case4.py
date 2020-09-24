from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.chrome.options import Options
import unittest, time, re, json

class Screen(object):
    def __init__(self, driver):
        self.driver = driver

    def __call__(self, func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                now_time = time.strftime("%Y_%m_%d_%H_%M_%S")
                self.driver.get_screenshot_as_file(".\%s.png" %now_time)
                raise
        return inner

class Case4(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        self.driver=webdriver.Chrome(chrome_options=chrome_options)
        self.verificationErrors = []
        self.vars = {}

    def test_case4(self):
        driver = self.driver
        driver.get("https://www.baidu.com")
        driver.set_window_size(1366, 635)
        driver.find_element(By.ID, "kw").click()
        driver.find_element(By.ID, "kw").clear()
        driver.find_element(By.ID, "kw").send_keys(u"东方心绮楼")
        driver.find_element(By.ID, "kw").send_keys(Keys.ENTER)
        for i in range(60):
            try:
                if self.is_element_present(By.LINK_TEXT, u"东方心绮楼 - 百度百科"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        driver.find_element(By.LINK_TEXT, u"东方心绮楼 - 百度百科").click()
        driver.switch_to.window(driver.window_handles[1])
        driver.find_element(By.LINK_TEXT, u"秦心").click()
        driver.switch_to.window(driver.window_handles[2])
        driver.find_element(By.LINK_TEXT, u"秦心：作品《东方Project》中的角色").click()
        driver.switch_to.window(driver.window_handles[3])
        self.assertEqual(u"秦心", driver.find_element(By.XPATH, "//h1").text)

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.driver.get_screenshot_as_file(r".\%s.png" %__name__)
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
