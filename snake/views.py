from django.shortcuts import render

# Create your views here.


def snake(request):
    return render(request, 'snake/snake.html', {})


def index(request):
    return render(request, 'snake/snake_index.html', {})


def instructions(request):
    return render(request, 'snake/instructions.html', {})


def contactme(request):
    return render(request, 'snake/contactme.html', {})


def matchmsg(request):
    return render(request, 'snake/matchmsg.html', {})


def document(request):
    return render(request, 'snake/document.html', {})


def download(request):
    if request.method == 'GET':
        return render(request, 'snake/download.html', {})
    elif request.method == "POST":
        from django.http import FileResponse
        import os
        file_path = os.path.abspath('') + '\\download\\SnakeExampleAI.rar'
        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="SnakeExampleAI.rar"'
        return response

