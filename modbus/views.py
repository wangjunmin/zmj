
import logging
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from django_eventstream import get_current_event_id
from modbus.forms import UploadFileForm
from modbus.models import SensorRead
from modbus.monitor.monitor import doMonitor
from modbus.util.excel2model import row2model

from modbus.util.showdata import show_data

# Create your views here.


def home(request):
    context = {}
    context['url'] = '/events/'
    context['last_id'] = get_current_event_id(['time'])
    return render(request, 'modbus/index.html', context)


def show_it(request):
    '''
    推送前端的服务
    '''
    show_data()
    return JsonResponse({})


def show_monitor(request):
    monitor_val = doMonitor()
    return render(request, 'modbus/monitor.html', monitor_val)


def imp_excel(request):

    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            result_dict = request.FILES["file"].get_array(sheet_name="Sheet1",
                                                          name_columns_by_row=0
                                                          )
            result_dict.pop(0)
            for item in result_dict:
                row2model(item)

            return HttpResponse("数据导入成功。")
    else:
        form = UploadFileForm()

    return render(
        request,
        "modbus/import_excel.html",
        {
            "form": form,
            "title": "上传测点定义Excel文件",
            "header": (
                "请选择填写好的测点定义文件 "
            ),
        },
    )
