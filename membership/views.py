from django.http.response import JsonResponse
from django.shortcuts import render

def index(request):
    return JsonResponse({"message": "Index"})