from django.shortcuts import render

# Create your views here.
# Create your views here.
@login_required
def token(request: HttpRequest) -> HttpResponse:
    # return render(request, 'portal/index.html')
    return redirect('/dashboard')
