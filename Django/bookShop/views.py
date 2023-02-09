from django.shortcuts import render
from django.http import HttpResponse, JsonResponse


def home(request):
    return HttpResponse("oi")
