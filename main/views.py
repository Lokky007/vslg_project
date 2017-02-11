# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UploadFileForm
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.db import transaction
from main.models import file_record
import os
from django.contrib.auth.models import User

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)

#@login_required
def Main(request):
    results = file_record.objects.all()
    return render(request, 'main/file_list.html', {'results': results})

def NewFile(request):
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            print("uspecne ulozeno")
            if form.is_valid():
                filename = form.cleaned_data.get("title")

                username = request.user.username
                dir_path = settings.MEDIA_ROOT + username + "/"
                file_path = dir_path + request.FILES['file'].name

                file_status = Handle_uploaded_file(request, request.FILES['file'], file_path, dir_path)
                if file_status:
                    Save_file_record(request, filename, file_path)
                    return HttpResponseRedirect('/main/insert/successfully/')
                else:
                    error = 'Uložení souboru se nezdařilo. Kontaktujte prosím administrátora'
                    return render(request, 'main/insert_file.html', {'form': form, 'error': error})

        else:
            form = UploadFileForm()
            print("presmerovani na insert file")
        return render(request, 'main/insert_file.html', {'form': form})

def Overview(request):
    results = file_record.objects.filter(owner=request.user.id)
    return render(request, 'main/overview.html', {'results': results})

# page only for visualisation of correct save
def File_saved(request):
    return render(request, 'main/file_saved.html', {})

def Delete_file(request, file_id, result=""):

    enabled_delete = file_record.objects.filter(owner=request.user.id, id=file_id).count()
    record = file_record.objects.get(id=file_id)
    file_exist = os.path.isfile(record.path)
    print file_exist
    # if select found only one record for delete with condition id file and id user-> continue
    if enabled_delete == 1 and file_exist:
        os.remove(record.path)
        record.delete()
        result = "Smazání záznamu proběhlo úspěšně."

    else:
        result = "Smazání záznamu se nezdařilo. Kontaktujte administrátora"

    return render(request, 'main/delete.html', {'result': result})


#
# additional function
#
def Handle_uploaded_file(request, file, file_path, dir_path):

    try:
        # if folder not exist, create it
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        # save file
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
                return True
    except:
        return False


def Save_file_record(request, filename, file_path):
    user_id = User.objects.get(id=request.user.id)

    record = file_record(file_name=filename, owner=user_id, path=file_path)
    record.save()
