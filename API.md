# Information-Retrieval

## 各模块说明文档

---

### 1. app.py（查询与Web服务模块）

**功能说明：**

- 提供基于 Flask 的网页检索界面。
- 加载倒排索引和文档向量，支持关键词查询（TF-IDF+余弦相似度）。
- 展示相关文档标题、相似度分数及高亮匹配句子。

**如何使用：**

```sh
python app.py
```

默认监听 9090 端口，浏览器访问 [http://localhost:9090](http://localhost:9090)。

**主要接口：**

- `/` ：GET/POST，主检索页面，POST 时处理查询并返回结果。

---

### 2. html_sort.py（网页排序与倒排索引模块）

**功能说明：**

- 构建倒排索引（inverted.index）。
- 计算文档的TF-IDF向量。
- 提供索引加载、文档向量计算等接口。

**如何使用：**

- 作为模块被 app.py 调用，无需单独运行。
- 可在命令行或交互式环境中导入并调用 `HtmlSort` 类的相关方法。

**主要接口：**

- `load_inverted_index()`：加载倒排索引和文档列表。
- `compute_doc_vectors()`：计算所有文档的TF-IDF向量。

---

### 3. src/web_crawler.py（网页爬虫模块）

**功能说明：**

- 爬取目标机构主页及其子页面，保存 HTML 文件到 `html/` 目录。
- 支持多线程、断点续爬、日志记录等。

**如何使用：**

```sh
python src/web_crawler.py
```

可根据脚本内参数设置起始URL、爬取数量等。

**主要接口：**

- 命令行运行，或导入 `crawl()` 函数自定义调用。

---

### 4. src/text_extractor.py（网页正文提取模块）

**功能说明：**

- 从 HTML 文件中抽取正文文本，去除标签、脚本等无关内容。
- 支持批量处理，输出纯文本到 `text/` 目录。

**如何使用：**

```sh
python src/text_extractor.py
```

自动处理 `html/` 目录下所有 HTML 文件。

**主要接口：**

- 命令行运行，或导入 `extract_text()` 函数自定义调用。

---

### 5. src/text_tokenization.py（分词分句模块）

**功能说明：**

- 对抽取后的文本进行中文分词和分句。
- 输出分词结果到 `tokenized_text/` 目录。

**如何使用：**

```sh
python src/text_tokenization.py
```

自动处理 `text/` 目录下所有文本文件。

**主要接口：**

- 命令行运行，或导入 `tokenize_text()` 函数自定义调用。

---

### 6. src/inverted_index.py（倒排索引构建模块）

**功能说明：**

- 根据分词结果构建倒排索引，统计词项出现的文档及频次。
- 输出索引文件 `inverted.index`。

**如何使用：**

```sh
python src/inverted_index.py
```

自动处理 `tokenized_text/` 目录下所有分词文件。

**主要接口：**

- 命令行运行，或导入 `build_inverted_index()` 函数自定义调用。

---

### 7. test.py（网页源码抓取与测试脚本）

**功能说明：**

- 用于快速测试网页抓取功能。
- 可作为 web_crawler.py 的简化版或调试脚本。

**如何使用：**

```sh
python test.py
```

根据脚本内参数抓取网页源码。

---

