from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_sameorigin

# Create your views here.
@xframe_options_sameorigin
def index(request):
  return render(request, 'build/index.html')

@xframe_options_sameorigin
def report(request, id):
  return render(request, 'build/index.html')