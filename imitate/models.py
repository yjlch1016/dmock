# Create your models here.
from django.db import models


class Interface(models.Model):
    # 接口表

    mode_choice = (
        ("GET", "GET"),
        ("POST", "POST"),
        ("PUT", "PUT"),
        ("DELETE", "DELETE"),
        ("PATCH", "PATCH"),
    )
    # 请求方式枚举
    # 第一个元素是存储在数据库里面的值
    # 第二个元素是页面显示的值

    interface_name = models.CharField(
        max_length=32, verbose_name="接口名称",
        help_text="请输入接口名称", db_index=True)
    # 接口名称，并创建索引
    interface_url = models.CharField(
        max_length=255, verbose_name="接口地址", help_text="请输入接口地址")
    # 接口地址
    request_mode = models.CharField(
        choices=mode_choice, max_length=11,
        verbose_name="请求方式", default="GET",
        help_text="请选择请求方式")
    # 请求方式
    create_time = models.DateTimeField(
        auto_now_add=True, blank=True, null=True, verbose_name="创建时间")
    # 创建时间
    update_time = models.DateTimeField(
        auto_now=True, blank=True, null=True, verbose_name="修改时间")

    # 修改时间

    class Meta:
        db_table = "interface"
        verbose_name = "接口列表"
        verbose_name_plural = "接口列表"

    def __str__(self):
        return self.interface_name


class Scene(models.Model):
    # 场景表

    body_choice = (
        ("x-www-form-urlencoded", "application/x-www-form-urlencoded"),
        ("json", "application/json"),
        ("form-data", "multipart/form-data"),
        ("xml", "text/xml"),
    )
    # 请求体类型枚举

    scene_group = models.ForeignKey(
        Interface, on_delete=models.CASCADE,
        verbose_name="接口", related_name="interfaces",
        help_text="请选择接口")
    # 外键，关联接口id
    scene_name = models.CharField(
        max_length=32, verbose_name="场景名称",
        help_text="请输入场景名称", db_index=True)
    # 场景名称，并创建索引
    request_head = models.TextField(
        verbose_name="请求头", blank=True, null=True,
        help_text="请输入字典格式的请求头", default="")
    # 请求头
    request_parameter = models.TextField(
        verbose_name="请求参数", blank=True, null=True,
        help_text="请输入字典格式的请求参数", default="")
    # 请求参数
    body_type = models.CharField(
        choices=body_choice, max_length=21,
        blank=True, null=True,
        verbose_name="请求体类型", default="x-www-form-urlencoded",
        help_text="请选择请求体类型")
    # 请求体类型
    request_body = models.TextField(
        verbose_name="请求体", blank=True, null=True,
        help_text="请输入浏览器原生表单、json、文件或xml格式的请求体", default="")
    # 请求体
    response_result = models.TextField(
        verbose_name="响应结果", blank=True, null=True,
        help_text="请输入字典格式的响应结果", default="")
    # 响应结果
    create_time = models.DateTimeField(
        auto_now_add=True, blank=True, null=True, verbose_name="创建时间")
    # 创建时间
    update_time = models.DateTimeField(
        auto_now=True, blank=True, null=True, verbose_name="修改时间")

    # 修改时间

    class Meta:
        db_table = "scene"
        verbose_name = "场景列表"
        verbose_name_plural = "场景列表"

    def __str__(self):
        return self.scene_name
