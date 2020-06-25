# dmock  
基于Django的轻量级Mock平台  
dmock即Django+Mock的缩写  


![PyCharm截图](https://github.com/yjlch1016/dmock/blob/master/static/img/dmock.png)  


# 模型  
接口表一对多场景表  

一、接口表  
1、接口名称  
2、接口地址  
3、请求方式  
4、创建时间  
5、修改时间  

二、场景表  
1、外键，关联接口id  
2、场景名称  
3、请求头  
4、请求参数  
5、请求体类型  
6、请求体  
7、响应结果  
8、创建时间  
9、修改时间  


# 本地调试  
python manage.py collectstatic  
复制xadmin静态文件  

python manage.py makemigrations  
激活模型  

python manage.py migrate  
迁移  

python manage.py createsuperuser  
创建超级管理员账号  
输入账号：admin  
输入邮箱：123456789@qq.com  
输入密码：test123456  
二次确认  

python manage.py runserver  
启动服务  

http://127.0.0.1:8000/admin/  
用户名：admin  
密码：test123456  


# 本地打包  
docker build -t mock .  
mock为镜像名称，随便取  

docker run -d --name mock2019 -p 80:80 mock:latest  
启动容器  
后台运行  
给容器取个别名mock2019  
映射80端口  

http://x.x.x.x/admin/  
宿主机的IP地址  
账号：admin  
密码：test123456  

docker exec -it mock2019 /bin/bash  
进入容器内部  

exit  
退出容器内部  

docker stop mock2019  
停止容器  

docker rm mock2019  
删除容器  
