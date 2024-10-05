from rest_framework.generics import RetrieveUpdateAPIView
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from common.views.mixins import ListViewSet, RetrieveViewSet
from users.serializers import users as user_s
from rest_framework.filters import SearchFilter


User = get_user_model()


@extend_schema_view(
    post=extend_schema(
        summary='Регистрация пользователя',
        tags=['Аутентификация & Авторизация']),
)
class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = user_s.RegistrationSerializer


@extend_schema_view(
    post=extend_schema(
        request=user_s.ChangePasswordSerializer,
        summary='Смена пароля', tags=['Аутентификация & Авторизация']),
)
class ChangePasswordView(APIView):
    serializer_class = user_s.ChangePasswordSerializer

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(instance=user, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_204_NO_CONTENT)


@extend_schema_view(
    get=extend_schema(summary='Профиль пользователя', tags=['Пользователи']),
    patch=extend_schema(
        summary='Изменить частично профиль пользователя', tags=['Пользователи']),
)
class MeView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = user_s.MeSerializer
    http_method_names = ('get', 'patch')

    lookup_field = 'pk'

    def get_object(self):
        return User.objects.prefetch_related(
            'events', 'events__photos').get(pk=self.request.user.pk)


@extend_schema_view(
    retrieve=extend_schema(
        summary='Деталка профилей пользователей', tags=['Пользователи']),
)
class UserView(RetrieveViewSet):
    queryset = User.objects.exclude(
        is_superuser=True).prefetch_related('events', 'events__photos')
    serializer_class = user_s.MeSerializer


@extend_schema_view(
    list=extend_schema(
        summary='Список пользователей Search', tags=['Словари']),
)
class UserListSearchView(ListViewSet):
    queryset = User.objects.exclude(is_superuser=True)
    serializer_class = user_s.UserSearchListSerializer
    filter_backends = (
        SearchFilter,
    )
    search_fields = ('phone', 'email', 'username',)
