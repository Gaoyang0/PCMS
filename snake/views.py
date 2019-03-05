from django.shortcuts import render

# Create your views here.


def snake(request):
    return render(request, 'snake/snake.html', {})


def control(request):
    return render(request, 'snake/control.html')
