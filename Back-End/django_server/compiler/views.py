from django.shortcuts import render
from django.http import HttpResponse, FileResponse
import os
# Create your views here.


def get_analysis_table(request):
    file_name = 'output.xlsx'  # Excel文件名
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(file_path, 'rb') as f:
        file_content = f.read()  # 读取文件内容
    response = HttpResponse(file_content, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=analysis_table.xlsx'
    return response