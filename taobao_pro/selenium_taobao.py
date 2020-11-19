import time

from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from taobao_pro.models.MySQLModel import tb_mysql


class tb_index():
    def __init__(self):
        chrome_option = Options()
        chrome_option.add_argument("--disable-extensions")
        chrome_option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        self.driver = webdriver.Chrome(options=chrome_option)
        self.url = "https://www.taobao.com/"

    def main(self):
        try:
            self.driver.maximize_window()  # 很重要！！
        except:
            pass
        self.driver.get(self.url)
        if WebDriverWait(self.driver,100,1).until(EC.presence_of_element_located((By.XPATH,"//div[@class='service J_Service']"))):
            page_source = self.driver.page_source
            html = etree.HTML(page_source)
            info_dict = {}
            all_li = html.xpath("//ul[@class='service-bd']/li")
            for num in range(1,len(all_li)+1):
                info_dict['main_category'] = str(html.xpath("//ul[@class='service-bd']/li[{num}]/a/text()".format(num=num)))
                element = self.driver.find_element_by_xpath("//ul[@class='service-bd']/li[{num}]".format(num=num))
                ActionChains(self.driver).move_to_element(element).perform()
                page_source2 = self.driver.page_source
                html2 = etree.HTML(page_source2)
                div_style = html2.xpath("//div[@class='service-float-item clearfix']")
                for style in div_style:
                    style_text = style.xpath("./@style")[0]
                    if style_text == "display: block;":
                        all_div = style.xpath("./div[1]/div")
                        for div in all_div:
                            info_dict['second_category_name'] = div.xpath("./h5/text()")[0]
                            all_p_a = div.xpath("./p/a")
                            for p_a in all_p_a:
                                info_dict['category_name'] = p_a.xpath("./text()")[0]
                                info_dict['category_href'] = p_a.xpath("./@href")[0]
                                info_dict['crawl_time'] = time.strftime("%Y--%m--%d %H:%M:%S",time.localtime(time.time()))
                                tb_mysql.index_category_data(info_dict)

    def page_cookie(self,url):
        try:
            self.driver.maximize_window()  # 很重要！！
        except:
            pass
        self.driver.get(url)
        Cookies = self.driver.get_cookies()
        cookie_dict = {}
        for cookie in Cookies:
            # 写入文件
            # 此处大家修改一下自己文件的所在路径
            f = open('tb_cookie.txt', 'w', encoding='utf-8')
            cookie_dict[cookie['name']] = cookie['value']
            f.write(str(cookie_dict))
            f.close()


tb_selenium = tb_index()


if __name__ == '__main__':
    # tb_selenium.main()
    tb_selenium.page_cookie("https://s.taobao.com/search?q=%E8%80%81%E8%8A%B1%E9%95%9C")