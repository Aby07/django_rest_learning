from django.shortcuts import render
from django.http import HttpResponse


def students(request):
    context={
        'id': 1,
        'name': 'Abcs',
        'class': 'X'
    }
    students = [context]
    return HttpResponse(students)