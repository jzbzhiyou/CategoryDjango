# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse
from models import Category
import requests
import json
import re


def index(request):
    # url = "http://v.juhe.cn/weather/index"
    # response = requests.get(url, {
    #     "cityname": u"郑州",
    #     "dtype": "json",
    #     "key": "764bea985cfd0e960fdca55c95d26f27"
    # })
    # json_str = response.text
    # print json_str

    # response = requests.get("http://api.map.baidu.com/telematics/v3/weather?location=郑州&output=json&ak=TueGDhCvwI6fOrQnLM0qmXxY9N0OkOiQ&callback=?")
    # result = response.text
    # result = json.loads(result)
    # weather = result['results'][0]['weather_data'][0]
    return render(request, "index.html", {
        # "city_name": u"郑州",
        # "weather": weather,
    })


def cate_add(request):
    if request.method == "POST":
        cate_name = request.POST.get("cate_name", "")
        cate_pid = int(request.POST.get("cate_pid", 0))
        if cate_pid == 0:
            cate = Category()
            cate.cate_name = cate_name
            cate.cate_pid = cate_pid
            cate.cate_level = 0
            cate.save()
            cate.cate_path = str(cate.id) + ","
            cate.save()
        else:
            p_cate = Category.objects.filter(id=cate_pid)
            if not p_cate:
                return HttpResponse("Parent Category Not Exists!!")
            p_cate = p_cate[0]
            cate = Category()
            cate.cate_name = cate_name
            cate.cate_pid = cate_pid
            cate.cate_level = 0
            cate.save()
            cate.cate_level = p_cate.cate_level + 1
            cate.cate_path = p_cate.cate_path + str(cate.id) + ","
            cate.save()
        return HttpResponse("Add Category Success!!")

    categorys = select_all_categorys()
    return render(request, "cate_add.html", {
        "categorys": categorys,
    })


def cate_delete(request):
    error = dict()
    if request.method == "POST":
        id = int(request.POST.get("id", 0))
        cate = Category.objects.filter(id=id)
        if cate:
            cate[0].delete()
            error['status'] = 1
            error['msg'] = u"删除成功"
            return HttpResponse(json.dumps(error), content_type="application/json", status=200)
        else:
            error['status'] = 0
            error['msg'] = u"该分类不存在"
            return HttpResponse(json.dumps(error), content_type="application/json", status=404)
    error['status'] = 0
    error['msg'] = u"请求方法不合适!!"
    return HttpResponse(json.dumps(error), content_type="application/json", status=404)


def cate_update(request):
    error = dict()
    if request.method == "POST":
        id = int(request.POST.get("id", 0))
        cate_name = request.POST.get("cate_name", "")
        cate_pid = int(request.POST.get("cate_pid", 0))

        cate = Category.objects.filter(id=id)
        if cate:
            cate = cate[0]
            cate.cate_name = cate_name
            cate.cate_pid = cate_pid
            cate.save()
            error['status'] = 1
            error['msg'] = u"更新成功"
            return HttpResponse(json.dumps(error), content_type="application/json", status=200)
        else:
            error['status'] = 0
            error['msg'] = u"该分类不存在"
            return HttpResponse(json.dumps(error), content_type="application/json", status=404)
    error['status'] = 0
    error['msg'] = u"请求方法不合适!!"
    return HttpResponse(json.dumps(error), content_type="application/json", status=404)


def cate_select(request):
    categorys = select_all_categorys()
    return render(request, "cate_select.html", {
        "categorys": categorys,
    })


def select_all_categorys():
    categorys = Category.objects.order_by("cate_path").all()
    for cate in categorys:
        cate.cate_name = "|--" * cate.cate_level + cate.cate_name
    return categorys


def get_weather(request):
    response = requests.get("http://api.map.baidu.com/telematics/v3/weather?location=郑州&output=json&ak=TueGDhCvwI6fOrQnLM0qmXxY9N0OkOiQ&callback=?")
    result = response.text
    # result = json.loads(result)
    # weather = result['results'][0]['weather_data'][0]
    return HttpResponse(result)


def get_phone(request):
    if request.method == "POST":
        phone = request.POST.get("phone", "")
    else:
        phone = request.GET.get("phone", "")
    pattern = re.compile("^((13[0-9])|(14[5|7])|(15([0-3]|[5-9]))|(18[0,5-9]))\d{8}$")
    if pattern.match(phone):
        response = requests.get("http://sj.apidata.cn/?mobile=" + phone)
        result = response.text
        return HttpResponse(result, content_type="application/json")
    error = dict()
    error['status'] = 0
    error['message'] = "Not a phone"
    return HttpResponse(json.dumps(error), content_type="application/json", status=400)


def music(request):
    if request.method=="GET":
        type = request.GET.get("type","")
        if type:
            url = "http://tingapi.ting.baidu.com/v1/restserver/ting?method=baidu.ting.billboard.billList&type=2&size=20&offset=0"
            response = requests.get(url)
            result = response.text
            return HttpResponse(result)
    return render(request,"music.html")