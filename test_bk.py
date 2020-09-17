from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import unittest, requests, json

class Bk(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.vars = {}

    def test_bk_search_business(self):
        url = "http://paas.canwaytest3.com/api/c/compapi/v2/cc/search_business/"
        headers = {"Accept": "application/json"}
        params = {
            "bk_app_code": "shinkirou",
            "bk_app_secret": "dd52e08c-5fca-4dc8-9a8e-5f20fb2ae2ae",
            "bk_username": "admin",
            "blueking_language": "zh-hans",
            "fields": [
                "bk_biz_id",
                "bk_biz_name"
            ]
        }
        res = requests.post(url, json=params, headers=headers, verify=False)
        search = json.loads(res.content)
        businessList = search["data"]["info"]
        for i in businessList:
            print(str(i))

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
