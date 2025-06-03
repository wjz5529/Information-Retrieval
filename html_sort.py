# -*- coding: utf-8 -*-

'''
模块介绍：该模块用于对网页文本进行相关性排序
模块名称：网页相关性排序, html_sort.py
模块功能：
'''

import os
import math
import re
from collections import defaultdict, Counter

class HtmlSort():
    def __init__(self, indexfilepath='inverted.index', outfilepath = 'query_result.txt', infiledir = "tokenized_text", log_dir='Log'):
        self.indexfilepath = indexfilepath
        self.outfilepath = outfilepath
        self.infiledir = infiledir
        self.log_dir = log_dir

        self.load_inverted_index()
        self.compute_doc_vectors()

    def load_inverted_index(self):
        """
        加载倒排索引文件文件格式为：
        word1: doc1, doc2, doc3, ...
        word2: doc4, doc5, ...
        """
        inverted_index = defaultdict(set)
        all_docs = set()

        with open(self.indexfilepath, 'r', encoding='utf-8') as f:
            for line in f:
                colon_pos = line.rfind(':')
                if colon_pos == -1:
                    continue
                if colon_pos == 1:
                    term = line[0]

                term = line[:colon_pos]
                docs = line[colon_pos + 1:].strip().split(',')

                for doc in docs:
                    inverted_index[term].add(doc)
                    all_docs.add(doc)
        
        self.inverted_index = inverted_index
        self.all_docs = all_docs

        return inverted_index, all_docs
    
    def compute_tf(self, doc, term):
        """
        计算文档中词项的TF值
        """
        count_appear = 0    # 词项出现次数
        count_sum = 0       # 文档总词数

        # 读取文档内容
        filepath = os.path.join(self.infiledir, doc)
        with open(filepath, 'r', encoding = 'utf-8') as f:
            content = f.read()
            for line in content.splitlines():
                line = line.strip()
                if not line:
                    continue
                words = line.split(' ')
                count_sum += len(words)
                count_appear += words.count(term)
        
        return count_appear / count_sum if count_sum > 0 else 0.0
    
    def compute_doc_vectors(self):
        """
        计算所有文档的TF-IDF向量
        """
        N = len(self.all_docs)
        doc_vectors = defaultdict(lambda: defaultdict(float))

        for term, docs in self.inverted_index.items():
            df = len(docs)
            idf = math.log(N / df) if df != 0 else 0    # 计算idf
            for doc in docs:
                tf = self.compute_tf(doc, term)
                doc_vectors[doc][term] += tf * idf

        self.doc_vectors = doc_vectors
    
        return doc_vectors
    
if __name__ == "__main__":
    html_sort = HtmlSort()
    inverted_index, all_docs = html_sort.load_inverted_index()
    print("倒排索引加载完成")
    print(f"总文档数: {len(all_docs)}")
    print(f"倒排索引条目数: {len(inverted_index)}")