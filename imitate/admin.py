# Register your models here.
import re

import xadmin
from django.contrib.auth.models import Group, User
from django.utils.html import format_html
from xadmin import views
from xadmin.layout import Main, Fieldset
from xadmin.models import Permission, Log
from xadmin.plugins.actions import BaseActionView
from xadmin.plugins.batch import BatchChangeAction

from imitate.models import Interface, Scene


class CopyAction(BaseActionView):
    # 添加复制动作

    action_name = "copy_data"
    description = "复制所选的 %(verbose_name_plural)s"
    model_perm = 'change'
    icon = 'fa fa-facebook'

    def do_action(self, queryset):
        for qs in queryset:
            qs.id = None
            # 先让这条数据的id为空
            qs.save()
        return None


class SceneAdmin(object):
    model = Scene
    extra = 1
    # 提供1个足够的选项行，也可以提供N个
    style = "accordion"

    # 折叠

    def save_models(self):
        # 重写保存方法
        obj = self.new_obj
        obj.request_head = re.sub("\s", "", obj.request_head)
        obj.request_parameter = re.sub("\s", "", obj.request_parameter)
        obj.request_body = re.sub("\s", "", obj.request_body)
        obj.response_result = re.sub("\s", "", obj.response_result)
        # 一次性去除空格、换行符、制表符
        self.new_obj.save()

    def interface_name(self, obj):
        # 给外键添加颜色
        button_html = '<a style="color: red" href="/admin/imitate/interface/%s/update/">%s</a>' % (
            obj.scene_group.id, obj.scene_group)
        # %s(,)匹配多个
        return format_html(button_html)

    interface_name.short_description = '<span style="color: red">接口名称</span>'
    interface_name.allow_tags = True

    def update_button(self, obj):
        # 修改按钮
        button_html = '<a class="icon fa fa-edit" style="color: green" href="/admin/imitate/scene/%s/update/">修改</a>' % obj.id
        return format_html(button_html)

    update_button.short_description = '<span style="color: green">修改</span>'
    update_button.allow_tags = True

    def delete_button(self, obj):
        # 删除按钮
        button_html = '<a class="icon fa fa-times" style="color: blue" href="/admin/imitate/scene/%s/delete/">删除</a>' % obj.id
        return format_html(button_html)

    delete_button.short_description = '<span style="color: blue">删除</span>'
    delete_button.allow_tags = True

    form_layout = (
        Main(
            Fieldset('场景信息部分',
                     'scene_group', 'scene_name', 'request_head',
                     'request_parameter', 'body_type', 'request_body', 'response_result'),
        ),
        # Side(
        #     Fieldset('时间部分',
        #              'create_time', 'update_time'),
        # )
    )
    # 详情页面字段分区，请注意不是fieldsets

    list_display = [
        'id',
        'interface_name',
        'scene_name',
        'request_head',
        'request_parameter',
        'body_type',
        'request_body',
        'response_result',
        'create_time',
        'update_time',
        'update_button',
        'delete_button',
    ]

    ordering = ("id",)
    search_fields = ("scene_name",)
    list_filter = ["create_time"]
    list_display_links = ('id', 'interface_name', 'scene_name')
    show_detail_fields = ['scene_name']
    list_editable = ['scene_name']
    raw_id_fields = ('scene_group',)
    list_per_page = 10

    batch_fields = (
        'scene_name',
        'request_head',
        'request_parameter',
        'body_type',
        'request_body',
        'response_result',
    )
    # 可批量修改的字段
    actions = [CopyAction, BatchChangeAction]
    # 列表页面，添加复制动作与批量修改动作


class InterfaceAdmin(object):
    inlines = [SceneAdmin]

    # 使用内嵌显示

    def scene_total(self, obj):
        # 利用外键反向统计场景总数
        button_html = '<span style="color: red">%s</span>' % obj.interfaces.all().count()
        return format_html(button_html)

    scene_total.short_description = '<span style="color: red">场景总数</span>'
    scene_total.allow_tags = True

    def update_button(self, obj):
        # 修改按钮
        button_html = '<a class="icon fa fa-edit" style="color: green" href="/admin/imitate/interface/%s/update/">修改</a>' % obj.id
        return format_html(button_html)

    update_button.short_description = '<span style="color: green">修改</span>'
    update_button.allow_tags = True

    def delete_button(self, obj):
        # 删除按钮
        button_html = '<a class="icon fa fa-times" style="color: blue" href="/admin/imitate/interface/%s/delete/">删除</a>' % obj.id
        return format_html(button_html)

    delete_button.short_description = '<span style="color: blue">删除</span>'
    delete_button.allow_tags = True

    form_layout = (
        Main(
            Fieldset('接口信息部分',
                     'interface_name', 'interface_url', 'request_mode'),
        ),
        # Side(
        #     Fieldset('时间部分',
        #              'create_time', 'update_time'),
        # )
    )

    list_display = [
        'id',
        'interface_name',
        'interface_url',
        'request_mode',
        'scene_total',
        'create_time',
        'update_time',
        'update_button',
        'delete_button',
    ]
    ordering = ("id",)
    search_fields = ("interface_name",)
    list_filter = ["create_time"]
    show_detail_fields = ['interface_name']
    list_display_links = ('id', 'interface_name')
    list_editable = ['interface_name']
    list_per_page = 10

    batch_fields = (
        'interface_name',
        'interface_url',
        'request_mode',
    )
    # 可批量修改的字段
    actions = [CopyAction, BatchChangeAction]
    # 列表页面，添加复制动作与批量修改动作


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True
    # 开启主题自由切换


class GlobalSetting(object):
    global_search_models = [
        Interface,
        Scene,
    ]
    # 配置全局搜索选项
    # 默认搜索组、用户、日志记录

    site_title = "Mock平台"
    # 标题
    site_footer = "测试部门"
    # 页脚

    menu_style = "accordion"
    # 左侧菜单收缩功能
    apps_icons = {
        "imitate": "fa fa-github-alt",
    }
    # 配置应用图标，即一级菜单图标
    global_models_icon = {
        Interface: "fa fa-html5",
        Scene: "fa fa-css3",
    }

    # 配置模型图标，即二级菜单图标

    def get_site_menu(self):
        return (
            {
                'title': '模拟管理',
                'icon': 'fa fa-github-alt',
                'perm': self.get_model_perm(Interface, 'change'),
                # 权限
                'menus': (
                    {
                        'title': '接口列表',
                        'icon': 'fa fa-html5',
                        'url': self.get_model_url(Interface, 'changelist')
                    },
                    {
                        'title': '场景列表',
                        'icon': 'fa fa-css3',
                        'url': self.get_model_url(Scene, 'changelist')
                    },
                )
            },
            {
                'title': '后台管理',
                'icon': 'fa fa-gittip',
                'perm': self.get_model_perm(Group, 'change'),
                'menus': (
                    {
                        'title': '组',
                        'icon': 'fa fa-sun-o',
                        'url': self.get_model_url(Group, 'changelist')
                    },
                    {
                        'title': '用户',
                        'icon': 'fa fa-moon-o',
                        'url': self.get_model_url(User, 'changelist')
                    },
                    {
                        'title': '权限',
                        'icon': 'fa fa-weibo',
                        'url': self.get_model_url(Permission, 'changelist')
                    },
                    {
                        'title': '日志记录',
                        'icon': 'fa fa-renren',
                        'url': self.get_model_url(Log, 'changelist')
                    },
                )
            },
        )
    # 自定义应用的顺序


xadmin.site.register(Interface, InterfaceAdmin)
xadmin.site.register(Scene, SceneAdmin)

xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)
