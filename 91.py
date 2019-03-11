# -*- coding: utf_8 -*-
import os
import re
import requests

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from urllib import request
from bs4 import BeautifulSoup


def get_data_selenium(video_url):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    settings = dict(DesiredCapabilities.ANDROID)  # 设置userAgent

    driver = webdriver.Chrome(options=options, desired_capabilities=settings)
    driver.get(video_url)
    source = driver.page_source
    driver.close()
    return source


def get_tid_url(tid):
    return "http://f.91p02.rocks/viewthread.php?tid=" + tid + "&extra=page%3D2%26amp%3Bfilter%3Ddigest"


def save_image(img_name, path, name):
    img_link = "http://f.91p02.rocks/" + img_name
    img_response = requests.get(img_link)
    save_path = "/data/spider/91porn/" + path + "/"

    if os.path.exists(save_path) is False:
        os.mkdir(save_path)

    with open(save_path + name, "wb") as code:
        code.write(img_response.content)


def get_data_urlib(url):
    list_response = request.urlopen(url).read()
    response = BeautifulSoup(list_response, "html.parser").prettify().strip()
    return response


if __name__ == '__main__':

    page_num = 1
    while True:
        print("当前页数:" + str(page_num))
        url = "http://f.91p02.rocks/forumdisplay.php?fid=19&filter=digest&page=" + str(page_num)
        page_source = get_data_selenium(url)

        regular = re.compile("<span id=\"thread_([0-9]+)\">")
        img_regular = re.compile("file=\"(.*)\" width")
        title_regular = re.compile("<h1>(.*)</h1>")
        result = re.findall(regular, page_source)

        index = 0
        while index < len(result):
            if str(result[index]) == "181956":
                index = index + 1
                print(result[index])
                continue

            url = get_tid_url(result[index])
            data = get_data_selenium(url)
            img_list = re.findall(img_regular, data)
            title_list = re.findall(title_regular, data)
            title = "无名"
            if len(title_list) >= 1:
                title = title_list[0]

            print("命中帖子:" + title + "共计" + str(len(img_list)) + "张图片")
            img_index = 0
            while img_index < len(img_list):
                print("正在下载第" + (str(img_index + 1)) + "张图片")
                img_name = str(img_list[img_index])
                img_save_name = img_name.split("/")[1]
                save_image(img_list[img_index], title, img_save_name)
                img_index = img_index + 1
            index = index + 1
        page_num = page_num + 1

