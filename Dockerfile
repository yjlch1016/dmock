FROM ubuntu:18.04
# 基础镜像

MAINTAINER yangjianliang <526861348@qq.com>
# 作者

RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
# 设置apt源为阿里云源

RUN apt-get clean && \
    apt-get update && \
    apt-get upgrade -y
# 检查软件包并升级

RUN apt-get install -y \
	git \
	python3 && \
	apt-get update && \
	apt-get install -y \
	python3-dev \
	python3-setuptools && \
	apt-get update && \
	apt-get install -y \
	python3-pip && \
	apt-get update && \
	apt-get install -y \
	nginx \
	supervisor &&\
	language-pack-zh-hans* &&\
	apt-get update && \
	ln -fs /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
	apt-get install -y \
	tzdata && \
	rm -rf /var/lib/apt/lists/*
# 安装软件

COPY deploy_conf/nginx-app.conf /etc/nginx/sites-available/default
COPY deploy_conf/supervisor-app.conf /etc/supervisor/conf.d/
COPY deploy_conf/pip.conf /root/.pip/pip.conf
# 复制配置文件

COPY . /django/dmock/
# 拷贝代码
RUN pip3 install https://codeload.github.com/sshwsfc/xadmin/zip/django2 && \
pip3 install -r /django/dmock/requirements.txt
# 安装python依赖库

RUN sed -i '35,36d' /usr/local/lib/python3.6/dist-packages/django/db/backends/mysql/base.py && \
sed -i '145,146d' /usr/local/lib/python3.6/dist-packages/django/db/backends/mysql/operations.py && \
sed -i '93d' /usr/local/lib/python3.6/dist-packages/django/forms/boundfield.py && \
sed -i '38,40c <h4>轻量级mock平台</h4>' /usr/local/lib/python3.6/dist-packages/xadmin/templates/xadmin/views/login.html
# 修改Django源码

RUN mkdir /django/dmock/media
# 创建/django/dmock/media目录

ENV LANG zh_CN.UTF-8
ENV LANGUAGE zh_CN.UTF-8
ENV LC_ALL zh_CN.UTF-8
# 设置环境变量，选择zh_CN.UTF-8作为默认字符集，用以支持中文

ENV PYTHONUNBUFFERED=1
# 设置环境变量，不缓冲，等同于python3 -u

EXPOSE 80
# 暴露80端口

ENTRYPOINT ["supervisord", "-c", "/etc/supervisor/conf.d/supervisor-app.conf"]
# 启动supervisor并加载配置文件
