from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'portal/index.html')