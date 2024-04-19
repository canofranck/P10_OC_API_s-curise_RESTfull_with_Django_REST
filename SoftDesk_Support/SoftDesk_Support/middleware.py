from django.http import HttpResponseForbidden


class BlockUnauthenticatedMiddleware:
    """
    Custom Django middleware to block access for unauthenticated users to the base pages of the API.

    This middleware intercepts all incoming requests and checks if the user is authenticated.
    If the user is not authenticated and the request is intended for a base URL of the API,
    a forbidden response (403) is returned, thus preventing access to the resource.

    Main uses:
    - Request processing: Checking user authentication.
    - Response processing: Returning a forbidden response if the user is not authenticated.
    - Logging and debugging: Ability to log incoming requests and outgoing responses.
    - Error handling: Capturing and handling authentication-related errors.
    - Customizing processing flow: Modifying Django's base behavior by acting on requests and responses.

    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Executes the middleware for each incoming request.

        :param request: The incoming request.
        :return: The response to the request.
        """
        # Checks if the request path starts with /api/token/ or /api/token/refresh/
        if request.path.startswith("/api/token/") or request.path.startswith(
            "/api/token/refresh/"
        ):
            print("je suis pas authentifier mais je le loggue")
            return self.get_response(request)

        # Checks if the user is authenticated and the request path starts with /api/
        elif request.user.is_authenticated and request.path.startswith(
            "/api/"
        ):
            print("je suis authentifier")
            return self.get_response(request)

        # Checks if the user is not authenticated and the request path starts with /api/
        elif not request.user.is_authenticated and request.path.startswith(
            "/api/"
        ):
            print("je suis pas authentifier")
            return HttpResponseForbidden(
                "You are not authorized to access this resource."
            )

        # For all other paths, pass the request to the next middleware in the chain
        return self.get_response(request)
