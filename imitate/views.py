import json
import re

import demjson
from django.http import HttpResponse

# Create your views here.
from imitate.models import Scene, Interface


def mock(request, interface):
    if request.method == "GET":
        path = request.path
        # 获取本次请求的路径，不是数据库里存的路径
        route = Interface.objects.filter(interface_url=path)
        print(route)

        if route:
            # 如果数据库里存在这个路径
            headers = request.headers
            # 获取本次请求的请求头，不是数据库里存的请求头
            headers = demjson.decode(str(headers))
            headers = demjson.encode(headers)
            print(headers)
            params = request.GET.dict()
            # 获取本次请求的请求参数，不是数据库里存的请求参数
            print(params)
            params = json.dumps(params, separators=(",", ":"))

            obj = Scene.objects.get(
                request_head__gte=headers,
                request_parameter=params,
            )
            print(obj)
            print(obj.response_result)

            return HttpResponse(
                obj.response_result,
                content_type="application/json;charset=UTF-8"
            )
        else:
            return HttpResponse("请求的接口不存在！请检查路径是否正确！")

    if request.method == "POST":
        path = request.path
        # 获取本次请求的路径，不是数据库里存的路径
        route = Interface.objects.filter(interface_url=path)

        if route:
            # 如果数据库里存在这个路径
            headers = request.headers
            # 获取本次请求的请求头，不是数据库里存的请求头
            headers = demjson.decode(str(headers))
            headers = demjson.encode(headers)
            params = request.GET.dict()
            # 获取本次请求的请求参数，不是数据库里存的请求参数
            params = json.dumps(params, separators=(",", ":"))
            body = request.body.decode("utf-8")
            # 获取本次请求的请求体，不是数据库里存的请求体
            body = re.sub("\n|\t| ", "", body)
            # 去除换行、tab与空格

            obj = Scene.objects.get(
                request_head__gte=headers,
                request_parameter=params,
                request_body=body,
            )

            return HttpResponse(
                obj.response_result,
                content_type="application/json;charset=UTF-8"
            )
        else:
            return HttpResponse("请求的接口不存在！请检查路径是否正确！")
