# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UploadFileForm, PasswordSetting, UploadLinkForm, SearchForm, EditFile, EmailUpdate
from django.conf import settings
from main.models import file_record
import os
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.encoding import smart_str
from django.http import HttpResponse

from django.views.static import serve

@login_required
def Main(request):
    if request.method == 'POST':
        form = SearchForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            author = form.cleaned_data.get("author")

            if title:
                search = file_record.objects.filter(file_name__icontains=title, enable_post=True)\
                    .order_by('owner').order_by('-date')
            elif author:
                id_user = User.objects.filter(Q(file_record__owner__last_name__icontains=author) |
                                              Q(file_record__owner__first_name__icontains=author),
                                              file_record__enable_post=True).order_by('owner').\
                    order_by('-file_record__date')

                search = file_record.objects.filter(enable_post=True, owner=id_user).order_by('owner')\
                    .order_by('-date')

            else:
                search = file_record.objects.filter(enable_post=True).order_by('owner')\
                    .order_by('-date')

            results = search
        else:
            results = file_record.objects.filter(enable_post=True).order_by('owner').order_by('-date')
    else:
        form = SearchForm()
        results = file_record.objects.filter(enable_post=True).order_by('owner').order_by('-date')

    return render(request, 'main/file_list.html', {'results': results, 'form': form})

@login_required
def Download_file(request, file_id):

    file = file_record.objects.get(id=file_id)
    filepath = file.path
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))


@login_required
def NewFile(request):
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                filename = form.cleaned_data.get("title")
                file_enabled = form.cleaned_data.get("status")

                username = request.user.username
                dir_path = settings.MEDIA_ROOT + username + "/"
                file_path = dir_path + request.FILES['file'].name

                file_status = Handle_uploaded_file(request, request.FILES['file'], file_path, dir_path)
                if file_status:
                    Save_file_record(request, filename, file_path, file_enabled)
                    return HttpResponseRedirect('/main/insert/successfully/')
                else:
                    error = 'Uložení souboru se nezdařilo. Kontaktujte prosím administrátora'
                    return render(request, 'main/insert_file.html', {'form': form, 'error': error})

        else:
            form = UploadFileForm()
        return render(request, 'main/insert_file.html', {'form': form})

@login_required
def Overview(request, error=''):
    results = file_record.objects.filter(owner=request.user.id).order_by('-date')
    success = request.GET.get('success', 1)
    if success == '0':
        error = 'Operace se nezdařila. Opakujte akci nebo kontaktujte administrátora'
    return render(request, 'main/overview.html', {'results': results, 'error': error})

@login_required
def NewLink(request):
    if request.method == 'POST':
        form = UploadLinkForm(request.POST)
        if form.is_valid():

            filename = form.cleaned_data.get("title")
            link = form.cleaned_data.get("link")
            status = form.cleaned_data.get("status")
            user_id = User.objects.get(id=request.user.id)


            try:
                record = file_record(file_name=filename, owner=user_id, link=link, enable_post=status)
                record.save()
                return HttpResponseRedirect('/main/insert/successfully/')
            except:
                error = 'Evidence odkazu se nezdařila. Kontaktujte prosím administrátora'
                return render(request, 'main/insert_file.html', {'form': form, 'error': error})

        else:
            error = 'Evidence odkazu se nezdařila. Kontaktujte prosím administrátora'
            return render(request, 'main/insert_file.html', {'form': form, 'error': error})



    else:
        form = UploadLinkForm()
    return render(request, 'main/insert_link.html', {'form': form})

# Account settings
@login_required
def Settings(request):

    user = User.objects.get(username=request.user.username)

    if request.method == 'POST':
        form = PasswordSetting(data=request.POST, user=user)

        if form.is_valid():
            new_password = form.cleaned_data.get("new_password")

            user.set_password(new_password)
            user.save()

            message = 'Heslo bylo změněno'

        else:
            message = 'Heslo nebylo ulozeno'

        return render(request, 'main/settings.html', {'form': form, 'message': message})

    else:
        form = PasswordSetting(user=user)

        data = {'email': request.user.email}
        form_email = EmailUpdate(initial=data)

    return render(request, 'main/settings.html', {'form': form, 'form_email': form_email})

# Update File
@login_required
def Update_file(request, file_id):
    record = file_record.objects.get(id=file_id)

    if request.method == 'POST':

        # recognize type of form form update (3 elements for file)
        if len(request.POST) != 3:
            link_form = UploadLinkForm(request.POST)
            if link_form.is_valid():

                link_href = link_form.cleaned_data.get("link")
                title_href = link_form.cleaned_data.get("title")
                status_href = link_form.cleaned_data.get("status")

                print link_href, title_href, status_href

                record.file_name = title_href
                record.link = link_href
                record.enable_post = status_href
                record.save()
        else:
            file_form = EditFile(request.POST)
            if file_form.is_valid():

                title = file_form.cleaned_data.get("title")
                status = file_form.cleaned_data.get("status")

                record.file_name = title
                record.enable_post = status
                record.save()

        return redirect('/main/overview')

    else:
        if record.path is not None:
            data = {'title': record.file_name, 'enable_post': record.enable_post}
            form = EditFile(initial=data)

            return render(request, 'main/insert_file.html', {'form': form})

        else:

            data = {'title': record.file_name, 'link': record.link, 'status': record.enable_post}
            form = UploadLinkForm(initial=data)
            return render(request, 'main/update_record.html', {'form': form})


# page only for visualisation of correct save
@login_required
def File_saved(request):
    return render(request, 'main/file_saved.html', {})

@login_required
def Delete_file(request, file_id, result=""):

    enabled_delete = file_record.objects.filter(owner=request.user.id, id=file_id).count()
    record = file_record.objects.get(id=file_id)
    if record.path is not None:
        file_exist = os.path.isfile(record.path)
        # if select found only one record for delete with condition id file and id user-> continue
        if enabled_delete == 1 and file_exist:
            os.remove(record.path)
            record.delete()
            result = "Smazání záznamu proběhlo úspěšně."
        else:
            result = "Smazání záznamu se nezdařilo. Kontaktujte administrátora"
    else:
        record.delete()
        result = "Smazání záznamu proběhlo úspěšně."

    return render(request, 'main/delete.html', {'result': result})

@login_required
def Status_file(request, file_id, result=1):

    new_status = True
    enabled_change = file_record.objects.filter(owner=request.user.id, id=file_id).count()
    record = file_record.objects.get(id=file_id)
    if record.path is not None:
        file_exist = os.path.isfile(record.path)
        # if select found only one record for delete with condition id file and id user-> continue
        if enabled_change == 1 and file_exist:
            if record.enable_post:
                new_status = False

            record.enable_post = new_status
            record.save()

        else:
            result = 0
    else:
        if enabled_change == 1:
            if record.enable_post:
                new_status = False

            record.enable_post = new_status
            record.save()
        else:
            result = 0

    return redirect('/main/overview/?success=%d' % result)


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


def Save_file_record(request, filename, file_path, file_status):
    user_id = User.objects.get(id=request.user.id)

    record = file_record(file_name=filename, owner=user_id, path=file_path, enable_post=file_status)
    record.save()
