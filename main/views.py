from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)

#@login_required
def Main(request):
    return render(request, 'main/file_list.html', {})

def NewFile(request):
    return render(request, 'main/insert_file.html', {})

def Overview(request):
    return render(request, 'main/overview.html', {})


