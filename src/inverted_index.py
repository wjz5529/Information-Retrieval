# -*- coding: utf-8 -*-

'''
模块介绍：该模块用于构建文件的倒排索引
模块名称：构建倒排索引, inverted_index.py
模块功能：
'''

import jieba
import os
import logging
from datetime import datetime

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

        self.index = {}
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
    
    def build_inverted_index(self):