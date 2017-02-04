from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UploadFileForm
from django.shortcuts import get_object_or_404
from django.conf import settings


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
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            print("uspecne ulozeno")
            if form.is_valid():
                filename = form.cleaned_data.get("title")
                handle_uploaded_file(request.FILES['file'], filename)
                return HttpResponseRedirect('/success/url/')

        else:
            form = UploadFileForm()
            print("presmerovani na insert file")
        return render(request, 'main/insert_file.html', {'form': form})

def Overview(request):
    return render(request, 'main/overview.html', {})

def File_saved(request):
    return render(request, 'main/file_saved.html', {})




def handle_uploaded_file(f, filename):
    print (settings.MEDIA_ROOT + filename)
    with open(settings.MEDIA_ROOT + filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
