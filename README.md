#学生管理系统
===========================

###########环境依赖
python 2.7
flask
flask_sqlalchemy
flask_wtf

###########使用步骤
1. 数据库安装
config.py文件中指定数据库路径

2. 初始化数据库
utils/init_db.py 根据需要进行初始化，包括创建数据库、插入初始数据。

3.启动flask应用
执行run.py

###########目录结构描述
├── Readme.md
├── App
│   ├── main
│   ├── static
│   ├── templates
│   ├── user
│   ├── __init__.py
│   ├── route.py
│
└── utils
    └──init_db.py      //数据库初始化



###########V1.0.0 版本内容更新
1. 新功能     aaaaaaaaa
2. 新功能     bbbbbbbbb
3. 新功能     ccccccccc
4. 新功能     ddddddddd

##################待实现内容：
1.在blueprint的属性（template_folder）中指定templates_path，无需在每此渲染时写html文件的“全”路径