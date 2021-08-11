from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
@xframe_options_sameorigin
def index(request):
  return render(request, 'build/index.html')

@login_required
@xframe_options_sameorigin
def report(request, id):
  return render(request, 'build/index.html')