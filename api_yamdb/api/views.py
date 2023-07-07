from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, mixins, serializers, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Review, Title, User
from .filters import TitleFilter
from .permissions import (
    IsAdmin,
    IsAdminOrModeratorOrAuthorOrReadOnly,
    IsAdminOrReadOnly,
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    ShowTitleSerializer,
    SignUpSerializer,
    TitleSerializer,
    TokenSerializer,
    UserSerializer,
)


EMAIL_SUBJECT = 'YAMDB: Код подтверждения регистрации.'
EMAIL_TEXT = '{username}! Ваш код подтверждения: {confirmation_code}'
EMAIL_FROM = 'pupkin@yamdb.ru'

USER_NOT_UNIQUE_USERNAME = 'Логин {username} уже кем-то используется.'
USER_NOT_UNIQUE_EMAIL = 'Почта {email} уже кем-то используется.'

BAD_TOKEN = (
    'Проверьте, что вводите корректный код подтверждения из почты. '
    'Новый код доступен по адресу /api/v1/auth/signup/'
)


@api_view(['POST'])
@permission_classes((AllowAny,))
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']
    try:
        user, created = User.objects.get_or_create(
            username=username, email=email)
    except IntegrityError:
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                USER_NOT_UNIQUE_USERNAME.format(username=username),
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                USER_NOT_UNIQUE_EMAIL.format(email=email),
                status=status.HTTP_400_BAD_REQUEST
            )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        EMAIL_SUBJECT,
        EMAIL_TEXT.format(
            username=username,
            confirmation_code=confirmation_code),
        EMAIL_FROM,
        [user.email],
        fail_silently=False,
    )
    return Response(
        serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    confirmation_code = serializer.validated_data['confirmation_code']
    user = get_object_or_404(User, username=username)
    if not default_token_generator.check_token(user, confirmation_code):
        raise serializers.ValidationError(BAD_TOKEN)
    token = {
        'token': str(AccessToken.for_user(user)),
    }
    return Response(
        token, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'patch', 'delete',)

    @action(
        methods=('get', 'patch'),
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True,
        )
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(partial=True, role=request.user.role)
        return Response(
            serializer.data, status=status.HTTP_200_OK)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')).order_by('name')

    serializer_class = (ShowTitleSerializer, TitleSerializer)
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ShowTitleSerializer
        return TitleSerializer


class CategoryGenreViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):

    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'


class CategoryViewSet(CategoryGenreViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminOrModeratorOrAuthorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminOrModeratorOrAuthorOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
