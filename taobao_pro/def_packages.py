import os
import re

from taobao_pro.selenium_taobao import tb_selenium

def get_cookie(url):
    if os.path.exists("tb_cookie.txt"):
        with open("tb_cookie.txt", "r") as f:
            try:
                cookie = f.readlines(1)[0]
            except:
                tb_selenium.page_cookie(url)
                cookie = f.readlines(1)[0]
        r = re.compile(r"'(.*?)': '(.*?)'")
        result = r.findall(cookie)
        cookie_dict = {}
        for item in result:
            cookie_dict[item[0]] = item[1]
        return cookie_dict
    else:
        tb_selenium.page_cookie(url)
        get_cookie(url)


def handle_click_url(category_href,value, pagesize):
    click_url = "{category_href}&sort=sale-desc&cps=yes&ppath={value}&s={pagesize}".format(
        category_href=category_href,value=value, pagesize=pagesize)
    return click_url

def handle_next_url(category_href, pagesize):
    next_url = "{category_href}&sort=sale-desc&cps=yes&s={pagesize}".format(
        category_href=category_href, pagesize=pagesize)
    return next_url


def tb_log(log):
    with open("tb_log.txt","a+",encoding="utf-8") as f:
        f.write(log + "\n")
    f.close()