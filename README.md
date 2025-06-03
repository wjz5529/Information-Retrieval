# Information-Retrieval

## 如何使用

### 1.运行环境
1.操作系统：Windows11/10  
2.运行语言及版本：Python3.9+

### 2.安装Python依赖
在终端中运行以下指令:
````sh
::用与网络交互
pip install flask
pip install requests

:: 用于正文提取以及分词
pip install bs4
pip install jieba
pip install collections
pip install lxml
````

### 3.目录结构
```
├── app.py                      # 查询模块
├── html_sort.py                # 网页排序模块
├── src/
│   ├── web_crawler.py          # 爬虫模块
│   ├── text_extractor.py       # 网页正文提取模块 
│   ├── text_tokenization.py    # 分词分句模块
│   └── inverted_index.py       # 倒排索引模块
├── html/                       # 存放原始网页HTML文件
├── text/                       # 存放网页正文提取后的文本文件
├── tokenized_text/             # 存放分词后的文本文件
├── inverted.index              # 生成的倒排索引文件
├── templates/                  # Flask模板文件
├── Log/                        # 日志文件目录
├── API.md                      # 模块接口说明文档
└── README.md                   # 项目说明文档
```

### 4.主要功能
#### 1.  **网页爬取模块**  
运行src/web_crawler.py以爬取对应机构下的1000个网页源码

#### 2.  **网页正文提取模块**  
运行src/text_extractor.pyt以对网页源码进行正文提取

#### 3.  **分词分句模块**  
运行src/text_tokenization.py以对网页正文进行分词分句

#### 4.  **倒排索引模块**  
运行src/inverted_index.py以构建倒排索引

#### 5.  **网页排序模块**  
运行html_sort对网页进行相关性排序

#### 6.  **查询模块**  
运行app.py后，访问网址127.0.0.1:9090以进入查询模块，在查询框中输入查询项后点击"搜索"以获取查询结果

### 5.使用方法
#### 1. 先按照以下顺序依次运行Python文件以获取倒排索引文件
````sh
cd src
python web_crawler.py       ::执行爬虫模块
python text_extractor.py    ::执行网页正文提取模块
python text_tokenization.py ::执行分词分句模块
python inverted_index.py    ::执行倒排索引模块
cd ..
````

#### 2. 运行app.py以启动查询模块程序,此过程需要等待几秒钟
````sh
python app.py
````

#### 3. 在浏览器中访问127.0.0.1:9090以进入查询模块的UI界面

#### 4. 在查询框中输入要查询的关键字，格式如下：
````
查询词1 查询词2 ··· 查询词n
````

#### 5. 点击搜索以进行查询