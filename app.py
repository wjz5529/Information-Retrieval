from flask import Flask, render_template, request, jsonify
from html_sort import HtmlSort
import math
from collections import Counter
import os
import re
from bs4 import BeautifulSoup

app = Flask(__name__)

# 初始化网页相关性排序内容
htmlsort = HtmlSort()

def build_query_vector(query_terms, inverted_index, N):
    """
    构建查询的TF-IDF向量
    """
    counter = Counter(query_terms)
    query_vec = {}
    for term, tf in counter.items():
        if term in inverted_index:
            df = len(inverted_index[term])
            idf = math.log(N / df)
            query_vec[term] = tf * idf
    return query_vec

def cosine_similarity(vec1, vec2):
    """
    计算两个向量的余弦相似度
    """
    dot = sum(vec1[t] * vec2.get(t, 0.0) for t in vec1)
    norm1 = math.sqrt(sum(v ** 2 for v in vec1.values()))
    norm2 = math.sqrt(sum(v ** 2 for v in vec2.values()))
    return dot / (norm1 * norm2) if norm1 and norm2 else 0.0

def query_documents(query):
    """
    主查询函数
    """
    inverted_index, all_docs = htmlsort.load_inverted_index()
    doc_vectors = htmlsort.compute_doc_vectors()

    query_terms = query.strip().split()
    print("处理为 OR 查询，词项有：", query_terms)

    query_vector = build_query_vector(query_terms, inverted_index, len(all_docs))
    if not query_vector:
        print("查询向量为空")
        return [], []

    results = []
    for doc in all_docs:
        sim = cosine_similarity(query_vector, doc_vectors[doc])
        if sim > 0:
            results.append((doc, sim))

    results.sort(key=lambda x: (-x[1], x[0]))  # 相似度降序
    return results, query_terms

def extract_html_title(filepath):
    """
    获取对应文件的标题
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('title')
        return title.string 


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form.get("query", "").strip()
        if not query:
            return render_template("index.html", error="请输入查询词！")

        results, query_terms = query_documents(query)
        if not results:
            return render_template("index.html", error="没有找到相关文档")

        # 提取匹配的句子并高亮关键词
        processed_results = []
        for doc, sim in results:
            doc_path = os.path.join("tokenized_text", doc)
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()
                matched_lines = []
                for line in content.splitlines():
                    line = line.strip()
                    if any(term in line for term in query_terms):
                        highlighted = line
                        for term in query_terms:
                            highlighted = re.sub(f"({re.escape(term)})", r"<mark>\1</mark>", highlighted)
                        matched_lines.append(highlighted)
            processed_results.append({
                "doc": extract_html_title(os.path.join("html", doc)),
                "score": f"{sim:.4f}",
                "matches": matched_lines
            })

        return render_template("index.html", results=processed_results, query=query)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = False, port = '9090')