from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.news.models import News
from apps.news.serializers.list import NewsListSerializer
from apps.shared.utils.custom_pagination import CustomPageNumberPagination
from apps.shared.utils.custom_response import CustomResponse


class NewsListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    serializer_class = NewsListSerializer

    def get_queryset(self):
        return News.objects.filter(status=True).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(
                page, many=True, context={'request': request}
            )
            paginated_data = self.get_paginated_response(serializer.data)
            return CustomResponse.success(
                message_key="SUCCESS",
                data=paginated_data,
                request=request
            )

        serializer = self.get_serializer(
            queryset, many=True, context={'request': request}
        )
        return CustomResponse.success(
            message_key="SUCCESS",
            data=serializer.data,
            request=request,
            status_code=status.HTTP_200_OK
        )
