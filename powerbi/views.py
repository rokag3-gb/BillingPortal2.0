from django.shortcuts import render
from django.conf import settings
from .services.pbiembedservice import PbiEmbedService
# Create your views here.
@login_required
def token(request: HttpRequest) -> HttpResponse:
    powerbi_config = getattr(settings, "POWERBI", {})
    # return render(request, 'portal/index.html')
    # return redirect('/dashboard')

    try:
        embed_info = PbiEmbedService().get_embed_params_for_single_report(powerbi_config['WORKSPACE_ID'], powerbi_config['REPORT_ID'])
        return embed_info
    except Exception as ex:
        return json.dumps({'errorMsg': str(ex)}), 500