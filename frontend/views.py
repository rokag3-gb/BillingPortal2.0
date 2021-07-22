from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_sameorigin

# Create your views here.
@xframe_options_sameorigin
def index(request):
  return render(request, 'frontend/index.html')