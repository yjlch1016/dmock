FROM registry.cn-hangzhou.aliyuncs.com/yangjianliang/django_xadmin:0.0.1
# 基础镜像

RUN apt-get update && \
    apt-get install -y \
	nginx \
	supervisor
# 安装nginx与supervisor

COPY deploy_conf/nginx-app.conf /etc/nginx/sites-available/default
COPY deploy_conf/supervisor-app.conf /etc/supervisor/conf.d/
# 复制配置文件

COPY . /django/dmock/
# 拷贝代码
RUN pip3 install -r /django/dmock/requirements.txt
# 安装Python第三方依赖库

RUN sed -i '38,40c <h4>轻量级mock平台</h4>' /usr/local/lib/python3.6/dist-packages/xadmin/templates/xadmin/views/login.html && \
    sed -i '30,31c <style type="text/css">table {table-layout: inherit;}td {white-space: nowrap;overflow: hidden;text-overflow: ellipsis;}</style>' /usr/local/lib/python3.6/dist-packages/xadmin/templates/xadmin/base.html
# 修改Django源码

RUN mkdir /django/dmock/media
# 创建/django/dmock/media目录

EXPOSE 80
# 暴露80端口

ENTRYPOINT ["supervisord", "-c", "/etc/supervisor/conf.d/supervisor-app.conf"]
# 启动supervisor并加载配置文件
