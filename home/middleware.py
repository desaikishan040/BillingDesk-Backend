from django.http import HttpResponseForbidden

class IPAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the IP address of the client
        ip_address = request.META.get('REMOTE_ADDR')
        # Check if the IP address is allowed
        if ip_address not in ['192.168.1.1', '127.0.0.1']:
            return HttpResponseForbidden('Access denied')

        response = self.get_response(request)

        return response