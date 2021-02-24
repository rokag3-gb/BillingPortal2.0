from django.shortcuts import render
from django.conf import settings

from portal.models import NavMenu
from .services.pbiembedservice import PbiEmbedService
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def token(request: HttpRequest) -> HttpResponse:
    powerbi_config = getattr(settings, "POWERBI", {})
    # return render(request, 'portal/index.html')
    # return redirect('/dashboard')
    mid = request.GET.get('id', None)
    if mid is None:
        report_id = NavMenu.objects.filter(menu_id=2)[0].report_id  # Dashboard
    else:
        report_id = NavMenu.objects.filter(menu_id=mid)[0].report_id

    try:
        embed_info = PbiEmbedService().get_embed_params_for_single_report(powerbi_config['WORKSPACE_ID'], report_id)
        return JsonResponse(embed_info)
    except Exception as ex:
        return JsonResponse({'errorMsg': str(ex)}, status_code=500)