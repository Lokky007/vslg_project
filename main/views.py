from django.http import HttpResponse

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)

# Create your views here.

def Main(request):
    return HttpResponse("return this string")
