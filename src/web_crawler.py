# -*- coding: utf-8 -*-

'''
模块介绍：该模块用于爬取指定网页并提取网页源码信息
模块名称：网页爬虫, web_crawler.py
模块功能：
'''
import requests
from bs4 import BeautifulSoup
import re
import os
import logging
from datetime import datetime
import hashlib

# 定义网页爬虫类
class WebCrawler:
    def __init__ (self, base_url, output_dir="html", log_dir="Log", max_urls=1000):
        """初始化爬虫类"""
        self.base_url = base_url
        self.output_dir = output_dir
        self.max_urls = max_urls
        self.log_dir = log_dir

        self.url_queue = set() # 用于存储待爬取的URL队列
        self.current_url_count = 0 # 记录已经保存的网页数量
        self.current_url = None # 当前正在爬取的URL

        # 创建输出目录
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"输出目录创建成功：{output_dir}")
        else:
            print(f"输出目录已存在：{output_dir}")

        # 创建日志文件
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            print(f"日志文件创建成功：{log_dir}")
        else:
            print(f"日志文件已存在：{log_dir}")

        self.logger = self._setup_logging()
        self.logger.info(f"爬虫初始化完成，目标网站：{self.base_url}")
        self.logger.info(f"网页源码保存目录：{self.output_dir}")
        self.logger.info(f"日志保存目录：{self.log_dir}")

    def _setup_logging(self):
        """配置日志系统"""
        # 创建logger
        self.logger = logging.getLogger('web_crawler')
        self.logger.setLevel(logging.DEBUG)
        
        # 创建文件handler
        log_file = os.path.join(self.log_dir, f"web_crawl_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # 创建控制台handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 创建formatter并添加到handler
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 添加handler到logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        self.logger.info("日志系统配置完成")

        return self.logger
    
    # 添加待爬取的URL
    def add_url(self, url):
        self.url_queue.add(url)
    
    # 获取对应网页源码
    def get_html(self, url):
        try:
            response = requests.get(url, timeout=30)
            response.encoding = 'utf-8'
            self.logger.info(f"成功获取{url}网页源码")
            return response.text

        except requests.RequestException as e:
            self.logger.error(f"获取{url}网页源码失败：{e}")
            return None
    
    # 将网页源码写入文件
    def write_to_file(self, filename, url, html):
        try:
            filepath = os.path.join(self.output_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)
            self.logger.info(f"网页{url}源码已保存到：{filepath}")
        except Exception as e:
            self.logger.error(f"保存{url}网页源码失败：{e}")
            return None

    # 提取与当前网页相关的URL
    def extract_links(self, url, html):
        try:
            soup = BeautifulSoup(html, 'lxml')
            for link in soup.find_all('a', href=True):
                href = link['href']
                # 判断当前链接是否为静态链接
                if href.endswith('.html') or href.endswith('.htm'):
                    # 判断是否为相对链接
                    if re.match(rf'{url}.*', href):
                        self.add_url(href)
                    else:
                        self.add_url(url + href)
        except Exception as e:
            self.logger.error(f"提取{url}网页链接失败：{e}")
            return None
        
    def run(self):
        self.logger.info("爬虫开始运行")
        self.add_url(self.base_url)
        while self.url_queue and self.current_url_count < self.max_urls:
            self.current_url = self.url_queue.pop()
            self.logger.info(f"正在爬取：{self.current_url}")
            html = self.get_html(self.current_url)

            if html:
                self.write_to_file(f"{hashlib.md5((self.current_url).encode()).hexdigest()}.txt", self.current_url, html)
                self.extract_links(self.current_url, html)              
                self.current_url_count += 1
                self.logger.info(f"已爬取{self.current_url}，当前已保存网页数量：{self.current_url_count}")
        
        self.logger.info("爬虫运行结束")

# 示例用法
if __name__ == "__main__":
    base_url = "http://scst.suda.edu.cn/"
    crawler = WebCrawler(base_url)
    crawler.run()