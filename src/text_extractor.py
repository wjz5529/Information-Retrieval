# -*- coding: utf-8 -*-

'''
模块介绍：该模块用于从指定网页源码中提取正文
模块名称：正文提取, text_extractor.py
模块功能：
'''
import os
import re
import logging
from bs4 import BeautifulSoup
from datetime import datetime

class TextExtractor:
    def __init__ (self, file_dir='html', output_dir='text', log_dir='Log'):
        """初始化文本提取器类"""
        self.file_dir = file_dir
        self.output_dir = output_dir
        self.log_dir = log_dir

        # 创建输出目录
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"输出目录创建成功：{output_dir}")
        else:
            print(f"输出目录已存在：{output_dir}")

        # 创建日志文件目录
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            print(f"日志文件创建成功：{log_dir}")
        else:
            print(f"日志文件已存在：{log_dir}")

        self.logger = self._setup_logging()
        self.logger.info(f"文本提取器初始化完成，目标目录：{self.file_dir}")
        self.logger.info(f"文本保存目录：{self.output_dir}")
        self.logger.info(f"日志保存目录：{self.log_dir}")

    
    def _setup_logging(self):
        """配置日志系统"""
        # 创建logger
        self.logger = logging.getLogger('text_extractor')
        self.logger.setLevel(logging.DEBUG)
        
        # 创建文件handler
        log_file = os.path.join(self.log_dir, f"text_extractor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
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

    def extract_text(self):
        """从HTML文件中提取文本"""
        try:
            # 遍历文件夹中的所有HTML文件
            for filename in os.listdir(self.file_dir):
                if filename.endswith('.txt'):
                    # 读取网页源码文件
                    infilepath = os.path.join(self.file_dir, filename)
                    outfilepath = os.path.join(self.output_dir, filename)
                    with open(infilepath, 'r', encoding='utf-8') as file:                        
                        self.logger.info(f"成功读取{filename}文件")
                        html_content = file.read()
                        # 使用BeautifulSoup解析HTML
                        soup = BeautifulSoup(html_content, 'html.parser')
                        # 提取正文内容
                        body_text = soup.body.get_text() if soup.body else ''
                        # 清理文本
                        body_text = re.sub(r'\n\s*\n+', '\n\n', body_text.strip())
                        text = ''
                        for line in body_text.splitlines():
                            line = line.strip()
                            if not line:
                                continue
                            # 替换多余的空格
                            line = re.sub(r'\s+', '', line)
                            text += line + '\n'
 

                        with open(outfilepath, 'w', encoding='utf-8') as outfile:
                            outfile.write(text)
                            self.logger.info(f"成功提取{filename}文件的文本")
            self.logger.info("所有文件文本提取完成") 
                       
        except Exception as e:
            self.logger.error(f"提取文本失败：{e}")
            print(f"提取文本失败：{e}")
    
    def run(self):
        """运行文本提取器"""
        self.logger.info("开始提取文本")
        self.extract_text()
        self.logger.info("文本提取器运行完成")
        print("文本提取器运行完成")
    

if __name__ == "__main__":
    # 创建文本提取器实例
    extractor = TextExtractor()
    # 提取文本
    extractor.run()