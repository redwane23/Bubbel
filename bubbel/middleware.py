from django.utils.deprecation import MiddlewareMixin
from django.middleware.csrf import get_token

#custom middlwear to ensure all functions that inheart from base templet have the csrf token
class EnsureCSRFMiddleware(MiddlewareMixin):
    def process_view(self,request,view_func,view_args,view_kwargs):
        get_token(request)
        return None