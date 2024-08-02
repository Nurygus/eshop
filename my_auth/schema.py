from drf_spectacular.extensions import (
    OpenApiAuthenticationExtension,
    OpenApiViewExtension,
)

from .serializers import LoginResponseSerializer, LogoutResponseSerializer


class KnoxAuthentication(OpenApiAuthenticationExtension):
    """
    Knox authentication Open API definition.
    """

    target_class = "knox.auth.TokenAuthentication"
    name = "TokenAuthentication"

    def get_security_definition(self, auto_schema):
        """
        Custom definition for APIView.
        """
        return {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Token-based authentication with required prefix 'Token'",
        }


class FixLoginView(OpenApiViewExtension):
    target_class = "knox.views.LoginView"

    def view_replacement(self):
        """
        Fix view
        """

        class Fixed(self.target_class):
            serializer_class = LoginResponseSerializer

        return Fixed


class FixLogoutView(OpenApiViewExtension):
    target_class = "knox.views.LogoutView"

    def view_replacement(self):
        """
        Fix view
        """

        class Fixed(self.target_class):
            serializer_class = LogoutResponseSerializer

        return Fixed


class FixLogoutAllView(OpenApiViewExtension):
    target_class = "knox.views.LogoutAllView"

    def view_replacement(self):
        """
        Fix view
        """

        class Fixed(self.target_class):
            serializer_class = LogoutResponseSerializer

        return Fixed
