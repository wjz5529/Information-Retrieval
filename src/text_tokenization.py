# -*- coding: utf-8 -*-

'''
模块介绍：该模块用于对正文进行分词处理
模块名称：正文分词, text_tokenization.py
模块功能：
'''

import jieba
import os
import logging
from datetime import datetime

class TextTokenization:
    def __init__(self, file_dir='text', output_dir='tokenized_text', log_dir='Log'):
        """初始化分词器"""
        self.file_dir = file_dir
        self.output_dir = output_dir
        self.log_dir = log_dir

        self.word_count = 0
        self.sentence_count = 0

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
        
        self.tokenizer = jieba
        self.logger = self._setup_logging()
        self.logger.info(f"分词器初始化完成，目标目录：{self.file_dir}")
        self.logger.info(f"分词结果保存目录：{self.output_dir}")
        self.logger.info(f"日志保存目录：{self.log_dir}")

    def _setup_logging(self):
        """配置日志系统"""
        # 创建logger
        self.logger = logging.getLogger('text_tokenization')
        self.logger.setLevel(logging.DEBUG)
        
        # 创建文件handler
        log_file = os.path.join(self.log_dir, f"text_tokenization_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
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

    def tokenize_text(self):
        """对文本进行分词"""
        try:
            # 遍历文件夹中的所有文件
            for filename in os.listdir(self.file_dir):
                if filename.endswith('.txt'):
                    infilepath = os.path.join(self.file_dir, filename)
                    outfilepath = os.path.join(self.output_dir, filename)
                    with open(infilepath, 'r', encoding='utf-8') as f:
                        text = f.read()

                    # 统计行数
                    for line in text.splitlines():
                        if line:
                            self.sentence_count += 1
                    
                    # 分词
                    tokens = self.tokenizer.cut(text)
                    tokenized_text = ' '.join(tokens)

                    # 统计词数
                    for token in tokenized_text:
                        if token:
                            self.word_count += 1

                    # 保存分词结果
                    with open(outfilepath, 'w', encoding='utf-8') as f:
                        f.write(tokenized_text)
                    
                    self.logger.info(f"分词完成，结果保存到：{outfilepath}")

        except Exception as e:
            self.logger.error(f"分词失败：{e}")

    def run(self):
        """运行分词器"""
        self.logger.info("开始运行分词器")
        self.tokenize_text()
        self.logger.info("分词器运行完成")
        print(f"单词数：{self.word_count}, 句子数：{self.sentence_count}")
        print("分词处理完成")

'''运行示例'''
if __name__ == "__main__":
    # 创建分词器实例
    tokenizer = TextTokenization()
    # 执行分词
    tokenizer.run()