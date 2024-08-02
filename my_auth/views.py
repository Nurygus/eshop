from .schema import LogoutResponseSerializer
from django.contrib.auth import login


from rest_framework import permissions, viewsets, mixins, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.settings import api_settings

from drf_spectacular.utils import extend_schema, extend_schema_view

from knox import views as knox_views

from django.conf import settings
from django.core.mail import send_mail

from django.contrib.auth.models import Group

from .permissions import UserPermission, IsAnonymousUser
from .serializers import LoginSerializer, UserSerializer, GroupSerializer
from django.contrib.auth import get_user_model
User = get_user_model()


@extend_schema(
    description='Аккаунт.',
    tags=['Auth']
)
@extend_schema_view(
    signup=extend_schema(
        summary="Зарегестрировать нового пользователя.",
    ),
)
class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [UserPermission,]

    @action(detail=False, methods=['post'])
    def signup(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})

        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        self.sendWelcomeEmail(user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def sendWelcomeEmail(self, user):
        isOk = send_mail(subject="Добро пожаловать",
                         message=f"{user.username} бла бла бла!",
                         from_email=settings.EMAIL_HOST_USER,
                         recipient_list=[user.email,],
                         fail_silently=True
                         )
        return isOk


@extend_schema(
    summary='Войти в систему, то есть получить токен.',
    tags=['Auth']
)
class LoginView(generics.GenericAPIView, knox_views.LoginView):
    permission_classes = [IsAnonymousUser,]
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            serializer.validated_data.pop('user', None)
            response = super().post(request, format=None)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response(response.data, status=status.HTTP_200_OK)


@extend_schema(
    summary="""Выйти из системы, текущий токен становится недействительным.
    Например выйти из аккаунта на телефоне, но оставить на другом устройстве.""",
    tags=['Auth']
)
class LogoutView(generics.GenericAPIView, knox_views.LogoutView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = LogoutResponseSerializer


@extend_schema(
    summary="""Выйти из системы, все токены становятся недействительными.
    Например выйти с аккаунта на всех устройствах.""",
    tags=['Auth']
)
class LogoutAllView(generics.GenericAPIView, knox_views.LogoutAllView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = LogoutResponseSerializer


@extend_schema(
    description="""Группы. Пользователей можно добовлять в множество групп.
    Пользователи в этой группе получают все права этой группы.""",
    tags=['Group']
)
@extend_schema_view(
)
class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.AllowAny,]
