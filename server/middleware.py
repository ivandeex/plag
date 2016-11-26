from django.utils.deprecation import MiddlewareMixin


class RealRemoteIPMiddleware(MiddlewareMixin):
    """
    This middleware makes Django WSGI application take real remote
    IP address from special headers sent by Nginx, fixing issues
    with debug context processor and INTERNAL_IPS setting.
    """
    def process_request(self, request):
        for header in ('HTTP_X_REAL_IP', 'HTTP_X_FORWARDED_FOR'):
            real_ip_header = request.META.get(header)
            if real_ip_header:
                real_ip = real_ip_header.partition(',')[0].strip()
                request.META['REMOTE_ADDR'] = real_ip
                break
