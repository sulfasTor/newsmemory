from rest_framework import serializers

from .models import Article, ArticleEntity, ArticleLink, Entity, Reading, Source, Tag


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = "__all__"


class ArticleEntitySerializer(serializers.ModelSerializer):
    entity = EntitySerializer()

    class Meta:
        model = ArticleEntity
        fields = ("entity", "count", "salience")


class ArticleWriteEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleEntity
        fields = ("entity", "count", "salience")


class ArticleSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, source="tags", queryset=Tag.objects.all()
    )
    source = serializers.PrimaryKeyRelatedField(queryset=Source.objects.all())
    entities = ArticleEntitySerializer(source="article_entities", many=True, read_only=True)

    class Meta:
        model = Article
        fields = (
            "id",
            "source",
            "url",
            "title",
            "published_at",
            "byline",
            "language",
            "summary",
            "content",
            "tags",
            "tag_ids",
            "entities",
            "created_at",
            "updated_at",
        )


class ReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reading
        fields = "__all__"


class ArticleLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleLink
        fields = "__all__"
