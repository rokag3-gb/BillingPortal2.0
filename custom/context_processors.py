from django.conf import settings # import the settings file

def branding(request):
    # return the value you want as a dictionnary. you may add multiple values in there.
    branding = getattr(settings, "BRANDING", {})
    return {
        'BRANDING_WEBSITE_NAME': branding["NAME"],
        'BRANDING_LOGO_PATH': branding["LOGO_PATH"],
        'BRANDING_LOGO_PATH_DARKMODE': branding["LOGO_DARKMODE_PATH"],
        }