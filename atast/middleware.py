class SubdomainMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(":")[0].lower()
        request.subdomain = None

        if host.startswith("sss."):
            request.subdomain = "sss"
            request.urlconf = "atast.sss_urls"

        response = self.get_response(request)

        if hasattr(request, "urlconf"):
            delattr(request, "urlconf")

        return response
