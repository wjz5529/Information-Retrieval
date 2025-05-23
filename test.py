import requests
from bs4 import BeautifulSoup
import re

# 获取对应网页源码
def get_html(url):
    response = requests.get(url, timeout=30)
    response.encoding = 'utf-8'
    return response.text

# 将内容写入文件
def write_to_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

url = 'http://scst.suda.edu.cn/'
html = get_html(url)
# 将网页源码写入文件
write_to_file('webpage.html', html)
# 创建变量，使其成为BeautifulSoup实例
soup = BeautifulSoup(html, 'lxml')

for link in soup.find_all('a', href=True):
    # 获取链接
    href = link['href']
    print(f"href链接：{href}")
    # 判断链接是否有效
    if re.match(r'http://scst.suda.edu.cn/.*', href):
        print(href)