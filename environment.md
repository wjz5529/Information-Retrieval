# 搭建程序所需Python环境

## 说明：该文件旨在创建一个可以运行该仓库代码的Python环境

### Step1：创建并激活一个anconda环境（如果不需要可以跳过该步骤）

````cmd
conda create -n Information-Retrieval python = 3.9 ::Information-Retrieval可以替换为你喜欢的环境名
conda creative Information-Retrieval ::激活Python环境
````

### Step2：安装所需的Python包

````cmd
pip install lxml
pip install bs4
pip install jieba

REM 网络交互所需
pip install flask 
pip install requests
````
