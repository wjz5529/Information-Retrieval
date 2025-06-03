# -*- coding: utf-8 -*-

'''
模块介绍：该模块用于构建文件的倒排索引
模块名称：构建倒排索引, inverted_index.py
模块功能：
'''

from collections import defaultdict
import os
import logging
from datetime import datetime
import re

class InvertedIndex:
    def __init__(self, file_dir='tokenized_text', outfilepath = 'inverted.index', log_dir='Log'):
        '''初始化倒排索引类'''
        self.file_dir = file_dir
        self.outfilepath = outfilepath
        self.log_dir = log_dir

        # 创建输出目录
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
            print(f"输出目录创建成功：{file_dir}")
        else:
            print(f"输出目录已存在：{file_dir}")
        # 创建日志文件目录
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            print(f"日志文件创建成功：{log_dir}")
        else:
            print(f"日志文件已存在：{log_dir}")

        self.inverted_index = defaultdict(set)  # {term: set(doc_names)}
        self.logger = self._setup_logging()
        self.logger.info(f"倒排索引初始化完成，目标目录：{self.file_dir}")
        self.logger.info(f"倒排索引结果保存目录：{self.outfilepath}")
        self.logger.info(f"日志保存目录：{self.log_dir}")

    def _setup_logging(self):
        """配置日志系统"""
        # 创建logger
        self.logger = logging.getLogger('inverted_index')
        self.logger.setLevel(logging.DEBUG)
        
        # 创建文件handler
        log_file = os.path.join(self.log_dir, f"inverted_index_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
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
    
    def clean_text(self, text):
        """清理文本，移除非中文字符"""
        return text
    
    def build_inverted_index(self):
        """构建倒排索引"""
        self.logger.info("开始构建倒排索引")
        
        # 遍历对应目录下所有文件
        for filename in os.listdir(self.file_dir):

            file_path = os.path.join(self.file_dir, filename)
            if not os.path.isfile(file_path):
                continue
            
            with open(file_path, 'r', encoding='utf-8') as f:
                self.logger.info(f"处理文件: {filename}")
                content = f.read()
                cleaned_content = self.clean_text(content)
                for term in cleaned_content.split():
                    self.inverted_index[term].add(filename)
                self.logger.info(f"文件 {filename} 处理完成")

        self.logger.info("倒排索引构建完成")
                
    def save_index(self):
        """保存倒排索引到文件"""
        self.logger.info(f"保存倒排索引到 {self.outfilepath}")
        with open(self.outfilepath, 'w', encoding='utf-8') as f:
            for term, doc_names in self.inverted_index.items():
                f.write(f"{term}: {','.join(doc_names)}\n")
        self.logger.info("倒排索引保存完成")

    def run(self):
        """运行倒排索引构建流程"""
        self.logger.info("开始运行倒排索引构建")
        self.build_inverted_index()
        self.save_index()
        self.logger.info("倒排索引构建流程完成")

if __name__ == "__main__":
    indexer = InvertedIndex()
    indexer.run()