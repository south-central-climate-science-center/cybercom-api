
def title(request):
    from api import config
    return {'page_title': config.Page_Title,
            'application_title':config.Application_Title }
