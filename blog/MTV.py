from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options

class MTV():
    """
    自社のURLにログインするためのモジュール
    """
    def __init__(self, URL, AN, PW):
        self.URL = URL
        self.AN = AN
        self.PW = PW
    
    def login(self):
        #エラーをなくすコード。ブラウザ制御コメントを非表示化
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.use_chromium = True
        
        #ドライバー取得してログイン
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.get(self.URL)
        texts_account = driver.find_element_by_id("accountName")
        texts_password = driver.find_element_by_id("password")
        button_login = driver.find_element_by_id("login")

        texts_account.send_keys(self.AN)
        texts_password.send_keys(self.PW)
        button_login.click()
        
        return driver