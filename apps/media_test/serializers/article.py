import logging

from rest_framework import serializers

from apps.media_test.models.article import Article
from apps.shared.models import Media
from apps.shared.serializers.media import MediaDetailSerializer

logger = logging.getLogger(__name__)


class ArticleCreateSerializer(serializers.Serializer):
    """
    Serializer for creating/updating an Article.

    Accepts media references by UUID:
        - thumbnail_uuid: UUID of an existing Media object (optional)
        - gallery_uuids: list of UUIDs of existing Media objects (optional)
    """
    title = serializers.CharField(max_length=255)
    content = serializers.CharField(required=False, default='')
    thumbnail_uuid = serializers.UUIDField(required=False, allow_null=True)
    gallery_uuids = serializers.ListField(
        child=serializers.UUIDField(),
        required=False,
        default=list,
    )

    def validate_thumbnail_uuid(self, value):
        if value is None:
            return value
        try:
            Media.objects.get(uuid=value)
        except Media.DoesNotExist:
            raise serializers.ValidationError("Media with this UUID does not exist.")
        return value

    def validate_gallery_uuids(self, value):
        if not value:
            return value
        existing = Media.objects.filter(uuid__in=value).values_list('uuid', flat=True)
        existing_set = {str(u) for u in existing}
        missing = [str(u) for u in value if str(u) not in existing_set]
        if missing:
            raise serializers.ValidationError(
                f"Media with these UUIDs do not exist: {', '.join(missing)}"
            )
        return value

    def create(self, validated_data):
        thumbnail_uuid = validated_data.pop('thumbnail_uuid', None)
        gallery_uuids = validated_data.pop('gallery_uuids', [])

        thumbnail = None
        if thumbnail_uuid:
            thumbnail = Media.objects.get(uuid=thumbnail_uuid)

        article = Article.objects.create(
            title=validated_data['title'],
            content=validated_data.get('content', ''),
            thumbnail=thumbnail,
        )

        if gallery_uuids:
            gallery_media = Media.objects.filter(uuid__in=gallery_uuids)
            article.gallery.set(gallery_media)

        return article

    def update(self, instance, validated_data):
        thumbnail_uuid = validated_data.pop('thumbnail_uuid', None)
        gallery_uuids = validated_data.pop('gallery_uuids', None)

        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)

        if thumbnail_uuid is not None:
            instance.thumbnail = Media.objects.get(uuid=thumbnail_uuid)
        elif 'thumbnail_uuid' in self.initial_data and self.initial_data['thumbnail_uuid'] is None:
            instance.thumbnail = None

        instance.save()

        if gallery_uuids is not None:
            gallery_media = Media.objects.filter(uuid__in=gallery_uuids)
            instance.gallery.set(gallery_media)

        return instance


class ArticleDetailSerializer(serializers.ModelSerializer):
    """
    Read-only serializer for Article.
    Nests full Media detail for thumbnail and gallery.
    """
    thumbnail = MediaDetailSerializer(read_only=True)
    gallery = MediaDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = [
            'id',
            'uuid',
            'title',
            'content',
            'thumbnail',
            'gallery',
            'created_at',
            'updated_at',
        ]
        read_only_fields = fields

