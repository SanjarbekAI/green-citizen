import logging

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.media_test.models.article import Article
from apps.media_test.serializers.article import ArticleCreateSerializer, ArticleDetailSerializer
from apps.shared.utils.custom_pagination import CustomPageNumberPagination
from apps.shared.utils.custom_response import CustomResponse

logger = logging.getLogger(__name__)


class ArticleListView(APIView):
    """
    GET: List all articles with pagination.
    """

    def get(self, request):
        queryset = Article.objects.select_related('thumbnail').prefetch_related('gallery').all()

        paginator = CustomPageNumberPagination()
        page = paginator.paginate_queryset(queryset, request)

        if page is not None:
            serializer = ArticleDetailSerializer(page, many=True, context={'request': request})
            paginated = paginator.get_paginated_response(serializer.data)
            return CustomResponse.success(
                message_key="SUCCESS",
                request=request,
                data=paginated,
            )

        serializer = ArticleDetailSerializer(queryset, many=True, context={'request': request})
        return CustomResponse.success(
            message_key="SUCCESS",
            request=request,
            data=serializer.data,
        )


class ArticleCreateView(APIView):
    """
    POST: Create an article.

    Request body (JSON):
    {
        "title": "My Article",
        "content": "Some text...",
        "thumbnail_uuid": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",  // optional
        "gallery_uuids": ["uuid1", "uuid2"]                        // optional
    }
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ArticleCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return CustomResponse.validation_error(
                errors=serializer.errors,
                request=request,
            )

        article = serializer.save()
        data = ArticleDetailSerializer(article, context={'request': request}).data

        return CustomResponse.success(
            message_key="CREATED",
            request=request,
            data=data,
        )


class ArticleDetailView(APIView):
    """
    GET: Retrieve a single article by uuid.
    """

    def get(self, request, uuid):
        try:
            article = Article.objects.select_related('thumbnail').prefetch_related('gallery').get(uuid=uuid)
        except Article.DoesNotExist:
            return CustomResponse.not_found(
                message_key="NOT_FOUND",
                request=request,
            )

        data = ArticleDetailSerializer(article, context={'request': request}).data
        return CustomResponse.success(
            message_key="SUCCESS",
            request=request,
            data=data,
        )


class ArticleUpdateView(APIView):
    """
    PUT/PATCH: Update an article by uuid.

    Request body (JSON):
    {
        "title": "Updated Title",
        "content": "Updated content...",
        "thumbnail_uuid": "new-uuid-or-null",
        "gallery_uuids": ["uuid1", "uuid3"]
    }
    """

    def put(self, request, uuid):
        return self._update(request, uuid)

    def patch(self, request, uuid):
        return self._update(request, uuid)

    def _update(self, request, uuid):
        try:
            article = Article.objects.get(uuid=uuid)
        except Article.DoesNotExist:
            return CustomResponse.not_found(
                message_key="NOT_FOUND",
                request=request,
            )

        serializer = ArticleCreateSerializer(article, data=request.data, partial=True)
        if not serializer.is_valid():
            return CustomResponse.validation_error(
                errors=serializer.errors,
                request=request,
            )

        article = serializer.save()
        data = ArticleDetailSerializer(article, context={'request': request}).data

        return CustomResponse.success(
            message_key="UPDATED",
            request=request,
            data=data,
        )


class ArticleDeleteView(APIView):
    """
    DELETE: Delete an article by uuid.
    """

    def delete(self, request, uuid):
        try:
            article = Article.objects.get(uuid=uuid)
        except Article.DoesNotExist:
            return CustomResponse.not_found(
                message_key="NOT_FOUND",
                request=request,
            )

        article.delete()
        return CustomResponse.success(
            message_key="DELETED",
            request=request,
        )

