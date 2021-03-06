from django.conf import settings
from django.core.urlresolvers import reverse
from pinry.core.utils import safe_base_url, safe_sbase_url, safe_usbase_url


def template_settings(request):
    """
    site_name =     returns site name specified in settings.
    in_dev_env =    returns True if site is being served in the development
                    envrionment (not in production or staging)
    """
    in_dev_env = not getattr(settings, 'RACK_ENV', False)
    site_name = settings.SITE_NAME
    return {'site_name': site_name, 'in_dev_env':in_dev_env}

def urls(request):
    """
    SITE_URL =      base site url with automatic http/https.
    US_SITE_URL =   http base site url
    SSL_SITE_URL =  https base site url
    API_URL =       http for now to avoid cross site requests if that is fixed
                    then we can use auto http/https.
    """
    SITE_URL = safe_base_url(request)
    US_SITE_URL = safe_usbase_url(request)
    SSL_SITE_URL = safe_sbase_url(request)
  
    return {'BASE_URL': SITE_URL,
            'US_SITE_URL': US_SITE_URL, 
            'SSL_SITE_URL': SSL_SITE_URL, 
            'API_URL': US_SITE_URL + '/api/' + settings.API_NAME + '/',
           }
    
def staticPrefix(request):
    """
    STATIC_PREFIX:  Prepends the BASE_URL to STATIC_URL when in the development environment only!
                    This must be use for all static files rendered outsite request context.
                    IE: bookmarklet & email
                    Useage: {{STATIC_PREFIX}}{{STATIC_URL}}
                    Development server:
                        Set STATIC_URL = '/static/'
                        Set COMPRESS_URL = STATIC_URL
    """ 
    sp =  ''
    if not settings.RACK_ENV:
        sp = safe_base_url(request)
    return {'STATIC_PREFIX': sp,}

from urlparse import urlsplit
from .utils import redirect_to_referer
def redirects(request):
    """
    HTTP_REFERER:   redirects to refering page
    SESSION_NEXT:   redirects to path in request.session['next']
    """
    '''
    #If SessionNextMiddleware used:
    session_n = session_next(request)
    '''
    #If redirect_to_referer utility avalable:
    http_referer = redirect_to_referer(request)
    #No dependancies
    '''
    referer = request.META.get('HTTP_REFERER', None)
    if referer:
        try:
            redirect_to = urlsplit(referer, 'http', False)[2]
        except IndexError:
            pass
    else:
        redirect_to = '{% url core:home %}'
    '''
    return {'HTTP_REFERER':http_referer, 'SESSION_NEXT':'remove SESSION_NEXT'}

