from django.shortcuts import render
from django.http import HttpResponse, FileResponse, JsonResponse
import os
import requests
import json
# Create your views here.


def get_analysis_table(request):
    file_name = 'output.xlsx'  # Excel文件名
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(file_path, 'rb') as f:
        file_content = f.read()  # 读取文件内容
    response = HttpResponse(file_content, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=analysis_table.xlsx'
    return response

def parse(request):
    if request.method == 'POST':
        # Read text from POST request body
        text = request.body.decode('utf-8')

        file_name = 'req.txt'
        file_path = os.path.join(os.path.dirname(__file__), file_name)
        # Read request payload from file
        with open(file_path, "r") as file:
            payload = json.load(file)

        
        # Set payload input to the text from the POST request
        payload['input'] = text


        # Send POST request
        url = "http://lab.antlr.org/parse/"
        headers = {
            "Content-Type": "application/json",
            "Cookie": "_ga_6BBQE9CZKG=GS1.1.1704822579.1.0.1704822579.0.0.0; _ga=GA1.1.580636358.1704822579",
            "Host": "lab.antlr.org",
            "Origin": "http://lab.antlr.org",
            "Referer": "http://lab.antlr.org/",
        }
        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()

        print(response_data)
        result = response_data.get("result")
        parser_errors = result.get("parse_errors", [])
        lexer_errors = result.get("lexer_errors", [])

        to_chinese = {
            'extraneous': '不正确的',
            'mismatched': '不正确的',
            'input': '输入',
            'missing': '缺失',
            'expecting': '应当有一个',
            'at': '位于'
        }

        errors = ""
        for error in parser_errors:
            error.get("line"), error.get("msg")
            errors += "<语法分析器> (行:" + str(error.get("line")) + ") 错误信息: " + str(error.get("msg") + "\n\n")

        for error in lexer_errors:
            error.get("line"), error.get("msg")
            errors += "<词法分析器> (行:" + str(error.get("line")) + ") 错误信息: " + str(error.get("msg") + "\n\n")

        if not errors:
            errors += "通过语法分析"

        print(len(errors))
        # Replace specific strings using the 'to_chinese' dictionary
        for key, value in to_chinese.items():
            errors = errors.replace(key, value)

        return HttpResponse(errors, content_type="text/plain")

    return HttpResponse('error', content_type="text/plain")