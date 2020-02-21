# 学生管理系统

## 环境依赖
python 2.7
flask
flask_sqlalchemy
flask_wtf

##使用步骤
1. 数据库安装:
config.py文件中指定数据库路径

2. 初始化数据库:
utils/init_db.py 根据需要进行初始化，包括创建数据库、插入初始数据。

3.启动flask应用:
执行run.py

##目录结构描述




##V1.0.0 版本内容
###1.用户注册、登录、登出功能
###2.班级管理：
    班级列表：可编辑、删除班级和查看班级学生
    班级添加
###3.学生管理：
    学生列表：可编辑、删除学生
    添加学生
###4.权限管理：
    角色列表：可删除角色、为角色添加权限、减少权限
    添加角色
    权限列表：可编辑、删除权限
    添加权限
####当前程序支持的权限名称及简写：
    班级列表 	BJLB
    学生列表 	XSLB 	
    角色列表 	JSLB 	
    添加班级 	TJBJ 	
    添加学生 	TJXS
    添加角色 	TJJS 	
    权限列表 	QXLB
    添加权限 	TJQX
    添加用户 	TJYH
    用户列表 	YHLB        
###5.用户管理：
    用户列表：可为用户分配角色、删除用户
    添加用户
###6.系统管理：
    修改密码：修改当前用户密码
    退出：同登出


##**待实现内容**：
1.在blueprint的属性（template_folder）中指定templates_path，无需在每此渲染时写html文件的“全”路径（可优化）
2.目录结构待调整。建议将user，role，permission目录与main目录平行，放在同一级；grade和student作为main子目录
3.CSS样式的学习与优化。尝试使用bootstrap进行渲染。
4.规范统一endpoint和route的命名，如加不加s，加不加_
5.问题：切换页面时，地址栏url不改变。如何能改变