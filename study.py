from selenium import webdriver
import time


def fun_3():
    # province省份，creditcode统一社会信用代码，company市场主体(企业名字)，cpmc地理标志(特产)，
    url_search = 'https://jyboss-test.yy.com/n/zhuiya_recommend/zhuiya_recommend_manage'

    # 无头浏览
    option = webdriver.ChromeOptions()
    option.add_argument("headless")
    chrome_path = r'E:\AirtestIDE\chromedriver.exe'
    browser = webdriver.Chrome(options=option)
    browser.get(url_search)
    # 延迟10秒
    time.sleep(10)
    cookies = browser.get_cookies()
    print(cookies)
    print('ASP.NET_SessionId的值:', cookies[0].get('value'))
    # 关闭浏览器
    browser.close()



if __name__ == '__main__':
    fun_3()