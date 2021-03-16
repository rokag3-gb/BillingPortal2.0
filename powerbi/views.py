from django.shortcuts import render
from django.conf import settings

from portal.models import NavMenu
from custom.services import get_organization
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
        report_config = NavMenu.objects.filter(menu_id=2)[0]  # Dashboard
    else:
        report_config = NavMenu.objects.filter(menu_id=mid)[0]

    # TODO: report id가 없을때??

    try:
        embed_info = PbiEmbedService().get_embed_params_for_single_report(powerbi_config['WORKSPACE_ID'], report_config.report_id)
        return JsonResponse({
            'token': embed_info,
            'filter': {
                "$schema": "http://powerbi.com/product/schema#basic",
                "target": {
                    "table": report_config.filter_table,
                    "column": report_config.filter_column,
                },
                "operator": "In",
                "values": [get_organization(request).id], 
                "filterType": 1,
                "requireSingleSelection": True,
                "displaySettings": {
                    "isHiddenInViewMode": True
                }
            }
        })
    except Exception as ex:
        return JsonResponse({'errorMsg': str(ex)}, status=500)